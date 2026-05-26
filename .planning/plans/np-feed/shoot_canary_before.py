"""'BEFORE' снимок живой карточки HKN-PICO12M (публичная страница, read-only).
Пишет ТОЛЬКО в план-каталог. Репо/прод не трогает."""
import re
from playwright.sync_api import sync_playwright

BASE = "https://labresta.com.ua"
SLUG = "/khliborizka-hurakan-hkn-pico12m/"
OUTDIR = r"C:\Users\Yana\labresta-np-feed-plan"
PAGES = [("ua", BASE + SLUG), ("ru", BASE + "/ru" + SLUG)]

meta = []
with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={"width": 1440, "height": 1000},
                          locale="uk-UA")
    for tag, url in PAGES:
        pg = ctx.new_page()
        try:
            resp = pg.goto(url, wait_until="networkidle", timeout=45000)
            status = resp.status if resp else "?"
        except Exception as e:
            meta.append(f"[{tag}] {url} ERROR {e!r}")
            pg.close()
            continue
        pg.wait_for_timeout(2500)
        title = pg.title()
        # try to expand a description tab if present
        for sel in ["text=Опис", "text=Описание", "a:has-text('Опис')",
                    "a:has-text('Описание')", "[href*='description']"]:
            try:
                el = pg.locator(sel).first
                if el.count() and el.is_visible():
                    el.click(timeout=2500)
                    pg.wait_for_timeout(1200)
                    break
            except Exception:
                pass
        full = f"{OUTDIR}\\canary-before-{tag}-full.png"
        pg.screenshot(path=full, full_page=True)
        # description text
        desc_txt = ""
        for sel in ["#tab-description", ".product-description",
                    "[itemprop='description']", ".description", "#description"]:
            try:
                lo = pg.locator(sel).first
                if lo.count():
                    desc_txt = lo.inner_text(timeout=2500)
                    if desc_txt.strip():
                        break
            except Exception:
                pass
        body = pg.locator("body").inner_text()
        imgs = pg.locator("img").evaluate_all(
            "els => els.map(e => e.src).filter(s => s && /\\.(jpg|jpeg|png|webp)/i.test(s))")
        gallery = sorted(set(i for i in imgs if "pico12m" in i.lower()
                             or "/content/" in i.lower() or "uploads" in i.lower()))
        meta.append(f"[{tag}] status={status} title={title!r}")
        meta.append(f"[{tag}] screenshot={full}")
        meta.append(f"[{tag}] desc_len={len(desc_txt)} desc_head={desc_txt[:300]!r}")
        meta.append(f"[{tag}] candidate_images ({len(gallery)}):")
        for g in gallery[:20]:
            meta.append(f"    {g}")
        # save full description text
        with open(f"{OUTDIR}\\scratch_before_desc_{tag}.txt", "w",
                  encoding="utf-8") as f:
            f.write(f"URL: {url}\nTITLE: {title}\n\n--- DESC ELEMENT ---\n")
            f.write(desc_txt or "(не найден отдельный desc-элемент)")
            f.write("\n\n--- BODY (first 4000) ---\n")
            f.write(body[:4000])
        pg.close()
    br.close()

with open(f"{OUTDIR}\\scratch_canary_before.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(meta))
print("OK")
print("\n".join(m for m in meta if not m.startswith("    ")))
