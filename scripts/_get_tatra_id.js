(async () => {
  const r = await fetch('/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/', {cache:'no-store'});
  const html = await r.text();
  // Common Horoshop product ID embeddings
  const patterns = {
    data_product_id: /data-product[-_]id="(\d+)"/i,
    product_id_meta: /productID[^>]*content="(\d+)"/i,
    product_id_json: /"productID"\s*:\s*"?(\d+)/i,
    sku_in_jsonld:   /"sku"\s*:\s*"([^"]+)"/i,
    horoshop_pid:    /horoshop[._]product[._]id[^=]*=\s*"?(\d+)/i,
    h_data_id:       /<[^>]*data-id="(\d+)"/g,
    body_class:      /<body[^>]*class="([^"]+)"/i,
    productItem:     /productItem[^=]*=\s*"?(\d+)/i,
    onclick_id:      /onclick="[^"]*addToCart\([^)]*?(\d+)/i,
  };
  const out = {};
  for (const [k,p] of Object.entries(patterns)) {
    if (p.global) {
      out[k] = [...html.matchAll(p)].slice(0,5).map(m=>m[1]);
    } else {
      const m = html.match(p);
      out[k] = m ? m[1] : null;
    }
  }
  // JSON-LD blob
  const jsonld = [...html.matchAll(/<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1].slice(0,500));
  out.jsonld_snippets = jsonld;
  return JSON.stringify(out, null, 2);
})()
