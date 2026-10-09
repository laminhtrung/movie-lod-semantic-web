"""Render a readable, exhaustive schema poster directly from the canonical OWL."""
from pathlib import Path
import hashlib,json,html,subprocess,textwrap,tempfile,xml.etree.ElementTree as ET
from rdflib import Graph,RDF,RDFS,OWL,URIRef,BNode
from rdflib.collection import Collection
from playwright.sync_api import sync_playwright
from common import ROOT,BASE,EX,RES,DBO

ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

W,H=4800,4400
M=65;G=45;CW=(W-2*M-2*G)/3
FONT='Be Vietnam Pro'
INK='#173246';TEAL='#007F82';BLUE='#27609D';GREEN='#187858';PURPLE='#7655A2';GOLD='#A77412';GRAY='#526979'
parts=[]
def esc(x):return html.escape(str(x),quote=True)
def rect(x,y,w,h,fill='#fff',stroke='none',rx=22):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')
def text(x,y,value,size=29,color=INK,bold=False):parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{700 if bold else 400}">{esc(value)}</text>')
def lines(x,y,value,width,size=28,color=INK,bold=False,leading=1.4):
 out=[]
 for p in str(value).split('\n'):out+=textwrap.wrap(p,width=width,break_long_words=False,break_on_hyphens=False) or ['']
 for i,line in enumerate(out):text(x,y+i*size*leading,line,size,color,bold)
 return y+len(out)*size*leading

def panel(x,y,w,h,num,title,sub):
 rect(x,y,w,h);rect(x,y,w,104,'#EDF5F7',rx=22);text(x+30,y+45,num+'  '+title,36,TEAL,True);text(x+30,y+83,sub,24,GRAY)
 return x+32,y+137

def short(v):
 if v is None:return '—'
 for ns,prefix in [(str(EX),'ex:'),(str(DBO),'dbo:'),('http://rdfs.org/ns/void#','void:'),('http://www.w3.org/2001/XMLSchema#','xsd:')]:
  if str(v).startswith(ns):return prefix+str(v)[len(ns):]
 return str(v)

def bare(v):return short(v).split(':')[-1]

def expr(g,node):
 if isinstance(node,URIRef):return bare(node)
 for pred,join in [(OWL.intersectionOf,' and '),(OWL.unionOf,' or ')]:
  head=g.value(node,pred)
  if head:return '('+join.join(expr(g,x) for x in Collection(g,head))+')'
 p=g.value(node,OWL.onProperty)
 for pred,op in [(OWL.someValuesFrom,'some'),(OWL.hasValue,'value')]:
  value=g.value(node,pred)
  if value is not None:return bare(p)+' '+op+' '+bare(value)
 for pred,op in [(OWL.qualifiedCardinality,'exactly'),(OWL.minQualifiedCardinality,'min')]:
  v=g.value(node,pred)
  if v is not None:return bare(p)+' '+op+' '+str(v)+' '+bare(g.value(node,OWL.onClass))
 raise ValueError('Unrecognized OWL expression: '+str(node))

def graph_svg(dot,x,y,w,h,name):
 with tempfile.TemporaryDirectory(prefix='owl-diagram-') as tmp:
  source=Path(tmp)/(name+'.dot');svg=Path(tmp)/(name+'.svg');source.write_text(dot)
  subprocess.run(['dot','-Tsvg',str(source),'-o',str(svg)],check=True)
  root=ET.fromstring(svg.read_text());root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h));root.set('preserveAspectRatio','xMidYMin meet');parts.append(ET.tostring(root,encoding='unicode'))

def main():
 path=ROOT/'ontology/Movie_Knowledge_Graph.owl';g=Graph().parse(path);r=Graph().parse(ROOT/'data/processed/reasoned.ttl')
 classes=sorted({c for c in g.subjects(RDF.type,OWL.Class) if isinstance(c,URIRef)},key=str)
 obj=sorted(set(g.subjects(RDF.type,OWL.ObjectProperty)),key=str);data=sorted(set(g.subjects(RDF.type,OWL.DatatypeProperty)),key=str)
 assert len(classes)==37 and len(obj)==19 and len(data)==5
 def count(c):return len({v for v in r.subjects(RDF.type,c) if isinstance(v,URIRef) and str(v).startswith(BASE+'/')})
 rect(0,0,W,H,'#F1F5F7',rx=0)
 text(M,83,'MOVIELOD 3.0.0 — BẢN ĐỒ TOÀN BỘ ONTOLOGY',62,INK,True)
 text(M,139,'37 lớp có tên  •  19 object properties  •  5 datatype properties  •  4 cá thể vai trò',33,TEAL,True)
 text(M,187,'Đọc từ trái sang phải: lớp → mô hình quan hệ → định nghĩa OWL và kết quả suy luận.',29,GRAY)
 xs=[M,M+CW+G,M+2*(CW+G)]
 # 1. Exhaustive class hierarchy: only explicit named subclass axioms are drawn.
 x,y=panel(xs[0],235,CW,2110,'01','CÂY LỚP — ĐỦ 37 LỚP','Mũi tên: lớp cha → lớp con; số trong ngoặc = thành viên local sau suy luận')
 nodes=[];edges=[]
 for i,c in enumerate(classes):
  color=BLUE if str(c).startswith(str(DBO)) else PURPLE if short(c).startswith('void:') else GREEN
  nodes.append(f'n{i} [label="{short(c)}  ({count(c)})",color="{color}",fontcolor="{color}"];')
  for parent in g.objects(c,RDFS.subClassOf):
   if parent in classes:edges.append(f'n{classes.index(parent)} -> n{i};')
 dot='digraph G {rankdir=LR;graph[bgcolor="transparent",pad="0.2",nodesep="0.15",ranksep="0.30"];node[shape=box,style="rounded,filled",fillcolor="white",fontname="Be Vietnam Pro",fontsize=17,margin="0.08,0.05"];edge[color="#9AADB9",arrowsize=0.55];'+''.join(nodes+edges)+'}'
 graph_svg(dot,x,y,CW-64,1900,'class_hierarchy')
 # 2. Contextual credit model.
 x,y=panel(xs[1],235,CW,945,'02','TRUNG TÂM: NGƯỜI – CREDIT – PHIM','Contribution là bản ghi đóng góp; ContributionRole là lớp chứa các vai trò')
 core='''digraph G {rankdir=LR;graph[bgcolor="transparent",nodesep=.7,ranksep=.6,pad=.2];node[shape=box,style="rounded,filled",fillcolor="#E5F3EE",fontname="Be Vietnam Pro",fontsize=23,margin=".18,.14"];edge[fontname="Be Vietnam Pro",fontsize=17,color="#247A86",arrowsize=.7]; p[label="dbo:Person\\nNGƯỜI"];c[label="ex:Contribution\\nCREDIT"];f[label="dbo:Film\\nPHIM"];role[label="ex:ContributionRole\\nVAI TRÒ",fillcolor="#FFF1D2"];p->c[label="hasContribution"];c->p[label="contributionBy [F, =1]"];c->f[label="contributionTo [F, =1]"];f->c[label="contributionOf"];c->role[label="hasRole [F, =1]"];p->f[label="contributedTo (chain)",style=dashed,color="#A77412",constraint=false];}'''
 graph_svg(core,x,y,CW-64,445,'credit_model')
 y+=490
 y=lines(x,y,'Một người giữ nhiều vai trò bằng nhiều credit riêng. Mỗi credit có đúng 1 người, 1 phim và 1 vai trò.',72,29)
 y=lines(x,y+28,'4 cá thể thuộc ContributionRole:',70,28,INK,True)
 text(x,y+12,'ActorRole  •  DirectorRole  •  WriterRole  •  ProducerRole',27,GOLD,True)
 lines(x,y+57,'Bốn vai trò được khai báo AllDifferent. Đây là cá thể, không phải bốn lớp con của Person.',70,28)
 # 3. Exhaustive properties, using the domain/range present in the actual file.
 x,y=panel(xs[1],1225,CW,1640,'03','19 QUAN HỆ + 5 THUỘC TÍNH DỮ LIỆU','Domain / range đúng như trong OWL; “—” = không khai báo domain')
 text(x,y,'OBJECT PROPERTY',25,TEAL,True);text(x+510,y,'DOMAIN',25,TEAL,True);text(x+965,y,'RANGE',25,TEAL,True);y+=53
 for i,p in enumerate(obj):
  if i%2==0:rect(x-10,y-28,CW-45,49,'#F3F7F9',rx=6)
  name=short(p)+(' [F]' if (p,RDF.type,OWL.FunctionalProperty) in g else '')
  text(x,y,name,25);text(x+510,y,short(g.value(p,RDFS.domain)),24,GRAY);text(x+965,y,short(g.value(p,RDFS.range)),24,GRAY);y+=53
 y+=29;text(x,y,'DATATYPE PROPERTY',25,TEAL,True);text(x+510,y,'DOMAIN',25,TEAL,True);text(x+965,y,'KIỂU XSD',25,TEAL,True);y+=53
 for i,p in enumerate(data):
  rect(x-10,y-28,CW-45,49,'#EDF5F7' if i%2==0 else '#fff',rx=6)
  text(x,y,short(p),25);text(x+510,y,short(g.value(p,RDFS.domain)),24,GRAY);text(x+965,y,short(g.value(p,RDFS.range)),24,GRAY);y+=53
 lines(x,y+25,'runtime: GIÂY (double). releaseYear: năm nguyên. retrievedAt: thời điểm lấy nguồn; sha256: checksum phản hồi.',73,25,GRAY)
 # 4. Exhaustive equivalence expressions: 14 named defined classes.
 x,y=panel(xs[2],235,CW,2035,'04','14 LỚP CÓ ĐỊNH NGHĨA TƯƠNG ĐƯƠNG','≡ = điều kiện đủ và cần; tên không prefix bên dưới dùng dbo / ex như cây lớp')
 definitions=[(c,g.value(c,OWL.equivalentClass)) for c in classes if g.value(c,OWL.equivalentClass) is not None]
 assert len(definitions)==14
 order=['ActingContribution','DirectingContribution','WritingContribution','ProducingContribution','Filmmaker','ActionFilm','AwardWinningFilm','MultiCreditContributor','ThreeCreditContributor','WriterDirector','ActorFilmmaker','AwardWinningFilmmaker','AwardWinningActionFilm','GenreCrossingFilm']
 for name in order:
  c=EX[name];e=g.value(c,OWL.equivalentClass)
  text(x,y,name+'  ('+str(count(c))+')',29,GREEN,True);y+=38
  y=lines(x,y,'≡ '+expr(g,e),81,25,INK,leading=1.32)+26
 text(x,y+12,'some = có ít nhất một quan hệ đến lớp đó',26,TEAL,True)
 text(x,y+52,'value = liên kết đến đúng cá thể vai trò được chỉ ra',25,GRAY)
 text(x,y+92,'min n = ít nhất n cá thể khác nhau; and / or = giao / hợp',25,GRAY)
 # 5. Additional schema axioms, not just named class equivalences.
 x,y=panel(xs[0],2390,CW,1370,'05','RÀNG BUỘC & QUY TẮC SUY LUẬN','Đủ inverse, subproperty, property chain và ràng buộc qualified cardinality')
 headings=[('MỖI CREDIT — 3 RÀNG BUỘC EXACTLY 1',[
 'contributionBy exactly 1 dbo:Person','contributionTo exactly 1 dbo:Film','hasRole exactly 1 ex:ContributionRole']),
 ('INVERSE — CÁC CẶP QUAN HỆ NGƯỢC',[
 'hasContribution ↔ contributionBy','contributionTo ↔ contributionOf','ex:directed ↔ dbo:director','ex:actedIn ↔ dbo:starring','ex:productionOf ↔ dbo:productionCompany']),
 ('SUBPROPERTY & PROPERTY CHAIN',[
 'ex:directed, ex:actedIn ⊑ ex:contributedTo','hasContribution ∘ contributionTo ⊑ contributedTo']),
 ('CREDIT → NGHỀ NGHIỆP (SUY RA MỘT CHIỀU)',[
 'Person + some DirectingContribution → MovieDirector','Person + some WritingContribution → ScreenWriter','Person + some ProducingContribution → Producer','dbo:starring có range dbo:Actor → người được suy ra Actor'])]
 for title,items in headings:
  text(x,y,title,27,TEAL,True);y+=44
  for item in items:y=lines(x+7,y,'• '+item,77,26,leading=1.3)+12
  y+=25
 # 6. Identity, source metadata, annotations, corpus.
 x,y=panel(xs[1],2910,CW,850,'06','IDENTITY, NGUỒN & DỮ LIỆU THỰC','Các predicate chuẩn vẫn có trong dữ liệu, ngoài inventory 19 + 5 bên trên')
 for title,body in [
 ('owl:sameAs — đồng nhất thực thể','Inception local ↔ Wikidata Q25188 ↔ DBpedia Inception. 1.727 liên kết: 1.699 Wikidata + 28 DBpedia.'),
 ('ex:sourceSnapshot / prov:wasDerivedFrom','Liên kết thực thể với phản hồi nguồn. SourceSnapshot lưu URL, thời điểm và SHA-256; nguồn khác với identity.'),
 ('rdfs:label / dct:license / VoID Dataset','Nhãn là annotation; dataset mang metadata và giấy phép CC BY-SA 4.0. rdfs:label không phải datatype property riêng của ex:.'),
 ('CORPUS ĐANG DÙNG','30 phim • 851 người • 1.010 credit • 45 công ty • 75 genre • 672 award entity • 11 quốc gia • 15 ngôn ngữ • 76 phản hồi nguồn.')]:
  text(x,y,title,28,TEAL,True);y=lines(x,y+43,body,77,27)+28
 # 7. One concrete example distinguishes assertions and consequences.
 x,y=panel(xs[2],2315,CW,910,'07','VÍ DỤ: NOLAN & INCEPTION','Ba vai trò của một người trong cùng phim; không phải ba người khác nhau')
 for title,body in [
 ('FACTS ĐẦU VÀO','Nolan → 3 credit trên Inception: DirectorRole, WriterRole, ProducerRole. Inception: releaseYear 2010; runtime 8.880 giây (= 148 phút).'),
 ('LOẠI CREDIT & NGHỀ','Directing / Writing / ProducingContribution → MovieDirector / ScreenWriter / Producer → Filmmaker; Director AND ScreenWriter → WriterDirector.'),
 ('CARDINALITY ĐƯỢC CHỨNG MINH','3 role khác nhau + hasRole functional ⇒ 3 credit không thể là cùng một cá thể ⇒ ThreeCreditContributor và MultiCreditContributor.'),
 ('TRUY VẤN TRƯỚC / SAU','WriterDirector: 0 asserted → 10 reasoned. ASK Nolan thuộc ThreeCreditContributor: false → true. Property chain tạo 965 cặp người–phim local.')]:
  text(x,y,title,27,TEAL,True);y=lines(x,y+41,body,79,26)+27
 x,y=panel(xs[2],3270,CW,490,'08','NGỮ NGHĨA CẦN NHỚ','Giúp đọc sơ đồ đúng, tránh nhầm tính nhất quán với dữ liệu đầy đủ')
 for body in [
 'F = functional: tối đa 1 giá trị. “exactly 1” là ràng buộc OWL; dữ liệu thiếu vẫn cần structural validation riêng.',
 'OWL không mặc định mỗi IRI là một cá thể khác nhau. AllDifferent chỉ áp dụng cho bốn vai trò controlled.',
 'GenreCrossingFilm là membership Action + Drama. Kiểm thử min 2 genre cho 0 thành viên; không thay COUNT DISTINCT cho DL reasoning.']:
  y=lines(x,y,'• '+body,80,25)+22
 # Full-width scope/legend avoids implying a diagram of every one of 19k statements.
 rect(M,3810,W-2*M,465,'#173246')
 text(M+35,3868,'CHÚ GIẢI & PHẠM VI SƠ ĐỒ',34,'#fff',True)
 text(M+35,3928,'dbo: 17 lớp DBpedia     ex: 19 lớp mở rộng     void: 1 lớp Dataset',31,'#BDE7E2',True)
 text(M+35,3980,'Sơ đồ bao phủ toàn bộ schema: 37 lớp có tên, 19 object properties, 5 datatype properties và các tiên đề cốt lõi.',29,'#fff')
 text(M+35,4026,'Cây vẽ subclass khai báo; các quan hệ kế thừa thêm từ equivalentClass được đọc qua khối định nghĩa / reasoner.',28,'#D6E3E8')
 text(M+35,4072,'Số trong ngoặc là member local sau HermiT; các subset có thể chồng lấp. Dữ liệu được tóm tắt bằng số lượng và ví dụ.',28,'#D6E3E8')
 text(M+35,4118,'Full OWL: 19.025 triple • 83 blank node (biểu thức / RDF list) • consistent • 0 named class bất khả thỏa.',28,'#D6E3E8')
 text(M+35,4164,'Ontology: '+BASE+'/ontology',27,'#D6E3E8')
 text(M+35,4210,'Nguồn: Movie_Knowledge_Graph.owl + reasoned.ttl. Đây là sơ đồ tác giả dựng từ OWL, không phải screenshot Protégé.',27,'#D6E3E8')
 text(M,H-55,'File OWL SHA-256: '+hashlib.sha256(path.read_bytes()).hexdigest(),25,GRAY)
 # Embed fonts so SVG and exports are independent of installed font names.
 import base64
 fontroot=Path('/Users/gnexla/Library/Fonts')
 css=''
 for name,weight in [('BeVietnamPro-Regular.ttf',400),('BeVietnamPro-Bold.ttf',700)]:
  encoded=base64.b64encode((fontroot/name).read_bytes()).decode();css+=f"@font-face{{font-family:'Be Vietnam Pro';font-weight:{weight};src:url(data:font/ttf;base64,{encoded}) format('truetype');}}"
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>{css}text{{font-family:"Be Vietnam Pro",sans-serif;}}</style>'+''.join(parts)+'</svg>'
 output=ROOT/'docs/Ontology_toan_bo';output.with_suffix('.svg').write_text(svg)
 with sync_playwright() as p:
  chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');browser=p.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None)
  page=browser.new_page(viewport={'width':W,'height':H},device_scale_factor=1)
  page.set_content('<html><head><style>body{margin:0}svg{display:block}</style></head><body>'+svg+'</body></html>');page.evaluate('document.fonts.ready');page.screenshot(path=str(output.with_suffix('.png')))
  page.pdf(path=str(output.with_suffix('.pdf')),width=str(W)+'px',height=str(H)+'px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
  browser.close()
 report={'canonical_owl_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'classes_covered':len(classes),'object_properties_covered':len(obj),'datatype_properties_covered':len(data),'equivalent_class_definitions_covered':len(definitions),'canvas':[W,H],'scope':'Full named schema and core axioms; corpus counts and a concrete example','artifacts':[str(output.with_suffix(x).relative_to(ROOT)) for x in ['.png','.svg','.pdf']]}
 (ROOT/'evidence/ontology_diagram_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
