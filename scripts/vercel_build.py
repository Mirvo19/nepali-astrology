"""Stage assets for Vercel: static on CDN, templates at repo root for Lambda bundling."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
app_dir = root / "application"


def _sync_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


_sync_tree(app_dir / "static", root / "public" / "static")
_sync_tree(app_dir / "templates", root / "templates")

print("vercel build: copied application/static -> public/static")
print("vercel build: copied application/templates -> templates/")
