#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Adjust if your repo uses different folder names
CANDIDATE_DIRS = ["logo", "logos", "fonts", "guides", "palette", "assets"]

ALLOWED_EXTS = {
    ".svg", ".png", ".jpg", ".jpeg", ".webp",
    ".pdf",
    ".ttf", ".otf", ".woff", ".woff2",
    ".md"
}

def is_allowed(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in ALLOWED_EXTS

def collect_files(base_dir: Path):
    items = []
    if not base_dir.exists():
        return items

    for p in sorted(base_dir.rglob("*")):
        if is_allowed(p):
            rel = p.relative_to(ROOT).as_posix()
            items.append({
                "path": rel,
                "ext": p.suffix.lower(),
                "bytes": p.stat().st_size,
            })
    return items

def main():
    data = {
        "schemaVersion": 1,
        "repo": "acorns-finders/brand-kit",
        "items": [],
    }

    for d in CANDIDATE_DIRS:
        data["items"].extend(collect_files(ROOT / d))

    out = ROOT / "asset-manifest.json"
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
