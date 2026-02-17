# Lone Notify

A lightweight mobile-friendly web app that works on Android and iPhone browsers.

## Features
- Responsive design for phones.
- Browser notifications.
- Changeable notification sound (`Chime`, `Bell`, `Beep`, `Soft`).
- Schedule a reminder in N seconds.
- Installable as a basic PWA (manifest + service worker).

## Run locally
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000`.

## Notes for mobile
- On iPhone, add to Home Screen from Safari for a more app-like experience.
- Notification behavior depends on browser/OS support and permissions.
