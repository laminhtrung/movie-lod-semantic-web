"""Render a typeset MovieLOD entity diagram from the canonical OWL, then check layout.

Explicit paths keep reciprocal property labels on separate lanes. This drawing covers
all declared object/datatype properties and the core entities, not every subclass.
"""
import base64
import hashlib
import html
import json
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.collection import Collection
from playwright.sync_api import sync_playwright
from common import ROOT, EX, DBO

W, H = 2800, 3410
INK, MUTED = '#25313D', '#59636E'
parts, boxes, arrows, attributes = [], {}, [], []
source = ROOT/'ontology/Movie_Knowledge_Graph.owl'
g = Graph().parse(source)

def short(uri):
    for prefix, ns in [('dbo', DBO), ('ex', EX)]:
        if str(uri).startswith(str(ns)): return prefix+':'+str(uri)[len(str(ns)):]
    return str(uri).split('#')[-1]

def text(x, y, value, size=28, anchor='middle', weight=400, color=INK):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}">{html.escape(value)}</text>')

def entity(key, uri, cx, cy, width=340, height=110, fields=(), title=None):
    x,y=cx-width/2,cy-height/2
    boxes[key]=(x,y,width,height)
    if uri is not None: assert (uri,RDF.type,OWL.Class) in g, uri
    parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="white" stroke="{INK}" stroke-width="2"/>')
    text(cx,y+40,title or short(uri).split(':')[-1],32,weight=700)
    if uri is not None: text(cx,y+77,short(uri),26,color=MUTED)
    if fields:
        line_y=y+94 if uri is not None else y+57
        parts.append(f'<path d="M {x+18} {line_y} H {x+width-18}" stroke="#A8ADB3" stroke-width="1"/>')
        for i,field in enumerate(fields): text(cx,line_y+36+35*i,field,25,color=INK)

def relation(prop, domain, ran, points, lx, ly, anchor='middle', dashed=False, label=None, exact_one=False):
    if prop is not None:
        assert g.value(prop,RDFS.domain)==domain,(prop,'domain')
        assert g.value(prop,RDFS.range)==ran,(prop,'range')
    arrows.append({'property':str(prop) if prop else 'http://www.w3.org/2000/01/rdf-schema#subClassOf','domain':str(domain) if domain else None,'range':str(ran),'points':points,'label':label or short(prop)})
    d='M '+' L '.join(f'{x} {y}' for x,y in points)
    marker='generalization' if prop is None else 'arrow'
    parts.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2" marker-end="url(#{marker})"'+'/>')
    text(lx,ly,label or short(prop),27,anchor)
    if exact_one:
        x,y=points[-1]; px,py=points[-2]
        if y==py: text(x+(25 if x<px else -25),y-13,'1',24,'start' if x<px else 'end')
        else: text(x-20,y-22 if y>py else y+38,'1',24,'end')

def attr(prop, domain, datatype):
    assert g.value(prop,RDFS.domain)==domain and str(g.value(prop,RDFS.range)).endswith('#'+datatype), prop
    assert (prop,RDF.type,OWL.FunctionalProperty) not in g
    assert not any(g.subjects(OWL.onProperty,prop)), (prop,'cardinality/restriction exists; update notation')
    attributes.append(str(prop))

def section(y, number, title):
    parts.append(f'<path d="M 90 {y} H 2710" stroke="#B4BAC1" stroke-width="1"/>')
    text(90,y+47,number+'  '+title,30,'start',700)

text(90,85,'MovieLOD',48,'start',700)
text(90,132,'Ontology class diagram — UML notation with a complementary RDF view',29,'start',color=MUTED)
text(2710,100,'OWL 3.0.0',27,'end',color=MUTED)
section(170,'A','Contributions and roles')
entity('creditPerson',DBO.Person,300,430)
entity('credit',EX.Contribution,1300,430,400)
entity('creditFilm',DBO.Film,2300,430)
entity('role',EX.ContributionRole,1300,700,570)
# UML Comment: individual names are not class attributes or an enumeration axiom.
parts.append('<path d="M 90 565 H 900 L 925 590 V 775 H 90 Z M 900 565 V 590 H 925" fill="white" stroke="#59636E" stroke-width="1.5"/>')
text(115,603,'OWL individuals of ex:ContributionRole',25,'start',700)
text(115,644,'ex:ActorRole, ex:DirectorRole',25,'start')
text(115,684,'ex:WriterRole, ex:ProducerRole',25,'start')
text(115,727,'{owl:AllDifferent}; not an exhaustive enumeration',24,'start')
parts.append('<path d="M 925 700 H 1015" stroke="#59636E" stroke-width="1.5" stroke-dasharray="8 6"/>')
roles={EX.ActorRole,EX.DirectorRole,EX.WriterRole,EX.ProducerRole}
assert all((role,RDF.type,EX.ContributionRole) in g for role in roles)
assert any(set(Collection(g,g.value(a,OWL.distinctMembers)))==roles for a in g.subjects(RDF.type,OWL.AllDifferent))

relation(EX.hasContribution,DBO.Person,EX.Contribution,[(470,400),(1100,400)],785,381)
relation(EX.contributionBy,EX.Contribution,DBO.Person,[(1100,460),(470,460)],785,501,label='ex:contributionBy',exact_one=True)
relation(EX.contributionTo,EX.Contribution,DBO.Film,[(1500,400),(2130,400)],1815,381,label='ex:contributionTo',exact_one=True)
relation(EX.contributionOf,DBO.Film,EX.Contribution,[(2130,460),(1500,460)],1815,501)
relation(EX.hasRole,EX.Contribution,EX.ContributionRole,[(1300,485),(1300,645)],1360,563,anchor='start',label='ex:hasRole',exact_one=True)
relation(EX.contributedTo,DBO.Person,DBO.Film,[(300,375),(300,285),(2300,285),(2300,375)],1300,267)
section(820,'B','Films, people and production')
entity('person',DBO.Person,300,970)
entity('film',DBO.Film,300,1270,440,180,fields=('ex:releaseYear : xsd:integer [0..*]',))
entity('work',DBO.Work,1300,1270,520,180,fields=('dbo:runtime : xsd:double [0..*]',))
entity('actor',DBO.Actor,2400,970)
entity('company',DBO.Company,2400,1270,420)
entity('agent',DBO.Agent,2400,1560)
relation(DBO.director,DBO.Film,DBO.Person,[(245,1180),(245,1025)],215,1110,'end')
relation(EX.directed,DBO.Person,DBO.Film,[(355,1025),(355,1180)],385,1110,'start')
assert (DBO.Film,RDFS.subClassOf,DBO.Work) in g
relation(None,DBO.Film,DBO.Work,[(520,1270),(1040,1270)],780,1245,dashed=True,label='rdfs:subClassOf')
relation(DBO.writer,DBO.Work,DBO.Person,[(1160,1180),(1160,970),(470,970)],815,946)
relation(DBO.starring,DBO.Work,DBO.Actor,[(1440,1180),(1440,970),(2230,970)],1840,946)
# Crossings denote no junction; a white underlay keeps the Actor-to-Film path legible.
parts.append('<path d="M 2400 1025 L 2400 1120 L 640 1120 L 640 1230 L 520 1230" fill="none" stroke="white" stroke-width="10"/>')
relation(EX.actedIn,DBO.Actor,DBO.Film,[(2400,1025),(2400,1120),(640,1120),(640,1230),(520,1230)],1840,1096)
relation(DBO.productionCompany,DBO.Work,DBO.Company,[(1560,1240),(2190,1240)],1875,1215)
relation(EX.productionOf,DBO.Company,DBO.Work,[(2190,1300),(1560,1300)],1875,1344)
relation(DBO.producer,DBO.Work,DBO.Agent,[(1440,1360),(1440,1560),(2230,1560)],1850,1536)
attr(EX.releaseYear,DBO.Film,'integer');attr(DBO.runtime,DBO.Work,'double')
for prop in [EX.contributionBy, EX.contributionTo, EX.hasRole]:
    assert any(g.value(r,OWL.onProperty)==prop and int(g.value(r,OWL.qualifiedCardinality) or 0)==1 for r in g.objects(EX.Contribution,RDFS.subClassOf)), prop
section(1700,'C','OWL range view — properties without a domain axiom')
# An RDF placeholder, not a new class in the ontology or a UML class box.
boxes['resource']=(115,2017.5,570,165)
parts.append('<ellipse cx="400" cy="2100" rx="285" ry="82.5" fill="white" stroke="#25313D" stroke-width="2"/>')
text(400,2087,'Unspecified subject',30,weight=700)
text(400,2130,'No domain axiom',26,color=MUTED)

for key,cls,y in [('genre',DBO.Genre,1850),('award',DBO.Award,2000),('country',DBO.Country,2150),('language',DBO.Language,2300)]:
    entity(key,cls,2300,y,420)
entity('snapshot',EX.SourceSnapshot,2300,2545,680,245,fields=('ex:sourceUrl : xsd:anyURI [0..*]','ex:retrievedAt : xsd:dateTime [0..*]','ex:sha256 : xsd:string [0..*]'))
for p,cls,y,sy in [(DBO.genre,DBO.Genre,1850,2050),(DBO.award,DBO.Award,2000,2075),(DBO.country,DBO.Country,2150,2100),(DBO.language,DBO.Language,2300,2125),(EX.sourceSnapshot,EX.SourceSnapshot,2545,2150)]:
    end=1960 if cls==EX.SourceSnapshot else 2090
    relation(p,None,cls,[(400+285*(1-((sy-2100)/82.5)**2)**0.5,sy),(1100,y),(end,y)],1510,y-22)
# owl:sameAs is standard identity linking already present in the corpus.
assert any(g.triples((None,OWL.sameAs,None)))
# A separate RDF instance view prevents schema links being mistaken for assertions.
section(2740,'D','RDF identity links — Inception example')
subject=URIRef(str(EX).split('/ontology#')[0]+'/resource/film-Q25188')
external=[URIRef('http://dbpedia.org/resource/Inception'),URIRef('http://www.wikidata.org/entity/Q25188')]
assert all((subject,OWL.sameAs,obj) in g for obj in external)
boxes['identityFilm']=(110,2990,680,100)
parts.append('<rect x="110" y="2990" width="680" height="100" fill="white" stroke="#25313D" stroke-width="2"/>')
parts.append('<text x="450" y="3050" font-size="28" text-anchor="middle" text-decoration="underline" fill="#25313D">res:film-Q25188 : dbo:Film</text>')
for key,y,iri in [('dbpediaIRI',2940,external[0]),('wikidataIRI',3130,external[1])]:
    boxes[key]=(1800,y-50,800,100)
    parts.append(f'<ellipse cx="2200" cy="{y}" rx="400" ry="50" fill="white" stroke="#25313D" stroke-width="2"/>')
    text(2200,y+9,str(iri),27)
relation(OWL.sameAs,None,None,[(790,3020),(1200,2940),(1800,2940)],1490,2918,label='owl:sameAs')
relation(OWL.sameAs,None,None,[(790,3060),(1200,3130),(1800,3130)],1490,3108,label='owl:sameAs')
for p,t in [(EX.sourceUrl,'anyURI'),(EX.retrievedAt,'dateTime'),(EX.sha256,'string')]:attr(p,EX.SourceSnapshot,t)
parts.append('<path d="M 90 3260 H 2710" stroke="#B4BAC1" stroke-width="1"/>')
text(90,3305,'Open arrow: object property   ·   Hollow triangle: generalization   ·   Multiplicity 1: exactly one target',25,'start')
text(90,3345,'Omitted association multiplicities are unspecified. [0..*]: no datatype cardinality axiom. runtime is in seconds.',25,'start',color=MUTED)
text(90,3383,'Repeated names denote the same class. Core class view only; C: schema range view. D: instance links; no extra classes.',25,'start',color=MUTED)
assert {r['property'] for r in arrows if r['property'] not in [str(RDFS.subClassOf),str(OWL.sameAs)]} == {str(p) for p in g.subjects(RDF.type,OWL.ObjectProperty)}
assert set(attributes)=={str(p) for p in g.subjects(RDF.type,OWL.DatatypeProperty)}
# Detect paths entering unrelated boxes (using strict interiors).
def enters_box(a,b,box):
    x,y,w,h=box; low,high=0.0,1.0
    for start,end,mn,mx in [(a[0],b[0],x+1,x+w-1),(a[1],b[1],y+1,y+h-1)]:
        delta=end-start
        if delta==0:
            if not mn<start<mx: return False
        else:
            t0,t1=sorted(((mn-start)/delta,(mx-start)/delta))
            low=max(low,t0);high=min(high,t1)
            if low>=high:return False
    return low<high
path_box_overlaps=[]
for arrow in arrows:
    for a,b in zip(arrow['points'],arrow['points'][1:]):
        for key,box in boxes.items():
            if key=='resource' and a==arrow['points'][0] and arrow['domain'] is None and arrow['property']!=str(OWL.sameAs):continue
            if enters_box(a,b,box):path_box_overlaps.append([arrow['label'],key])
assert not path_box_overlaps,path_box_overlaps

font=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
encoded=base64.b64encode(font.read_bytes()).decode()
bold=base64.b64encode(Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf').read_bytes()).decode()
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>@font-face{{font-family:DiagramArial;font-weight:400;src:url(data:font/ttf;base64,{encoded})}}@font-face{{font-family:DiagramArial;font-weight:700;src:url(data:font/ttf;base64,{bold})}}text{{font-family:DiagramArial,Arial,sans-serif}}</style><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="{INK}" stroke-width="1.2"/></marker><marker id="generalization" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="14" markerHeight="14" orient="auto"><path d="M 1 1 L 11 6 L 1 11 z" fill="white" stroke="{INK}" stroke-width="1"/></marker></defs><rect width="100%" height="100%" fill="white"/>'''+''.join(parts)+'</svg>'
out=ROOT/'docs/MovieLOD_entity_diagram'
out.with_suffix('.svg').write_text(svg)
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page=browser.new_page(viewport={'width':W,'height':H},device_scale_factor=1)
    page.set_content('<html><head><style>body{margin:0}svg{display:block}</style></head><body>'+svg+'</body></html>')
    page.evaluate('document.fonts.ready')
    text_bounds=page.evaluate('''() => [...document.querySelectorAll('text')].map(e=>{const b=e.getBoundingClientRect();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height}})''')
    clipped=[b for b in text_bounds if b['x']<0 or b['y']<0 or b['x']+b['w']>W or b['y']+b['h']>H]
    overlaps=[]
    for i,a in enumerate(text_bounds):
        for b in text_bounds[i+1:]:
            if min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])>2 and min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])>2:
                overlaps.append([a['text'],b['text']])
    # Relationship labels must not sit on any entity box.
    label_names={a['label'] for a in arrows}
    label_box_overlaps=[]
    for b in text_bounds:
        if b['text'] not in label_names: continue
        for key,(x,y,w,h) in boxes.items():
            if min(b['x']+b['w'],x+w)-max(b['x'],x)>1 and min(b['y']+b['h'],y+h)-max(b['y'],y)>1:
                label_box_overlaps.append([b['text'],key])
    label_edge_overlaps=[]
    for b in text_bounds:
        if b['text'] not in label_names:continue
        label_box=(b['x']-2,b['y']-2,b['w']+4,b['h']+4)
        for arrow in arrows:
            if any(enters_box(a,c,label_box) for a,c in zip(arrow['points'],arrow['points'][1:])):
                label_edge_overlaps.append([b['text'],arrow['label']])
    node_text_overflow=[]
    for b in text_bounds:
        cx=b['x']+b['w']/2;cy=b['y']+b['h']/2
        for key,(x,y,w,h) in boxes.items():
            if x<cx<x+w and y<cy<y+h and not (x+3<=b['x'] and y+3<=b['y'] and b['x']+b['w']<=x+w-3 and b['y']+b['h']<=y+h-3):
                node_text_overflow.append([b['text'],key])
    assert not node_text_overflow,node_text_overflow
    assert not label_edge_overlaps,label_edge_overlaps
    assert not label_box_overlaps,label_box_overlaps
    assert not clipped,clipped
    assert not overlaps,overlaps
    page.screenshot(path=str(out.with_suffix('.png')))
    page.pdf(path=str(out.with_suffix('.pdf')),width=f'{W}px',height=f'{H}px',print_background=True,margin={k:'0' for k in ['top','bottom','left','right']})
    browser.close()
report={'owl_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'object_properties_checked':19,'datatype_properties_checked':5,'domain_range_matches_owl':True,'all_arrows_labelled':True,'text_clipping':clipped,'node_text_overflow':node_text_overflow,'text_overlaps':overlaps,'relationship_label_box_overlaps':label_box_overlaps,'arrow_box_overlaps':path_box_overlaps,'relationship_label_edge_overlaps':label_edge_overlaps,'canvas':[W,H],'scope':'Core classes in UML notation; complementary OWL range and RDF instance view; subclass taxonomy omitted','notation_reference':'OMG UML 2.5.1 sections 9.2.4, 9.8.4, 11.5.4','uml_generalization_solid_hollow_triangle':True,'uml_association_open_arrow':True,'owl_role_individuals_not_attributes':True,'all_different_verified':True,'identity_example_triples_verified':2,'qualified_cardinality_checked':True,'datatype_multiplicities_unrestricted_verified':True,'standard_identity_link_checked':True,'font_embedded':font.name,'visual_review':'pending'}
(ROOT/'evidence/entity_diagram_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
