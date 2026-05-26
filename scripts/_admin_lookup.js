(async () => {
  // We're inside the Horoshop admin (labresta.com.ua/adminLegacy/...) — session cookies attached automatically
  const out = {};
  // Try several common Horoshop admin search endpoints
  const tries = [
    {name:'search_h17', url:'/adminLegacy/data.php?handler=17&action=search&q=2062006550'},
    {name:'getList_h17', url:'/adminLegacy/data.php?handler=17&action=getList&search=2062006550&q=2062006550&page=1'},
    {name:'index_h17', url:'/adminLegacy/data.php?handler=17&search=2062006550'},
    {name:'data_h17', url:'/adminLegacy/data.php?handler=17&filter%5Barticle%5D=2062006550'},
  ];
  for (const t of tries) {
    try {
      const r = await fetch(t.url, {credentials:'include'});
      const text = await r.text();
      // Look for any reference to 2062006550 with surrounding context
      const idx = text.indexOf('2062006550');
      out[t.name] = {
        status: r.status,
        len: text.length,
        ctype: r.headers.get('content-type'),
        sku_idx: idx,
        sample: idx >= 0 ? text.slice(Math.max(0,idx-100), idx+400) : text.slice(0, 200)
      };
    } catch (e) {
      out[t.name] = {error: String(e)};
    }
  }
  return JSON.stringify(out, null, 2);
})()
