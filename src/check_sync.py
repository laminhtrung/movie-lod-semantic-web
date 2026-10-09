"""Check canonical/static/public graph and document equality and MP4 removal."""
import hashlib,json,tarfile,zipfile,re
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import requests
from rdflib import Graph,Dataset
from rdflib.compare import isomorphic
from common import ROOT,BASE,write_json

def main():
    pairs=[('data/processed/movies.ttl','web/dist/data/movies.ttl','turtle'),('data/processed/movies.jsonld','web/dist/data/movies.jsonld','json-ld'),('ontology/movie.ttl','web/dist/ontology.ttl','turtle'),('ontology/Movie_Knowledge_Graph.owl','web/dist/Movie_Knowledge_Graph.owl','xml'),('ontology/Movie_Ontology.owl','web/dist/Movie_Ontology.owl','xml'),('data/processed/reasoned.ttl','web/dist/data/reasoned.ttl','turtle'),('data/processed/inferred_classes.ttl','web/dist/data/inferred_classes.ttl','turtle')]
    def check(row):
        source,target,fmt=row;a=Graph().parse(ROOT/source,format=fmt);b=Graph().parse(ROOT/target,format=fmt)
        assert isomorphic(a,b),target
        path='/'+target.removeprefix('web/dist/');response=requests.get(BASE+path,timeout=60);response.raise_for_status();c=Graph().parse(data=response.content,format=fmt)
        assert isomorphic(a,c),path
        return {'path':path,'triples':len(a),'local_static_public_isomorphic':True}
    with ThreadPoolExecutor(max_workers=3) as pool:graphs=list(pool.map(check,pairs))
    response=requests.get(BASE+'/data/before_after.trig',timeout=60);response.raise_for_status()
    ds=Dataset().parse(ROOT/'data/processed/before_after.trig',format='trig');remote=Dataset().parse(data=response.content,format='trig')
    named=[]
    for name in ['urn:movie:asserted','urn:movie:reasoned']:
        assert isomorphic(ds.graph(name),remote.graph(name)),name
        named.append({'graph':name,'triples':len(ds.graph(name)),'matches':True})
    meta=json.loads((ROOT/'evidence/document_sync_checks.json').read_text());docs=[]
    for p in (ROOT/'docs/guide_images').glob('*.png'):
        meta['document_assets']['guide_images/'+p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    def check_doc(row):
        name,digest=row;response=requests.get(BASE+'/docs/'+name,timeout=60);response.raise_for_status()
        if name.endswith('.html'):
            markup=response.content.decode('utf-8')
            # Cloudflare adds its own challenge script to HTML, outside document content.
            def strip_challenge(match):
                script=match.group(0)
                return '' if '__CF$cv$params' in script and '/cdn-cgi/challenge-platform/' in script else script
            markup=re.sub(r'<script>.*?</script>',strip_challenge,markup,flags=re.S)
            assert markup==(ROOT/'docs'/name).read_text(),name
            return {'file':name,'public_document_content_matches':True,'hosting_challenge_script_ignored':True}
        assert hashlib.sha256(response.content).hexdigest()==digest,name
        return {'file':name,'public_sha256_matches':True}
    with ThreadPoolExecutor(max_workers=4) as pool:docs=list(pool.map(check_doc,meta['document_assets'].items()))
    video_files=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower()=='.mp4' and '.git' not in p.parts]
    assert not video_files
    archives=[]
    for p in ROOT.rglob('*.zip'):
        if '.git' in p.parts or '.venv' in p.parts:continue
        with zipfile.ZipFile(p) as z:assert not any(n.lower().endswith('.mp4') for n in z.namelist()),p
        archives.append(str(p.relative_to(ROOT)))
    stats=requests.get(BASE+'/data/statistics.json',timeout=40).json();assert stats['ontology_version']=='3.0.0' and stats['classes']==37
    queries=list((ROOT/'queries').glob('*.rq'));assert len(queries)==28
    assert not (ROOT/'queries/design').exists()
    meta=json.loads((ROOT/'evidence/ontology_design/query_results.json').read_text())
    for row in meta:assert (ROOT/'queries'/f"{row['number']:02}.rq").read_text().strip()==row['query'].strip()
    report={'passed':True,'checked_at':datetime.now(timezone.utc).isoformat(),'ontology_version':'3.0.0','canonical_static_public_graphs':graphs,'named_graphs':named,'public_documents':docs,'mp4_files':0,'mp4_entries_in_current_archives':0,'zip_archives_checked':archives,'hosting_provider':'GitHub Pages','canonical_queries_verified':len(queries),'statistics_match':True}
    write_json(ROOT/'evidence/full_sync_checks.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
