#!/bin/bash
# Usage: tools/run_guide.sh <config.py> <out.docx>
# Builds the guide from the template in sources/, renders with LibreOffice, fills TOC page numbers
# (3 passes until stable), validates, and leaves <out>.pdf and page JPEGs next to the output.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CFG="$(realpath "$1")"; OUT="$(realpath -m "$2")"
SK=/root/.claude/skills/synced/eff63170-8cde-4219-a73a-208168019aa0_c5ca6a1e-2ad9-49d2-b4bb-2816708a154b/docx
WORK="$(mktemp -d)"; TPL="$WORK/tpl"; mkdir -p "$TPL"
(cd "$TPL" && unzip -q "$ROOT/sources/2026-10-06-epic-training-quick-start-guide-template.dotx" && find . -type l -delete)
PAGES="$WORK/pages.json"; echo '{}' > "$PAGES"
for pass in 1 2 3; do
  python3 -I "$ROOT/tools/build_guide.py" "$TPL" "$OUT" "$CFG" "$PAGES" >/dev/null
  (cd "$(dirname "$OUT")" && python3 "$SK/scripts/office/soffice.py" --headless --convert-to pdf "$OUT" >/dev/null 2>&1)
  PDF="${OUT%.docx}.pdf"
  python3 -I - "$OUT.headings.json" "$PDF" "$PAGES" <<'P'
import json, re, subprocess, sys
heads = json.load(open(sys.argv[1])); pdf = sys.argv[2]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
norm = lambda t: re.sub(r'\s+', ' ', t.replace(' ', ' ')).strip()
# a heading matches only where a line STARTS with it (a title also appears inside other lines and the header)
lines = {p: [norm(l) for l in subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True).stdout.splitlines() if l.strip()] for p in range(2, n + 1)}
pg = {}
for h in heads:
    key = norm(h)[:40]
    for p in range(2, n + 1):
        if any(l.startswith(key) for l in lines[p]):
            pg[h] = p; break
old = json.load(open(sys.argv[3])); json.dump(pg, open(sys.argv[3], 'w'))
print('pages', n, 'stable' if old == pg else 'changed', 'missing:', [h for h in heads if h not in pg])
P
done
python3 -I "$ROOT/tools/build_guide.py" "$TPL" "$OUT" "$CFG" "$PAGES"
(cd "$(dirname "$OUT")" && python3 "$SK/scripts/office/soffice.py" --headless --convert-to pdf "$OUT" >/dev/null 2>&1)
rm -f "$OUT.headings.json"
python3 "$SK/scripts/office/validate.py" "$OUT" | tail -2
