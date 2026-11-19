# Mallik Group Payment & 18-Digit Key System

**Owner / Architect:** Niraj Mallik (`©Nirajmallik@hub`)  
**Organization:** `Mallikgroup-for-Humanity`  
**License:** MIT License © 2026 Niraj Mallik  
**Repository Visibility:** Private  

## Payment Rails & Settlement Channels

### UAE Channels (AED)
* **Al Maryah Community Bank (mBank UAE Direct IBAN):** `AE900975554769760000001` (Account Holder: **Niraj Mallik**)
* **Botim / PayBy / Aani Instant Transfer:** `+971502297451` (Account Holder: **Niraj Mallik**)
* **Card Payment (Visa / Mastercard / Apple Pay):** Settled directly into **mBank UAE** (`AE900975554769760000001`) via hosted link / WhatsApp (`+971502297451`)

### Nepal Channels (NPR)
* **Excel Development Bank Ltd.:** QR code (`excel-bank-qr.jpg`) for Nepali mobile banking / Fonepay / eSewa / Khalti (Account Holder: **Niraj Mallik**)
* **Rastriya Banijya Bank Ltd.:** Account `2140100005105010` — **Shivaganj branch** (Account Holder: **Niraj Mallik**)

## Subscription Tiers & 18-Digit Key Flow
1. **Free Humanity Tier (`0 AED / 0 NPR`):** Up to 3 free runs per day via `mallik-tier-gate.js` without requiring a key.
2. **Pro Monthly (`19 AED / 699 NPR` — 30 days) & Pro Yearly (`149 AED / 5,499 NPR` — 365 days):**
   * Customer selects a plan on `nepal-banks.html` and copies their auto-generated `MG-XXXX` reference code.
   * Customer completes payment and sends the receipt + `MG-XXXX` reference on WhatsApp (`+971502297451`).
   * Owner approves the order locally using `owner-approve.html` (`#cgjolj2Y`), generating a Luhn-valid **18-digit Pro key** stored in Firebase Realtime Database (`nmdc-ajs-security-default-rtdb/mallik_payments`).
   * Customer claims or enters their 18-digit key to unlock unlimited Pro access.

## Key Files in This Repository
* `nepal-banks.html` — Customer payment portal (mBank UAE, Botim/Aani, Card, Excel Bank QR, RBB Shivaganj) + `MG-XXXX` reference & key lookup
* `mallik-tier-gate.js` — Client-side Free Tier + 18-digit Luhn & Firebase Pro key verifier
* `owner-approve.html` — Local owner approval console for issuing 18-digit keys
* `firebase.rules.json` — Hardened Firebase Realtime Database security rules
* `excel-bank-qr.jpg` — Excel Development Bank Ltd. QR code for Niraj Mallik
