(async () => {
  // 1. Search the catalog list for SKU
  const sr = await fetch('/adminLegacy/data.php?handler=17&action=search&q=2062006550', {credentials:'include'});
  const html = await sr.text();

  // 2. Find product edit href — Horoshop admin lists usually link via data-id or onclick → editor
  // Try several patterns
  const patterns = [
    /href="([^"]*handler=17[^"]*action=edit[^"]*)"/gi,
    /href="([^"]*handler=17&id=\d+[^"]*)"/gi,
    /data-id="(\d+)"/gi,
    /onclick="[^"]*edit[^"]*(\d{4,})/gi,
    /<tr[^>]*data-id="(\d+)"[^>]*>[\s\S]{0,400}2062006550/gi,
  ];
  const hits = {};
  for (let i=0;i<patterns.length;i++){
    const m = [...html.matchAll(patterns[i])].slice(0,5).map(x=>x[1]);
    hits[`p${i}`] = m;
  }

  // 3. Look at context around the SKU match
  const idx = html.indexOf('2062006550');
  const before = html.slice(Math.max(0,idx-2000), idx);
  // Find data-id="NNN" pattern immediately preceding
  const rowIdMatch = before.match(/data-id="(\d+)"[^>]*>[^<]*$/m) || before.match(/data-id="(\d+)"/g);
  hits.row_context_500_before = before.slice(-800);
  hits.row_context_300_after = html.slice(idx, idx+800);
  hits.idx = idx;

  return JSON.stringify(hits, null, 2);
})()
