import os
import re


def minify_css(content):
    content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)
    content = re.sub(r"\s+", " ", content)
    content = re.sub(r"\s*([{};:,>~+])\s*", r"\1", content)
    return content.strip()


def minify_js(content):
    content = re.sub(r"(?<!:)//[^\n]*", "", content)
    content = re.sub(r"\n\s*\n", "\n", content)
    return content.strip()


static_dir = os.path.join("app", "static")
for root, _, files in os.walk(static_dir):
    for f in files:
        path = os.path.join(root, f)
        if f.endswith(".css") and not f.endswith(".min.css"):
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(minify_css(content))
        elif f.endswith(".js") and not f.endswith(".min.js"):
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(minify_js(content))

print("build complete")
