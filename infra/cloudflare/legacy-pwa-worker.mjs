// Cloudflare Worker "jakeuj-legacy-pwa".
//
// Legacy hosts of the PWA project sites. Visitors who used the old subdomain
// still have a service worker there that serves the cached app offline-first, so
// a plain 301 never reaches them. This worker:
//   * serves a self-unregistering service worker at the old worker URL, so the
//     browser's next update check removes the old worker and reloads the page;
//   * 301-redirects every other request to https://jakeuj.com/<slug>/<path>.
//
// These hosts must NOT also be in the Bulk Redirect list: Bulk Redirects run
// before Workers and would redirect /sw.js too.
const APPS = {
  "bahamut-markdown-converter.jakeuj.com": { slug: "bahamut-markdown-converter", workers: ["/sw.js"] },
  "bandit.jakeuj.com": { slug: "bandit-save-editor", workers: ["/sw.js"] },
};

const KILL_SWITCH = `// This app moved to a new address. Remove the old service worker and reload.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) await caches.delete(key);
    await self.registration.unregister();
    for (const client of await self.clients.matchAll({ type: "window" })) client.navigate(client.url);
  })());
});
`;

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const app = APPS[url.hostname];
    if (!app) return new Response("Not found", { status: 404 });
    if (app.workers.includes(url.pathname)) {
      return new Response(KILL_SWITCH, {
        headers: {
          "content-type": "text/javascript; charset=utf-8",
          "cache-control": "no-store",
          "x-robots-tag": "noindex",
        },
      });
    }
    return Response.redirect(`https://jakeuj.com/${app.slug}${url.pathname}${url.search}`, 301);
  },
};
