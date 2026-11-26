#!/usr/bin/env python3
"""Sync the standalone Kosher Latvia site from the Tab-hosted source.

Pulls the live product data and images from the Tab site and rewrites
data.js and past-data.js so the static copy is identical to what the
owner last published there.

Usage:  python3 update_from_tab.py
"""
import json, pathlib, re, sys, urllib.request, concurrent.futures as cf

BASE = "https://kosher-latvia.sites.tab.bot/"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122 Safari/537.36"}
ROOT = pathlib.Path(__file__).resolve().parent


def fetch_json(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def norm(p):
    i = p.get("img")
    if isinstance(i, str) and i:
        i = i.split("?")[0]
        if i.startswith("/"):
            i = i[1:]
        p["img"] = i
    return p


def download(path):
    target = ROOT / path
    if target.exists() and target.stat().st_size > 0:
        return (path, False, None)
    try:
        req = urllib.request.Request(BASE + path, headers=UA)
        data = urllib.request.urlopen(req, timeout=60).read()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return (path, True, None)
    except Exception as e:  # noqa: BLE001
        return (path, False, str(e))


def main():
    print("Fetching data from Tab...")
    data = fetch_json("api/data")
    past = fetch_json("api/past")
    archive = past.get("items", []) if isinstance(past, dict) else (past or [])

    for p in data.get("products", []) + archive:
        norm(p)

    archive_items = data.pop("archive", None)
    if archive_items and not archive:
        archive = [norm(p) for p in archive_items]

    (ROOT / "data.js").write_text(
        "window.KOSHER_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";",
        encoding="utf-8")
    (ROOT / "past-data.js").write_text(
        "window.KOSHER_PAST = " + json.dumps(archive, ensure_ascii=False, separators=(",", ":")) + ";",
        encoding="utf-8")

    imgs = sorted({p["img"] for p in data.get("products", []) + archive if p.get("img")})
    print(f"products={len(data.get('products', []))} archive={len(archive)} images={len(imgs)}")
    added = 0
    fails = []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for path, was_new, err in ex.map(download, imgs):
            if err:
                fails.append((path, err))
            elif was_new:
                added += 1
    # store logos, kashrut symbols and other assets referenced from css/js/html
    refs = set()
    for f in list(ROOT.glob("*.js")) + list(ROOT.glob("*.css")) + list(ROOT.glob("*.html")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"[\"'\(](\.?/?(?:img|u)/[A-Za-z0-9_./\-]+\.(?:svg|png|jpg|jpeg|webp))", text):
            refs.add(m.group(1).lstrip(".").lstrip("/"))
    extra = sorted(r for r in refs if not (ROOT / r).exists())
    if extra:
        with cf.ThreadPoolExecutor(max_workers=12) as ex:
            for path, was_new, err in ex.map(download, extra):
                if err:
                    fails.append((path, err))
                elif was_new:
                    added += 1

    print(f"new images downloaded={added} failures={len(fails)}")
    for f in fails[:5]:
        print("  FAIL", f)
    print("data version:", data.get("updated"))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
