"""Stage assets for Vercel: static on CDN, templates at repo root for Lambda bundling."""
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
app_dir = root / "application"


def _sync_tree(src: Path, dst: Path) -> None:
    # Copying disabled: we now point Vercel at `application/static` and
    # include `application/**` in the Python lambda bundle. Keeping this
    # helper for compatibility but not performing any filesystem writes.
    return


print("vercel build: copy disabled — using application/static and application/templates directly")
