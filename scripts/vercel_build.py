"""Copy static assets into public/ for Vercel CDN (Flask templates stay in application/)."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = root / "application" / "static"
dst = root / "public" / "static"

if src.exists():
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

print("vercel build: static files copied to public/static")
