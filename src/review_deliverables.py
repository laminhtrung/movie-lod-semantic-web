import sys,json,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import ROOT,EX,DBO,RES,write_json
from validate import check_data
from rdflib import Graph,RDF,OWL,URIRef
s=Graph().parse(ROOT/'ontology/movie.ttl');g=Graph().parse(ROOT/'data/processed/movies.ttl')
ss=json.loads((ROOT/'data/raw/snapshots.json').read_text());missing=[];bad=[];ok=[]
for row in ss:
 p=ROOT/row['path']
 if not p.exists():missing.append(row['path'])
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
 else:ok.append(row['path'])
r=Graph().parse(ROOT/'data/processed/reasoned.ttl')
from rdflib import Dataset
named=Dataset().parse(ROOT/'data/processed/before_after.trig',format='trig')
queries=[]
meta=json.loads((ROOT/'evidence/ontology_design/query_results.json').read_text())
for row in meta:
 p=ROOT/'queries'/f"{row['number']:02}.rq"
 scope='dataset' if row['number']==27 else 'asserted' if row['group']=='A' else 'reasoned'
 target={'asserted':g,'reasoned':r,'dataset':named}[scope]
 result=target.query(p.read_text())
 queries.append({'file':p.name,'mode':scope,'rows':len(list(result))})
review_date=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).date().isoformat()
out={'review_date':review_date,'data_triples':len(g),'schema_triples':len(s),'named_classes':len({x for x in s.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef)}),'data_errors':check_data(g),'raw_snapshots_listed':len(ss),'raw_hashes_matching':len(ok),'missing_raw_files':missing,'hash_mismatches':bad,'queries':queries,'inference_scope':'Uses current canonical graph scopes; HermiT proof and pytest are separate verification.'}
write_json(ROOT/('evidence/review_'+review_date+'.json'),out)
print(json.dumps(out,ensure_ascii=False,indent=2))
