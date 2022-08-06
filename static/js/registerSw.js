//var staticCacheName = "django-pwa-v" + new Date().getTime();
//var filesToCache = [
//    '/offline/',
//];
//
//// Cache on install
//self.addEventListener("install", event => {
//    this.skipWaiting();
//    event.waitUntil(
//        caches.open(staticCacheName)
//            .then(cache => {
//                return cache.addAll(filesToCache);
//            })
//    )
//});
//
//// Clear cache on activate
//self.addEventListener('activate', event => {
//    event.waitUntil(
//        caches.keys().then(cacheNames => {
//            return Promise.all(
//                cacheNames
//                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
//                    .filter(cacheName => (cacheName !== staticCacheName))
//                    .map(cacheName => caches.delete(cacheName))
//            );
//        })
//    );
//});
//
//// Serve from Cache
//self.addEventListener("fetch", event => {
//    event.respondWith(
//        caches.match(event.request)
//            .then(response => {
//                return response || fetch(event.request);
//            })
//            .catch(() => {
//                return caches.match('/offline/');
//            })
//    )
//});

function urlB64ToUnit8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}

// esto OK
const registerServiceWorker = async () => {
  if ('serviceWorker' in navigator) {
    try {
      const reg = await navigator.serviceWorker.register('sw.js');
      //initialiseState(reg);
      //if (registration.installing) {
      //  console.log('Service worker installing');
      //} else if (registration.waiting) {
      //  console.log('Service worker installed');
      //} else if (registration.active) {
      //  console.log('Service worker active');
      //}
    } catch (error) {
      console.error(error);
    }
  }
};


//const initialiseState = (reg) => {
//    if (!reg.showNotification) {
//        showNotAllowed('Showing notifications isn\'t supported ☹️😢');
//        return
//    }
//    if (Notification.permission === 'denied') {
//        showNotAllowed('You prevented us from showing notifications ☹️🤔');
//        return
//    }
//    if (!'PushManager' in window) {
//        showNotAllowed("Push isn't allowed in your browser 🤔");
//        return
//    }
//    subscribe(reg);
//}
//
//const subscribe = async (reg) => {
//    const subscription = await reg.pushManager.getSubscription();
//    if (subscription) {
//        sendSubData(subscription);
//        return;
//    }
//
//    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
//    const key = vapidMeta.content;
//    const options = {
//        userVisibleOnly: true,
//        // if key exists, create applicationServerKey property
//        ...(key && {applicationServerKey: urlB64ToUnit8Array(key)})
//    };
//
//    const sub = await reg.pushManager.subscribe(options);
//    sendSubData(sub)
//};
//
//const sendSubData = async (subscription) => {
//    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
//    const data = {
//        status_type: 'subscribe',
//        subscription: subscription.toJSON(),
//        browser: browser,
//    };
//
//    const res = await fetch('/webpush/save_information', {
//        method: 'POST',
//        body: JSON.stringify(data),
//        headers: {
//            'content-type': 'application/json'
//        },
//        credentials: "include"
//    });
//
//    handleResponse(res);
//};
//
//const handleResponse = (res) => {
//    console.log(res.status);
//};
//
registerServiceWorker();
