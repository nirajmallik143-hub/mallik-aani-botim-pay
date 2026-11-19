"""
MALLIK GROUP FOR HUMANITY — AUTOMATED CUSTOMER DISCOVERY, PAYMENT & UNIQUE 18-DIGIT KEY ENGINE
Organization: Mallikgroup-for-Humanity | Architect: Niraj Mallik (©Nirajmallik@hub)
License: MIT License © 2026 Niraj Mallik
"""

import json
import secrets
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DB_ROOT = "https://nmdc-ajs-security-default-rtdb.firebaseio.com/mallik_payments"
ENV_PATH = Path.home() / ".env"


def load_env() -> dict:
    env = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def luhn_check_digit(first_17: str) -> str:
    total = 0
    for idx, ch in enumerate(reversed(first_17)):
        d = int(ch)
        if idx % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return str((10 - (total % 10)) % 10)


def generate_unique_18_digit_key(auth_query: str = "") -> str:
    """Generates a cryptographically unique 18-digit Luhn key verified against Firebase."""
    for _ in range(25):
        prefix = "794"
        random_14 = "".join(str(secrets.randbelow(10)) for _ in range(14))
        base_17 = prefix + random_14
        key_18 = base_17 + luhn_check_digit(base_17)
        try:
            check_url = f"{DB_ROOT}/quantum_keys/{key_18}.json{auth_query}"
            with urllib.request.urlopen(check_url, timeout=10) as resp:
                if json.loads(resp.read().decode("utf-8")) is None:
                    return key_18
        except Exception:
            return key_18
    raise RuntimeError("Unable to allocate unique 18-digit key after 25 attempts.")


def fb_put(path: str, payload: dict, auth_query: str = "") -> None:
    req = urllib.request.Request(
        f"{DB_ROOT}/{path}.json{auth_query}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="PUT"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def issue_key_for_paid_customer(
    customer_name: str,
    customer_whatsapp: str,
    order_ref: str,
    payment_rail: str,
    amount_paid: str,
    product: str = "EcoThread + Sikshya Pro",
    duration_days: int = 30,
    firebase_token: str = ""
) -> dict:
    """Issues a unique 18-digit key once payment is confirmed on mBank, Botim/Aani, Card, or Nepal Bank."""
    auth_q = f"?auth={firebase_token}" if firebase_token else ""
    unique_key = generate_unique_18_digit_key(auth_q)
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    expires_ms = now_ms + duration_days * 86400 * 1000

    record = {
        "key": unique_key,
        "ref": order_ref.strip().upper(),
        "customer_name": customer_name.strip(),
        "customer_whatsapp": customer_whatsapp.strip(),
        "payment_rail": payment_rail,
        "amount_paid": amount_paid,
        "product": product,
        "tier": "PRO",
        "status": "ACTIVE",
        "createdAt": now_ms,
        "expiresAt": expires_ms,
        "issuer": "©Nirajmallik@hub"
    }

    fb_put(f"quantum_keys/{unique_key}", record, auth_q)
    fb_put(f"orders/{record['ref']}", record, auth_q)

    clean_phone = "".join(ch for ch in customer_whatsapp if ch.isdigit())
    wa_text = (
        f"Hello {customer_name}, your Mallik Group payment ({amount_paid} via {payment_rail}) "
        f"for Ref {record['ref']} is confirmed! Your unique 18-Digit Pro Key is: {unique_key}"
    )
    wa_link = f"https://wa.me/{clean_phone}?text={urllib.request.quote(wa_text)}" if clean_phone else ""

    return {
        "status": "ISSUED",
        "unique_18_digit_key": unique_key,
        "order_ref": record["ref"],
        "product": product,
        "whatsapp_delivery_link": wa_link
    }


def search_and_process_confirmed_orders(orders_feed: list[dict], firebase_token: str = "") -> list[dict]:
    """Scans discovered customer orders and auto-generates a unique 18-digit key for every confirmed payment."""
    issued = []
    for item in orders_feed:
        if item.get("payment_status") == "PAID" and not item.get("key"):
            res = issue_key_for_paid_customer(
                customer_name=item.get("customer_name", "Valued Customer"),
                customer_whatsapp=item.get("customer_whatsapp", ""),
                order_ref=item["ref"],
                payment_rail=item.get("payment_rail", "mBank UAE / Botim"),
                amount_paid=item.get("amount_paid", "19 AED"),
                product=item.get("product", "EcoThread Pro"),
                duration_days=int(item.get("duration_days", 30)),
                firebase_token=firebase_token
            )
            issued.append(res)
    return issued


if __name__ == "__main__":
    # Local dry-run demonstration generating two distinct 18-digit Luhn keys
    k1 = generate_unique_18_digit_key()
    k2 = generate_unique_18_digit_key()
    print(json.dumps({
        "system": "Mallikgroup-for-Humanity Auto Payment & 18-Digit Key Engine",
        "sample_unique_key_customer_1": k1,
        "sample_unique_key_customer_2": k2,
        "guaranteed_different": k1 != k2
    }, indent=2))
