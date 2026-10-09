"""Check English slides with Vietnamese guidance only in empty photo slots."""
import hashlib
import json
import re
from pathlib import Path
from pptx import Presentation
from pypdf import PdfReader
from common import ROOT, write_json


def contains_vietnamese(text):
    text=text.replace('Protégé','Protege').replace('PROTÉGÉ','PROTEGE')
    return bool(re.search('[À-žẠ-ỹ]',text))


def main():
    presentation=Presentation(ROOT/'docs/Slide.pptx')
    pdf=PdfReader(ROOT/'docs/Slide.pdf')
    bad, outside, slots=[],[],[]
    for number,slide in enumerate(presentation.slides,1):
        for shape in slide.shapes:
            if shape.name.startswith('PHOTO_'):
                if shape.has_text_frame and 'CẦN BỔ SUNG' in shape.text:slots.append(number)
            elif shape.has_text_frame and contains_vietnamese(shape.text):
                bad.append({'slide':number,'text':shape.text})
            if shape.left<0 or shape.top<0 or shape.left+shape.width>presentation.slide_width+1000 or shape.top+shape.height>presentation.slide_height+1000:
                outside.append({'slide':number,'shape':shape.name})
        narration=slide.notes_slide.notes_text_frame.text.split('ẢNH PROTÉGÉ CẦN BỔ SUNG')[0]
        assert narration.strip() and not contains_vietnamese(narration), number
    assert not bad,bad
    assert not outside,outside
    assert len(slots)==11,slots
    assert len(presentation.slides)==len(pdf.pages)==24
    assert all('Data checked:' in page.extract_text() for page in pdf.pages)
    for name in ['12_sources_en']:
        assert not contains_vietnamese((ROOT/'evidence/screenshots'/f'{name}.html').read_text())
    report={'slides':24,'notes':24,'slide_language':'English','speaker_notes_language':'English','placeholder_language':'Vietnamese',
            'vietnamese_placeholder_slides':slots,'unexpected_non_english_text':bad,'outside_shapes':outside,
            'pdf_searchable':True,'evidence_images':['12_sources_en.png','docs/sync_images/verification.png'],
            'pptx_sha256':hashlib.sha256((ROOT/'docs/Slide.pptx').read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256((ROOT/'docs/Slide.pdf').read_bytes()).hexdigest(),
            'mp4_included':False}
    write_json(ROOT/'evidence/presentation_language_checks.json',report)
    write_json(ROOT/'evidence/presentation_checks.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
