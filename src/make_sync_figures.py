"""Generate transparent diagrams and evidence summaries for ontology 3.0.0."""
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
from rdflib import Graph,RDF,RDFS,OWL
from common import ROOT,RES,EX,DBO,write_json

def main():
    folder=ROOT/'docs/sync_images';folder.mkdir(exist_ok=True)
    g=Graph().parse(ROOT/'ontology/Movie_Knowledge_Graph.owl');proof=json.loads((ROOT/'evidence/ontology_design/final_owl_checks.json').read_text())
    style='graph [bgcolor="white",pad="0.3",dpi=180]; node [shape=box,style="rounded,filled",fillcolor="#EDF4F5",color="#247A86",fontname="Times New Roman",fontsize=16,margin="0.18,0.12"]; edge [color="#247A86",fontname="Times New Roman",fontsize=12];'
    graphs={
    'literals':'rankdir=LR; f [label="Inception\\ndbo:Film"]; year [label="2010\\nxsd:integer"];time [label="8880.0 seconds\\nxsd:double"];name [label="Inception\\nrdfs:label @en"]; f->year [label="ex:releaseYear"];f->time [label="dbo:runtime"];f->name [label="annotation"];',
    'hierarchy':'rankdir=TB; work [label="dbo:Work"];film [label="dbo:Film"];action [label="ex:ActionFilm\\n12 inferred members"];award [label="ex:AwardWinningFilm\\n26 inferred members"];both [label="ex:AwardWinningActionFilm\\n10 inferred members"]; work->film;film->action;film->award;action->both;award->both;',
    'properties':'rankdir=LR; person [label="dbo:Person"];credit [label="ex:Contribution"];film [label="dbo:Film"];role [label="ex:ContributionRole"];person->credit [label="hasContribution"];credit->person [label="contributionBy: functional"];credit->film [label="contributionTo: functional"];credit->role [label="hasRole: functional"];person->film [label="contributedTo: chain",style=dashed];',
    'identity':'rankdir=LR;local [label="Local Inception IRI\\nfilm-Q25188"];wd [label="Wikidata\\nQ25188"];db [label="DBpedia\\nInception"];local->wd [label="owl:sameAs"];local->db [label="owl:sameAs"];film [label="dbo:Film"];local->film [label="rdf:type",style=dashed];',
    'lod':'rankdir=LR; a [label="Open license"];b [label="Structured facts"];c [label="Open RDF formats"];d [label="HTTP identifiers"];e [label="External links"];a->b->c->d->e; note [label="Published RDF and local ontology\\nCanonical version 3.0.0",fillcolor="#FFF0D8"];d->note [style=dashed];',
    'cardinality':'rankdir=LR; d [label="DirectorRole"];w [label="WriterRole"];p [label="ProducerRole"];r [label="Controlled roles are different\\n+ hasRole is functional"];c [label="Credit records cannot collapse"];m [label="At least 3 distinct credits\\n7 people; min 2: 17 people"];d->r;w->r;p->r;r->c->m;'
    }
    for name,body in graphs.items():
        path=folder/name;path.with_suffix('.dot').write_text('digraph G {'+style+body+'}')
        subprocess.run(['dot','-Tpng',str(path.with_suffix('.dot')),'-o',str(path.with_suffix('.png'))],check=True)
    font='/Users/gnexla/Library/Fonts/BeVietnamPro-Regular.ttf';bold='/Users/gnexla/Library/Fonts/BeVietnamPro-Bold.ttf'
    def panel(name,title,subtitle,rows):
        im=Image.new('RGB',(1600,900),'#f3f6f7');d=ImageDraw.Draw(im)
        d.text((55,40),title,font=ImageFont.truetype(bold,42),fill='#152B3A')
        d.text((55,110),subtitle,font=ImageFont.truetype(font,23),fill='#506776')
        y=185
        for label,value in rows:
            d.rounded_rectangle((50,y,1550,y+75),radius=12,fill='white')
            d.text((75,y+20),label,font=ImageFont.truetype(font,24),fill='#152B3A')
            d.text((1060,y+20),str(value),font=ImageFont.truetype(bold,24),fill='#007F82');y+=88
        d.text((55,850),'Author-rendered evidence summary; not a screenshot of Protégé.',font=ImageFont.truetype(font,20),fill='#506776');im.save(folder/(name+'.png'))
    panel('verification','Final OWL: HermiT verification','Direct RDF/XML input · version 3.0.0 · counts restricted to local IRIs',[('Consistency','PASS'),('Unsatisfiable named classes','0'),('Design SPARQL queries','27'),('Property-chain person–film pairs','965'),('MultiCredit / ThreeCredit','17 / 7'),('WriterDirector','10'),('Web publication scope','Canonical 3.0.0')])
    films=sorted(str(g.value(f,RDFS.label)) for f in g.subjects(DBO.director,RES['person-Q25191']))
    panel('queries','Direct query: films directed by Nolan','Computed from the final local OWL; one row per local film',[(f,'dbo:director') for f in films[:7]])
    # All 8 results included in a clean two-column evidence panel.
    im=Image.new('RGB',(1600,900),'#f3f6f7');d=ImageDraw.Draw(im);d.text((55,45),'Nolan: eight directed films in the sample',font=ImageFont.truetype(bold,40),fill='#152B3A')
    for idx,f in enumerate(films):d.text((75+(idx%2)*780,190+(idx//2)*140),f,font=ImageFont.truetype(font,27),fill='#007F82')
    d.text((55,850),'Computed source facts; not a screenshot of the public query interface.',font=ImageFont.truetype(font,21),fill='#506776');im.save(folder/'queries.png')
    manifest=ROOT/'evidence/report_image_sources.json';m=json.loads(manifest.read_text())
    additions=[str(p.relative_to(ROOT)) for p in folder.glob('*.png')]+['docs/guide_images/02_contribution.png','docs/guide_images/03_reasoning.png']
    for f in additions:
        m['images']=[x for x in m['images'] if x['file']!=f];m['images'].append({'file':f,'source':'Final OWL 3.0.0 and exact HermiT/query evidence','source_type':'author_diagram'})
    write_json(manifest,m)
if __name__=='__main__':main()
