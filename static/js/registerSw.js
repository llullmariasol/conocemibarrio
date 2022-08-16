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

const registerServiceWorker = async () => {
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      initialiseState(registration);
      if (registration.installing) {
        console.log('Service worker installing');
      } else if (registration.waiting) {
        console.log('Service worker installed');
      } else if (registration.active) {
        console.log('Service worker active');
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const initialiseState = (registration) => {
    if (!registration.showNotification) {
        console.log('Showing notifications is not supported');
        return
    }
    if (Notification.permission === 'denied') {
        console.log('You prevented us from showing notifications');
        return
    }
    if (!'PushManager' in window) {
        console.log('Push is not allowed in your browser');
        return
    }
    subscribe(registration);

    // Use serviceWorker.ready to ensure that you can subscribe for push
    navigator.serviceWorker.ready.then(
      (registration) => {
        const vapidMeta = document.querySelector('meta[name="vapid-key"]');
        const key = vapidMeta.content;
        console.log(key);
        const options = {
          userVisibleOnly: true,
          applicationServerKey: urlB64ToUnit8Array(key),
        };
        registration.pushManager.subscribe(options).then(
          (pushSubscription) => {
            console.log(pushSubscription.endpoint);
            // The push subscription details needed by the application
            // server are now available, and can be sent to it using,
            // for example, an XMLHttpRequest.
          }, (error) => {
            // During development it often helps to log errors to the
            // console. In a production environment it might make sense to
            // also report information about errors back to the
            // application server.
            console.error(error);
          }
        );
      });

}

//const subscribe = async (registration) => {
//    const subscription = await registration.pushManager.getSubscription();
//    if (subscription) {
//        sendSubData(subscription);
//        return;
//    }
//
//    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
//    const key = vapidMeta.content;
//    const sub = await registration.pushManager.subscribe({
//        userVisibleOnly: true,
//        applicationServerKey: urlB64ToUnit8Array(key)
//        });
//
//    sendSubData(sub)
//};

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

//const handleResponse = (res) => {
//    console.log(res.status);
//};

registerServiceWorker();
