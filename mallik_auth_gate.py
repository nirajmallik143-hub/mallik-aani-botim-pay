# ©Nirajmallik@hub
# Copyright (c) 2026 Niraj Mallik (nirajmallik143-hub)
# Licensed under the MIT License.

import json
import os
import re
import time
import urllib.request
from pathlib import Path

FIREBASE_PAYMENTS_ROOT = "https://nmdc-ajs-security-default-rtdb.firebaseio.com/mallik_payments"


def load_env(env_file: str = "~/.env") -> None:
    p = Path(env_file).expanduser()
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def _fetch_json(url: str):
    try:
        with urllib.request.urlopen(url, timeout=6) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def verify_app_login(access_key: str) -> dict:
    load_env("~/.env")
    key = (access_key or "").strip()
    owner_secret = os.getenv("MALLIK_OWNER_KEY", "#cgjolj2Y").strip()

    # 1. Owner access check
    if key == owner_secret:
        return {
            "allowed": True,
            "role": "OWNER",
            "brand": "©Nirajmallik@hub",
            "message": "Owner authenticated (#cgjolj2Y)."
        }

    # 2. Customer 18-digit payment key check
    if not re.fullmatch(r"\d{18}", key):
        return {
            "allowed": False,
            "role": "NONE",
            "message": "Customer login requires a valid 18-digit payment key (or Owner key)."
        }

    now_ms = int(time.time() * 1000)
    rec = _fetch_json(f"{FIREBASE_PAYMENTS_ROOT}/quantum_keys/{key}.json") or _fetch_json(
        f"{FIREBASE_PAYMENTS_ROOT}/{key}.json"
    )
    if not isinstance(rec, dict):
        return {
            "allowed": False,
            "role": "CUSTOMER",
            "message": "18-digit key not found in payment records. Complete payment first."
        }

    expires_at = rec.get("expiresAt")
    if isinstance(expires_at, (int, float)) and expires_at <= now_ms:
        return {
            "allowed": False,
            "role": "CUSTOMER",
            "message": "18-digit subscription key has expired."
        }

    return {
        "allowed": True,
        "role": "CUSTOMER",
        "brand": "©Nirajmallik@hub",
        "key": key,
        "message": "Customer 18-digit payment key verified."
    }


if __name__ == "__main__":
    print(verify_app_login("#cgjolj2Y"))
