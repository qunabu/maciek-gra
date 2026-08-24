/* Service worker gry „Maciek kontra NFZ".

   Zasada: gra ma zawsze chodzić z najnowszej wersji, ale też działać bez
   internetu.

   • index.html, manifest i sam sw.js  -> NAJPIERW SIEĆ (cache to tylko zapas
     na offline), więc po wejściu zawsze widać świeżą wersję gry;
   • dźwięki, muzyka i obrazki         -> NAJPIERW CACHE, a w tle po cichu
     pobiera się nowsza wersja pliku, żeby start był natychmiastowy;
   • nowy worker NIE wchodzi na siłę — strona pyta gracza „nowa wersja,
     odświeżyć?" i dopiero wtedy woła skipWaiting.                           */

const WERSJA = '1.6.0';
const CACHE  = 'maciek-nfz-' + WERSJA;

/* to, co musi być dostępne offline od pierwszego uruchomienia */
const SZKIELET = [
  './',
  './index.html',
  './manifest.webmanifest',
  './maciek_ship.png',
  './artur_sprite.png',
  './mateusz_sprite.png',
  './baba1_sprite.png', './baba2_sprite.png', './baba3_sprite.png',
  './baba4_sprite.png', './baba5_sprite.png', './baba6_sprite.png',
  './ikona-192.png',
  './ikona-512.png',
  './ikona-maskowalna-512.png',
  './apple-touch-icon.png',
  './favicon-64.png'
];

/* audio dociągane po cichu już po instalacji — nie blokuje startu */
const AUDIO = [
  'sfx_strzal','sfx_bum','sfx_drukarka','sfx_monitor','sfx_paragraf','sfx_pacjent',
  'sfx_kara','sfx_boss','sfx_hit','sfx_smierc','sfx_hiper',
  'sfx_naprawa','sfx_klucz','sfx_toner','sfx_telefon','sfx_akordeon',
  'm_start','m_strzal1','m_strzal2','m_strzal3','m_drukarka','m_monitor','m_paragraf',
  'm_babcia','m_debil','m_pacjent','m_smierc','m_koniec','m_boss','m_zycie','m_kara',
  'm_wygrana','m_low','m_naprawa','m_toner','m_zepsuta',
  'u_fala','u_ostrzez','u_kara','u_kontrola','u_boss','u_koniec','u_ratio_ok','u_bonus','u_naprawa',
  'k_wejscie','k_atak1','k_atak2','k_atak3','k_atak4','k_trafiona','k_smierc','k_wygrana',
  'b_spoznil','b_drukarka','b_przycisk','b_czekac','b_prywatnie','b_kolejka',
  'b_internet','b_skladki','b_nawszystko','b_lekarz','b_monitor','b_stopa',
  'a_telefon','a_gdzie','a_100ms','a_oddzwon','a_zajete','a_nieodbiera',
  'mt_1','mt_2','mt_3','mt_4',
  'muz_menu','muz_gra','muz_boss','muz_koniec','muz_wygrana'
].map(n => './audio/' + n + '.mp3');

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    // pojedynczy brakujący plik nie może wywrócić instalacji
    await Promise.all(SZKIELET.map(u => c.add(new Request(u, { cache: 'reload' })).catch(() => {})));
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    const nazwy = await caches.keys();
    await Promise.all(nazwy.filter(n => n !== CACHE).map(n => caches.delete(n)));
    if (self.registration.navigationPreload) await self.registration.navigationPreload.enable();
    await self.clients.claim();
  })());
  /* audio dociągamy POZA waitUntil — w środku nowy worker wisiałby w stanie
     „activating" przez ~50 pobrań i podmiana wersji trwałaby wieki. Jeśli
     przeglądarka uśpi workera w połowie, pętla dokończy się przy następnym
     wejściu: pliki, które już są w cache, są pomijane. */
  dociagnijAudio();
});

async function dociagnijAudio() {
  const c = await caches.open(CACHE);
  for (const u of AUDIO) {
    if (await c.match(u)) continue;
    await c.add(new Request(u, { cache: 'reload' })).catch(() => {});
  }
  const klienci = await self.clients.matchAll();
  klienci.forEach(k => k.postMessage({ typ: 'offline-gotowe', wersja: WERSJA }));
}

self.addEventListener('message', e => {
  if (e.data === 'wskakuj') self.skipWaiting();
  if (e.data === 'wersja') e.source && e.source.postMessage({ typ: 'wersja', wersja: WERSJA });
});

/* do cache trafiają tylko pełne odpowiedzi 200 – kawałki plików (206, tak
   przeglądarka pobiera mp3) w Cache API nie wolno zapisywać */
function schowaj(c, zad, odp) {
  if (odp && odp.status === 200 && odp.type !== 'opaque') c.put(zad, odp.clone()).catch(() => {});
}

function najpierwSiec(zad, wstepne) {
  return (async () => {
    const c = await caches.open(CACHE);
    try {
      const odp = await (wstepne || fetch(zad, { cache: 'no-store' }));
      schowaj(c, zad, odp);
      return odp;
    } catch (err) {
      const zapas = await c.match(zad) || await c.match('./index.html');
      if (zapas) return zapas;
      throw err;
    }
  })();
}

function najpierwCache(zad) {
  return (async () => {
    const c = await caches.open(CACHE);
    const z = await c.match(zad);
    const swiezy = fetch(zad).then(odp => { schowaj(c, zad, odp); return odp; }).catch(() => null);
    return z || (await swiezy) || Response.error();
  })();
}

self.addEventListener('fetch', e => {
  const zad = e.request;
  if (zad.method !== 'GET') return;
  const url = new URL(zad.url);
  if (url.origin !== location.origin) return;

  if (zad.mode === 'navigate') {
    e.respondWith(najpierwSiec(zad, e.preloadResponse
      ? e.preloadResponse.then(r => r || fetch(zad, { cache: 'no-store' })) : null));
    return;
  }
  if (/\.(html|webmanifest|json)$/.test(url.pathname)) {
    e.respondWith(najpierwSiec(zad));
    return;
  }
  e.respondWith(najpierwCache(zad));
});
