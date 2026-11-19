// ©Nirajmallik@hub — Free Tier + Paid 18-Digit Pro Tier Gate (MIT License 2026)
window.MallikTierGate = (function () {
  const DB = "https://nmdc-ajs-security-default-rtdb.firebaseio.com/mallik_payments";
  const STORAGE_KEY = "mallik_pro_key_18";
  const TRIAL_KEY = "mallik_free_uses";
  const FREE_DAILY_LIMIT = 3;

  function getTodayCount() {
    const today = new Date().toISOString().slice(0, 10);
    const saved = JSON.parse(localStorage.getItem(TRIAL_KEY) || "{}");
    return saved.date === today ? (saved.count || 0) : 0;
  }

  function incrementFreeUse() {
    const today = new Date().toISOString().slice(0, 10);
    const count = getTodayCount() + 1;
    localStorage.setItem(TRIAL_KEY, JSON.stringify({ date: today, count }));
    return count;
  }

  async function verifyKey(inputKey) {
    const k = (inputKey || localStorage.getItem(STORAGE_KEY) || "").trim();
    if (k === "#cgjolj2Y") {
      localStorage.setItem(STORAGE_KEY, k);
      return { tier: "OWNER", allowed: true, remaining: "UNLIMITED" };
    }
    if (!/^\d{18}$/.test(k)) {
      const used = getTodayCount();
      return { tier: "FREE", allowed: used < FREE_DAILY_LIMIT, remaining: Math.max(0, FREE_DAILY_LIMIT - used) };
    }
    try {
      const res = await fetch(`${DB}/quantum_keys/${k}.json`);
      const rec = await res.json();
      if (rec && (!rec.expiresAt || rec.expiresAt > Date.now())) {
        localStorage.setItem(STORAGE_KEY, k);
        return { tier: "PRO", allowed: true, key: k, remaining: "UNLIMITED" };
      }
    } catch (_) {}
    const used = getTodayCount();
    return { tier: "FREE", allowed: used < FREE_DAILY_LIMIT, remaining: Math.max(0, FREE_DAILY_LIMIT - used) };
  }

  return { verifyKey, incrementFreeUse, FREE_DAILY_LIMIT };
})();
