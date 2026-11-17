"""Build a guide .docx from the Epic Training Quick Start Guide template XML.

Usage: python3 -I build_guide.py <template_unzipped_dir> <out_docx> <config.py> [pages.json]

Config (see guides/*.py) defines TITLE, HEADER_TITLE, APP_AUD, LINKS {rId: url}, CONTENT.
Content kinds:
  bullet3         third-level bullet under a step; bullet0b = second level of a standalone bullet list
  h1 h2 h3        headings (add 'pagebreak' as third item to start a main topic on a new page)
  p               plain paragraph (Normal style)
  step / bullet   numbered step (restarts per list) / level-2 bullet under a step
  bullet0         standalone bullet list item (not under a step)
  shot / shot0    highlighted [Screenshot: ...] placeholder, indented under a step / flush left
  table           data table: text = {'widths': [twips...], 'title': str|None, 'header': [...], 'rows': [[...]]}; black 0.5 pt borders, bold header, no shading
  tip / note      Efficiency Tip box / Important Note box (cloned from the template, icons kept)
Inline markup: **bold**, __italic__, [[hand-added marker]] (yellow), ((blank)) (purple blank placeholder),
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
            for j, sub in enumerate(seg.split('__')):
                if not sub:
                    continue
                it = '<w:i/><w:iCs/>' if j % 2 else ''
                out.append('<w:r><w:rPr>%s%s%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, b, it, esc(sub).replace('\n', '</w:t><w:br/><w:t xml:space="preserve">')))
    return ''.join(out)

_bm = [100]
toc_entries = []  # (level, text, bookmark)

def plain_h(text):
    return text.replace('((blank))', BLANK)

def heading_runs(text, base_rpr=''):
    out = []
    for i, piece in enumerate(text.split('((blank))')):
        if i:
            out.append('<w:r><w:rPr>%s<w:shd w:val="clear" w:color="auto" w:fill="%s"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, PURPLE, BLANK))
        if piece:
            out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % ('<w:rPr>%s</w:rPr>' % base_rpr if base_rpr else '', esc(piece)))
    return ''.join(out)

def heading(level, text):
    _bm[0] += 1
    name = '_Toc2414%05d' % _bm[0]
    toc_entries.append((level, text, name))
    return ('<w:p><w:pPr><w:pStyle w:val="Heading%d"/></w:pPr><w:bookmarkStart w:id="%d" w:name="%s"/>'
            '%s<w:bookmarkEnd w:id="%d"/></w:p>') % (level, _bm[0], name, heading_runs(text), _bm[0])

def plain(text, keep=False):
    return '<w:p>%s%s</w:p>' % ('<w:pPr><w:keepNext/></w:pPr>' if keep else '', runs(text))

def list_item(text, numid, ilvl, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>%s<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr></w:pPr>%s</w:p>'
            % ('<w:keepNext/>' if keep else '', ilvl, numid, runs(text)))

def shot(text, indent=720):
    return '<w:p><w:pPr>%s</w:pPr>%s</w:p>' % ('<w:ind w:left="%d"/>' % indent if indent else '', runs(text))

def bullet0(text, numid, keep=False, left=720):
    return ('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>%s<w:numPr><w:ilvl w:val="1"/><w:numId w:val="%d"/></w:numPr>'
            '<w:ind w:left="%d" w:hanging="360"/></w:pPr>%s</w:p>' % ('<w:keepNext/>' if keep else '', numid, left, runs(text)))

PAGEBREAK = '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

BORDERS = ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="auto"/>' % e for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))

def data_table(spec):
    """spec: {'widths': [...], 'title': str|None, 'header': [...], 'rows': [[...], ...]}; borders match the callout boxes, no shading."""
    widths = spec['widths']
    total = sum(widths)
    def cell(text, w, bold=False, span=1):
        tcpr = '<w:tcW w:w="%d" w:type="dxa"/>%s' % (w, '<w:gridSpan w:val="%d"/>' % span if span > 1 else '')
        rpr = '<w:b/><w:bCs/>' if bold else ''
        return '<w:tc><w:tcPr>%s</w:tcPr><w:p><w:pPr><w:keepNext/><w:spacing w:before="40" w:after="40"/></w:pPr>%s</w:p></w:tc>' % (tcpr, runs(text, base_rpr=rpr))
    def row(cells, header=False):
        trpr = '<w:trPr><w:cantSplit/>%s</w:trPr>' % ('<w:tblHeader/>' if header else '')
        return '<w:tr>%s%s</w:tr>' % (trpr, ''.join(cells))
    rows = []
    if spec.get('title'):
        rows.append(row([cell(spec['title'], total, True, len(widths))]))
    rows.append(row([cell(t, w, True) for t, w in zip(spec['header'], widths)], header=True))
    for r in spec['rows']:
        rows.append(row([cell(t, w) for t, w in zip(r, widths)]))
    # keepNext on every row but the last keeps the table on one page
    xml = ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:tblInd w:w="115" w:type="dxa"/><w:tblBorders>%s</w:tblBorders>'
           '<w:tblLayout w:type="fixed"/><w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>') % (total, BORDERS, ''.join('<w:gridCol w:w="%d"/>' % w for w in widths), ''.join(rows))
    i = xml.rfind('<w:keepNext/>')
    # last row: drop keepNext so the table does not chain onto the next paragraph
    last = xml.rfind('<w:tr>')
    xml = xml[:last] + xml[last:].replace('<w:keepNext/>', '')
    return xml + '<w:p/>' 

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
    keep = nxt in ('shot', 'shot0', 'tip', 'note', 'table')
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
    elif kind == 'bullet3':      # third level under a step: bullet indented one more step
        body.append(bullet0(text, current, keep, left=1800))
    elif kind == 'bullet0b':     # second level of a standalone bullet list
        body.append(bullet0(text, current, keep, left=1080))
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
    elif kind == 'table':
        body.append(data_table(text)); in_list = in_list

# TOC ------------------------------------------------------------------
def toc_para(level, text, bm, first):
    pg = str(pages.get(plain_h(text), 2))
    ppr = ('<w:pPr><w:pStyle w:val="TOC%d"/><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9350"/></w:tabs>'
           '<w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>'
           '<w:noProof/><w:kern w:val="2"/><w:sz w:val="24"/><w:szCs w:val="24"/><w14:ligatures w14:val="standardContextual"/></w:rPr></w:pPr>') % level
    start = ''
    if first:
        start = ('<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
                 '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    nw = '<w:rPr><w:noProof/><w:webHidden/></w:rPr>'
    link = ('<w:hyperlink w:anchor="%s" w:history="1">%s'
            '<w:r>%s<w:tab/></w:r><w:r>%s<w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r>%s<w:instrText xml:space="preserve"> PAGEREF %s \\h </w:instrText></w:r>'
            '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r><w:r>%s<w:t>%s</w:t></w:r><w:r>%s<w:fldChar w:fldCharType="end"/></w:r></w:hyperlink>'
            ) % (bm, heading_runs(text, '<w:rStyle w:val="Hyperlink"/><w:noProof/>'), nw, nw, nw, bm, nw, nw, pg, nw)
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
    start = par.index(rs[0]); end = par.index(rs[-1]) + len(rs[-1])
    if '((blank))' not in text:
        first = re.sub(r'<w:t[^>]*>.*?</w:t>', '<w:t xml:space="preserve">%s</w:t>' % esc(text), first, flags=re.S)
        return par[:start] + first + par[end:]
    # text holds a purple blank: rebuild the runs from the first run's formatting
    rpr = re.search(r'<w:rPr>(.*?)</w:rPr>', first, re.S)
    rpr = rpr.group(1) if rpr else ''
    new = []
    for i, piece in enumerate(text.split('((blank))')):
        if i:
            new.append('<w:r><w:rPr>%s<w:shd w:val="clear" w:color="auto" w:fill="%s"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, PURPLE, BLANK))
        if piece:
            new.append('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(piece)))
    return par[:start] + ''.join(new) + par[end:]
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
json.dump([plain_h(t) for _, t, _ in toc_entries], open(OUT + '.headings.json', 'w'))
print('built', OUT, 'headings:', len(toc_entries), 'lists:', len(nums))
