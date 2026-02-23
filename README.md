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

## Inventory spreadsheet template
A ready-to-use multi-sheet inventory workbook is included at:

- `inventory_tracking_template.xml`

It contains:
- `A_Inventory_Tracking`
- `B_Equipment_Tracking`
- `C_Allocated_Tracking`
- `D_Monthly_Figures`
- `README` (usage notes)

To regenerate it after edits:
```bash
python3 create_inventory_workbook.py
```
