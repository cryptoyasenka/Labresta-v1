"""Tests for Step 4.87 asymmetric bracket-token containment gate.

Step 4.85 fires only when BOTH sides carry parens with disjoint discriminator
sets. Step 4.87 covers the asymmetric case: one side has a paren with real
discriminator tokens, the other doesn't. If those tokens don't appear anywhere
in the other side's full text (name + article + display_article), the
candidate is a variant mismatch and gets rejected.

Exceptions:
  - '(no stand)' / '(без підставки)' — base-package signal, skip gate.
  - SP supplier_article appears verbatim in PP — PP parens are specs.
  - candidate has _skip_post_gates (display_article fast-match) — bypass.

Noise tokens (рівні / уровні / колби / персон / автомат / ручн / технолог /
приготуванн / preposition fillers) are stripped from discriminator before
the containment check, so legitimate descriptive parens like '(на 4 рівні)'
or '(приготування за технологією Sous Vide)' don't trigger rejection.
"""

from app.services.matcher import find_match_candidates


def _make_prom(id, name, brand="Sirman", price=150000, model=None,
               article=None, display_article=None):
    return {
        "id": id, "name": name, "brand": brand, "price": price,
        "model": model, "article": article, "display_article": display_article,
    }


class TestStep487AsymmetricRejects:
    """SP-paren disc with no echo in PP full text → reject."""

    def test_sirman_teflon_paren_vs_pp_no_teflon_rejected(self):
        # SP '(тефлон)' is a real variant marker; PP has no 'тефлон' anywhere.
        prom = [_make_prom(1, "Слайсер Sirman Mantegna 300", price=150000)]
        result = find_match_candidates(
            "Слайсер Sirman Mantegna 300 (тефлон)", "Sirman", prom,
            supplier_price_cents=150000,
        )
        assert result == []

    def test_robot_coupe_workstation_paren_rejected(self):
        # SP '(робоча станція)' — the work-station accessory bundle.
        # PP has neither 'робоча' nor 'станція' in name/article.
        prom = [_make_prom(1, "Robot Coupe CL55 з важелем",
                           brand="Robot Coupe", price=300000)]
        result = find_match_candidates(
            "Robot Coupe CL55 (робоча станція)", "Robot Coupe", prom,
            supplier_price_cents=300000,
        )
        assert result == []


class TestStep487PPSideRejects:
    """PP-paren disc with no echo in SP full text → reject."""

    def test_apach_pp_pidstavkoyu_vs_sp_plain_rejected(self):
        # PP '(з підставкою)' marker — stand bundle. SP plain APRE-77T/PL
        # has no 'підставкою' token. Reject.
        prom = [_make_prom(1, "Підлогова Apach APRE-77T (з підставкою)",
                           brand="Apach", price=900000)]
        result = find_match_candidates(
            "Apach APRE-77T/PL", "Apach", prom,
            supplier_price_cents=900000,
        )
        assert result == []

    def test_ewt_wik185_paren_vs_sp_block_motor_rejected(self):
        # PP '(WIK185)' — sub-model code variant. SP carries 'Блок-мотор'
        # for IB270TV with no 'WIK185' anywhere.
        prom = [_make_prom(1, "EWT IB270TV (WIK185)",
                           brand="EWT", price=80000)]
        result = find_match_candidates(
            "EWT Блок-мотор для IB270TV", "EWT", prom,
            supplier_price_cents=80000,
        )
        assert result == []


class TestStep487BasePackagePass:
    """'(no stand)' / '(без підставки)' = base-package marker, gate skipped."""

    def test_t64e_no_stand_vs_pp_plain_base_passes(self):
        # SP '(no stand)' is a base-version signal — the plain catalog row
        # IS the legitimate target despite no echo in PP text.
        prom = [_make_prom(1, "Піч для піци Moretti Forni T64E",
                           brand="Moretti Forni", price=839200)]
        result = find_match_candidates(
            "Moretti Forni T64E (no stand)", "Moretti Forni", prom,
            supplier_price_cents=916600,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_bez_pidstavki_vs_pp_plain_passes(self):
        # Cyrillic 'без' — same base-package semantics.
        prom = [_make_prom(1, "Піч Moretti Forni P60E",
                           brand="Moretti Forni", price=500000)]
        result = find_match_candidates(
            "Moretti Forni P60E (без підставки)", "Moretti Forni", prom,
            supplier_price_cents=500000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)


class TestStep487NoiseExpansion:
    """Noise stripping covers descriptive paren content — gate doesn't fire."""

    def test_tecnodom_pp_rivni_paren_passes(self):
        # PP '(на 4 рівні 440х350 мм)' — descriptive specs, not variant.
        # Noise: 'на' (preposition), '4' (digit), 'рівні' (рівн\w*), '440х350'
        # (digit/x), 'мм' — all stripped → empty discriminator → gate skip.
        prom = [_make_prom(1, "Шафа Tecnodom FEM04NE595V (на 4 рівні 440х350 мм)",
                           brand="Tecnodom", price=400000)]
        result = find_match_candidates(
            "Tecnodom FEM04NE595V", "Tecnodom", prom,
            supplier_price_cents=400000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_faby_pp_kolby_paren_passes(self):
        # PP '(3 колби х10 л)' — 'колби' (колб\w*) stripped, only specs left.
        prom = [_make_prom(1, "Соковижималка Faby 3NL (3 колби х10 л)",
                           brand="Faby", price=120000)]
        result = find_match_candidates(
            "Faby 3NL", "Faby", prom,
            supplier_price_cents=120000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_pp_pre_technology_descriptor_passes_via_overlap(self):
        # PP '(приготування за технологією Sous Vide)' vs SP '(Sous Vide)' —
        # 'приготування', 'за', 'технологією' all noise → PP disc {sous, vide};
        # SP disc {sous, vide}; Step 4.85 overlap pass; Step 4.87 subset pass.
        prom = [_make_prom(1, "Sirman Softcooker XP (приготування за технологією Sous Vide)",
                           brand="Sirman", price=150000)]
        result = find_match_candidates(
            "Sirman Softcooker XP (Sous Vide)", "Sirman", prom,
            supplier_price_cents=150000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)


class TestStep487ArticleBypass:
    """SP supplier_article verbatim in PP → bypass gate (PP parens = specs)."""

    def test_supplier_article_in_pp_specs_passes(self):
        # PP has temperature/abbrev specs in parens; SP article is a strong
        # signal these parens are descriptive, not variant markers.
        prom = [_make_prom(1, "Шафа FAGOR NEO CONCEPT AFN-1602 EXP (-18°C)",
                           brand="Fagor", price=600000)]
        result = find_match_candidates(
            "Шафа Fagor AFN-1602 EXP", "Fagor", prom,
            supplier_price_cents=600000,
            supplier_article="AFN-1602 EXP",
        )
        assert any(r["prom_product_id"] == 1 for r in result)


class TestStep487EdgeCases:
    """Empty parens, both-noise, no parens — gate stays inert."""

    def test_empty_parens_one_side_passes(self):
        prom = [_make_prom(1, "Sirman MyModel ()", brand="Sirman", price=50000)]
        result = find_match_candidates(
            "Sirman MyModel", "Sirman", prom,
            supplier_price_cents=50000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)

    def test_pp_only_noise_paren_passes(self):
        # PP '(380 В)' — pure noise. SP plain. Discriminator empty → no gate.
        prom = [_make_prom(1, "Картоплечистка Fimar PPN10 (380 В)",
                           brand="Fimar", price=120000)]
        result = find_match_candidates(
            "Fimar PPN10", "Fimar", prom,
            supplier_price_cents=120000,
        )
        assert any(r["prom_product_id"] == 1 for r in result)
