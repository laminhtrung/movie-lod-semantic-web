import hashlib
import json
import re
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Dataset
from common import ROOT, EX, DBO, write_json

def check_data(g):
    """Check the basic movie, credit and source fields used by this application."""
    errors=[]
    films=set(g.subjects(RDF.type,DBO.Film))
    if not films:
        errors.append('Dataset has no films.')
    for film in films:
        if len(list(g.objects(film,RDFS.label)))!=1:
            errors.append(f'{film}: expected one title.')
        if not any(g.objects(film,EX.sourceSnapshot)):
            errors.append(f'{film}: missing source snapshot.')
        if not any(isinstance(link,URIRef) for link in g.objects(film,OWL.sameAs)):
            errors.append(f'{film}: missing external IRI.')
    for contribution in g.subjects(RDF.type,EX.Contribution):
        for prop,kind in [(EX.contributionTo,DBO.Film),(EX.contributionBy,DBO.Person)]:
            values=list(g.objects(contribution,prop))
            if len(values)!=1 or (values[0],RDF.type,kind) not in g:
                errors.append(f'{contribution}: expected one typed {prop}.')
        roles=list(g.objects(contribution,EX.hasRole))
        if len(roles)!=1 or roles[0] not in [EX.DirectorRole,EX.ActorRole,EX.WriterRole,EX.ProducerRole]:
            errors.append(f'{contribution}: expected one contribution role.')
        if not any(g.objects(contribution,EX.sourceSnapshot)):
            errors.append(f'{contribution}: missing source snapshot.')
    for snapshot in g.subjects(RDF.type,EX.SourceSnapshot):
        for prop in [EX.sourceUrl,EX.retrievedAt,EX.sha256]:
            values=list(g.objects(snapshot,prop))
            if len(values)!=1:
                errors.append(f'{snapshot}: expected one {prop}.')
            elif prop==EX.sha256 and not re.fullmatch('[0-9a-f]{64}',str(values[0])):
                errors.append(f'{snapshot}: invalid SHA-256.')
    return errors

def run():
    g=Graph().parse(ROOT/'data/processed/movies.ttl')
    errors=check_data(g)
    snapshots=json.loads((ROOT/'data/raw/snapshots.json').read_text())
    checked=[]
    for s in snapshots:
        path=ROOT/s['path']
        actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        checked.append({'path':s['path'],'sha256':actual,'matches':actual==s['sha256'],'exists':path.is_file()})
    reasoned=g+Graph().parse(ROOT/'ontology/movie.ttl')
    inference_path=ROOT/'data/processed/inferred_classes.ttl'
    if inference_path.exists():
        reasoned.parse(inference_path)
    query_results=[]
    questions=json.loads((ROOT/'evidence/ontology_design/query_results.json').read_text())
    named=Dataset().parse(ROOT/'data/processed/before_after.trig',format='trig')
    for row in questions:
        path=ROOT/'queries'/f"{row['number']:02}.rq"
        mode='dataset' if row['number']==27 else 'asserted' if row['group']=='A' else 'reasoned'
        result={'asserted':g,'reasoned':reasoned,'dataset':named}[mode].query(path.read_text())
        data=json.loads(result.serialize(format='json')) if result.type in ['SELECT','ASK'] else {'triples':len(result.graph)}
        count=len(data.get('results',{}).get('bindings',[])) if result.type=='SELECT' else int(bool(result.askAnswer)) if result.type=='ASK' else len(result.graph)
        assert count==(row['asserted_rows'] if mode=='asserted' else row['reasoned_rows']),(path.name,count)
        query_results.append({'file':path.name,'mode':mode,'result':data})
    write_json(ROOT/'evidence/query_results.json',query_results)
    summary={'data_checks_passed':not errors,'data_errors':errors,'source_hashes_match':all(s['matches'] for s in checked),
             'snapshots_checked':len(checked),'query_files_executed':len(query_results),
             'missing_source_files':[s['path'] for s in checked if not s['exists']],
             'source_hash_checks':checked,
             'films_have_sources':all(any(g.objects(f,EX.sourceSnapshot)) for f in g.subjects(RDF.type,DBO.Film)),
             'films_have_external_links':all(any(g.objects(f,OWL.sameAs)) for f in g.subjects(RDF.type,DBO.Film))}
    write_json(ROOT/'evidence/validation.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    if not all([summary['data_checks_passed'],summary['source_hashes_match'],summary['films_have_sources'],summary['films_have_external_links']]):
        raise SystemExit('Validation failed; inspect evidence/')

if __name__=='__main__':run()
