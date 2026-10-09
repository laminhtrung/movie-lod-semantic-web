"""Export the validated DBpedia-based design to the canonical OWL files.
Canonical schema, data and query exports now share version 3.0.0.
"""
import argparse,hashlib,json,re,subprocess
from rdflib import Graph,RDF,RDFS,OWL,URIRef,Literal
from common import ROOT,EX,RES,BASE,DBO,write_json
from build import timestamp_literal
from ontology_design import schema_hierarchy

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--java',required=True);args=parser.parse_args()
    source=ROOT/'evidence/ontology_design';report=json.loads((source/'reasoning.json').read_text())
    assert report['consistent'] and not report['unsatisfiable_named_classes']
    s=Graph().parse(source/'schema.ttl');d=Graph().parse(source/'asserted.ttl')
    for a,p,v in list(d.triples((None,EX.retrievedAt,None))):d.remove((a,p,v));d.add((a,p,timestamp_literal(str(v))))
    ontology=URIRef(BASE+'/ontology');s.set((ontology,OWL.versionInfo,Literal('3.0.0')))
    s.set((ontology,RDFS.label,Literal('MovieLOD — DBpedia-based movie ontology',lang='en')))
    complete=s+d
    path=ROOT/'ontology/Movie_Knowledge_Graph.owl';complete.serialize(path,format='xml')
    s.serialize(ROOT/'ontology/Movie_Ontology.owl',format='xml');s.serialize(ROOT/'ontology/movie.ttl',format='turtle')
    cp=str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit')+':'+str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit/HermiT.jar')
    command=[args.java,'-Xmx2048M','-cp',cp,'org.semanticweb.HermiT.cli.CommandLine','-k','-U','-c','-I',str(path)]
    result=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    (source/'final_owl_hermit.log').write_text(result.stdout)
    assert result.returncode==0 and 'Exception' not in result.stdout,result.stdout[-2000:]
    assert 'http://www.w3.org/2002/07/owl#Thing is satisfiable.' in result.stdout
    unsat=re.findall(r'^\s*<([^>]+)>\s*$',result.stdout.split("Classes equivalent to 'owl:Nothing':")[-1].split('SubClassOf(')[0],re.M)
    assert not unsat,unsat
    inferred=Graph();hierarchy=schema_hierarchy(s,result.stdout)
    for a,c in re.findall(r'Type\(\s*<([^>]+)>\s*<([^>]+)>\s*\)',result.stdout):
        for parent in hierarchy.transitive_objects(URIRef(c),RDFS.subClassOf):
            if isinstance(parent,URIRef):inferred.add((URIRef(a),RDF.type,parent))
    counts={name:len({a for a in inferred.subjects(RDF.type,URIRef(str(DBO if name.startswith('dbo:') else EX)+name.split(':')[1])) if str(a).startswith(str(RES))}) for name in report['counts'] if name.startswith(('dbo:','ex:'))}
    for name,values in report['counts'].items():
        if name.startswith(('dbo:','ex:')):assert counts[name]==values['reasoned'],(name,counts[name],values['reasoned'])
    output={'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'version':'3.0.0','consistent':True,'unsatisfiable_named_classes':unsat,'reasoner':'HermiT 1.3.8.1099 direct RDF/XML input','class_counts':counts,'source_design_matches_reasoned_membership':True,'video_status':'Removed by user request','application_migration_status':'Canonical model and application assets are version 3.0.0; see publication evidence for deployed status.'}
    write_json(source/'final_owl_checks.json',output);print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
