#!/usr/bin/env python3
"""Generate pcl-cgre.gresource.xml from source resources and compiled UI files."""

import os, sys, xml.sax.saxutils as saxutils

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
UI_DIR = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(ROOT, "build", "data", "ui")

# Collect all resource files relative to ROOT
files = []
for dirpath, _, filenames in os.walk(ROOT):
    for f in sorted(filenames):
        full = os.path.join(dirpath, f)
        rel = os.path.relpath(full, ROOT)
        # Only include specific directories
        if rel.startswith("resources/icons/pcl-cgre/"):
            alias = rel.replace("resources/icons/pcl-cgre/", "icons/")
            files.append((full, alias))
        elif rel.startswith("resources/blocks/"):
            alias = rel.replace("resources/", "")
            files.append((full, alias))
        elif rel.startswith("resources/Heads/"):
            alias = rel.replace("resources/Heads/", "heads/")
            files.append((full, alias))
        elif rel == "resources/lirpa_loof.json":
            files.append((full, "lirpa_loof.json"))
        # Note: fonts/ are NOT embedded in GResource.
        # FontHelper.cpp loads them from disk via FcConfigAppFontAddFile().

# Also include compiled .ui files from the active build dir.
if os.path.isdir(UI_DIR):
    for f in sorted(os.listdir(UI_DIR)):
        if f.endswith(".ui"):
            full = os.path.join(UI_DIR, f)
            files.append((full, f"data/ui/{f}"))

if not files:
    print("<!-- No resource files found -->", file=sys.stderr)

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<gresources>')
print('  <gresource prefix="/pcl/cgre">')
for full, alias in sorted(files, key=lambda x: x[1]):
    alias_esc = saxutils.escape(alias)
    full_esc = saxutils.escape(full)
    print(f'    <file alias="{alias_esc}">{full_esc}</file>')
print('  </gresource>')
print('</gresources>')
