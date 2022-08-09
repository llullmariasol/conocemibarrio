const addResourcesToCache = async (resources) => {
  const cache = await caches.open('v1');
  await cache.addAll(resources);
};

const putInCache = async (request, response) => {
  const cache = await caches.open('v1');
  await cache.put(request, response);
};

const cacheFirst = async ({ request, preloadResponsePromise, fallbackUrl }) => {
  // First try to get the resource from the cache
  const responseFromCache = await caches.match(request);
  if (responseFromCache) {
    return responseFromCache;
  }

  // Next try to use (and cache) the preloaded response, if it's there
  const preloadResponse = await preloadResponsePromise;
  if (preloadResponse) {
    console.info('using preload response', preloadResponse);
    putInCache(request, preloadResponse.clone());
    return preloadResponse;
  }

  // Next try to get the resource from the network
  try {
    const responseFromNetwork = await fetch(request);
    // response may be used only once
    // we need to save clone to put one copy in cache
    // and serve second one
    putInCache(request, responseFromNetwork.clone());
    return responseFromNetwork;
  } catch (error) {
    const fallbackResponse = await caches.match(fallbackUrl);
    if (fallbackResponse) {
      return fallbackResponse;
    }
    // when even the fallback response is not available,
    // there is nothing we can do, but we must always
    // return a Response object
    return new Response('Network error happened', {
      status: 408,
      headers: { 'Content-Type': 'text/plain' },
    });
  }
};

// Enable navigation preload
//const enableNavigationPreload = async () => {
//  if (self.registration.navigationPreload) {
//    // Enable navigation preloads!
//    await self.registration.navigationPreload.enable();
//  }
//};

self.addEventListener('activate', (event) => {
  console.log('Ready to handle fetches!');
});

self.addEventListener("install", (event) => {
  event.waitUntil(
    addResourcesToCache([
      "/static/img/chat.png",
      "/static/img/default.jpeg",
      "/static/img/forum.png",
      "/static/img/home.png",
      "/static/img/location.png",
      "/static/img/logo.png",
      "/static/img/profile.png",
      "/static/img/safetypin.png",
      "/static/img/square.png",
    ])
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    cacheFirst({
      request: event.request,
      preloadResponsePromise: event.preloadResponse,
      fallbackUrl: "./templates/offline.html",
    })
  );
});

// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'Nueva notificación';
    const body = data.body || '-';
    console.log(head);
    console.log(body);
    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, {
            body: body,
            icon: "https://conocemibarrio.herokuapp.com/static/img/square.png"
        })
    );
});
