/* Service worker: deixa o app abrir sem internet.
   - HTML: tenta a rede primeiro (pega atualização) e cai no cache se estiver offline.
   - Ícones, manifest e fontes: usa o cache e atualiza em segundo plano.
   Ao mudar arquivos do app, aumente VERSAO pra limpar o cache antigo. */
const VERSAO = 'zicao-v12';
const ARQUIVOS = ['./', 'index.html', 'manifest.webmanifest?v=2', 'favicon.svg?v=2',
  'icons/apple-touch-icon.png?v=2', 'icons/icon-192.png?v=2', 'icons/icon-512.png?v=2', 'logo.png?v=1'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSAO).then(c => c.addAll(ARQUIVOS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== VERSAO).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => {
      const copia = r.clone(); caches.open(VERSAO).then(c => c.put('./', copia)); return r;
    }).catch(() => caches.match('./')));
    return;
  }
  e.respondWith(caches.match(req).then(cache => {
    const rede = fetch(req).then(r => {
      if (r.ok || r.type === 'opaque') { const copia = r.clone(); caches.open(VERSAO).then(c => c.put(req, copia)); }
      return r;
    }).catch(() => cache);
    return cache || rede;
  }));
});
