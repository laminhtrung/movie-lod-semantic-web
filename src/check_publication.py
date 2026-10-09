"""Verify public LOD documents and compare them with the submitted local graphs."""
import hashlib,json
from datetime import datetime
from zoneinfo import ZoneInfo
from concurrent.futures import ThreadPoolExecutor
import requests
from rdflib import Graph,RDF,OWL,URIRef
from rdflib.compare import isomorphic
from common import ROOT,BASE,RES,write_json
PATHS=['/','/dataset','/data/movies.ttl','/data/movies.jsonld','/ontology.ttl','/resource/film-Q25188','/resource/film-Q25188/index.ttl','/LICENSE-DATA.txt']
def main():
    local=Graph().parse(ROOT/'data/processed/movies.ttl');schema=Graph().parse(ROOT/'ontology/movie.ttl');film=Graph()
    for t in local.triples((RES['film-Q25188'],None,None)):film.add(t)
    def check(path):
        try:
            response=requests.get(BASE+path,timeout=40,headers={'User-Agent':'MovieLOD-LOD-Verification/3.0'})
            row={'path':path,'url':BASE+path,'http_status':response.status_code,'content_type':response.headers.get('Content-Type'),'sha256':hashlib.sha256(response.content).hexdigest()}
            if response.ok and path.endswith(('.ttl','.jsonld')):
                graph=Graph().parse(data=response.text,format='json-ld' if path.endswith('.jsonld') else 'turtle');row['triples']=len(graph)
                expected=schema if path=='/ontology.ttl' else film if path.endswith('/index.ttl') else local
                row['matches_local_graph']=isomorphic(graph,expected)
                if path=='/ontology.ttl':row['named_classes']=len({s for s in graph.subjects(RDF.type,OWL.Class) if isinstance(s,URIRef)})
            if path=='/LICENSE-DATA.txt':row['open_license_present']='CC BY-SA 4.0' in response.text
            if path=='/resource/film-Q25188':row['html_has_rdf_link']='index.ttl' in response.text and 'application/ld+json' in response.text
            return row
        except Exception as e:return {'path':path,'url':BASE+path,'error':str(e)}
    with ThreadPoolExecutor(max_workers=4) as pool:checks=list(pool.map(check,PATHS))
    summary={'all_urls_public_http_200':all(r.get('http_status')==200 for r in checks),'all_rdf_graphs_match_local':all(r.get('matches_local_graph') for r in checks if r['path'].endswith(('.ttl','.jsonld'))),'open_license_present':next(r for r in checks if r['path']=='/LICENSE-DATA.txt').get('open_license_present',False),'film_iri_has_machine_readable_description':next(r for r in checks if r['path']=='/resource/film-Q25188').get('html_has_rdf_link',False),'local_data_triples':len(local),'local_schema_triples':len(schema),'local_named_classes':len({s for s in schema.subjects(RDF.type,OWL.Class) if isinstance(s,URIRef)})}
    summary['publication_complete']=all(summary[k] for k in ['all_urls_public_http_200','all_rdf_graphs_match_local','open_license_present','film_iri_has_machine_readable_description'])
    report={'checked_at':datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(),'authentication':'No cookies, credentials or signed-in browser session supplied','summary':summary,'checks':checks}
    write_json(ROOT/'evidence/publication_checks.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
    if not summary['publication_complete']:raise SystemExit('Publication does not yet match the submitted graph.')
if __name__=='__main__':main()
