# ©Nirajmallik@hub
# Copyright (c) 2026 Niraj Mallik (nirajmallik143-hub)
# Licensed under the MIT License.

import os
from pathlib import Path


def load_env_file(env_path: str = "~/.env") -> None:
    path = Path(env_path).expanduser()
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
y        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def get_mallik_ai_registry() -> dict:
    load_env_file("~/.env")
    mallik_key = os.getenv("MALLIK_GROUP_API_KEY", "").strip()

    providers = {
        "mallik_group": mallik_key,
        "gemini": os.getenv("GEMINI_API_KEY", "").strip(),
        "openai": os.getenv("OPENAI_API_KEY", "").strip(),
        "anthropic": os.getenv("ANTHROPIC_API_KEY", "").strip(),
        "deepseek": os.getenv("DEEPSEEK_API_KEY", "").strip(),
        "elevenlabs": os.getenv("ELEVENLABS_API_KEY", "").strip(),
        "github": os.getenv("GITHUB_TOKEN", "").strip(),
    }

    return {
        "brand": "©Nirajmallik@hub",
        "mallik_group_key_configured": bool(mallik_key),
        "providers": providers,
        "active_providers": [name for name, token in providers.items() if token],
    }


def resolve_ai_key(provider: str, client_mallik_key: str = "") -> str:
    registry = get_mallik_ai_registry()
    master_key = registry["providers"]["mallik_group"]

    # If a Mallik Group API key is enforced, require a matching key when configured
    if master_key and client_mallik_key and client_mallik_key != master_key:
        raise PermissionError("Invalid Mallik Group API key.")

    key = registry["providers"].get(provider.lower(), "")
    if not key:
        raise ValueError(f"Missing API key environment variable for provider: {provider}")
    return key


def main() -> None:
    registry = get_mallik_ai_registry()
    print(f"Initialized {registry['brand']} AI Gateway")
    print(f"MALLIK_GROUP_API_KEY set: {registry['mallik_group_key_configured']}")
    print(f"Configured keys: {', '.join(registry['active_providers']) or 'none yet in ~/.env'}")


if __name__ == "__main__":
    main()
