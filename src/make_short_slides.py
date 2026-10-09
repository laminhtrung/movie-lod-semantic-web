"""Create the 13-slide current summary without touching the full deck or MP4."""
from copy import deepcopy
from pathlib import Path
import subprocess,tempfile,shutil
from pptx import Presentation
from pptx.util import Inches
from common import ROOT
import make_slides as renderer
selected=[1,2,3,4,5,9,10,12,13,14,17,22,24]
original=renderer.SLIDES
items=[deepcopy(original[n-1]) for n in selected]
for i,s in enumerate(items,1):s['number']=i
renderer.SLIDES=items
prs=Presentation();prs.slide_width=Inches(16);prs.slide_height=Inches(9)
folder=ROOT/'docs/slides_short_13';folder.mkdir(exist_ok=True)
for s in items:
    c=renderer.Canvas(prs,s['number'],s['title'],s['subtitle'],s['kind']=='cover');renderer.render_slide(c,s)
    notes=s['speech']
    if 'photo' in s:
        spec=renderer.PROTEGE_SHOTS[s['photo']];notes+='\n\nẢNH PROTÉGÉ CẦN BỔ SUNG\n'+'\n'.join(spec['steps'])+'\n'+spec['expect']
    c.ps.notes_slide.notes_text_frame.text=notes;c.im.save(folder/f"{s['number']:02d}.png")
file=ROOT/'docs/Slide_ngan_13.pptx';prs.save(file)
with tempfile.TemporaryDirectory(prefix='movie-short-v3-') as tmp:
    target=Path(tmp)/'pdf';target.mkdir();profile=Path(tmp)/'profile'
    subprocess.run(['/Applications/LibreOffice.app/Contents/MacOS/soffice','-env:UserInstallation='+profile.as_uri(),'--headless','--convert-to','pdf','--outdir',str(target),str(file)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    shutil.copy2(target/'Slide_ngan_13.pdf',file.with_suffix('.pdf'))
lines=['# MovieLOD — Script cho 13 slide tóm tắt','', 'Bản 3.0.0; chữ slide/notes tiếng Anh, script này tiếng Việt. Bộ chính vẫn 24 slide; bản ngắn chọn nội dung cốt lõi. MP4 đã được loại; dùng demo ứng dụng trực tiếp.','']
for original_index,s in zip(selected,items):lines+=['## Slide '+str(s['number'])+' — '+s['title'],'','Tương ứng slide '+str(original_index)+' của bộ chính.','',s['speech_vi'],'']
(ROOT/'docs/Script_thuyet_trinh_ngan_13.md').write_text('\n'.join(lines)+'\n')
print('Updated 13-slide summary and Vietnamese script.')
