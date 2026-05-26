(async () => {
  // Open the TATRA page in this tab itself and read JS state via DOM directly
  const url = 'https://labresta.com.ua/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/';
  const r = await fetch(url, {cache:'no-store'});
  const html = await r.text();
  // Find dataLayer pushes, product_id, item_id keywords
  const patterns = [
    /product_id["']?\s*[:=]\s*["']?(\d+)/gi,
    /item_id["']?\s*[:=]\s*["']?(\d+)/gi,
    /productId["']?\s*[:=]\s*["']?(\d+)/gi,
    /id["']?\s*:\s*(\d{4,8})/gi,
    /goods_id["']?\s*[:=]\s*["']?(\d+)/gi,
    /dataLayer\.push\(([\s\S]*?)\);/gi,
  ];
  const out = {};
  for (let i=0;i<patterns.length;i++){
    const matches = [...html.matchAll(patterns[i])].slice(0,3).map(m=>m[1] || m[0].slice(0,400));
    out[`p${i}`] = matches;
  }
  // Also look for "2062006550" itself in the page
  const skuIdx = html.indexOf('2062006550');
  out.sku_in_page = skuIdx >= 0 ? html.slice(Math.max(0,skuIdx-200), skuIdx+200).replace(/\s+/g,' ') : 'NOT FOUND';
  // Look for short URL with .html or .json variant
  const altUrls = [...html.matchAll(/[\/"]([^"'\s]+(?:tatra)[^"'\s]*)/gi)].slice(0,5).map(m=>m[1]);
  out.altUrls = altUrls;
  return JSON.stringify(out, null, 2);
})()
