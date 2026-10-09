"""Verify exact report pagination, typography, spacing and source-backed figures."""
import hashlib
import json
import zipfile
import fitz
from lxml import etree
from common import ROOT,write_json
from report_content import PAGES

def main():
    pdf=fitz.open(ROOT/'docs/Bao_cao.pdf');assert len(pdf)==15
    cover=pdf[0].get_text()
    pairs=[('Lã Minh Trung','20251319M'),('Nguyễn Thu Uyên','20252279M'),('Nguyễn Thị Nhã Linh','20261262M'),('Nguyễn Khắc Thái Bình','20251324M')]
    assert all(name+' — '+identifier in cover for name,identifier in pairs)
    assert 'Supervisor: TS. Đỗ Bá Lâm' in cover
    assert len(pdf[0].get_image_info())==1
    toc=pdf[1].get_text()
    assert 'TABLE OF CONTENTS' in toc and 'Abstract\n' not in toc
    fonts=set();sizes=set()
    for index,page in enumerate(pdf):
        if index:
            assert PAGES[index]['title'] in ' '.join(page.get_text().split())
            footer=page.get_text(clip=fitz.Rect(0,790,page.rect.width,page.rect.height)).strip()
            assert footer==str(index+1),(index,footer)
        fonts.update(f[3] for f in page.get_fonts())
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):sizes.update(round(span['size'],2) for span in line['spans'])
    assert sizes=={13.0},sizes
    assert all('TimesNewRoman' in f for f in fonts),fonts
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};prefix='{'+ns['w']+'}'
    with zipfile.ZipFile(ROOT/'docs/Bao_cao.docx') as z:
        root=etree.fromstring(z.read('word/document.xml'))
        toc_active=False
        for element in root.find('w:body',ns):
            if element.tag==prefix+'p':
                text=''.join(element.itertext())
                if text=='TABLE OF CONTENTS':toc_active=True
                elif text=='1. INTRODUCTION AND OBJECTIVES':toc_active=False
            elif toc_active:assert element.tag!=prefix+'tbl'
        leaders=root.findall('.//w:tab[@w:leader="dot"]',ns)
        assert len(leaders)==20
        margins=root.find('.//w:pgMar',ns)
        assert all(margins.get(prefix+k)==v for k,v in {'left':'1701','right':'1134','top':'1134','bottom':'1134'}.items())
        for paragraph in root.findall('.//w:p',ns):
            if not paragraph.findall('.//w:t',ns):continue
            spacing=paragraph.find('w:pPr/w:spacing',ns)
            assert spacing is not None and spacing.get(prefix+'line')=='360'
        for run in root.findall('.//w:r',ns):
            if run.find('w:t',ns) is None:continue
            font=run.find('w:rPr/w:rFonts',ns);size=run.find('w:rPr/w:sz',ns)
            assert font is not None and font.get(prefix+'ascii')=='Times New Roman'
            assert size is not None and size.get(prefix+'val')=='26'
    sources=json.loads((ROOT/'evidence/report_image_sources.json').read_text())
    assert sources['source_pdf_sha256']==hashlib.sha256((ROOT/sources['source_pdf']).read_bytes()).hexdigest()
    known={i['file'] for i in sources['images']}
    figures=[b for p in PAGES for b in p['blocks'] if b['type']=='image']
    assert len(figures)==11 and all(b['path'] in known for b in figures)
    report=json.loads((ROOT/'evidence/report_format_checks.json').read_text())
    report.update(verified=True,actual_pdf_fonts=sorted(fonts),actual_pdf_text_sizes=sorted(sizes),
                  all_visible_word_runs_times_new_roman_13=True,all_visible_body_paragraphs_line_spacing_1_5=True,
                  page_numbers_verified=True,page_titles_match_plan=True,all_figures_have_attributed_sources=True,
                  figures_from_supplied_pdf=sum(next(x for x in sources['images'] if x['file']==b['path']).get('source_type')!='author_diagram' for b in figures),
                  author_generated_diagrams=sum(next(x for x in sources['images'] if x['file']==b['path']).get('source_type')=='author_diagram' for b in figures),
                  cover_names_ids_and_supervisor_verified=True,official_logo_on_cover=True,
                  toc_own_page_no_table=True,toc_dotted_leaders=20)
    write_json(ROOT/'evidence/report_format_checks.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
