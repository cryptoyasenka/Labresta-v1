"""Fuzzy matching engine with brand blocking for supplier-to-catalog matching.

Uses rapidfuzz WRatio scorer with brand-based blocking to reduce search space.
Match candidates are ranked and stored for human review — no auto-approve.
"""

import logging
import re
import unicodedata

from rapidfuzz import fuzz, process, utils
from sqlalchemy import select

from app.extensions import db
from app.models.catalog import PromProduct
from app.models.product_match import ProductMatch
from app.models.supplier_product import SupplierProduct

logger = logging.getLogger(__name__)

# --- Confidence thresholds (per user decisions from CONTEXT.md) ---
# Benchmark (2026-02-27, 3 MARESTO products vs 6101 prom.ua catalog):
#   100% products found candidates, avg top-1 score 85.5%, all high-confidence.
#   60% cutoff validated as reasonable for Cyrillic product names with WRatio.
SCORE_CUTOFF = 60.0  # User decision: 60% minimum threshold
MATCH_LIMIT = 3  # User decision: top-3 candidates per product
# Oversample factor for rapidfuzz top-K before post-gates run. Raw WRatio
# ranks the correct target below the MATCH_LIMIT cutoff when descriptor
# words diverge (sp 'HKN-FNT-M з набором дисків NEW' scores pp 'HKN-FNT-A
# З НАБОРОМ ДИСКІВ' at 93% but the true match pp 'HKN-FNT-M NEW з
# електронним блоком' at 63%). Post-gates (asymmetric SKU suffix,
# name-model mismatch, etc.) correctly reject the wrong hit — but only
# if they see it in the candidate pool. Feed them the top-K above the
# score cutoff, then truncate to MATCH_LIMIT after filtering.
FUZZY_OVERSAMPLE_LIMIT = 50
CONFIDENCE_HIGH = 80.0  # >80% = High confidence
CONFIDENCE_MEDIUM = 60.0  # 60-80% = Medium confidence
# Below 60% = Low (filtered out by SCORE_CUTOFF, never stored)

BRAND_MATCH_THRESHOLD = 80  # Fuzzy brand match threshold for blocking
MAX_PRICE_RATIO = 3.0  # Reject candidates where price differs by more than 3x

# --- Model / article matching ---
# Model codes are precise identifiers — treat them literally, not fuzzy.
# "XFT133" vs "XFT134" differ by ONE character (fuzz.ratio=91) but are
# completely different products. A loose threshold caused false 98% matches
# between SNACK2100TN-FC and SNACK3100TN-FC in MARESTO → Horoshop.
MODEL_BOOST_POINTS = 10.0  # Bonus points when model/article matches (after normalize)
MODEL_BOOST_THRESHOLD = 80  # Legacy: kept for reference, not used for strict compare

# --- Product type gate ---
TYPE_MATCH_THRESHOLD = 50  # Minimum type similarity to keep candidate
MIN_TYPE_LENGTH = 2  # Minimum chars for extracted type to be usable

# --- Voltage variant gate ---
# "(220)", "(220 В)", "(380 В)", "380 В", "13 кг/год, 380 В" etc. mark
# single-phase vs three-phase SKUs. Same model number with different voltage
# is a DIFFERENT product in the store. Restricted to standard EU mains voltages
# (220, 230, 380, 400) to avoid confusing model/dimension numbers with voltages.
VOLTAGE_TAGS = frozenset({"220", "230", "380", "400"})
VOLTAGE_RE = re.compile(
    r"(?:\((\d{3})(?:\s*[ВBV])?\s*\)|(?<!\d)(\d{3})\s*[ВBV]\b)",
    re.IGNORECASE | re.UNICODE,
)
# Phase markers: '1ф', '3ф', '1ph', '3ph' — infer voltage implication.
# 1-phase → 220/230 V family, 3-phase → 380/400 V family. Suppliers and
# catalog use these labels interchangeably: sp#5113 'ATS 22 UT 1ф' must
# not match pp#2985 'ATS 22 UT 380 В' (that's the 3-phase variant).
PHASE_RE = re.compile(
    r"(?<![a-zа-я0-9])([13])\s*(?:ф|ph|phase|фаз[ан]?(?:и|ы|ий)?)(?![a-zа-я0-9])",
    re.IGNORECASE | re.UNICODE,
)
_PHASE_TO_VOLTAGES = {"1": frozenset({"220", "230"}), "3": frozenset({"380", "400"})}


def extract_voltages(name: str) -> set[str]:
    """Extract canonical voltage tags ({'220','230','380','400'}) from a name.

    Matches three forms: '(220)', '(220 В)' and bare '220 В' / '380В' in any
    context (including inside multi-value parentheses like '(13 кг/год, 380 В)').
    Also expands phase markers ('1ф' → {'220','230'}, '3ф' → {'380','400'})
    so a supplier-labeled 1-phase product cannot match a 380 V catalog entry.
    """
    if not name:
        return set()
    vs = set()
    for m in VOLTAGE_RE.finditer(name):
        v = m.group(1) or m.group(2)
        if v in VOLTAGE_TAGS:
            vs.add(v)
    for m in PHASE_RE.finditer(name):
        vs |= _PHASE_TO_VOLTAGES.get(m.group(1), frozenset())
    return vs


def normalize_text(text: str) -> str:
    """Apply NFC unicode normalization and canonicalize slitny/razdelny SKU forms.

    NFC fixes Cyrillic composition edge cases (Research Pitfall 5).

    Additionally inserts a space at every letter↔digit transition so rapidfuzz
    WRatio treats 'ATS22UT' and 'ATS 22 UT' as equivalent token sequences.
    Without this, a razdelny supplier name ('ATS 22 UT повний унгер 1ф') scores
    noticeably lower against a slitny catalog name ('ATS22UT 1Ф (220В)') than
    against an unrelated razdelny catalog name ('APACH ATS 22 UT 380 В') — and
    with MATCH_LIMIT=3 the correct target drops out of the top-K before the
    post-gates can even see it. Normalizing the shapes here keeps the fuzzy
    ranking aligned with the containment gate's view of identity.
    """
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    # rapidfuzz.utils.default_process will collapse the inserted whitespace
    # and lowercase, so we only add spaces here — no other normalization.
    return _ALNUM_BOUNDARY_RE.sub(" ", text)


def get_confidence_label(score: float) -> str:
    """Map a fuzzy match score to a confidence tier label.

    Used by Phase 4 UI for display.
    """
    if score >= CONFIDENCE_HIGH:
        return "high"
    elif score >= CONFIDENCE_MEDIUM:
        return "medium"
    else:
        return "low"


# Cyrillic↔Latin homoglyph map for SKU identity comparison only.
# Suppliers occasionally type manufacturer SKUs with Cyrillic lookalikes
# (sp#4983 article='GXSN2ТN' — Cyrillic Т inside a Latin SKU). Applied only
# when the string is mixed-script (has both Latin and Cyrillic): pure-Cyrillic
# values like 'АВТОМАТ' are preserved since they are legitimate words, not
# corrupted SKU codes.
_HOMOGLYPH_CYR_TO_LAT = str.maketrans({
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X",
    "а": "a", "в": "b", "е": "e", "к": "k", "м": "m", "н": "h",
    "о": "o", "р": "p", "с": "c", "т": "t", "у": "y", "х": "x",
})
_LATIN_LETTER_RE = re.compile(r"[A-Za-z]")
_CYRILLIC_LETTER_RE = re.compile(r"[А-Яа-яЁёІіЇїЄєҐґ]")


def _fix_cyrillic_homoglyphs(value: str) -> str:
    """Transliterate Cyrillic homoglyph letters to Latin when the SKU is
    mixed-script. No-op for pure Cyrillic or pure Latin strings."""
    if _LATIN_LETTER_RE.search(value) and _CYRILLIC_LETTER_RE.search(value):
        return value.translate(_HOMOGLYPH_CYR_TO_LAT)
    return value


def normalize_model(value: str | None) -> str:
    """Normalize a model/article string for strict literal comparison.

    Lowercases, strips whitespace, and removes all non-alphanumeric characters
    so that "XFT-133" == "xft133" == "XFT 133" but "XFT133" != "XFT134".
    Also fixes Cyrillic homoglyphs in mixed-script SKUs (e.g. 'GXSN2ТN' with
    Cyrillic Т → 'GXSN2TN') so the corrupted-input form matches the catalog.
    """
    if not value or not value.strip():
        return ""
    fixed = _fix_cyrillic_homoglyphs(value.strip())
    return re.sub(r"[^a-z0-9]", "", fixed.lower())


_PAREN_CODE_RE = re.compile(r"\(([A-Za-z0-9.\-_/]{6,})\)")


def extract_article_codes(name: str) -> list[str]:
    """Extract article-like codes from a supplier name.

    Looks for parenthesized alphanumeric tokens that are long (≥6 chars) and
    contain at least one digit — these almost always denote manufacturer SKUs
    embedded by the supplier (e.g. "Rational iVario Pro 2-S (WY9ENRA.0011923)"
    → "WY9ENRA.0011923"). The pattern intentionally ignores short parenthetical
    notes like "(220)", "(тефлон)", "(3035)" — those are variant markers, not
    full article codes.
    """
    if not name:
        return []
    out = []
    for m in _PAREN_CODE_RE.finditer(name):
        tok = m.group(1)
        if any(c.isdigit() for c in tok) and any(c.isalpha() for c in tok):
            out.append(tok)
    return out


def extract_model_from_name(name: str, brand: str | None) -> str:
    """Extract model/article number from product name — first usable token after brand.

    Looks for a token that's a plausible model identifier: contains at least one
    digit AND is either ≥3 chars long OR contains a letter. This excludes generic
    tokens like "2", "40", "65" (sizes, capacities, quantities) while keeping
    real article codes like "28054" and alphanumeric codes like "R2", "XFT133".

    Brand matching is whitespace/punctuation-insensitive so that
    "Restoitalia" in a product name is found when the catalog stores the
    brand as "RESTO ITALIA" (or vice versa).

    Example: "Диск для овощерезки Robot Coupe 28054" with brand "Robot Coupe"
             → "28054"
             "Piч конвекційна Unox XFT133" with brand "Unox"
             → "xft133"
             "Mясорубка Sirman Sirio 2 Cromato" with brand "Sirman"
             → "" (rejects "2" as too generic)
    """
    if not name or not brand or not brand.strip():
        return ""

    brand_norm = normalize_model(brand)
    if not brand_norm:
        return ""

    # Walk the name and find where the normalized brand ends, ignoring
    # whitespace/punctuation differences between the brand token in the name
    # and the stored brand string.
    after_idx = -1
    buf = []
    for i, ch in enumerate(name):
        if ch.isalnum():
            buf.append(ch.lower())
            joined = "".join(buf)
            if joined.endswith(brand_norm):
                after_idx = i + 1
                break

    if after_idx < 0:
        return ""

    after_brand = name[after_idx:].strip()
    # Remove leading punctuation/noise
    after_brand = re.sub(r"^[\s.,:;()\-]+", "", after_brand).strip()

    if not after_brand:
        return ""

    # Strip parenthesized qualifiers before scanning for model tokens —
    # "(380)", "(220 В)", "(на базі)" are voltage/feature tags, not model codes.
    # Without this, "RESTO 4 (380)" would return "(380)" as the model when the
    # real model digit ("4") is filtered out for being too generic, producing
    # a false equivalence with "RESTO 44 (380)".
    after_brand_scan = re.sub(r"\([^)]*\)", " ", after_brand)

    # Glue short uppercase letter prefix to a following digit token written
    # with a space between them ("R 301", "IP 3500", "OGG 4070"). Without
    # this merge, the model becomes the digits alone (letter(s) dropped as
    # a too-short token) and fails strict equality against supplier's joined
    # "R301".
    after_brand_scan = _glue_letter_digit(after_brand_scan)

    # Take the first token that's a plausible model code
    for token in after_brand_scan.split():
        if not re.search(r"\d", token):
            continue
        # Skip size-notation fractions ("1/2", "I/2", "II/3") — supplier may
        # write Roman where catalog writes Arabic, and normalize_model strips
        # the slash, so "I/2" would become "i2" and clash with catalog "12".
        if _is_size_fraction(token):
            continue
        has_letter = bool(re.search(r"[a-zа-яёіїєґ]", token.lower()))
        if len(token) >= 3 or has_letter:
            return token.lower()

    return ""


def after_brand_remainder(name: str, brand: str | None) -> str:
    """Return the portion of `name` after the first occurrence of `brand`.

    Brand matching is whitespace/punctuation-insensitive (walks alphanumerics
    only), so 'Restoitalia' in name matches brand 'RESTO ITALIA'. Returns
    full name unchanged if the brand cannot be located — callers then compare
    full-name tokens, which is still useful.
    """
    if not name:
        return ""
    if not brand or not brand.strip():
        return name
    brand_norm = normalize_model(brand)
    if not brand_norm:
        return name
    buf = []
    for i, ch in enumerate(name):
        if ch.isalnum():
            buf.append(ch.lower())
            if "".join(buf).endswith(brand_norm):
                return name[i + 1:].strip()
    return name


# NB: '+' is intentionally NOT a token separator.
#   '+' in EU catalog names typically marks a variant/bundle suffix
#      ("BISTRO+6 дисків", "F8+8"), not a general separator.
# '-' IS a separator: inside dashed SKUs like "HKN-FNT-M" or "EFT-60/2" the
# dashed pieces are independent identifiers. Without this split, "HKN-FNT-M"
# merged to "hknfntm" which _near_duplicate_token then treated as a sibling
# of "hknfnta" (only 1 char diff), causing FNT-M → FNT-A false matches.
# Compound letter↔digit boundary split below guarantees "ATS12U" and
# "ATS 12 U" produce the same token set {ats, 12, u}, so slitny and
# razdelny catalog styles align through the containment gate.
_TOKEN_SPLIT_RE = re.compile(r"[\s.,:;()/\-]+", re.UNICODE)
# '+' is kept inside tokens as a first-class character so 'BISTRO+6' does
# not collapse to 'bistro6' and then split to {bistro, 6} — that bundle
# marker must stay distinct from the base 'bistro'.
_TOKEN_STRIP_RE = re.compile(r"[^a-z0-9а-яёіїєґ+]", re.UNICODE)
_PAREN_CONTENT_RE = re.compile(r"\([^)]*\)")

# Split at every letter↔digit transition so slitny and razdelny SKU forms
# align: 'ats12u' → {ats, 12, u}; 'hknlpd150s' → {hknlpd, 150, s}; 'eft60'
# → {eft, 60}. Tokens with '+' like 'bistro+6' do not pass this regex (the
# '+' sits between letters and the next digit and no letter↔digit boundary
# is directly available) so BISTRO+6 stays whole.
_ALNUM_BOUNDARY_RE = re.compile(
    r"(?<=[a-zа-яёіїєґ])(?=\d)|(?<=\d)(?=[a-zа-яёіїєґ])",
    re.UNICODE | re.IGNORECASE,
)


def _split_alnum_boundary(token: str) -> list[str]:
    """Split a token at every direct letter↔digit transition.

    'ats12u' → ['ats','12','u']; 'hknlpd150s' → ['hknlpd','150','s'];
    'eft60' → ['eft','60']; '75pe' → ['75','pe']. Pure letters or pure
    digits pass through. Tokens containing '+' (kept by _TOKEN_STRIP_RE)
    preserve '+' inside one chunk because the regex only fires on direct
    letter↔digit adjacency: 'bistro+6' → ['bistro+6'].
    """
    parts = _ALNUM_BOUNDARY_RE.split(token)
    return [p for p in parts if p]

# Glue a short uppercase letter prefix to a following digit token when the
# catalog stores a model with a space ("R 301", "IP 3500", "OGG 4070", "СМ 250").
# Lowercase tokens are not glued to avoid welding adjectives to sizes (e.g.
# "для 10" → "для10"). Restricted to 1-4 letters, which covers all observed
# model prefixes in the catalog while staying narrow enough to not disturb
# normal prose. Applied uniformly in extract_model_from_name and
# meaningful_tokens so strict-model equality and containment both see the
# same joined token on both sides.
_LETTER_DIGIT_GLUE_RE = re.compile(
    r"(?<![A-Za-zА-Яа-яІЇЄіїєҐґ0-9])"
    # Don't glue when the letter-prefix is itself a trailing SKU suffix
    # coming after a digit token ("ATS 12 U 1/2" must not glue "U 1" → "U1";
    # the trailing 'U' belongs to "ATS12", handled by TRAILING_LETTER_GLUE).
    r"(?<!\d\s)"
    r"([A-ZА-ЯІЇЄҐ]{1,4})\s+(\d)",
)

# Second-pass glue: fuse a trailing single uppercase letter to a preceding
# letter-digit compound ("ATS12 U" → "ATS12U", "ATS22 UT" → "ATS22UT"). This
# catches razdelny catalog styles where the SKU suffix is written as a
# separate word after the digit ("ATS 12 U 1/2"). The first-pass glue merges
# the letter prefix and first digit; this second pass picks up the trailing
# letter token so strict-model equality and containment see identical
# "ATS12U" / "ATS22UT" tokens on both sides.
_TRAILING_LETTER_GLUE_RE = re.compile(
    r"([A-ZА-ЯІЇЄҐ]+\d+)\s+([A-ZА-ЯІЇЄҐ]{1,2})(?![A-Za-zА-Яа-яІЇЄіїєҐґ0-9])",
)

# Common uppercase descriptor words that appear in cookware product names and
# must NOT be glued to a following digit. Without this guard, "STAR PLUS 40"
# would become "STAR PLUS40" and tokenize as {star, plus40} instead of
# {star, plus, 40}, breaking the containment gate. All entries are either
# common English/Italian words or dictionary-like terms that never serve as a
# model prefix in the observed catalog (real model prefixes OFEI/OFGI/OTGD/
# OTGI/OTEI/QUBE are non-words and stay glued).
_GLUE_STOPWORDS = frozenset({
    "PLUS", "MAX", "MAXI", "MINI", "MIN", "PRO", "ECO", "BIO", "STD",
    "TOP", "STAR", "ULTRA", "SMART", "SLIM", "SUPER", "NEW", "OLD", "BIG",
    "CHEF", "AUTO", "CORE", "INOX", "MEAT", "SARO", "COMBI", "ALL", "HOT",
})

# Cyrillic suffix tokens that look like trailing SKU letters but are actually
# phase/voltage descriptors ("1Ф", "3Ф"). Strip them before the trailing-letter
# glue fires so "ATS12 Ф" does not collapse to "ATS12Ф".
_TRAILING_LETTER_STOPWORDS = frozenset({"Ф", "ф", "В", "в"})


def _glue_letter_digit(text: str) -> str:
    def _sub(m: re.Match[str]) -> str:
        letters, digit = m.group(1), m.group(2)
        if letters.upper() in _GLUE_STOPWORDS:
            return m.group(0)
        return f"{letters}{digit}"

    def _sub_trailing(m: re.Match[str]) -> str:
        compound, suffix = m.group(1), m.group(2)
        if suffix in _TRAILING_LETTER_STOPWORDS:
            return m.group(0)
        return f"{compound}{suffix}"

    text = _LETTER_DIGIT_GLUE_RE.sub(_sub, text)
    text = _TRAILING_LETTER_GLUE_RE.sub(_sub_trailing, text)
    return text


# Size-notation fractions that must NOT be treated as model codes.
# Catalog stores half-size grills as "1/2", supplier writes Roman "I/2" — both
# are size descriptors. Without this guard, extract_model_from_name returns
# "i2" for the supplier and "12" for the catalog (slash dropped by
# normalize_model), and the name-model mismatch gate rejects the pair even
# though everything else lines up. Covers Arabic/Arabic ("1/2", "3/4"),
# Roman/Arabic ("I/2", "II/3", "IV/2"), and Arabic/Roman ("2/I").
_SIZE_FRACTION_RE = re.compile(r"^(?:[IVXivx]+/\d+|\d+/[IVXivx]+|\d+/\d+)$")


def _is_size_fraction(token: str) -> bool:
    return bool(_SIZE_FRACTION_RE.match(token))


# Roman → Arabic map for size-fraction normalization. Restricted to I..X since
# catalog sizes never exceed single-digit numerators ("I/2", "II/3", rarely
# "IV/2"). Applied before tokenization so containment sees the same integer
# on both sides regardless of which script the numerator was written in.
_ROMAN_TO_ARABIC = {
    "i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5",
    "vi": "6", "vii": "7", "viii": "8", "ix": "9", "x": "10",
}
_ROMAN_FRACTION_RE = re.compile(
    r"(?<![A-Za-zА-Яа-яІЇЄіїєҐґ0-9])([IVXivx]{1,4})\s*/\s*(\d{1,2}|[IVXivx]{1,4})"
    r"(?![A-Za-zА-Яа-яІЇЄіїєҐґ0-9])",
)


def _normalize_roman_fractions(text: str) -> str:
    """Rewrite Roman-numerator size fractions ('I/2', 'II/3') to Arabic.

    Only touches tokens that look like size fractions — standalone Roman
    words in unrelated positions (e.g. a descriptor 'IV') are left alone
    because the regex requires the '/digit' pattern. Preserves original
    case elsewhere in the string.
    """
    if not text:
        return text

    def _sub(m: re.Match[str]) -> str:
        left = _ROMAN_TO_ARABIC.get(m.group(1).lower(), m.group(1))
        right_raw = m.group(2)
        right = _ROMAN_TO_ARABIC.get(right_raw.lower(), right_raw)
        return f"{left}/{right}"

    return _ROMAN_FRACTION_RE.sub(_sub, text)


def _near_duplicate_token(a: str, b: str) -> bool:
    """True if two tokens look like morphological variants (suffix-only diff).

    Accepts pairs like 'диска'/'диски' (gender/case), 'кухоний'/'кухонний'
    (typo/doubled consonant) but rejects semantically distinct tokens like
    'abs'/'inox', 'white'/'black', '40'/'60', or pairs where the diff adds
    a digit suffix ('bistro'/'bistro6' — the latter is a bundled variant,
    not a morphological form). Requires both tokens ≥4 chars, common prefix
    within 2 chars of the shorter length, and the diverging tails must be
    alphabetic (no digits — digits signal a distinct SKU variant).
    """
    if a == b:
        return True
    la, lb = len(a), len(b)
    if la < 4 or lb < 4 or abs(la - lb) > 2:
        return False
    common = 0
    for ca, cb in zip(a, b):
        if ca == cb:
            common += 1
        else:
            break
    if common < min(la, lb) - 2:
        return False
    if any(c.isdigit() for c in a[common:]) or any(c.isdigit() for c in b[common:]):
        return False
    return True


def _tokens_subset_morph(a: set[str], b: set[str]) -> bool:
    """Like a.issubset(b), but tolerates morphological near-duplicates.

    Each token in `a` must either be exactly in `b` or have a
    `_near_duplicate_token` partner in `b`. Used by the after-brand
    containment gate so that morphological noise in descriptor tokens
    does not falsely reject same-model matches.
    """
    missing = a - b
    if not missing:
        return True
    extras = b - a
    for tok in missing:
        if not any(_near_duplicate_token(tok, other) for other in extras):
            return False
    return True


def _digit_only_discriminator(sup: set[str], prom: set[str]) -> bool:
    """True when exactly one side has extras consisting ONLY of digit tokens.

    Digit-only extras mark SKU discriminators (series 'Neapolis 4' vs
    'Neapolis', size 'STAR PLUS 40' vs '60'). But a digit token embedded
    alongside descriptive words in extras means the other side just has a
    longer description ('21 кг/добу', '41 літ, 2 корзини') and is still
    the same model — subset_morph should apply there.

    Rule: trigger only when at least one side's extras are non-empty AND
    all of those extras are pure digits. If any extras side mixes digits
    with non-digit tokens, it is a description, not a discriminator.
    Standard mains voltages (220/230/380/400) are already stripped by
    `meaningful_tokens`, so any digit reaching this check is genuine.
    """
    def _all_digit_non_empty(s: set[str]) -> bool:
        return bool(s) and all(tok.isdigit() for tok in s)
    sup_extras = sup - prom
    prom_extras = prom - sup
    return _all_digit_non_empty(sup_extras) or _all_digit_non_empty(prom_extras)


# SKU discriminator suffix length threshold. Short (≤4 char) alphabetic tokens
# like 'RD', 'LD', 'B', 'F', 'ABS', 'INOX' mark SKU variants, not descriptors.
# Longer tokens (≥5 chars) are prose words ('решітка', 'кухонний', 'запасний')
# and indicate bundled accessories or verbose catalog wording — those should
# still match the base product via the subset-containment rule.
_SKU_DISCRIM_MAX_LEN = 4


def _short_alpha_discriminator(sup: set[str], prom: set[str]) -> bool:
    """True when exactly one side has short alphabetic tokens as its only extras.

    Short (≤4 char) pure-letter tokens appearing on ONE side only are SKU
    discriminators — 'RD'/'LD' (dishwasher variant), 'B'/'F' (model suffix),
    'ABS'/'INOX' (material). The base descriptions otherwise match; the lone
    short token is the SKU distinguisher.

    Rule: fires only when exactly ONE side's extras are non-empty AND all of
    that side's extras are pure-letter AND short. If BOTH sides have extras,
    subset_morph already rejects via the existing path (neither side is a
    subset of the other). If the single side's extras include a long word,
    it is a descriptor — don't trigger.

    Intentionally narrower than digit_only: mixed-length extras on one side
    ({'abs', 'корпус', '21', 'кг'}) stay with subset_morph, so verbose catalog
    rows like 'Brema CB184AHC ABS, корпус пластик 21 кг/добу' keep matching
    supplier's 'Brema CB184AHC ABS' where the supplier is a strict subset.
    """
    def _all_short_alpha(s: set[str]) -> bool:
        return bool(s) and all(
            tok.isalpha() and len(tok) <= _SKU_DISCRIM_MAX_LEN for tok in s
        )
    sup_extras = sup - prom
    prom_extras = prom - sup
    if sup_extras and not prom_extras:
        return _all_short_alpha(sup_extras)
    if prom_extras and not sup_extras:
        return _all_short_alpha(prom_extras)
    return False


def _asymmetric_sku_suffix(sup: set[str], prom: set[str]) -> bool:
    """True when one side's extras contain a 1-char Latin letter, other is empty.

    A lone 1-char ASCII letter in asymmetric extras is almost always an SKU
    marker — 'U' (Unger attachment in Apach ATS12U), 'B' (Built-in / Black),
    'F' (Front / Freezer), 'R' (Right). Real bug: 'Apach ATS 12 U 1/2 унгер
    1ф' matched 'APACH ATS 12 1Ф' at 95% because the supplier's extras {u, 1,
    2, унгер} are a mixed bag that neither digit_only nor short_alpha catch,
    and the base subset rule treated prom as ⊂ sup.

    Narrow by design: requires ONE side empty so verbose descriptors still
    pass (e.g. prom's 'корпус пластик 21 кг/добу' with supplier's exact base
    SKU — prom_extras have no 1-char Latin, rule skips, subset_morph accepts).
    """
    def _has_one_char_latin(s: set[str]) -> bool:
        return any(len(t) == 1 and t.isascii() and t.isalpha() for t in s)
    sup_extras = sup - prom
    prom_extras = prom - sup
    if sup_extras and not prom_extras:
        return _has_one_char_latin(sup_extras)
    if prom_extras and not sup_extras:
        return _has_one_char_latin(prom_extras)
    return False


def meaningful_tokens(text: str) -> set[str]:
    """Tokenize text into comparable normalized tokens.

    Parenthesized content is stripped before splitting: parens in catalog
    names usually hold either article/SKU codes ('(WZ9ENRA.0021988)'),
    quantity markers ('(набір 100 шт.)'), voltage tags ('(380 В)'), or
    minor spelling variants ('(саладета)' vs '(саладетта)') — none of which
    should drive a containment mismatch.

    Digits of any length are kept ('4' distinguishes 'RESTO 4' from 'RESTO 44').
    Letter tokens require length >= 2 (drops prepositions like 'з', 'в', 'і'),
    except 1-char Latin letters which are kept — catalog SKU suffixes like
    'GE-500 B DD' (where 'B' marks a Built-in variant distinct from bare
    'GE-500 DD') are almost always ASCII. Cyrillic 1-char tokens stay filtered
    since they are prepositions, not SKU markers.
    Standard mains voltage numbers (220/230/380/400) are excluded — they're
    handled by the dedicated voltage gate, not by token containment.
    """
    if not text:
        return set()
    # Normalize Roman-numerator size fractions ('I/2' → '1/2') so catalog
    # Arabic and supplier Roman halves produce the same digit tokens after
    # slash-splitting. Without this, {2} on one side vs {1, 2} on the other
    # creates a spurious digit-only diff that the containment gate would
    # reject as a model discriminator.
    pre = _normalize_roman_fractions(text)
    # Glue short uppercase model prefix to following digits before lowercasing
    # so "R 301" / "IP 3500" / "OGG 4070" become single tokens {r301,ip3500,...}.
    # Must run pre-lowercase because the regex keys on uppercase letters.
    cleaned = _PAREN_CONTENT_RE.sub(" ", _glue_letter_digit(pre).lower())
    out = set()
    for raw in _TOKEN_SPLIT_RE.split(cleaned):
        tok = _TOKEN_STRIP_RE.sub("", raw)
        if not tok:
            continue
        # Split at letter↔digit boundaries so "ATS12U" tokenizes like
        # "ATS 12 U" and the containment gate aligns slitny/razdelny catalog
        # styles. Pure-letter or pure-digit tokens come back as [tok].
        for sub in _split_alnum_boundary(tok):
            if not sub:
                continue
            if sub.isdigit():
                out.add(sub)
            elif len(sub) >= 2:
                out.add(sub)
            elif sub.isascii() and sub.isalpha():
                # 1-char Latin SKU suffix ('B', 'F', 'R', 'U') — keep as
                # discriminator. Cyrillic 1-char tokens (prepositions 'з',
                # 'в', 'і') stay filtered.
                out.add(sub)
    return out - VOLTAGE_TAGS


# Cyrillic → Latin transliteration for cross-script type comparison.
# Catalog sometimes mixes "Гриль Salamandra" (Cyrillic category + Latin model
# name) with supplier's "Гриль саламандра" (all-Cyrillic) — token_sort_ratio
# then collapses to ~22 because "саламандра" vs "salamandra" share no literal
# characters. Normalizing both sides to Latin lets the ratio compare meaning
# rather than script.
_CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "ґ": "g", "д": "d", "е": "e",
    "ё": "e", "є": "ye", "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e",
    "ю": "yu", "я": "ya",
}


def _transliterate_cyr(text: str) -> str:
    out = []
    for ch in text.lower():
        out.append(_CYR_TO_LAT.get(ch, ch))
    return "".join(out)


def extract_product_type(name: str, brand: str | None) -> str:
    """Extract product type from name — words before the brand.

    Example: "Макароноварка ел. Angelo Po 0S1CP1E" with brand "Angelo Po"
             → "Макароноварка ел."
    """
    if not name:
        return ""
    if not brand or not brand.strip():
        return ""

    name_lower = name.lower()
    brand_lower = brand.strip().lower()

    idx = name_lower.find(brand_lower)
    if idx <= 0:
        return ""

    type_part = name[:idx].strip()
    # Remove trailing punctuation/noise
    type_part = re.sub(r"[\s.,:;()\-]+$", "", type_part).strip()

    if len(type_part) < MIN_TYPE_LENGTH:
        return ""

    return type_part


def find_match_candidates(
    supplier_product_name: str,
    supplier_brand: str | None,
    prom_products: list[dict],
    score_cutoff: float = SCORE_CUTOFF,
    limit: int = MATCH_LIMIT,
    supplier_price_cents: int | None = None,
    supplier_model: str | None = None,
    supplier_article: str | None = None,
) -> list[dict]:
    """Find top match candidates for a supplier product against prom catalog.

    Uses brand-based blocking to reduce search space, then WRatio scorer
    for fuzzy name matching, with product type gate and model matching.

    Args:
        supplier_product_name: Name of the supplier product to match.
        supplier_brand: Brand/vendor of the supplier product (optional).
        prom_products: List of dicts with keys: id, name, brand, price,
            model (optional), article (optional).
        score_cutoff: Minimum score threshold (default 60%).
        limit: Maximum candidates to return (default 3).
        supplier_price_cents: Supplier product price in cents (optional).
        supplier_model: Supplier product model field (optional).
        supplier_article: Supplier product article/vendorCode (optional).

    Returns:
        List of candidate dicts sorted by score descending:
        [{"prom_product_id": int, "score": float, "prom_name": str,
          "confidence": str}, ...]
    """
    if not prom_products or not supplier_product_name:
        return []

    # Step 1: Brand-based blocking
    # When supplier has a brand, it MUST exist in the catalog. If we don't
    # stock that brand, no product in the catalog can be a valid match —
    # falling back to the full pool produces word-overlap junk ("Плита X"
    # matching "Плита Y" from an unrelated brand). Return empty instead.
    # When supplier brand is missing (MARESTO skipped <vendor>), we require
    # catalog brand to also be missing — cross-brand matching with unknown
    # supplier brand produces nonsense (Термометр GLKG10 vs Гриль GGM).
    candidates_pool = prom_products
    brand_was_matched = False
    sup_brand_present = bool(supplier_brand and supplier_brand.strip())
    if sup_brand_present:
        brand_lower = supplier_brand.strip().lower()
        brand_filtered = [
            p
            for p in prom_products
            if p.get("brand")
            and fuzz.ratio(p["brand"].lower(), brand_lower) > BRAND_MATCH_THRESHOLD
        ]
        if brand_filtered:
            candidates_pool = brand_filtered
            brand_was_matched = True
        else:
            logger.debug(
                "Supplier brand %r not found in catalog — skipping product",
                supplier_brand,
            )
            return []
    else:
        # Both-None policy: only compare against pp rows also missing a brand,
        # and tighten the score cutoff (full-catalog fuzzy is too noisy without
        # brand anchor).
        candidates_pool = [p for p in prom_products if not (p.get("brand") and p["brand"].strip())]
        if not candidates_pool:
            return []
        score_cutoff = max(score_cutoff, CONFIDENCE_HIGH)

    # Step 2: Build choices dict — {prom_id: normalized_name}
    choices = {p["id"]: normalize_text(p["name"]) for p in candidates_pool}

    if not choices:
        return []

    # Step 2.5: Article/Model exact-match fast path
    fast_match_ids = set()
    fast_matches = []
    sup_model = normalize_model(supplier_model)
    sup_article = normalize_model(supplier_article)

    # Also try extracting model from name when fields are empty
    sup_name_model_for_fast = ""
    if not sup_model and not sup_article and brand_was_matched and supplier_brand:
        sup_name_model_for_fast = extract_model_from_name(supplier_product_name, supplier_brand)

    # Normalize supplier name once for display_article substring checks.
    # Horoshop's "Артикул для відображення на сайті" (e.g. Sirman "60SN002") is
    # often embedded verbatim inside supplier names (Merx, MARESTO), so a
    # containment check on the normalized forms is a very strong match signal.
    sup_name_norm = normalize_model(supplier_product_name)

    if sup_model or sup_article or sup_name_model_for_fast or sup_name_norm:
        sup_name_model_for_fast_norm = normalize_model(sup_name_model_for_fast)
        for p in candidates_pool:
            prom_article = normalize_model(p.get("article"))
            prom_model = normalize_model(p.get("model"))
            prom_display = normalize_model(p.get("display_article"))

            # Strict equality after normalize — "XFT133" != "XFT134"
            matched = False
            display_match = False
            if sup_article and prom_article and sup_article == prom_article:
                matched = True
            if not matched and sup_model and prom_model and sup_model == prom_model:
                matched = True
            # Display article (manufacturer SKU from catalog card) fast-path.
            # Length >=4 to avoid trivial substring collisions on short codes.
            # Manufacturer SKUs are unique per product variant — when found,
            # bypass the after-brand containment gate (which would otherwise
            # reject "Sirman 60SN002 LT10" vs "Sirman Plutone LT10" because
            # the descriptor tokens differ).
            if not matched and prom_display and len(prom_display) >= 4:
                if sup_article and sup_article == prom_display:
                    matched = True
                    display_match = True
                elif (
                    sup_name_norm
                    and len(prom_display) >= 6
                    and any(c.isalpha() for c in prom_display)
                    and any(c.isdigit() for c in prom_display)
                    and prom_display in sup_name_norm
                ):
                    matched = True
                    display_match = True

            # Fallback: compare model numbers extracted from names (also strict)
            if not matched and sup_name_model_for_fast_norm:
                prom_brand = p.get("brand") or supplier_brand
                prom_name_model = normalize_model(
                    extract_model_from_name(p["name"], prom_brand)
                )
                if prom_name_model and sup_name_model_for_fast_norm == prom_name_model:
                    matched = True

            # Pure-letter manufacturer SKUs (HKN-FNT-M, HKN-LPD-S): when the
            # supplier provided article is a dash-joined letter-only code and
            # appears verbatim inside the prom product name, accept as SKU
            # match. Extracting model from name requires a digit token
            # (skipped for dash-only letter SKUs), and the after-brand
            # containment gate rejects when descriptor extras don't overlap
            # (sp#4698 'з набором дисків' vs pp#3269 'з електронним блоком').
            #
            # Restricted to "raw article has a dash AND no digits" so digit-
            # bearing articles like 'ATS12U 1/2' do NOT skip the voltage/
            # phase post-gate (sp#4529 '3ф' must not collide with pp#2980
            # '220 В 1ф' just because the SKU string overlaps). Length >=6
            # post-normalize mirrors the prom_display branch above.
            if not matched and sup_article and len(sup_article) >= 6:
                raw_article = (supplier_article or "").strip()
                has_dash = "-" in raw_article
                has_digit = any(c.isdigit() for c in raw_article)
                is_pure_letter_sku = has_dash and not has_digit
                if is_pure_letter_sku:
                    prom_name_norm = normalize_model(p["name"])
                    if prom_name_norm and sup_article in prom_name_norm:
                        matched = True
                        display_match = True

            # Digit-bearing article fast-path: when catalog has no explicit
            # article/display (~186 NP pp rows of Hurakan/Apach/Fagor/Tatra),
            # the full SKU ("HKN-20SN2V", "AFN-1602 EXP", "AC800dig DD") lives
            # only inside pp.name. Descriptor words in sp.name ("на 20 л дві
            # швидкості" vs pp "20 л, 2 шв.") break the containment gate, and
            # fuzzy doesn't always surface these pairs above the threshold.
            # Guard against prefix collisions (sp 'APE8AD' vs pp 'APE8ADS') by
            # enforcing word-boundary on raw pp.name.
            if (
                not matched
                and sup_article
                and len(sup_article) >= 6
                and not prom_article
                and not prom_display
            ):
                raw_article = (supplier_article or "").strip()
                # Require structural SKU markers: digit OR non-alphanumeric
                # separator (dash, space, dot, paren). Pure-letter no-structure
                # strings like "HKNFNTMNEW" are too weak a signal — fall back
                # to fuzzy + containment for those.
                has_digit = any(c.isdigit() for c in raw_article)
                has_structure = any(not c.isalnum() for c in raw_article)
                if len(raw_article) >= 5 and (has_digit or has_structure):
                    prom_name_norm = normalize_model(p["name"])
                    if prom_name_norm and sup_article in prom_name_norm:
                        raw_article_fixed = _fix_cyrillic_homoglyphs(raw_article)
                        prom_name_fixed = _fix_cyrillic_homoglyphs(p["name"] or "")
                        escaped = re.escape(raw_article_fixed)
                        # Flexible internal whitespace in article.
                        escaped = re.sub(r"(\\[ \t])+", r"\\s+", escaped)
                        boundary_re = re.compile(
                            rf"(?<![0-9A-Za-zА-Яа-яЁёІіЇїЄєҐґ]){escaped}"
                            rf"(?![0-9A-Za-zА-Яа-яЁёІіЇїЄєҐґ])",
                            re.IGNORECASE | re.UNICODE,
                        )
                        if boundary_re.search(prom_name_fixed):
                            matched = True
                            display_match = True

            if matched and p["id"] not in fast_match_ids:
                fast_match_ids.add(p["id"])
                fast_matches.append(
                    {
                        "prom_product_id": p["id"],
                        "score": 100.0,
                        "prom_name": p["name"],
                        "confidence": "high",
                        "_skip_post_gates": display_match,
                    }
                )
                if len(fast_matches) >= limit:
                    break

    # Step 3: Extract matches using rapidfuzz WRatio.
    # Oversample FUZZY_OVERSAMPLE_LIMIT candidates and let post-gates filter
    # them down. Final truncation to MATCH_LIMIT happens after all gates run
    # so descriptor-word noise can't bury a correct SKU match (sp#4698
    # 'HKN-FNT-M з набором дисків' where pp#3269 'HKN-FNT-M NEW з електронним
    # блоком' scores 63% while pp#3291 'HKN-FNT-A З НАБОРОМ ДИСКІВ' scores 93%).
    fuzzy_limit = limit - len(fast_matches)
    fuzzy_output = []
    if fuzzy_limit > 0:
        extract_limit = max(FUZZY_OVERSAMPLE_LIMIT, fuzzy_limit + len(fast_match_ids))
        results = process.extract(
            normalize_text(supplier_product_name),
            choices,
            scorer=fuzz.WRatio,
            processor=utils.default_process,
            score_cutoff=score_cutoff,
            limit=extract_limit,
        )

        # Step 4: Build result list (skip fast-path matches).
        # Do NOT slice to fuzzy_limit here — post-gates need visibility into
        # all oversampled candidates to promote the correct target when raw
        # WRatio ranks an accessory-descriptor sibling higher.
        for matched_name, score, prom_id in results:
            if prom_id in fast_match_ids:
                continue
            fuzzy_output.append(
                {
                    "prom_product_id": prom_id,
                    "score": round(score, 2),
                    "prom_name": matched_name,
                    "confidence": get_confidence_label(score),
                }
            )

    # Step 4.5: Type gate — reject candidates where product types differ
    if brand_was_matched and supplier_brand:
        supplier_type = extract_product_type(supplier_product_name, supplier_brand)
        if supplier_type:
            type_filtered = []
            for candidate in fuzzy_output:
                # Find prom product brand for type extraction
                prom_brand = None
                prom_name_full = candidate["prom_name"]
                for p in candidates_pool:
                    if p["id"] == candidate["prom_product_id"]:
                        prom_brand = p.get("brand") or supplier_brand
                        prom_name_full = p["name"]
                        break

                prom_type = extract_product_type(prom_name_full, prom_brand)
                if prom_type:
                    # Transliterate both to Latin so Cyrillic "саламандра"
                    # and Latin "Salamandra" compare as the same token.
                    type_score = fuzz.token_sort_ratio(
                        _transliterate_cyr(supplier_type),
                        _transliterate_cyr(prom_type),
                    )
                    if type_score < TYPE_MATCH_THRESHOLD:
                        logger.debug(
                            "Type gate rejected: '%s' vs '%s' (score=%d) for prom_id=%d",
                            supplier_type,
                            prom_type,
                            type_score,
                            candidate["prom_product_id"],
                        )
                        continue
                # If type couldn't be extracted, let it pass
                type_filtered.append(candidate)
            fuzzy_output = type_filtered

    # Step 4.6: Model field gate — when both sides have the same field (article
    # or model) populated, require exact literal equality. Mismatch = reject.
    # Match = small score boost.
    if sup_model or sup_article:
        kept = []
        for candidate in fuzzy_output:
            prom_model = ""
            prom_article = ""
            for p in candidates_pool:
                if p["id"] == candidate["prom_product_id"]:
                    prom_model = normalize_model(p.get("model"))
                    prom_article = normalize_model(p.get("article"))
                    break

            has_both = False
            exact = False
            if sup_article and prom_article:
                has_both = True
                exact = sup_article == prom_article
            elif sup_model and prom_model:
                has_both = True
                exact = sup_model == prom_model

            if has_both and not exact:
                logger.debug(
                    "Model field mismatch rejected: sup='%s' vs prom='%s' for prom_id=%d",
                    sup_article or sup_model, prom_article or prom_model,
                    candidate["prom_product_id"],
                )
                continue
            if has_both and exact:
                candidate["score"] = min(
                    100.0, round(candidate["score"] + MODEL_BOOST_POINTS, 2)
                )
                candidate["confidence"] = get_confidence_label(candidate["score"])
            kept.append(candidate)
        fuzzy_output = kept

    # Step 4.7: Display-article mismatch gate.
    # When the supplier name embeds a manufacturer article code in parentheses
    # (e.g. "Rational iVario Pro 2-S (WY9ENRA.0011923)") AND the catalog has a
    # display_article filled in, they MUST match after normalization — otherwise
    # these are different SKUs of the same product family (voltage/capacity/
    # generation variants). Catches cases where fuzzy name score hits 100%
    # because the base description is identical.
    sup_paren_codes = [normalize_model(c) for c in extract_article_codes(supplier_product_name)]
    sup_paren_codes = [c for c in sup_paren_codes if c]
    if sup_paren_codes:
        kept = []
        for candidate in fast_matches + fuzzy_output:
            prom_display = ""
            prom_article_norm = ""
            for p in candidates_pool:
                if p["id"] == candidate["prom_product_id"]:
                    prom_display = normalize_model(p.get("display_article"))
                    prom_article_norm = normalize_model(p.get("article"))
                    break
            prom_codes = {c for c in (prom_display, prom_article_norm) if c}
            if not prom_codes:
                kept.append(candidate)
                continue
            if any(sc in prom_codes for sc in sup_paren_codes):
                kept.append(candidate)
            else:
                logger.debug(
                    "Paren-code mismatch rejected: sup=%s vs prom=%s for prom_id=%d",
                    sup_paren_codes, prom_codes, candidate["prom_product_id"],
                )
        fast_ids = {c["prom_product_id"] for c in fast_matches}
        fast_matches = [c for c in kept if c["prom_product_id"] in fast_ids]
        fuzzy_output = [c for c in kept if c["prom_product_id"] not in fast_ids]

    # Step 4.7: Name-based model gate — when article/model fields are empty,
    # extract model numbers from product names. If both have extracted models
    # and they don't match after strict normalize, reject the candidate.
    # Catches SNACK2100TN-FC vs SNACK3100TN-FC (fuzz.ratio=93%, looks similar
    # but clearly different products).
    if brand_was_matched and supplier_brand:
        sup_name_model = normalize_model(
            extract_model_from_name(supplier_product_name, supplier_brand)
        )
        if sup_name_model:
            kept = []
            for candidate in fuzzy_output:
                prom_name_full = candidate["prom_name"]
                prom_brand_for_model = supplier_brand  # same brand due to blocking
                for p in candidates_pool:
                    if p["id"] == candidate["prom_product_id"]:
                        prom_brand_for_model = p.get("brand") or supplier_brand
                        prom_name_full = p["name"]
                        break

                prom_name_model = normalize_model(
                    extract_model_from_name(prom_name_full, prom_brand_for_model)
                )
                if prom_name_model and sup_name_model != prom_name_model:
                    logger.debug(
                        "Name-model mismatch rejected: '%s' vs '%s' for prom_id=%d",
                        sup_name_model, prom_name_model,
                        candidate["prom_product_id"],
                    )
                    continue
                kept.append(candidate)
            fuzzy_output = kept

    # Step 4.8: Voltage variant gate — applies to BOTH fast-path and fuzzy.
    # Same model with (220) vs (380) = different SKU in the store.
    sup_voltages = extract_voltages(supplier_product_name)

    def _voltage_ok(candidate) -> bool:
        if not sup_voltages:
            return True
        prom_name_full = candidate["prom_name"]
        for p in candidates_pool:
            if p["id"] == candidate["prom_product_id"]:
                prom_name_full = p["name"]
                break
        prom_voltages = extract_voltages(prom_name_full)
        if prom_voltages and not (sup_voltages & prom_voltages):
            logger.debug(
                "Voltage variant rejected: sup=%s vs prom=%s for prom_id=%d",
                sup_voltages, prom_voltages, candidate["prom_product_id"],
            )
            return False
        return True

    fast_matches = [c for c in fast_matches if _voltage_ok(c)]
    fuzzy_output = [c for c in fuzzy_output if _voltage_ok(c)]

    # Step 4.9: After-brand token-containment gate.
    # Within the same brand, false positives arise when the model code matches
    # fuzzily but the NON-model tokens (variant markers like ABS/INOX/BISTRO+6,
    # size digits like 40/60, descriptive suffixes like "з важелем") differ.
    # Rule: one side's after-brand tokens must be a subset of the other's.
    # Bidirectional so that supplier names carrying extra accessories
    # ("VIS60 + решітка + ЭПУ") still match the base PROM product "VIS60".
    run_containment = (brand_was_matched and supplier_brand) or not sup_brand_present
    if run_containment:
        if sup_brand_present:
            sup_after_tokens = meaningful_tokens(
                after_brand_remainder(supplier_product_name, supplier_brand)
            )
        else:
            # No brand to strip — compare full-name meaningful tokens.
            sup_after_tokens = meaningful_tokens(supplier_product_name)
        if sup_after_tokens:
            contained = []
            for candidate in fast_matches + fuzzy_output:
                # display_article fast-matches bypass containment — manufacturer
                # SKU equality is stronger evidence than name-token similarity.
                if candidate.get("_skip_post_gates"):
                    contained.append(candidate)
                    continue
                prom_name_full = candidate["prom_name"]
                prom_brand_for_tokens = supplier_brand
                for p in candidates_pool:
                    if p["id"] == candidate["prom_product_id"]:
                        prom_brand_for_tokens = p.get("brand") or supplier_brand
                        prom_name_full = p["name"]
                        break
                prom_after_tokens = meaningful_tokens(
                    after_brand_remainder(prom_name_full, prom_brand_for_tokens)
                )
                if not prom_after_tokens:
                    contained.append(candidate)
                    continue
                # Sub-brand / family names may sit BEFORE the brand on one side
                # and AFTER on the other (e.g. catalog "Гриль Salamandra SIRMAN
                # Mobile PRO 1/2" vs supplier "Sirman SALAMANDRA MOBILE PRO I/2"
                # — "salamandra" is in both full names but captured after-brand
                # only on the supplier side). Don't let such positioning
                # asymmetry create false after-brand differences: drop tokens
                # from one side's after-brand set that the OTHER side already
                # has somewhere in its full name.
                sup_full_tokens = meaningful_tokens(supplier_product_name)
                prom_full_tokens = meaningful_tokens(prom_name_full)
                sup_only_pre = sup_full_tokens - sup_after_tokens
                prom_only_pre = prom_full_tokens - prom_after_tokens
                sup_after_eff = sup_after_tokens - prom_only_pre
                prom_after_eff = prom_after_tokens - sup_only_pre
                if not sup_after_eff or not prom_after_eff:
                    contained.append(candidate)
                    continue
                # Pure-digit-only extras on one side discriminate SKUs —
                # reject before the subset check would otherwise absorb it.
                # Handles 'Neapolis 4' vs 'Neapolis (без розстійки)' where
                # extract_model_from_name cannot latch onto the single
                # digit so the name-model gate leaves the pair intact.
                if _digit_only_discriminator(sup_after_eff, prom_after_eff):
                    logger.debug(
                        "Containment rejected (digit-only discriminator): "
                        "sup=%s prom=%s for prom_id=%d",
                        sup_after_eff, prom_after_eff,
                        candidate["prom_product_id"],
                    )
                # Short alphabetic extras on ONE side (≤4 chars, pure letters)
                # are SKU discriminators (RD/LD/B/F/ABS/INOX), not accessory
                # descriptors. Handles 'GT-500 DD' vs 'GT-500 RD DD' where
                # extract_model_from_name returns the same token on both
                # sides and subset_morph would otherwise absorb the 'rd' diff.
                elif _short_alpha_discriminator(sup_after_eff, prom_after_eff):
                    logger.debug(
                        "Containment rejected (short-alpha discriminator): "
                        "sup=%s prom=%s for prom_id=%d",
                        sup_after_eff, prom_after_eff,
                        candidate["prom_product_id"],
                    )
                # Lone 1-char Latin in asymmetric extras = SKU suffix.
                # Catches 'ATS 12 U 1/2 унгер' vs 'ATS 12' where sup's extras
                # mix the 'u' marker with digits and a long Cyrillic word —
                # neither short_alpha nor digit_only fires there.
                elif _asymmetric_sku_suffix(sup_after_eff, prom_after_eff):
                    logger.debug(
                        "Containment rejected (asymmetric 1-char Latin SKU suffix): "
                        "sup=%s prom=%s for prom_id=%d",
                        sup_after_eff, prom_after_eff,
                        candidate["prom_product_id"],
                    )
                elif _tokens_subset_morph(sup_after_eff, prom_after_eff) or (
                    _tokens_subset_morph(prom_after_eff, sup_after_eff)
                ):
                    contained.append(candidate)
                else:
                    logger.debug(
                        "Containment rejected: sup=%s prom=%s diff=%s for prom_id=%d",
                        sup_after_eff, prom_after_eff,
                        sup_after_eff ^ prom_after_eff,
                        candidate["prom_product_id"],
                    )
            fast_ids = {c["prom_product_id"] for c in fast_matches}
            fast_matches = [c for c in contained if c["prom_product_id"] in fast_ids]
            fuzzy_output = [c for c in contained if c["prom_product_id"] not in fast_ids]

    # Merge fast-path + fuzzy, sort by score
    output = fast_matches + fuzzy_output
    output.sort(key=lambda x: x["score"], reverse=True)
    output = output[:limit]

    # Filter out candidates that dropped below cutoff after penalty
    output = [c for c in output if c["score"] >= score_cutoff]

    # Step 5: Price plausibility gate — reject implausible price ratios
    if supplier_price_cents and supplier_price_cents > 0:
        plausible = []
        for candidate in output:
            prom_price = None
            for p in candidates_pool:
                if p["id"] == candidate["prom_product_id"]:
                    prom_price = p.get("price")
                    break
            if prom_price and prom_price > 0:
                ratio = max(supplier_price_cents / prom_price, prom_price / supplier_price_cents)
                if ratio > MAX_PRICE_RATIO:
                    logger.debug(
                        "Price plausibility rejected: supplier=%d vs prom=%d (ratio=%.1fx) for prom_id=%d",
                        supplier_price_cents, prom_price, ratio, candidate["prom_product_id"],
                    )
                    continue
            plausible.append(candidate)
        output = plausible

    for c in output:
        c.pop("_skip_post_gates", None)
    return output


def find_match_for_product(
    supplier_product,
    exclude_prom_ids: list[int] | None = None,
) -> ProductMatch | None:
    """Find the best match candidate for a single supplier product.

    Used by the match review UI when a match is rejected and the system
    needs to find an alternative candidate.

    Args:
        supplier_product: SupplierProduct instance to match.
        exclude_prom_ids: List of prom product IDs to exclude (e.g., rejected ones).

    Returns:
        A new ProductMatch instance (not yet added to session) or None.
    """
    prom_all = db.session.execute(select(PromProduct)).scalars().all()

    exclude_set = set(exclude_prom_ids or [])
    prom_list = [
        {"id": p.id, "name": p.name, "brand": p.brand, "price": p.price,
         "model": p.model, "article": p.article, "display_article": p.display_article}
        for p in prom_all
        if p.id not in exclude_set
    ]

    if not prom_list:
        return None

    candidates = find_match_candidates(
        supplier_product.name,
        supplier_product.brand,
        prom_list,
        supplier_price_cents=supplier_product.price_cents,
        supplier_model=supplier_product.model,
        supplier_article=supplier_product.article,
        limit=1,
    )

    if not candidates:
        return None

    best = candidates[0]

    # Check if this pair already exists
    existing = db.session.execute(
        select(ProductMatch).where(
            ProductMatch.supplier_product_id == supplier_product.id,
            ProductMatch.prom_product_id == best["prom_product_id"],
        )
    ).scalar_one_or_none()

    if existing:
        return None

    return ProductMatch(
        supplier_product_id=supplier_product.id,
        prom_product_id=best["prom_product_id"],
        score=best["score"],
        status="candidate",
    )


def run_matching_for_supplier(supplier_id: int) -> int:
    """Run fuzzy matching for all unmatched products of a supplier.

    Skips products that already have confirmed or manual matches.
    Creates ProductMatch rows with status='candidate' for human review.

    Args:
        supplier_id: ID of the supplier to process.

    Returns:
        Count of new match candidates generated.
    """
    # Step 1: Get THIS supplier's product IDs with confirmed/manual matches
    # (skip these). Scoping by supplier_id keeps the id set small; without
    # the join we'd load every confirmed sp_id across all suppliers.
    matched_ids_query = (
        select(ProductMatch.supplier_product_id)
        .join(SupplierProduct, ProductMatch.supplier_product_id == SupplierProduct.id)
        .where(
            SupplierProduct.supplier_id == supplier_id,
            ProductMatch.status.in_(["confirmed", "manual"]),
        )
        .distinct()
    )
    matched_ids = set(
        db.session.execute(matched_ids_query).scalars().all()
    )

    # Step 2: Get unmatched supplier products (including unavailable — they may
    # come back in stock, and we want the catalog match ready in advance).
    # YML generator keeps unavailable items as available="false" in the feed.
    sp_query = select(SupplierProduct).where(
        SupplierProduct.supplier_id == supplier_id,
        SupplierProduct.id.notin_(matched_ids) if matched_ids else True,
    )
    unmatched_products = db.session.execute(sp_query).scalars().all()

    # Step 3: Load all prom products
    prom_all = db.session.execute(select(PromProduct)).scalars().all()
    prom_list = [
        {"id": p.id, "name": p.name, "brand": p.brand, "price": p.price,
         "model": p.model, "article": p.article, "display_article": p.display_article}
        for p in prom_all
    ]

    if not unmatched_products or not prom_list:
        logger.info(
            "No unmatched products or no prom catalog for supplier %d",
            supplier_id,
        )
        return 0

    # Step 4: Match each unmatched product
    total_candidates = 0
    for sp in unmatched_products:
        candidates = find_match_candidates(
            sp.name, sp.brand, prom_list,
            supplier_price_cents=sp.price_cents,
            supplier_model=sp.model,
            supplier_article=sp.article,
        )
        for c in candidates:
            # Check if pair already exists (avoid duplicates)
            existing = db.session.execute(
                select(ProductMatch).where(
                    ProductMatch.supplier_product_id == sp.id,
                    ProductMatch.prom_product_id == c["prom_product_id"],
                )
            ).scalar_one_or_none()

            if existing is None:
                match = ProductMatch(
                    supplier_product_id=sp.id,
                    prom_product_id=c["prom_product_id"],
                    score=c["score"],
                    status="candidate",
                )
                db.session.add(match)
                total_candidates += 1

    db.session.commit()
    logger.info(
        "%d new match candidates generated for supplier %d",
        total_candidates,
        supplier_id,
    )
    return total_candidates
