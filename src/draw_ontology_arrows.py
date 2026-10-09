"""One node-and-arrow drawing of the named OWL schema, with every edge labelled."""
import hashlib,json,subprocess,tempfile,textwrap,html,xml.etree.ElementTree as ET,base64
from pathlib import Path
from rdflib import Graph,RDF,RDFS,OWL,URIRef
from playwright.sync_api import sync_playwright
from common import ROOT,EX,DBO,BASE
from draw_full_ontology import short,expr
ET.register_namespace('', 'http://www.w3.org/2000/svg')

def quoted(s):return '"'+str(s).replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'

def main():
 source=ROOT/'ontology/Movie_Knowledge_Graph.owl';g=Graph().parse(source)
 classes=sorted({c for c in g.subjects(RDF.type,OWL.Class) if isinstance(c,URIRef)},key=str)
 props=set(g.subjects(RDF.type,OWL.ObjectProperty));data=set(g.subjects(RDF.type,OWL.DatatypeProperty));covered=set();covered_data=set()
 width,height=6000,4250;gap=45;col=(width-140-2*gap)/3;parts=[]
 def render(name,dot,x,y,w,h):
  with tempfile.TemporaryDirectory(prefix='owl-map-') as tmp:
   p=Path(tmp)/'graph.dot';out=p.with_suffix('.svg');p.write_text(dot);subprocess.run(['dot','-Tsvg',str(p),'-o',str(out)],check=True)
   root=ET.fromstring(out.read_text());root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h));root.set('preserveAspectRatio','xMidYMid meet');parts.append(ET.tostring(root,encoding='unicode'))
 def header():return 'digraph G {graph[bgcolor="transparent",pad=".25",nodesep=".42",ranksep=".7",splines=spline,outputorder=edgesfirst];node[shape=box,style="rounded,filled",fillcolor="#E3F1ED",color="#498574",fontname="Be Vietnam Pro",fontsize=21,margin=".15,.10",penwidth=1.5];edge[fontname="Be Vietnam Pro",fontsize=18,arrowsize=.85,penwidth=1.6,color="#007F82",fontcolor="#005F63"];'
 def frame(x,y,w,h,title):
  parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="#F7FAFC" stroke="#DDE7EC" stroke-width="2"/><text x="{x+30}" y="{y+58}" font-size="38" font-weight="700" fill="#173246">{html.escape(title)}</text>')
 def node(c,label=None):return quoted(short(c))+' [label='+quoted(label or short(c))+',fillcolor="'+('#DFEBF8' if str(c).startswith(str(DBO)) else '#E3F1ED')+'"];'
 def edge(p):
  domain=g.value(p,RDFS.domain);ran=g.value(p,RDFS.range);a=quoted(short(domain)) if domain is not None else 'subject';b=quoted(short(ran))
  label=short(p)
  if (p,RDF.type,OWL.FunctionalProperty) in g:label+='\n[functional; exactly 1]'
  if p==EX.contributedTo:label+='\n[hasContribution ∘ contributionTo]'
  if p in [EX.directed,EX.actedIn]:label+='\n[subPropertyOf contributedTo]'
  covered.add(p);return f'{a} -> {b} [label={quoted(label)}];'
 # Three close-up regions of one drawing: no crossing from unrelated relationships.
 x,y=70,200;frame(x,y,col,1600,'ĐÓNG GÓP & VAI TRÒ')
 dot=header()+'rankdir=LR;'
 for c in [DBO.Person,EX.Contribution,DBO.Film,EX.ContributionRole]:dot+=node(c)
 for p in [EX.hasContribution,EX.contributionBy,EX.contributionTo,EX.contributionOf,EX.hasRole,EX.contributedTo]:dot+=edge(p)
 dot+='roles [label="ex:ActorRole\\nex:DirectorRole\\nex:WriterRole\\nex:ProducerRole\\n(AllDifferent: 4 cá thể khác nhau)",shape=ellipse,fillcolor="#FFF0D0",color="#B78C39"];roles -> '+quoted(short(EX.ContributionRole))+' [label="rdf:type\\n(là cá thể của)",color="#AD7820",fontcolor="#946117",style=dotted];}'
 render('credits',dot,x+25,y+95,col-50,1455)
 x=70+col+gap;frame(x,y,col,1600,'PHIM, NGƯỜI & CÔNG TY')
 dot=header()+'rankdir=LR;'
 for c in [DBO.Film,DBO.Work,DBO.Person,DBO.Actor,DBO.Agent,DBO.Company]:dot+=node(c)
 for p in [DBO.director,DBO.starring,DBO.writer,DBO.producer,DBO.productionCompany,EX.directed,EX.actedIn,EX.productionOf]:dot+=edge(p)
 dot+=quoted(short(DBO.Film))+' -> '+quoted(short(DBO.Work))+' [label="rdfs:subClassOf",style=dashed,color="#8090A5",fontcolor="#68788B"];'
 for p in [DBO.runtime,EX.releaseYear]:
  ran=g.value(p,RDFS.range);domain=g.value(p,RDFS.domain);dot+=quoted(short(ran))+' [shape=note,fillcolor="#FFF0D0",color="#B78C39"];';dot+=quoted(short(domain))+' -> '+quoted(short(ran))+' [label='+quoted(short(p)+(' (giây)' if p==DBO.runtime else ''))+',color="#AD7820",fontcolor="#946117"];';covered_data.add(p)
 dot+='}';render('films',dot,x+25,y+95,col-50,1455)
 x=70+2*(col+gap);frame(x,y,col,1600,'THỂ LOẠI, NGUỒN & GIÁ TRỊ')
 dot=header()+'rankdir=LR;subject [label="Chủ thể sử dụng property\\n(domain không khai báo)",fillcolor="#F0F2F5",color="#9CA7B5",style="rounded,dashed,filled"];'
 for c in [DBO.Genre,DBO.Award,DBO.Country,DBO.Language,EX.SourceSnapshot]:dot+=node(c)
 for p in [DBO.genre,DBO.award,DBO.country,DBO.language,EX.sourceSnapshot]:dot+=edge(p)
 for p in [EX.sourceUrl,EX.retrievedAt,EX.sha256]:
  ran=g.value(p,RDFS.range);dot+=quoted(short(ran))+' [shape=note,fillcolor="#FFF0D0",color="#B78C39"];';dot+=quoted(short(EX.SourceSnapshot))+' -> '+quoted(short(ran))+' [label='+quoted(short(p))+',color="#AD7820",fontcolor="#946117"];';covered_data.add(p)
 dot+='}';render('source',dot,x+25,y+95,col-50,1455)
 # Named hierarchy uses three adjacent branches inside the same picture.
 def under(c,root):return root in set(g.transitive_objects(c,RDFS.subClassOf))
 people=[c for c in classes if under(c,DBO.Agent)]
 filmgenres=[c for c in classes if under(c,DBO.Work) or under(c,DBO.Genre)]
 other=[c for c in classes if c not in people and c not in filmgenres]
 assert len(set(people+filmgenres+other))==37
 for i,(group,title) in enumerate([(people,'KẾ THỪA: NGƯỜI & TỔ CHỨC'),(filmgenres,'KẾ THỪA: PHIM & THỂ LOẠI'),(other,'KẾ THỪA: CREDIT & CÁC LỚP KHÁC')]):
  x,y=70+i*(col+gap),1870;frame(x,y,col,2180,title)
  dot=header()+'rankdir=LR;graph[nodesep=".25",ranksep=".8"];node[fontsize=24];edge[fontsize=19];'
  for c in group:dot+=node(c)
  for c in group:
   for parent in g.objects(c,RDFS.subClassOf):
    if parent in group:dot+=quoted(short(c))+' -> '+quoted(short(parent))+' [label="rdfs:subClassOf\\n(là lớp con của)",style=dashed,color="#8090A5",fontcolor="#68788B"];'
  dot+='}';render('hierarchy'+str(i),dot,x+25,y+90,col-50,2040)
 assert covered==props,(covered,props)
 assert covered_data==data
 css=''
 for f,weight in [('BeVietnamPro-Regular.ttf',400),('BeVietnamPro-Bold.ttf',700)]:
  b=base64.b64encode((Path('/Users/gnexla/Library/Fonts')/f).read_bytes()).decode();css+=f"@font-face{{font-family:'Be Vietnam Pro';font-weight:{weight};src:url(data:font/ttf;base64,{b})}}"
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><style>{css}text{{font-family:"Be Vietnam Pro",sans-serif}}</style><rect width="100%" height="100%" fill="white"/><text x="70" y="75" font-size="57" font-weight="700" fill="#173246">MOVIELOD — SƠ ĐỒ LỚP VÀ QUAN HỆ TRONG OWL</text><text x="70" y="137" font-size="31" fill="#526979">Xanh: object property • vàng: datatype / cá thể • nét đứt: kế thừa • các ô cùng tên ở các vùng là cùng một lớp</text>'+''.join(parts)+f'<text x="70" y="4150" font-size="30" fill="#526979">37 lớp • 19 object properties • 5 datatype properties • đọc trực tiếp từ Movie_Knowledge_Graph.owl 3.0.0</text></svg>'
 p=ROOT/'docs/Ontology_quan_he';p.with_suffix('.svg').write_text(svg)
 with sync_playwright() as pw:
  chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');browser=pw.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None);page=browser.new_page(viewport={'width':width,'height':height});page.set_content('<html><head><style>body{margin:0}svg{display:block}</style></head><body>'+svg+'</body></html>');page.evaluate('document.fonts.ready');page.screenshot(path=str(p.with_suffix('.png')));page.pdf(path=str(p.with_suffix('.pdf')),width=str(width)+'px',height=str(height)+'px',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'});browser.close()
 check={'classes':len(classes),'labelled_object_property_arrows':len(covered),'labelled_datatype_arrows':len(covered_data),'owl_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'canvas':[width,height],'all_relation_arrows_labelled':True,'style':'One node-and-arrow drawing, no prose tables'}
 (ROOT/'evidence/ontology_arrow_diagram_checks.json').write_text(json.dumps(check,indent=2)+'\n');print(check)
if __name__=='__main__':main()
