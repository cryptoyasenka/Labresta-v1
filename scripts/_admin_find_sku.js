(async () => {
  const sr = await fetch('/adminLegacy/data.php?handler=17&action=search&q=2062006550', {credentials:'include'});
  const html = await sr.text();
  // Find ALL occurrences of the SKU
  const idxs = [];
  let i = 0;
  while ((i = html.indexOf('2062006550', i)) !== -1) {
    idxs.push(i);
    i++;
  }
  // Around each occurrence, capture 200 chars
  const ctx = idxs.map(idx => ({
    idx,
    around: html.slice(Math.max(0,idx-200), idx+200).replace(/\s+/g,' ')
  }));
  // Also count rows in the table
  const trRows = (html.match(/<tr [^>]*class="[^"]*datagrid-row[^"]*"/g) || []).length;
  const productLinks = [...html.matchAll(/href="([^"]*handler=17[^"]*action=edit[^"]*)"/g)].length;
  return JSON.stringify({total_occurrences: idxs.length, trRows, productLinks, ctx}, null, 2);
})()
