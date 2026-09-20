#!/usr/bin/env python3
"""Build a single-file copy of the site for publishing as a Claude Artifact.

An artifact publish carries one HTML file, so relative assets never resolve.
This inlines every image as a data URI and repoints internal page links at the
live site. Production files are left alone; only dist/artifact.html changes.
"""
import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIVE = "https://rehan-ali-labs.org"
SRC = ROOT / "index.html"
OUT = ROOT / "dist" / "artifact.html"

MIME = {".webp": "image/webp", ".png": "image/png",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}

html = SRC.read_text()
inlined, missing, total_bytes = 0, [], 0

def to_data_uri(match):
    global inlined, total_bytes
    attr, path = match.group(1), match.group(2)
    f = ROOT / path
    if not f.exists():
        missing.append(path)
        return match.group(0)
    mime = MIME.get(f.suffix.lower())
    if not mime:
        missing.append(path)
        return match.group(0)
    raw = f.read_bytes()
    total_bytes += len(raw)
    inlined += 1
    return f'{attr}="data:{mime};base64,{base64.b64encode(raw).decode()}"'

# Only rewrite relative paths; data: and http(s) URLs are already self-contained.
html = re.sub(r'(src)="((?!data:|https?:|//)[^"]+\.(?:webp|png|jpe?g|svg))"', to_data_uri, html)

# The bytes are in the document now, so lazy loading buys nothing and some
# renderers never fire it, leaving slides blank.
html = html.replace(' loading="lazy"', '')

# Internal page links cannot resolve inside an artifact, so send them to the live site.
pages = re.findall(r'href="((?!https?:|#|mailto:)[^"]+\.html)"', html)
for page in set(pages):
    html = html.replace(f'href="{page}"',
                        f'href="{LIVE}/{page}" target="_blank" rel="noopener noreferrer"')

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html)

print(f"inlined {inlined} images ({total_bytes/1024:.0f} KB raw)")
print(f"repointed {len(set(pages))} page link(s) to {LIVE}: {sorted(set(pages))}")
if missing:
    print("MISSING:", missing, file=sys.stderr)
    sys.exit(1)
print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size/1024:.0f} KB)")
