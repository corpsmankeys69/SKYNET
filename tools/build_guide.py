"""Build a guide .docx from the Epic Training Quick Start Guide template XML.

Usage: python3 -I build_guide.py <template_unzipped_dir> <out_docx> <config.py> [pages.json]

Config (see guides/*.py) defines TITLE, HEADER_TITLE, APP_AUD, LINKS {rId: url}, CONTENT.
Content kinds:
  h1 h2 h3        headings (add 'pagebreak' as third item to start a main topic on a new page)
  p               plain paragraph (Normal style)
  step / bullet   numbered step (restarts per list) / level-2 bullet under a step
  bullet0         standalone bullet list item (not under a step)
  shot / shot0    highlighted [Screenshot: ...] placeholder, indented under a step / flush left
  tip / note      Efficiency Tip box / Important Note box (cloned from the template, icons kept)
Inline markup: **bold**, [[hand-added marker]] (yellow), ((blank)) (purple blank placeholder),
               {{link:rId|text}} (hyperlink using LINKS[rId]).
Page numbers for the TOC come from pages.json (see run_guide.sh).
"""
import json, os, re, shutil, sys, zipfile, random

SRC, OUT, CONFIG = sys.argv[1], sys.argv[2], sys.argv[3]
PAGES = sys.argv[4] if len(sys.argv) > 4 else 'none'
pages = json.load(open(PAGES)) if PAGES != 'none' and os.path.exists(PAGES) else {}
cfg = {}
exec(open(CONFIG, encoding='utf8').read(), cfg)
TITLE, HEADER_TITLE, APP_AUD, LINKS, CONTENT = (cfg[k] for k in ('TITLE', 'HEADER_TITLE', 'APP_AUD', 'LINKS', 'CONTENT'))

PURPLE = 'C3A6F0'   # Word has no purple highlight, so shading is used
BLANK = '[' + '\u00a0' * 6 + ']'

# ---------------------------------------------------------------- helpers
def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def runs(text, base_rpr='', italic=False):
    """Parse **bold**, [[marker]], ((blank)) and {{link:rId|text}} markup into runs."""
    out = []
    for part in re.split(r'(\[\[.*?\]\]|\(\(blank\)\)|\{\{link:.*?\}\})', text):
        if not part:
            continue
        if part.startswith('[['):
            label = '[' + part[2:-2] + ']'
            out.append('<w:r><w:rPr>%s<w:highlight w:val="yellow"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, esc(label)))
            continue
        if part == '((blank))':
            out.append('<w:r><w:rPr>%s<w:shd w:val="clear" w:color="auto" w:fill="%s"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, PURPLE, BLANK))
            continue
        if part.startswith('{{link:'):
            rid, label = part[7:-2].split('|', 1)
            out.append('<w:hyperlink r:id="%s" w:history="1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:hyperlink>' % (rid, esc(label)))
            continue
        for i, seg in enumerate(part.split('**')):
            if not seg:
                continue
            b = '<w:b/><w:bCs/>' if i % 2 else ''
            out.append('<w:r><w:rPr>%s%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, b, esc(seg)))
    return ''.join(out)

_bm = [100]
toc_entries = []  # (level, text, bookmark)

def heading(level, text):
    _bm[0] += 1
    name = '_Toc2414%05d' % _bm[0]
    toc_entries.append((level, text, name))
    return ('<w:p><w:pPr><w:pStyle w:val="Heading%d"/></w:pPr><w:bookmarkStart w:id="%d" w:name="%s"/>'
            '<w:r><w:t>%s</w:t></w:r><w:bookmarkEnd w:id="%d"/></w:p>') % (level, _bm[0], name, esc(text), _bm[0])

def plain(text, keep=False):
    return '<w:p>%s%s</w:p>' % ('<w:pPr><w:keepNext/></w:pPr>' if keep else '', runs(text))

def list_item(text, numid, ilvl, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>%s<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr></w:pPr>%s</w:p>'
            % ('<w:keepNext/>' if keep else '', ilvl, numid, runs(text)))

def shot(text, indent=720):
    return '<w:p><w:pPr>%s</w:pPr>%s</w:p>' % ('<w:ind w:left="%d"/>' % indent if indent else '', runs(text))

def bullet0(text, numid, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>%s<w:numPr><w:ilvl w:val="1"/><w:numId w:val="%d"/></w:numPr>'
            '<w:ind w:left="720" w:hanging="360"/></w:pPr>%s</w:p>' % ('<w:keepNext/>' if keep else '', numid, runs(text)))

PAGEBREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

# callout box templates cloned from the template's own tables
d = open(os.path.join(SRC, 'word/document.xml'), encoding='utf8').read()
tbls = re.findall(r'<w:tbl>.*?</w:tbl>', d, re.S)
BOX_TIP, BOX_NOTE = tbls[0], tbls[1]
assert 'descr="Tip"' in BOX_TIP and 'descr="Critical Tip"' in BOX_NOTE

_id = [5000]
def unique(x):
    x = re.sub(r' w14:paraId="[^"]*"| w14:textId="[^"]*"', '', x)
    def docpr(m):
        _id[0] += 1
        return '<wp:docPr id="%d" name="Group %d"' % (_id[0], _id[0])
    x = re.sub(r'<wp:docPr id="\d+" name="[^"]*"', docpr, x)
    x = re.sub(r'wp14:anchorId="\w+"', lambda m: 'wp14:anchorId="%08X"' % random.randint(0x10000000, 0x7FFFFFFF), x)
    x = re.sub(r'wp14:editId="\w+"', lambda m: 'wp14:editId="%08X"' % random.randint(0x10000000, 0x7FFFFFFF), x)
    x = re.sub(r'relativeHeight="\d+"', lambda m: 'relativeHeight="%d"' % random.randint(251650000, 251999999), x)
    return x

def box(kind, text):
    t = BOX_TIP if kind == 'tip' else BOX_NOTE
    # replace the text-cell paragraph (second cell) with TipText runs
    i = t.index('<w:vAlign w:val="center"/>')
    m = re.compile(r'<w:p[ >].*?</w:p>', re.S).search(t, i)
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', m.group(0), re.S).group(0)
    ppr = re.sub(r'<w:rPr>.*?</w:rPr>', '', ppr)  # drop paragraph-mark rPr
    newp = '<w:p>%s%s</w:p>' % (ppr, runs(text, base_rpr='<w:rStyle w:val="TipText"/>'))
    t = t[:m.start()] + newp + t[m.end():]
    return unique(t)

# ---------------------------------------------------------------- body
body = []
nums = []          # new w:num definitions
numid = 4
current = None

def new_list():
    global numid, current
    numid += 1
    nums.append('<w:num w:numId="%d"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>' % numid)
    current = numid

in_list = False
for idx, item in enumerate(CONTENT):
    kind, text = item[0], item[1]
    nxt = CONTENT[idx + 1][0] if idx + 1 < len(CONTENT) else ''
    keep = nxt in ('shot', 'shot0', 'tip', 'note')
    flags = item[2:] if len(item) > 2 else ()
    if kind in ('h1', 'h2', 'h3'):
        if 'pagebreak' in flags:
            body.append(PAGEBREAK)
        elif kind == 'h3' and body and not body[-1].startswith('<w:p><w:r><w:br'):
            body.append('<w:p/>')
        body.append(heading(int(kind[1]), text))
        in_list = False
    elif kind == 'p':
        body.append(plain(text, keep)); in_list = False
    elif kind == 'step':
        if not in_list:
            new_list(); in_list = True
        body.append(list_item(text, current, 0, keep))
    elif kind == 'bullet':
        body.append(list_item(text, current, 1, keep))
    elif kind == 'bullet0':
        if not in_list:
            new_list(); in_list = True
        body.append(bullet0(text, current, keep))
    elif kind == 'shot':
        body.append(shot(text))
    elif kind == 'shot0':
        body.append(shot(text, 0))
    elif kind in ('tip', 'note'):
        body.append(box(kind, text))

# TOC ------------------------------------------------------------------
def toc_para(level, text, bm, first):
    pg = str(pages.get(text, 2))
    ppr = ('<w:pPr><w:pStyle w:val="TOC%d"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9350"/></w:tabs>'
           '<w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>'
           '<w:noProof/><w:kern w:val="2"/><w:sz w:val="24"/><w:szCs w:val="24"/><w14:ligatures w14:val="standardContextual"/></w:rPr></w:pPr>') % level
    start = ''
    if first:
        start = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
                 '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    nw = '<w:rPr><w:noProof/><w:webHidden/></w:rPr>'
    link = ('<w:hyperlink w:anchor="%s" w:history="1"><w:r><w:rPr><w:rStyle w:val="Hyperlink"/><w:noProof/></w:rPr><w:t>%s</w:t></w:r>'
            '<w:r>%s<w:tab/></w:r><w:r>%s<w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r>%s<w:instrText xml:space="preserve"> PAGEREF %s \\h </w:instrText></w:r>'
            '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r><w:r>%s<w:t>%s</w:t></w:r><w:r>%s<w:fldChar w:fldCharType="end"/></w:r></w:hyperlink>'
            ) % (bm, esc(text), nw, nw, nw, bm, nw, nw, pg, nw)
    return '<w:p>%s%s%s</w:p>' % (ppr, start, link)

toc_xml = ''.join(toc_para(l, t, b, i == 0) for i, (l, t, b) in enumerate(toc_entries))

# assemble document.xml using the template's own front matter
head_end = d.index('<w:body>') + len('<w:body>')
sdt_start = d.index('<w:sdt>')
toc_heading_start = d.rfind('<w:p ', 0, d.index('TOCHeading'))
toc_heading_end = d.index('</w:p>', toc_heading_start) + 6
front = d[head_end:toc_heading_end]            # empty para + sdt open + TOC heading
tail_fld_end = '<w:p><w:r><w:rPr><w:b/><w:bCs/><w:noProof/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p></w:sdtContent></w:sdt>'
spacer = '<w:p><w:r><w:br/></w:r></w:p><w:p/>'
sect = re.search(r'<w:sectPr.*?</w:sectPr>', d, re.S).group(0)
doc = (d[:head_end] + re.sub(r' w14:paraId="[^"]*"| w14:textId="[^"]*"', '', front) + toc_xml + tail_fld_end +
       spacer + PAGEBREAK + ''.join(body) + '<w:p/>' + sect + '</w:body></w:document>')

# ---------------------------------------------------------------- package
work = OUT + '_build'
if os.path.exists(work):
    shutil.rmtree(work)
shutil.copytree(SRC, work)
open(os.path.join(work, 'word/document.xml'), 'w', encoding='utf8').write(doc)

# numbering: append new nums
p = os.path.join(work, 'word/numbering.xml')
n = open(p, encoding='utf8').read()
n = n.replace('</w:numbering>', ''.join(nums) + '</w:numbering>')
open(p, 'w', encoding='utf8').write(n)

# header: title and app | audience
p = os.path.join(work, 'word/header1.xml')
h = open(p, encoding='utf8').read()
paras = re.findall(r'<w:p [^>]*>.*?</w:p>', h, re.S)
def set_text(par, text):
    rs = re.findall(r'<w:r[ >].*?</w:r>', par, re.S)
    first = rs[0]
    first = re.sub(r'<w:t[^>]*>.*?</w:t>', '<w:t xml:space="preserve">%s</w:t>' % esc(text), first, flags=re.S)
    start = par.index(rs[0]); end = par.index(rs[-1]) + len(rs[-1])
    return par[:start] + first + par[end:]
h = h.replace(paras[1], set_text(paras[1], HEADER_TITLE))
h = h.replace(paras[2], set_text(paras[2], APP_AUD))
# brand word in the header line 1 becomes the purple blank placeholder
m = re.search(r'<w:r( [^>]*)?>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)<w:t>Epic</w:t></w:r>', h, re.S)
assert m, 'brand run not found'
h = h.replace(m.group(0), m.group(0).replace('</w:rPr>', '<w:shd w:val="clear" w:color="auto" w:fill="%s"/></w:rPr>' % PURPLE, 1).replace('<w:t>Epic</w:t>', '<w:t>%s</w:t>' % BLANK))
open(p, 'w', encoding='utf8').write(h)

# content type: template -> document ; core title
p = os.path.join(work, '[Content_Types].xml')
c = open(p, encoding='utf8').read().replace('wordprocessingml.template.main+xml', 'wordprocessingml.document.main+xml')
open(p, 'w', encoding='utf8').write(c)
p = os.path.join(work, 'docProps/core.xml')
c = open(p, encoding='utf8').read()
c = re.sub(r'<dc:title>.*?</dc:title>', '<dc:title>%s</dc:title>' % esc(HEADER_TITLE), c)
open(p, 'w', encoding='utf8').write(c)

# template name and old links must not leak into the finished guide
p = os.path.join(work, 'docProps/app.xml')
c = open(p, encoding='utf8').read()
c = re.sub(r'<Template>.*?</Template>', '<Template>Normal.dotm</Template>', c)
c = c.replace('Epic Training Quick Start Guide', esc(HEADER_TITLE))
open(p, 'w', encoding='utf8').write(c)
p = os.path.join(work, 'word/_rels/document.xml.rels')
c = open(p, encoding='utf8').read()
c = re.sub(r'<Relationship Id="rId\d+"[^>]*epic\.com[^>]*/>', '', c)
add = ''.join('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="%s" TargetMode="External"/>' % (k, esc(v)) for k, v in LINKS.items())
c = c.replace('</Relationships>', add + '</Relationships>')
open(p, 'w', encoding='utf8').write(c)


if os.path.exists(OUT):
    os.remove(OUT)
z = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
# [Content_Types].xml first
order = ['[Content_Types].xml'] + sorted(
    os.path.relpath(os.path.join(r, f), work) for r, _, fs in os.walk(work) for f in fs
    if os.path.relpath(os.path.join(r, f), work) != '[Content_Types].xml')
for rel in order:
    z.write(os.path.join(work, rel), rel)
z.close()
shutil.rmtree(work)
json.dump([t for _, t, _ in toc_entries], open(OUT + '.headings.json', 'w'))
print('built', OUT, 'headings:', len(toc_entries), 'lists:', len(nums))
