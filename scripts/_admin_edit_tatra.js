(async () => {
  const tries = [
    '/adminLegacy/data.php?handler=17&action=edit&id=2792',
    '/adminLegacy/data.php?handler=17&action=editForm&id=2792',
    '/adminLegacy/data.php?handler=17&id=2792',
    '/adminLegacy/data.php?handler=17&action=edit&item_id=2792',
    '/adminLegacy/products.php?id=2792',
    '/adminLegacy/data.php?handler=4&id=2792',  // some Horoshop installs use handler=4 for product edit
  ];
  const out = {};
  for (const url of tries) {
    try {
      const r = await fetch(url, {credentials:'include'});
      const html = await r.text();
      // Look for description-related textarea names
      const descMatches = {};
      for (const fname of ['description', 'description_ua', 'description_ru', 'descriptionUkr', 'descrUa', 'desc_ua', 'desc[ua]', 'desc[ru]']) {
        const re = new RegExp(`name=["']${fname.replace(/[\[\]]/g,'\\$&')}["'][^>]*>([\\s\\S]*?)</textarea>`, 'i');
        const m = html.match(re);
        if (m) descMatches[fname] = m[1].slice(0, 400);
      }
      // Find ALL textareas with their names+first 200 chars
      const textareas = [...html.matchAll(/<textarea[^>]*name=["']([^"']+)["'][^>]*>([\s\S]*?)<\/textarea>/gi)].slice(0,15).map(m=>({name:m[1], len:m[2].length, head:m[2].slice(0,150)}));
      out[url] = {
        status: r.status,
        len: html.length,
        title: (html.match(/<title>([^<]+)/)||[])[1],
        has_TATRA: html.includes('TATRA TET.87S'),
        descMatches,
        textareas
      };
    } catch (e) {
      out[url] = {error: String(e)};
    }
  }
  return JSON.stringify(out, null, 2);
})()
