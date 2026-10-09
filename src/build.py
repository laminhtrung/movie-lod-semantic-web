"""Build a richer OWL model, normalize collected claims, and publish static RDF pages."""
import csv
import hashlib
import html
import json
from decimal import Decimal, InvalidOperation
from datetime import datetime
from pathlib import Path
from rdflib import Graph, URIRef, Literal, BNode, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from common import ROOT, CONFIG, BASE, EX, RES, DBO, PROV, VOID, DCT, write_json, prefix_html_links
from collect import claim_ids

def graph():
    g = Graph()
    for name, ns in [('ex', EX), ('res',RES),('dbo',DBO),('prov',PROV),('void',VOID),('dct',DCT),('owl',OWL),('rdfs',RDFS),('xsd',XSD)]:
        g.bind(name, ns)
    return g

def timestamp_literal(value):
    """Use milliseconds consistently; legacy HermiT rejects six fractional digits."""
    lexical = datetime.fromisoformat(value.replace('Z', '+00:00')).isoformat(timespec='milliseconds')
    return Literal(lexical, datatype=XSD.dateTime, normalize=False)

# Only supported author genre buckets are asserted; all vocabulary is version 3.
GENRE_KEYWORDS=[('action',EX.ActionGenre),('drama',EX.DramaGenre)]
def classify_genre(label):
    return [iri for key,iri in GENRE_KEYWORDS if key in label.lower()]

def schema():
    from ontology_design import build_design
    return build_design(original=Graph(),persist=False)[0]

def preferred_values(entity,prop):
    claims = [c for c in entity.get('claims',{}).get(prop,[]) if c.get('rank')!='deprecated']
    preferred=[c for c in claims if c.get('rank')=='preferred']
    return [c['mainsnak']['datavalue']['value'] for c in (preferred or claims) if 'datavalue' in c.get('mainsnak',{})]

def build():
    source=json.loads((ROOT/'data/processed/collected.json').read_text())
    snapshots=json.loads((ROOT/'data/raw/snapshots.json').read_text())
    entities=source['entities']; sg=schema(); g=graph()
    for role in [EX.DirectorRole,EX.ActorRole,EX.WriterRole,EX.ProducerRole]:
        for t in sg.triples((role,None,None)):g.add(t)
    snapshot_iris={}
    for snap in snapshots:
        s=RES['source-'+snap['sha256'][:24]];snapshot_iris[snap['url']]=s
        g.add((s,RDF.type,EX.SourceSnapshot));g.add((s,EX.sourceUrl,Literal(snap['url'],datatype=XSD.anyURI)))
        g.add((s,EX.retrievedAt,timestamp_literal(snap['retrieved_at'])))
        g.add((s,EX.sha256,Literal(snap['sha256'])));g.add((s,PROV.wasDerivedFrom,URIRef(snap['url'])))
        g.add((s,RDFS.label,Literal(snap['provider']+' source snapshot')))
    links, records, issues=[],[],[]
    def add_link(local,external,method):
        g.add((local,OWL.sameAs,URIRef(external)))
        links.append({'local':str(local),'external':external,'method':method})
    def add_entity(qid,kind):
        entity=entities.get(qid)
        if not entity or not entity.get('labels',{}).get('en'):
            issues.append({'entity':qid,'reason':'missing English label; omitted'})
            return None
        if kind=='person' and 'Q5' not in claim_ids(entity,'P31'):
            issues.append({'entity':qid,'reason':'not explicitly a human; omitted from Person'})
            return None
        local=RES[kind+'-'+qid]
        typ={'person':DBO.Person,'genre':DBO.MovieGenre,'country':DBO.Country,'language':DBO.Language,
             'company':DBO.Company,'award':DBO.Award}[kind]
        label=entity['labels']['en']['value']
        g.add((local,RDF.type,typ));g.add((local,RDFS.label,Literal(label,lang='en')))
        if kind=='genre':
            for extra in classify_genre(label):g.add((local,RDF.type,extra))
        add_link(local,'http://www.wikidata.org/entity/'+qid,'exact Wikidata QID from source claim')
        if entity.get('_snapshot_url'):
            g.add((local,EX.sourceSnapshot,snapshot_iris[entity['_snapshot_url']]))
        return local
    for film in source['films']:
        entity=entities[film['qid']];local=RES['film-'+film['qid']]
        title=entity.get('labels',{}).get('en',{}).get('value',film['wiki_title'])
        g.add((local,RDF.type,DBO.Film));g.add((local,RDFS.label,Literal(title,lang='en')))
        sn=snapshot_iris[film['wikidata_snapshot']];g.add((local,EX.sourceSnapshot,sn))
        g.add((local,PROV.wasDerivedFrom,URIRef('https://www.wikidata.org/wiki/'+film['qid'])))
        add_link(local,'http://www.wikidata.org/entity/'+film['qid'],'exact enwiki sitelink: '+film['wiki_title'])
        if film.get('dbpedia_uri'):
            add_link(local,film['dbpedia_uri'],'same enwiki title + DBpedia root rdf:type dbo:Film')
            g.add((local,EX.sourceSnapshot,snapshot_iris[film['dbpedia_snapshot']]))
        years=[]
        for value in preferred_values(entity,'P577'):
            if isinstance(value,dict) and value.get('time','').startswith('+') and value.get('precision',0)>=9 and value.get('calendarmodel','').endswith('Q1985727'):
                year=int(value['time'][1:5])
                if 1888<=year<=2100:years.append(year)
        year=min(years) if years else None
        if year:g.add((local,EX.releaseYear,Literal(year,datatype=XSD.integer)))
        minutes=[]
        for value in preferred_values(entity,'P2047'):
            if not isinstance(value,dict):continue
            try:
                amount=Decimal(value['amount']);unit=value.get('unit','')
                if unit.endswith('/Q7727'):m=amount
                elif unit.endswith('/Q11574'):m=amount/60
                elif unit.endswith('/Q25235'):m=amount*60
                else:continue
                if 0<m<1000:minutes.append(m)
            except (InvalidOperation,KeyError):continue
        runtime=minutes[0] if minutes else None
        if len(set(minutes))>1:issues.append({'film':title,'reason':'multiple runtimes; first non-deprecated/preferred claim retained','values':[str(m) for m in minutes]})
        if runtime is not None:
            g.add((local,DBO.runtime,Literal(float(runtime*60),datatype=XSD.double)))
        for prop,kind,pred in [('P136','genre',DBO.genre),('P495','country',DBO.country),('P364','language',DBO.language),
                                ('P166','award',DBO.award),('P272','company',DBO.productionCompany)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,kind)
                if target:g.add((local,pred,target))
        people={'director':[],'actor':[],'writer':[],'producer':[]}
        for prop,kind,pred,role in [('P57','director',DBO.director,EX.DirectorRole),('P161','actor',DBO.starring,EX.ActorRole),
                                     ('P58','writer',DBO.writer,EX.WriterRole),('P162','producer',DBO.producer,EX.ProducerRole)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,'person')
                if not target:continue
                contribution=RES['contribution-'+film['qid']+'-'+qid+'-'+kind]
                for triple in [(local,pred,target),(local,EX.contributionOf,contribution),(contribution,RDF.type,EX.Contribution),
                               (contribution,EX.contributionTo,local),(contribution,EX.contributionBy,target),
                               (contribution,EX.hasRole,role),(target,EX.hasContribution,contribution),
                               (contribution,EX.sourceSnapshot,sn)]:g.add(triple)
                g.add((contribution,RDFS.label,Literal(title+' — '+kind+' — '+entities[qid]['labels']['en']['value'])))
                for award_qid in claim_ids(entities[qid],'P166'):
                    award_target=add_entity(award_qid,'award')
                    if award_target:g.add((target,DBO.award,award_target))
                people[kind].append({'name':entities[qid]['labels']['en']['value'],'uri':str(target)})
        records.append({'uri':str(local),'qid':film['qid'],'title':title,'year':year,'runtime_minutes':float(runtime) if runtime is not None else None, **people})
    dataset=URIRef(BASE+'/dataset')
    for triple in [(dataset,RDF.type,VOID.Dataset),(dataset,RDF.type,VOID.Dataset),(dataset,DCT.title,Literal('MovieLOD course dataset')),
                   (dataset,DCT.license,URIRef(CONFIG['data_license'])),(dataset,DCT.source,URIRef('https://www.wikidata.org/')),
                   (dataset,DCT.source,URIRef('https://dbpedia.org/')),(dataset,VOID.dataDump,URIRef(BASE+'/data/movies.ttl')),
                   (dataset,RDFS.seeAlso,URIRef(BASE+'/#query'))]:g.add(triple)
    (ROOT/'ontology').mkdir(exist_ok=True)
    sg.serialize(ROOT/'ontology/movie.ttl',format='turtle');sg.serialize(ROOT/'ontology/Movie_Ontology.owl',format='xml')
    g.serialize(ROOT/'data/processed/movies.ttl',format='turtle');g.serialize(ROOT/'data/processed/movies.jsonld',format='json-ld')
    combined=g+sg;combined.serialize(ROOT/'ontology/Movie_Knowledge_Graph.owl',format='xml')
    # Remove repeated audit rows for reused people/terms.
    links=list({(x['local'],x['external']):x for x in links}.values())
    write_json(ROOT/'evidence/link_audit.json',sorted(links,key=lambda x:(x['local'],x['external'])))
    write_json(ROOT/'evidence/quality_issues.json',issues)
    with (ROOT/'data/processed/films.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['qid','title','year','runtime_minutes','directors'])
        writer.writeheader()
        for r in records:writer.writerow({k:r.get(k) for k in ['qid','title','year','runtime_minutes']}|{'directors':'; '.join(x['name'] for x in r['director'])})
    stats={'films':len(records),'persons':len(set(g.subjects(RDF.type,DBO.Person))), 'contributions':len(set(g.subjects(RDF.type,EX.Contribution))),
           'genres':len(set(g.subjects(RDF.type,DBO.MovieGenre))),'countries':len(set(g.subjects(RDF.type,DBO.Country))),
           'languages':len(set(g.subjects(RDF.type,DBO.Language))),'production_companies':len(set(g.subjects(RDF.type,DBO.Company))),
           'awards':len(set(g.subjects(RDF.type,DBO.Award))),'snapshots':len(snapshots),'data_triples':len(g),'schema_triples':len(sg),'combined_triples':len(g+sg),'ontology_version':'3.0.0',
           'classes':len({c for c in sg.subjects(RDF.type,OWL.Class) if isinstance(c, URIRef)}),
           'reused_dbpedia_classes':['http://dbpedia.org/ontology/'+name for name in ['Work','Film','Agent','Person','Artist','Actor','Writer','MovieDirector','ScreenWriter','Producer','Organisation','Company','Genre','MovieGenre','Award','Country','Language']],
           'same_as':len(links),'dbpedia_links':sum('dbpedia.org' in x['external'] for x in links),
           'wikidata_links':sum('wikidata.org' in x['external'] for x in links),
           'with_year':sum(r['year'] is not None for r in records),'with_runtime':sum(r['runtime_minutes'] is not None for r in records),
           'with_director':sum(bool(r['director']) for r in records),'base_url':BASE}
    write_json(ROOT/'evidence/statistics.json',stats)
    export_static(g,sg,records,stats)
    print(json.dumps(stats,ensure_ascii=False,indent=2))

def export_static(g,sg,records,stats):
    import shutil
    dist=ROOT/'web/dist';data=dist/'data';data.mkdir(parents=True,exist_ok=True)
    for name in ['movies.ttl','movies.jsonld','films.csv']:
        shutil.copy2(ROOT/'data/processed'/name,data/name)
    shutil.copy2(ROOT/'ontology/movie.ttl',dist/'ontology.ttl')
    shutil.copy2(ROOT/'ontology/Movie_Ontology.owl',dist/'Movie_Ontology.owl')
    shutil.copy2(ROOT/'ontology/Movie_Knowledge_Graph.owl',dist/'Movie_Knowledge_Graph.owl')
    write_json(data/'films.json',sorted(records,key=lambda x:x['title']))
    write_json(data/'statistics.json',stats)
    for s in set(g.subjects()):
        if isinstance(s,URIRef) and str(s).startswith(str(RES)):
            render_resource(g,s,dist/'resource'/str(s).removeprefix(str(RES)))
    render_resource(g,URIRef(BASE+'/dataset'),dist/'dataset')
    render_resource(sg,URIRef(BASE+'/ontology'),dist/'ontology',include_all=True)
    (dist/'_headers').write_text('/data/*\n  Access-Control-Allow-Origin: *\n/ontology.ttl\n  Content-Type: text/turtle; charset=utf-8\n/data/movies.ttl\n  Content-Type: text/turtle; charset=utf-8\n/resource/*/index.ttl\n  Content-Type: text/turtle; charset=utf-8\n',encoding='utf-8')

def render_resource(g,s,directory,include_all=False):
    directory.mkdir(parents=True,exist_ok=True)
    sub=g if include_all else graph()
    if not include_all:
        for triple in g.triples((s,None,None)):sub.add(triple)
    sub.serialize(directory/'index.ttl',format='turtle')
    label=str(g.value(s,RDFS.label) or g.value(s,DCT.title) or str(s).rsplit('/',1)[-1])
    def display(term):
        text=str(term);name=text.rsplit('#',1)[-1].rsplit('/',1)[-1]
        if isinstance(term,URIRef):
            href=text
            if text.startswith(BASE):href=text[len(BASE):] or '/'
            return '<a href="'+html.escape(href,quote=True)+'">'+html.escape(str(g.value(term,RDFS.label) or name))+'</a>'
        return html.escape(text)
    rows=''.join('<tr><td>'+display(p)+'</td><td>'+display(o)+'</td></tr>' for p,o in sorted(g.predicate_objects(s),key=lambda x:(str(x[0]),str(x[1]))))
    extra=''
    if include_all:
        for subject in sorted(set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,EX.ContributionRole)),key=str):
            anchor=str(subject).split('#')[-1].rsplit('/',1)[-1]
            label2=str(g.value(subject,RDFS.label) or anchor)
            properties=''.join('<tr><td>'+display(p)+'</td><td>'+display(o)+'</td></tr>' for p,o in sorted(g.predicate_objects(subject),key=lambda x:(str(x[0]),str(x[1]))))
            extra+='<section id="'+html.escape(anchor,quote=True)+'"><h2>'+html.escape(anchor+' — '+label2)+'</h2><table>'+properties+'</table></section>'
    ld=sub.serialize(format='json-ld').replace('</','<\\/')
    path=str(s)[len(BASE):]
    body='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(label)+' · MovieLOD</title><link rel="stylesheet" href="/style.css"><link rel="alternate" type="text/turtle" href="'+path+'/index.ttl"><script type="application/ld+json">'+ld+'</script></head><body class="resource-page"><main><a href="/">← MovieLOD</a><h1>'+html.escape(label)+'</h1><p class="iri">'+html.escape(str(s))+'</p><p><a href="'+path+'/index.ttl">Download RDF (Turtle)</a></p><table><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>'+rows+'</tbody></table><footer>Source data: Wikidata, DBpedia. <a href="/LICENSE-DATA.txt">License and attribution</a>.</footer></main></body></html>'
    if extra:body=body.replace('<footer>',extra+'<footer>')
    (directory/'index.html').write_text(prefix_html_links(body),encoding='utf-8')

if __name__=='__main__':build()
