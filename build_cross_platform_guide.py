"""
Mallikgroup-for-Humanity Cross-Platform Build & Play Store Release Helper
Architect: Niraj Mallik (©Nirajmallik@hub) | License: MIT License © 2026
"""

import json

TARGETS = {
    "web_browser": {
        "name": "Web Browser (PWA)",
        "cost": "Free",
        "steps": [
            "Host static frontend (index.html, nepal-banks.html, app-download.html, mallik-tier-gate.js)",
            "Users open directly in Chrome, Safari, Edge, or Mi Browser with zero install"
        ]
    },
    "android_play_store_and_apk": {
        "name": "Android (Google Play Store AAB + Direct APK)",
        "package_id": "com.nirajmallikhub.mallikhumanity",
        "cost": "Google Play Developer one-time registration fee for Play Store listing; free for direct APK",
        "steps": [
            "Wrap your web app with Capacitor or Bubblewrap (Trusted Web Activity) using package com.nirajmallikhub.mallikhumanity",
            "Build signed release APK (for direct download) and signed AAB (for Google Play Console upload)",
            "Upload AAB to Google Play Console, complete Data Safety & store listing, and publish"
        ]
    },
    "ios_app": {
        "name": "iOS (iPhone & iPad)",
        "cost": "Free via Safari Home Screen; Apple Developer membership for App Store",
        "steps": [
            "Immediate: Users open in Safari and tap Share -> Add to Home Screen",
            "Native App Store: Add Capacitor iOS target (npx cap add ios) and archive/sign in Xcode"
        ]
    },
    "windows_app": {
        "name": "Windows (Desktop App / Installer)",
        "cost": "Free",
        "steps": [
            "Immediate: Users open in Microsoft Edge or Google Chrome -> Apps -> Install this site as an app",
            "Packaged Installer: Wrap web bundle with Electron or PWABuilder for a Windows installer"
        ]
    }
}

if __name__ == "__main__":
    print(json.dumps({
        "owner": "©Nirajmallik@hub",
        "organization": "Mallikgroup-for-Humanity",
        "targets": TARGETS
    }, indent=2))
