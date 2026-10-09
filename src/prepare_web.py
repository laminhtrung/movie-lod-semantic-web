"""Prepare version-3 query samples and documents; never create/copy videos."""
import json,shutil
from common import ROOT,write_json
meta=json.loads((ROOT/'evidence/ontology_design/query_results.json').read_text())
order=[2]+[i for i in range(1,28) if i!=2]
samples=[]
for n in order:
    row=meta[n-1];samples.append({'file':f'{n:02}.rq','label':row['question'],'mode':'dataset' if n==27 else 'asserted' if row['group']=='A' else 'reasoned','query':(ROOT/'queries'/f'{n:02}.rq').read_text()})
write_json(ROOT/'web/dist/data/queries.json',samples)
shutil.copy2(ROOT/'LICENSE-DATA.txt',ROOT/'web/dist/LICENSE-DATA.txt')
docs=ROOT/'web/dist/docs';docs.mkdir(exist_ok=True)
for p in (ROOT/'docs').glob('*'):
    if p.is_file() and p.suffix in ['.pdf','.pptx','.docx'] and p.name!='Slide_full.pptx.pdf':shutil.copy2(p,docs/p.name)
print('Version-3 samples/documents prepared; MP4 omitted.')

images=docs/'guide_images';images.mkdir(exist_ok=True)
for p in (ROOT/'docs/guide_images').glob('*.png'):shutil.copy2(p,images/p.name)
