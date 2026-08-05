#!/usr/bin/env python3
"""Latest CATATAN UPDATE 2026 (gdoc 16BHgxfZ...) applied to live Supabase.

Two more pondok become SELESAI tersalurkan (red in table, faded-green on map):
  * PP Hidayatul Mubtadiin Kunci
  * PP Muhammadiyah Al-Mujahidin
Positions kept per the brief's numbered table (only status changes). Galon/
Distribusi counter -> 1984 (home + penerima). Marker color is a code change in
IndonesiaMap.tsx (not data).

Idempotent: matched by name/label, re-running yields the same end state.
Mirrors migration 0022. Reads creds from .dev.vars.
"""
import json, os, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = {}
with open(os.path.join(ROOT, ".dev.vars")) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v.strip().strip('"')

URL = env["SUPABASE_URL"].rstrip("/")
KEY = env["SUPABASE_SERVICE_ROLE_KEY"]
HDR = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


def req(method, path, body=None, prefer="return=representation"):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(URL + path, data=data, method=method,
                               headers={**HDR, "Prefer": prefer})
    with urllib.request.urlopen(r) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else None


# --- 1. Two more pondok -> selesai --- #
for name in ("PP Hidayatul Mubtadiin Kunci", "PP Muhammadiyah Al-Mujahidin"):
    q = urllib.parse.quote(name)
    req("PATCH", f"/rest/v1/penerima?name=eq.{q}",
        {"status": "selesai", "is_published": True})
    print(f"selesai: {name}")

# --- 1b. Reorder: 15 tersalurkan (1-15), then 6 selesai (16-21) --- #
order = [
    "PP An-Nur", "PP Fajrussa'adah", "PP Al-Kholifah", "PP Al-Murtadlo",
    "PP Ar-Ruhamaa'", "Pondok Nurul Jamil Al-Jumar", "PP Nurulhadi 2",
    "PP Ainul Yakin Special Children", "PP & Islamic Center Yasma Mulia",
    "PP Roudlotuth Tholabah", "Nurul Qur'an Islamic Boarding School",
    "PP Kun Solihan", "Yayasan Panti Asuhan Islam", "PP Thoriqul Mukminin",
    "PP Ash-Shiddiq 2",
    # selesai at the bottom
    "PP Hidayatul Mubtadiin Kunci", "PP Muhammadiyah Al-Mujahidin",
    "PP KI Ageng Wonokusumo", "PP Baitul Jannah Darussalam",
    "PP Assalafiyah Darussalam", "PP Al-Hikmah Gubuk Rubuh",
]
for i, name in enumerate(order, start=1):
    q = urllib.parse.quote(name)
    req("PATCH", f"/rest/v1/penerima?name=eq.{q}", {"sort_order": i})
    print(f"sort_order {i}: {name}")

# --- 2. Stats: Galon/Distribusi 1446 -> 1984 (home + penerima) --- #
stat_values = {
    "Kabupaten": 1, "Kabupaten Aktif": 1,
    "Lembaga Penerima": 21,
    "Galon/Distribusi": 1984,
    "Kecamatan": 9, "Kecamatan Terjangkau": 9,
}
for label, num in stat_values.items():
    q = urllib.parse.quote(label)
    req("PATCH", f"/rest/v1/stats?label=eq.{q}", {"num": num})
    print(f"stat: {label} -> {num}")

print("DONE")
