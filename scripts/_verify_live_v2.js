(async () => {
  const ts = Date.now();
  const checks = [
    {art:"1766968161", url:`https://labresta.com.ua/ru/termoprotsesor-sirman-softcooker-light-sous-vide/?_=${ts}`,
     want:["Термопроцессор SIRMAN Softcooker LIGHT","Sous Vide"],
     reject:["&deg;","&plusmn;","&laquo;","&ordm;","Апарат","Аппарат / термопроцессор"]},
    {art:"2110282234", url:`https://labresta.com.ua/ru/poverkhnia-dlia-smazhennia-goodfood-eg55r-rebrysta/?_=${ts}`,
     want:["GoodFood EG55R","двумя зонами"],
     reject:["одной зоной"]},
    {art:"1582804831", url:`https://labresta.com.ua/ru/frytiurnytsia-beckers-fr-8-lt/?_=${ts}`,
     want:["BECKERS FR 8 LT","Фритюрниця","обсмажування"],
     reject:["220 ВФритюрниц"]},
    // TATRA: try BOTH paths (root and /ua/) to figure out which serves UA
    {art:"2062006550-root", url:`https://labresta.com.ua/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/?_=${ts}`,
     want:["TATRA TET.87S","Підтримка чистоти","знімному","надлишк"],
     reject:[]},
    {art:"2062006550-ua",  url:`https://labresta.com.ua/ua/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/?_=${ts}`,
     want:["TATRA TET.87S","Підтримка чистоти","знімному","надлишк"],
     reject:[]},
    {art:"2062006550-ru",  url:`https://labresta.com.ua/ru/poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia/?_=${ts}`,
     want:["TATRA TET.87S"],
     reject:[]}
  ];
  const results = [];
  for (const c of checks) {
    try {
      const r = await fetch(c.url, {cache:'no-store', headers:{'Cache-Control':'no-cache','Pragma':'no-cache'}});
      const html = await r.text();
      const found = {};
      for (const w of c.want) found[w] = html.includes(w);
      const rej = {};
      for (const w of c.reject) rej[w] = html.includes(w);
      // Also probe for any UA-specific desc fragments
      const probes = ["Підтримка","перимет","знімному","надлишк","робочого простор","борта","бризок","гладкая","гладка"];
      const probe = {};
      for (const p of probes) probe[p] = html.includes(p);
      results.push({art:c.art, status:r.status, len:html.length, want:found, reject:rej, probe});
    } catch (e) {
      results.push({art:c.art, error: String(e)});
    }
  }
  return JSON.stringify(results, null, 2);
})()
