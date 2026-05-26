(async () => {
  const checks = [
    {art:"1766968161", lang:"ru", slug:"termoprotsesor-sirman-softcooker-light-sous-vide",
     want:["Термопроцессор SIRMAN Softcooker LIGHT","Sous Vide"],
     reject:["&deg;","&plusmn;","&laquo;","&ordm;","Апарат","Аппарат / термопроцессор"]},
    {art:"2110282234", lang:"ru", slug:"poverkhnia-dlia-smazhennia-goodfood-eg55r-rebrysta",
     want:["GoodFood EG55R","двумя зонами"],
     reject:["одной зоной"]},
    {art:"1582804831", lang:"ru", slug:"frytiurnytsia-beckers-fr-8-lt",
     want:["BECKERS FR 8 LT","Фритюрниця","обсмажування"],
     reject:["220 ВФритюрниц"]},
    {art:"2062006550", lang:"ua", slug:"poverkhnia-dlia-smazhennia-tatra-tet.87s-hladkaia",
     want:["TATRA TET.87S","Підтримка чистоти робочого простору","знімному лотку"],
     reject:[]}
  ];
  const results = [];
  for (const c of checks) {
    const url = `https://labresta.com.ua/${c.lang}/${c.slug}/`;
    try {
      const r = await fetch(url, {cache:'no-store'});
      const html = await r.text();
      const found = {};
      for (const w of c.want) found[w] = html.includes(w);
      const rej = {};
      for (const w of c.reject) rej[w] = html.includes(w);
      results.push({art:c.art, status:r.status, len:html.length, want:found, reject:rej});
    } catch (e) {
      results.push({art:c.art, error: String(e)});
    }
  }
  return JSON.stringify(results, null, 2);
})()