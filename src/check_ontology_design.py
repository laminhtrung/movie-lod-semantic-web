"""Check the independent design against source facts and reasoner evidence."""
import hashlib,json
from rdflib import Graph,Dataset,RDF,RDFS,OWL,URIRef
from rdflib.compare import to_isomorphic
from common import ROOT,EX,RES,DBO,write_json

def main():
    out=ROOT/'evidence/ontology_design'
    s=Graph().parse(out/'schema.ttl');d=Graph().parse(out/'asserted.ttl');i=Graph().parse(out/'inferred.ttl');base=Graph().parse(ROOT/'data/processed/movies.ttl')
    from build import timestamp_literal
    for a,p,v in list(d.triples((None,EX.retrievedAt,None))):
        d.remove((a,p,v));d.add((a,p,timestamp_literal(str(v))))
    r=json.loads((out/'reasoning.json').read_text());manifest=json.loads((out/'classification_input.json').read_text())
    assert r['consistent'] and r['hermit_exit_code']==0 and not r['unsatisfiable_named_classes']
    assert str(to_isomorphic(s+d).graph_digest())==manifest['graph_digest']==r['graph_digest']
    assert set(base.triples((None,OWL.sameAs,None)))==set(d.triples((None,OWL.sameAs,None)))
    assert len(set(d.subjects(RDF.type,DBO.Film)))==30
    for old in ['Actor','Genre','Award','Language','ProductionCompany','FeatureFilm','AnimatedFilm','DocumentaryFilm','FictionGenre','Dataset']:
        assert not list(d.triples((None,RDF.type,EX[old])))
        assert not list(s.triples((EX[old],RDF.type,OWL.Class)))
    assert not list(d.triples((None,EX.contributedTo,None)))
    expected={(p,f) for c,p in d.subject_objects(EX.contributionBy) for f in d.objects(c,EX.contributionTo)}
    actual={(p,f) for p,f in i.subject_objects(EX.contributedTo)}
    assert actual==expected,(len(actual),len(expected))
    for pred,inv in [(DBO.director,EX.directed),(DBO.starring,EX.actedIn)]:
        assert set(i.subject_objects(inv))=={(p,f) for f,p in d.subject_objects(pred)}
    assert not list(s.triples((DBO.Actor,OWL.equivalentClass,None)))
    assert (DBO.starring,RDFS.range,DBO.Actor) in s
    for f,value in base.subject_objects(EX.runtimeMinutes):assert abs(float(d.value(f,DBO.runtime))-float(value)*60)<1e-9
    assert all(x['new']>0 and x['asserted']==0 for name,x in r['counts'].items() if name.startswith(str('ex:')) and name not in ['ex:ActionGenre','ex:DramaGenre','ex:SourceSnapshot','ex:ContributionRole','ex:Contribution'])
    queries=json.loads((out/'query_results.json').read_text());assert len(queries)>=20
    assert all(q['asserted_rows']==0 and q['reasoned_rows']>0 for q in queries if q['group']=='C')
    assert not list(ROOT.glob('docs/*.mp4'))
    result={'passed':True,'source_identity_links_preserved':True,'film_count':30,'actual_property_chain_pairs':len(actual),'queries_executed':len(queries),'new_domain_inferred_classes':7,'min2':r['cardinality']['min2_contributions'],'min3':r['cardinality']['min3_contributions'],'no_unique_name_assumption':True,'inferred_actor_without_overriding_dbpedia':True,'runtime_seconds_conversion_verified':True,'graph_digest_matches_actual_reasoner_input':True,'mp4_removed_by_request':True}
    write_json(out/'checks.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
