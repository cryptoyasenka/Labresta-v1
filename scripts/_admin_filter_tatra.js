(async () => {
  const tries = [
    '/adminLegacy/data.php?handler=17&dgFilter%5B4527%5D=2062006550',  // 4527 = Артикул column id
    '/adminLegacy/data.php?handler=17&dg_filter%5B4527%5D=2062006550',
    '/adminLegacy/data.php?handler=17&action=search&dg_search=2062006550',
    '/adminLegacy/data.php?handler=17&dg_search=2062006550',
    '/adminLegacy/data.php?handler=17&dgSearch=2062006550',
    '/adminLegacy/data.php?handler=17&search=2062006550',
  ];
  const out = {};
  for (const url of tries) {
    try {
      const r = await fetch(url, {credentials:'include'});
      const html = await r.text();
      // Look for "з NNNN" pagination — if filter works, NNNN should be small (1 or few)
      const pageMatch = html.match(/<span>(\d+)–(\d+)<\/span>\s*з\s*(\d+)/);
      // Look for an edit link to a product
      const editLinks = [...html.matchAll(/href="([^"]*handler=17[^"]*action=edit[^"]*)"/g)].slice(0,3).map(m=>m[1]);
      const dataIds = [...html.matchAll(/data-id="(\d+)"/g)].slice(0,5).map(m=>m[1]);
      // Find product NAME containing TATRA TET.87S in this page
      const tatraIdx = html.indexOf('TATRA TET.87S');
      out[url] = {
        total: pageMatch ? Number(pageMatch[3]) : null,
        range: pageMatch ? `${pageMatch[1]}-${pageMatch[2]}` : null,
        editLinks,
        dataIds,
        tatraIdx,
        tatraCtx: tatraIdx>=0 ? html.slice(Math.max(0,tatraIdx-300), tatraIdx+300).replace(/\s+/g,' ') : null
      };
    } catch (e) {
      out[url] = {error: String(e)};
    }
  }
  return JSON.stringify(out, null, 2);
})()
