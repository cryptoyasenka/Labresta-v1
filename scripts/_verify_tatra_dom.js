(async () => {
  const ts = Date.now();
  const url = `https://labresta.com.ua/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/?_=${ts}`;
  const r = await fetch(url, {cache:'no-store'});
  const html = await r.text();

  // Pull out the canonical/og:url to confirm which lang this serves
  const og = (html.match(/property="og:url"[^>]*content="([^"]+)"/) || [])[1];
  const canonical = (html.match(/rel="canonical"[^>]*href="([^"]+)"/) || [])[1];
  const htmlLang = (html.match(/<html[^>]*lang="([^"]+)"/) || [])[1];
  const title = (html.match(/<title[^>]*>([^<]+)/) || [])[1];

  // Try several common Horoshop description containers
  const blocks = {};
  for (const sel of [
    ['main-text', /<div[^>]*class="[^"]*main-text[^"]*"[^>]*>([\s\S]*?)<\/div>/i],
    ['product-description', /<div[^>]*class="[^"]*product[-_]description[^"]*"[^>]*>([\s\S]*?)<\/div>/i],
    ['itemprop-desc',  /<[^>]*itemprop="description"[^>]*>([\s\S]*?)<\//i],
    ['meta-desc',  /<meta[^>]*name="description"[^>]*content="([^"]+)"/i],
    ['og-desc',  /<meta[^>]*property="og:description"[^>]*content="([^"]+)"/i],
    ['h2',  /<h2[^>]*>([\s\S]*?)<\/h2>/i],
  ]) {
    const m = html.match(sel[1]);
    blocks[sel[0]] = m ? m[1].slice(0, 300) : null;
  }

  // Find all <h2> headings on page
  const h2s = [...html.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/gi)].map(m => m[1].replace(/<[^>]+>/g,'').trim()).slice(0,10);

  // First 200 chars of body text after stripping tags (rough)
  const stripped = html.replace(/<script[\s\S]*?<\/script>/gi,'').replace(/<style[\s\S]*?<\/style>/gi,'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  const idxTatra = stripped.indexOf('TATRA TET.87S');
  const around = idxTatra >= 0 ? stripped.slice(Math.max(0,idxTatra-50), idxTatra+800) : null;

  return JSON.stringify({status:r.status, len:html.length, og, canonical, htmlLang, title, blocks, h2s, around}, null, 2);
})()
