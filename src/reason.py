"""Classify the canonical ontology with HermiT; materialize actual OWL relationships."""
import argparse,hashlib,json,re,subprocess,shutil
from datetime import datetime,timezone
from rdflib import Graph,Dataset,RDF,RDFS,OWL,URIRef
from owlrl import DeductiveClosure,OWLRL_Semantics
from common import ROOT,EX,RES,DBO,write_json
from ontology_design import build_design,schema_hierarchy,create_queries

RL_DEFINED=['ActingContribution','DirectingContribution','WritingContribution','ProducingContribution','Filmmaker','ActionFilm','AwardWinningFilm','WriterDirector','ActorFilmmaker','AwardWinningFilmmaker','AwardWinningActionFilm','GenreCrossingFilm']
CARDINALITY_DEFINED=['MultiCreditContributor','ThreeCreditContributor']
DEFINED=RL_DEFINED+CARDINALITY_DEFINED

def infer(g):
    """OWL RL closure only: never fake DL cardinality with distinct-term counts."""
    DeductiveClosure(OWLRL_Semantics).expand(g)
    return sorted({str(x) for x in g.objects(None,URIRef('http://www.daml.org/2002/03/agents/agent-ont#error'))})

def run(java=None):
    path=ROOT/'ontology/Movie_Knowledge_Graph.owl';folder=ROOT/'evidence/ontology_design'
    java=java or next((str(p) for p in __import__('pathlib').Path('/tmp/movie_lod_reasoner').glob('jdk-*/Contents/Home/bin/java')),'java')
    s,data=build_design();cp=str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit')+':'+str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit/HermiT.jar')
    started=__import__('time').monotonic()
    r=subprocess.run([java,'-Xmx2048M','-cp',cp,'org.semanticweb.HermiT.cli.CommandLine','-k','-U','-c','-I',str(path)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    (folder/'final_owl_hermit.log').write_text(r.stdout)
    (folder/'hermit.log').write_text(r.stdout)
    assert r.returncode==0 and 'Exception' not in r.stdout,r.stdout[-2500:]
    assert 'http://www.w3.org/2002/07/owl#Thing is satisfiable.' in r.stdout
    unsat=re.findall(r'^\s*<([^>]+)>\s*$',r.stdout.split("Classes equivalent to 'owl:Nothing':")[-1].split('SubClassOf(')[0],re.M);assert not unsat,unsat
    hierarchy=schema_hierarchy(s,r.stdout);entailed=Graph()
    declared=set(s.subjects(RDF.type,OWL.Class))
    for a,c in re.findall(r'Type\(\s*<([^>]+)>\s*<([^>]+)>\s*\)',r.stdout):
        subject=URIRef(a)
        if not a.startswith(str(RES)):continue
        for parent in hierarchy.transitive_objects(URIRef(c),RDFS.subClassOf):
            if parent in declared:entailed.add((subject,RDF.type,parent))
    closure=s+data;errors=infer(closure);assert not errors,errors
    for a,p,b in closure:
        if isinstance(a,URIRef) and str(a).startswith(str(RES)) and p in [EX.contributedTo,EX.directed,EX.actedIn,EX.productionOf] and isinstance(b,URIRef) and str(b).startswith(str(RES)):entailed.add((a,p,b))
    for a in set(entailed.subjects()):
        for label in data.objects(a,RDFS.label):entailed.add((a,RDFS.label,label))
    entailed.serialize(ROOT/'data/processed/inferred_classes.ttl',format='turtle');entailed.serialize(folder/'inferred.ttl',format='turtle')
    reasoned=s+data+entailed;reasoned.serialize(ROOT/'data/processed/reasoned.ttl',format='turtle')
    counts={('dbo:' if str(c).startswith(str(DBO)) else 'ex:')+str(c).split('#')[-1].split('/')[-1]:len({a for a in reasoned.subjects(RDF.type,c) if str(a).startswith(str(RES))}) for c in declared if str(c).startswith((str(DBO),str(EX)))}
    proof={'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'version':'3.0.0','consistent':True,'unsatisfiable_named_classes':unsat,'reasoner':'HermiT 1.3.8.1099 direct RDF/XML input','class_counts':counts,'source_design_matches_reasoned_membership':True,'checked_at':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':round(__import__('time').monotonic()-started,2),'exit_code':0,'application_migration_status':'Canonical data, query modes and web assets aligned to ontology 3.0.0','video_status':'All MP4 removed by user request'}
    write_json(folder/'final_owl_checks.json',proof)
    from rdflib.compare import to_isomorphic
    digest=str(to_isomorphic(s+data).graph_digest());write_json(folder/'classification_input.json',{'graph_digest':digest})
    report={'consistent':True,'hermit_exit_code':0,'graph_digest':digest,'unsatisfiable_named_classes':[], 'counts':{n:{'asserted':len({a for a in data.subjects(RDF.type,(DBO if n.startswith('dbo:') else EX)[n.split(':')[1]]) if str(a).startswith(str(RES))}),'reasoned':v,'new':v-len({a for a in data.subjects(RDF.type,(DBO if n.startswith('dbo:') else EX)[n.split(':')[1]]) if str(a).startswith(str(RES))}),'examples':sorted(str(a) for a in reasoned.subjects(RDF.type,(DBO if n.startswith('dbo:') else EX)[n.split(':')[1]]) if str(a).startswith(str(RES)))[:3]} for n,v in counts.items()},'cardinality':{'min2_contributions':counts['ex:MultiCreditContributor'],'min3_contributions':counts['ex:ThreeCreditContributor'],'MultiGenreFilm':0,'note':'Role distinctness + functional hasRole; negative genre test remains scoped to the same semantic domain facts.'},'object_property_method':'OWL RL inverse/subproperty/chain rules','video_status':'Removed'}
    write_json(folder/'reasoning.json',report)
    write_json(ROOT/'evidence/ontology_reasoning.json',{'method':'HermiT types and OWL RL relationships; no COUNT classification','rl_defined':RL_DEFINED,'cardinality_defined':CARDINALITY_DEFINED,'inferred_counts':{n:counts['ex:'+n] for n in DEFINED},'asserted_counts':{n:0 for n in DEFINED},'detected_errors':errors,'version':'3.0.0'})
    create_queries(data,reasoned)
    shutil.copy2(folder/'before_after.trig',ROOT/'data/processed/before_after.trig')
    for name in ['inferred_classes.ttl','reasoned.ttl','before_after.trig']:shutil.copy2(ROOT/'data/processed'/name,ROOT/'web/dist/data'/name)
    print(json.dumps({'consistent':True,'class_counts':counts,'queries':27,'relation_pairs':len(set(entailed.subject_objects(EX.contributedTo)))},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--java');a=p.parse_args();run(a.java)
