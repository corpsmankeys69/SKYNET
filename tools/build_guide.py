"""Build a Quick Start Guide .docx from the Epic Training template XML.

Usage: python3 -I build_guide.py <template_unzipped_dir> <out_docx> <pages.json or none>
Content is defined in CONTENT below; page numbers for the TOC come from pages.json (pass 2).
"""
import json, os, re, shutil, sys, zipfile, random

SRC, OUT, PAGES = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else 'none')
pages = json.load(open(PAGES)) if PAGES != 'none' and os.path.exists(PAGES) else {}

TITLE = 'Outpatient Clinician Rooming a Patient'
APP_AUD = 'Ambulatory | RN/MA'

# ---------------------------------------------------------------- content
# kinds: h1 h2 h3 | p (plain paragraph) | step (numbered) | bullet | shot (placeholder)
#        tip (efficiency box) | note (important box)
# Inline markup: **bold**, [[placeholder]] (highlighted marker for items added by hand)
CONTENT = [
 ('h1', 'Outpatient Clinician Rooming a Patient Quick Start Guide'),

 ('h2', 'Customize Your Schedule'),
 ('step', 'After logging in, click on the **Schedule** tab to access the **Department Schedule**.'),
 ('step', 'Click the drop-down arrow to the right of your name and click the push pin to the right of your **Department** name to see the **Calendar** view.'),
 ('shot', '[[Screenshot: schedule drop-down with Dept field and My Schedule list]]'),
 ('step', 'Select the drop-down arrow next to the **Department** name and left click to drop and drag your practitioner or resource (generic) schedule to your **My Schedule.**'),
 ('shot', '[[Screenshot: My Schedule and Department entries highlighted in the schedule list]]'),
 ('step', 'Highlight your name under **My Schedule** to see the appointments for today.'),

 ('h2', 'Review Patient Information', 'pagebreak'),
 ('step', 'Highlight an appointment on your **Schedule** to view additional patient information.'),
 ('step', 'Review the **SnapShot** report on the **Report Pane** from the **Schedule**.'),
 ('shot', '[[Screenshot: SnapShot report on the Report Pane]]'),
 ('step', 'If this is a commonly used **Report**, you can create a button on the **Report Pane** toolbar, so you do not have to search for it every time.'),
 ('step', 'Click the wrench on the **Report Pane** toolbar next to the **Search** field.'),
 ('step', 'The **Add or Remove Buttons** from **Toolbar** window appears.'),
 ('step', 'Click the **Add Current** button to pull in the current viewed **Report.**'),
 ('tip', 'You can change the **Button Name** in this window to your preference.'),
 ('step', 'Click **Accept**. The button is permanently added to your **Report Pane**.'),

 ('h2', 'Rooming a Patient', 'pagebreak'),
 ('h3', 'Document the Reason for Visit'),
 ('step', 'Open the **Rooming** activity tab and select the **Reason for Visit** section.'),
 ('shot', '[[Screenshot: Rooming activity tabs with Reason for Visit]]'),
 ('step', 'Use the speed buttons to select the **Chief Complaint**.'),
 ('note', "If you don't see a button for the patient's chief complaint, search for it in the **Chief Complaint** field. Enter the first few letters of the complaint and press **Enter**. A list of matching complaints appears. Double-click a complaint to select it."),
 ('step', 'Click one of the common **Chief Complaint buttons**. Or, in the **Chief Complaint** field, enter the first few letters of the complaint and press **Enter**. In the list of matches that appear, double-click a reason to select.'),
 ('shot', '[[Screenshot: Reason for Visit section with Chief Complaint buttons]]'),

 ('h3', 'Document Vitals'),
 ('step', 'Click the Vitals section to document the appropriate fields.'),
 ('tip', 'A Pain Score can also be documented under the Vitals section.'),
 ('step', 'To add another set of vitals for this visit, click **New Reading**. A new column with today\'s date and time appears.'),
 ('shot', '[[Screenshot: Vitals section]]'),

 ('h3', "Review and Update the Patient's Allergies"),
 ('step', 'Click the **Allergies** section.'),
 ('shot', '[[Screenshot: Allergies section]]'),
 ('step', 'To indicate that the patient does not have any allergies, select the **No Known Allergies** check box and click **Mark as Reviewed**.'),
 ('step', "To indicate that you were unable to assess the patient's allergies, click **Unable to Assess**, then enter a reason."),
 ('step', 'To add an allergy:'),
 ('bullet', 'Enter the first few letters of the allergy in the [[icon]] **Add** field and press **Enter**. A list of matching allergens appears.'),
 ('bullet', "Double-click the appropriate allergy and enter information like the type of allergy and the patient's reaction."),
 ('bullet', 'Click [[icon]] Accept.'),
 ('step', 'To update an allergy, click the name of an allergen and edit the information, as necessary.'),
 ('step', 'If an allergy was entered in error, click [[icon]] **Delete** and enter a reason for deletion.'),
 ('step', 'When you are done updating allergies, click [[icon]] **Mark as Reviewed**.'),
 ('note', "Marking a section of the patient's chart as reviewed is similar to initialing the paper chart. The chart is updated to indicate that you last reviewed the information, and the date and time appear."),

 ('h3', "Update a Patient's Current Medications"),
 ('step', 'Click the Med Review section.'),
 ('shot', '[[Screenshot: Med Review section]]'),
 ('step', 'Select or clear the Taking? check box to indicate whether the patient is currently taking a medication.'),
 ('step', 'To flag a medication for removal that the patient is no longer taking, hover your mouse over the medication and click the [[icon: red X]] that appears on the right.'),
 ('shot', '[[Screenshot: Med Review section with the red X on a medication]]'),
 ('step', 'The **Remove Order** window opens. Confirm the **Flag for removal** button is highlighted and click **Accept**.'),

 ('h3', 'Add a Patient-Reported Medication'),
 ('step', "In the **Med Review** section, click in the **Add Medication** search field, enter part of the medication's name and press **Enter**. A list of matching medications appears."),
 ('step', 'Double-click the appropriate medication.'),
 ('step', "Enter information about the medication, such as the dose, when the patient started taking it, and the frequency. Click **Accept**."),
 ('step', "When you have finished reviewing and updating the patient's medications, click [[icon]] Mark as Reviewed."),

 ('h3', "Verify the Patient's Pharmacy"),
 ('step', 'Ask the patient if the pharmacy listed in the **Med Review** section is correct.'),
 ('step', 'To change the pharmacy, click the **pharmacy name**.'),
 ('note', 'If the patient does not have a pharmacy, click **No pharmacy Selected** button.'),
 ('step', "Choose one of the suggested pharmacies or search for the patient’s preferred pharmacy and click **Accept**."),

 ('h3', 'Reconcile Outside Medication Info'),
 ('p', "When another organization has a medication on file for the patient, a banner appears at the top of the **Med Review** section. This data can come from other organizations that see the patient or from an outside pharmacy."),
 ('step', 'In the **Med Review** section, click **Go Reconcile** [[icon]] in the banner that indicates medications from outside sources are available.'),
 ('shot', '[[Screenshot: New medications from outside sources banner with Go Reconcile]]'),
 ('step', 'Review the information that appears in the **Reconcile Outside Info** activity.'),
 ('step', 'Click [[icon: green plus]] for any medications the patient confirms that they are taking. The **Medication Details** window opens.'),
 ('step', 'Enter information about the medication ([[icon: red !]] means that an item is required) and click **Accept**.'),
 ('note', '[[icon: ?]] appears next to medications that do not have an exact match in Epic. For example, a patient might report a brand name medication but not its strength. When you click [[icon: green plus]], you must enter a matching medication in the **Medication Details** window.'),
 ('step', 'Click [[icon: trash can]] for any medications that the patient denies taking.'),
 ('step', "When you are finished, click [[icon]] **Accept** to add the reconciled medications to the patient's medication list."),

 ('h3', "Document Patient’s Medical, Surgical, Family and Social History"),
 ('step', 'Click on the **History** section.'),
 ('shot', '[[Screenshot: History section, General Medical History]]'),
 ('step', 'Update the items as needed.'),
 ('tip', 'You can use the paper icon to add additional comments.'),
 ('step', 'Use the **green plus sign next to Add** to search for and add items that are not already listed.'),
 ('step', 'Indicate that you have reviewed and updated the history for the patient by clicking **Mark as Reviewed**.'),
 ('step', 'Repeat the steps above and document **Surgical history** as appropriate.'),

 ('h3', 'Exploring Family History'),
 ('step', 'Scroll down to the **Family History** and document information provided by the patient.'),
 ('shot', '[[Screenshot: Family History grid]]'),
 ('step', 'To update the living status of a family member, left click in the **Status** field to make changes.'),
 ('step', 'Click **Mark as Reviewed**.'),

 ('h3', 'Exploring Substance and Sexual Activity History'),
 ('step', 'Review and document the **Substance** and **Sexual Activity** history as needed.'),
 ('step', 'Click **Mark as Reviewed**.'),
]

# ---------------------------------------------------------------- helpers
def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def runs(text, base_rpr='', italic=False):
    """Parse **bold** and [[placeholder]] markup into runs."""
    out = []
    for part in re.split(r'(\[\[.*?\]\])', text):
        if not part:
            continue
        if part.startswith('[['):
            label = '[' + part[2:-2] + ']'
            out.append('<w:r><w:rPr>%s<w:highlight w:val="yellow"/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % (base_rpr, esc(label)))
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

def plain(text):
    return '<w:p>%s</w:p>' % runs(text)

def list_item(text, numid, ilvl, keep=False):
    return ('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>%s<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr></w:pPr>%s</w:p>'
            % ('<w:keepNext/>' if keep else '', ilvl, numid, runs(text)))

def shot(text):
    return '<w:p><w:pPr><w:ind w:left="720"/></w:pPr>%s</w:p>' % runs(text)

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
    keep = nxt in ('shot', 'tip', 'note')
    flags = item[2:] if len(item) > 2 else ()
    if kind in ('h1', 'h2', 'h3'):
        if 'pagebreak' in flags:
            body.append(PAGEBREAK)
        elif kind == 'h3' and body and not body[-1].startswith('<w:p><w:r><w:br'):
            body.append('<w:p/>')
        body.append(heading(int(kind[1]), text))
        in_list = False
    elif kind == 'p':
        body.append(plain(text)); in_list = False
    elif kind == 'step':
        if not in_list:
            new_list(); in_list = True
        body.append(list_item(text, current, 0, keep))
    elif kind == 'bullet':
        body.append(list_item(text, current, 1, keep))
    elif kind == 'shot':
        body.append(shot(text).replace('<w:pPr>', '<w:pPr>' + ('<w:keepNext/>' if False else ''), 1))
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
h = h.replace(paras[1], set_text(paras[1], TITLE + ' Quick Start Guide'))
h = h.replace(paras[2], set_text(paras[2], APP_AUD))
open(p, 'w', encoding='utf8').write(h)

# content type: template -> document ; core title
p = os.path.join(work, '[Content_Types].xml')
c = open(p, encoding='utf8').read().replace('wordprocessingml.template.main+xml', 'wordprocessingml.document.main+xml')
open(p, 'w', encoding='utf8').write(c)
p = os.path.join(work, 'docProps/core.xml')
c = open(p, encoding='utf8').read()
c = re.sub(r'<dc:title>.*?</dc:title>', '<dc:title>%s Quick Start Guide</dc:title>' % TITLE, c)
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
