"""Canonical DBpedia reuse schema and supporting semantic documentation.
No invented entities, no blanket inequality and no video generation.
"""
import json, hashlib, re, subprocess, argparse
from pathlib import Path
from decimal import Decimal
from rdflib import Graph, URIRef, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from common import ROOT, EX, RES, DBO, VOID, PROV, DCT, BASE, write_json
from build import preferred_values, timestamp_literal
OUT=ROOT/'evidence/ontology_design'
REFERENCE=ROOT/'evidence/dbpedia_reference.owl'
CLASSES=[]; PROPERTIES=[]; DEFINITIONS={}

def compact(t):
    if t is None:return '—'
    for ns,p in [(EX,'ex'),(DBO,'dbo'),(RES,'res'),(PROV,'prov'),(VOID,'void'),(RDFS,'rdfs'),(XSD,'xsd'),(OWL,'owl')]:
        if str(t).startswith(str(ns)):return p+':'+str(t)[len(str(ns)):]
    return str(t)

def build_design(original=None, persist=True):
    CLASSES.clear(); PROPERTIES.clear(); DEFINITIONS.clear()
    ref=Graph().parse(REFERENCE); ref += Graph().parse(ROOT/'evidence/dbpedia_development_reference.owl'); s=Graph(); s.bind('ex',EX);s.bind('dbo',DBO);s.bind('res',RES)
    o=URIRef(BASE+'/ontology');s.add((o,RDF.type,OWL.Ontology));s.add((o,OWL.versionInfo,Literal('3.0.0')));s.add((o,RDFS.label,Literal('MovieLOD — DBpedia-based movie ontology',lang='en')))
    def cls(u,parent=None,definition=None,source='',reason='',action='CREATE'):
        s.add((u,RDF.type,OWL.Class));s.add((u,RDFS.label,Literal(compact(u).split(':')[-1],lang='en')))
        s.add((u,RDFS.comment,Literal(reason,lang='en')))
        if parent:s.add((u,RDFS.subClassOf,parent))
        if definition:s.add((u,OWL.equivalentClass,expression(definition)))
        DEFINITIONS[compact(u)]=definition
        CLASSES.append(dict(uri=str(u),name=compact(u),parent=compact(parent),definition=definition,source=source,action=action,reason=reason,dbpedia_exists=bool(list(ref.predicate_objects(DBO[str(u).split('#')[-1].split('/')[-1]])))))
    def expression(e):
        if isinstance(e,URIRef):return e
        op,*args=e; b=BNode()
        if op in ('and','or'):
            s.add((b,RDF.type,OWL.Class));h=BNode();s.add((b,OWL.intersectionOf if op=='and' else OWL.unionOf,h));Collection(s,h,[expression(a) for a in args])
        else:
            s.add((b,RDF.type,OWL.Restriction));s.add((b,OWL.onProperty,args[0]))
            if op in ('some','value'):s.add((b,OWL.someValuesFrom if op=='some' else OWL.hasValue,args[1]))
            else:
                s.add((b,OWL.onClass,args[2]));s.add((b,OWL.minQualifiedCardinality if op=='min' else OWL.qualifiedCardinality,Literal(args[1],datatype=XSD.nonNegativeInteger)))
        return b
    # A selected reference module: preserve DBpedia domain/range and hierarchy, not a full import.
    reused=['Work','Film','Agent','Person','Artist','Actor','Writer','MovieDirector','ScreenWriter','Producer','Organisation','Company','Genre','MovieGenre','Award','Country','Language']
    sources={'Film':'P31','Person':'P31=Q5; P57/P161/P58/P162','Actor':'P161','Writer':'P58 via ScreenWriter','MovieDirector':'P57','ScreenWriter':'P58','Producer':'P162','Company':'P272','Genre':'P136','MovieGenre':'P136 in film context','Award':'P166','Country':'P495','Language':'P364'}
    for n in reused:
        u=DBO[n];par=next((p for p in ref.objects(u,RDFS.subClassOf) if p in [DBO[x] for x in reused]),None)
        cls(u,par,source=sources.get(n,'DBpedia supertype of supported entities'),reason='Reuse DBpedia meaning and its supported superclass; no local clone.',action='REUSE')
    cls(EX.Contribution,source='P57/P161/P58/P162',reason='A local credit association with one person, film and role; not the person or film itself.')
    cls(EX.ContributionRole,source='The four crawled credit predicates',reason='Local controlled role values, not subclasses of Person.')
    cls(EX.SourceSnapshot,source='snapshots.json URL/time/hash',reason='A retrieved response record, not a domain entity.')
    cls(VOID.Dataset,source='Published collection of crawled film records',reason='Reuse VoID dataset, remove ex:Dataset clone.',action='REUSE')
    for n in ['Action','Drama']:
        cls(EX[n+'Genre'],DBO.MovieGenre,source='P136 target English label',reason='Local normalized film-genre bucket selected by matching the crawled English label; no DBpedia class of this narrow meaning in reference module.',action='EXTEND')
    role_classes=[]
    for n,role in [('Acting','Actor'),('Directing','Director'),('Writing','Writer'),('Producing','Producer')]:
        cls(EX[n+'Contribution'],EX.Contribution,('and',EX.Contribution,('value',EX.hasRole,EX[role+'Role'])),source='Credit claim corresponding to '+role,reason='Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record.',action='EXTEND');role_classes.append(EX[n+'Contribution'])
    for credit, person_type in [(EX.DirectingContribution,DBO.MovieDirector),(EX.WritingContribution,DBO.ScreenWriter),(EX.ProducingContribution,DBO.Producer)]:
        s.add((expression(('and',DBO.Person,('some',EX.hasContribution,credit))),RDFS.subClassOf,person_type))
    # Actor is obtained from the unchanged range of dbo:starring. Do not redefine dbo:Actor.
    maker=('or',*[('some',EX.hasContribution,c) for c in role_classes[1:]])
    definitions={
      'Filmmaker':('and',DBO.Person,maker),
      'ActionFilm':('and',DBO.Film,('some',DBO.genre,EX.ActionGenre)),
      'AwardWinningFilm':('and',DBO.Film,('some',DBO.award,DBO.Award)),
      'MultiCreditContributor':('and',DBO.Person,('min',EX.hasContribution,2,EX.Contribution)),
      'ThreeCreditContributor':('and',DBO.Person,('min',EX.hasContribution,3,EX.Contribution)),
      'WriterDirector':('and',DBO.MovieDirector,DBO.ScreenWriter),
      'ActorFilmmaker':('and',DBO.Actor,EX.Filmmaker),
      'AwardWinningFilmmaker':('and',EX.Filmmaker,('some',DBO.award,DBO.Award)),
      'AwardWinningActionFilm':('and',EX.ActionFilm,EX.AwardWinningFilm),
      'GenreCrossingFilm':('and',DBO.Film,('some',DBO.genre,EX.ActionGenre),('some',DBO.genre,EX.DramaGenre)),
    }
    reasons={
      'MultiCreditContributor':'At least two semantically distinct credit records. Different roles prove their distinctness; the name is shorthand and does not exclude repeated same-role credits.',
      'ThreeCreditContributor':'At least three distinct credit records; three different role fillers prove distinctness. Not exactly three roles or an exhaustive career description.',
      'WriterDirector':'A person with both directing and writing credits in this dataset; classification is never manually asserted.',
      'GenreCrossingFilm':'Film carrying both action and drama genre memberships; this is not an unproved two-distinct-genre cardinality claim.'}
    for n,e in definitions.items():
        parent=DBO.Film if n.endswith('Film') else DBO.Person
        cls(EX[n],parent,e,source='P136/P166' if parent==DBO.Film else 'P57/P161/P58/P162; P166 when award-based',reason=reasons.get(n,'Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.'),action='EXTEND')
    def prop(u,domain,ran,source,inverse=None,functional=False,sub=None,datatype=False):
        s.add((u,RDF.type,OWL.DatatypeProperty if datatype else OWL.ObjectProperty))
        if domain:s.add((u,RDFS.domain,domain))
        if ran:s.add((u,RDFS.range,ran))
        if inverse:s.add((u,OWL.inverseOf,inverse))
        if functional:s.add((u,RDF.type,OWL.FunctionalProperty))
        if sub:s.add((u,RDFS.subPropertyOf,sub))
        PROPERTIES.append(dict(uri=str(u),name=compact(u),kind='Data' if datatype else 'Object',domain=compact(domain),range=compact(ran),source=source,inverse=compact(inverse),functional=functional,subproperty=compact(sub),action='REUSE' if str(u).startswith(str(DBO)) else 'CREATE'))
    for n,source in [('director','P57'),('starring','P161'),('writer','P58'),('producer','P162'),('productionCompany','P272'),('award','P166'),('genre','P136'),('country','P495'),('language','P364')]:
        prop(DBO[n],ref.value(DBO[n],RDFS.domain),ref.value(DBO[n],RDFS.range),source)
    prop(EX.hasContribution,DBO.Person,EX.Contribution,'Derived credit association',EX.contributionBy)
    prop(EX.contributionBy,EX.Contribution,DBO.Person,'P57/P161/P58/P162',functional=True)
    prop(EX.contributionTo,EX.Contribution,DBO.Film,'Containing source film',EX.contributionOf,functional=True)
    prop(EX.contributionOf,DBO.Film,EX.Contribution,'Inverse of contributionTo')
    prop(EX.hasRole,EX.Contribution,EX.ContributionRole,'Credit predicate to controlled role',functional=True)
    prop(EX.contributedTo,DBO.Person,DBO.Film,'OWL property chain')
    prop(EX.directed,DBO.Person,DBO.Film,'Inverse P57',DBO.director,sub=EX.contributedTo)
    prop(EX.actedIn,DBO.Actor,DBO.Film,'Inverse P161',DBO.starring,sub=EX.contributedTo)
    prop(EX.productionOf,DBO.Company,DBO.Work,'Inverse P272',DBO.productionCompany)
    prop(EX.sourceSnapshot,None,EX.SourceSnapshot,'Crawled entity response provenance')
    prop(DBO.runtime,DBO.Work,XSD.double,'P2047; normalize to seconds',datatype=True)
    # Year precision is deliberately not expanded into a fabricated date.
    prop(EX.releaseYear,DBO.Film,XSD.integer,'Earliest Gregorian P577 year, precision >=9',datatype=True)
    for n,t in [('sourceUrl',XSD.anyURI),('retrievedAt',XSD.dateTime),('sha256',XSD.string)]:
        prop(EX[n],EX.SourceSnapshot,t,'Snapshot manifest '+n,datatype=True)
    chain=BNode();s.add((EX.contributedTo,OWL.propertyChainAxiom,chain));Collection(s,chain,[EX.hasContribution,EX.contributionTo])
    for p,c in [(EX.contributionBy,DBO.Person),(EX.contributionTo,DBO.Film),(EX.hasRole,EX.ContributionRole)]:
        s.add((EX.Contribution,RDFS.subClassOf,expression(('exact',p,1,c))))
    roles=[EX[x+'Role'] for x in ['Actor','Director','Writer','Producer']]
    for r in roles:
        s.add((r,RDF.type,EX.ContributionRole));s.add((r,RDF.type,OWL.NamedIndividual));s.add((r,RDFS.label,Literal(str(r).split('#')[-1].replace('Role',''),lang='en')))
    b=BNode();h=BNode();s.add((b,RDF.type,OWL.AllDifferent));s.add((b,OWL.distinctMembers,h));Collection(s,h,roles)
    original=original if original is not None else Graph().parse(ROOT/'data/processed/movies.ttl');data=Graph()
    mapping={EX.Genre:DBO.MovieGenre,EX.Language:DBO.Language,EX.Award:DBO.Award,EX.ProductionCompany:DBO.Company,EX.Dataset:VOID.Dataset,
      EX.hasGenre:DBO.genre,EX.hasAward:DBO.award,EX.hasProductionCompany:DBO.productionCompany,EX.country:DBO.country,EX.language:DBO.language}
    allowed_types={DBO.Film,DBO.Person,DBO.Company,DBO.MovieGenre,DBO.Award,DBO.Country,DBO.Language,EX.Contribution,EX.ContributionRole,EX.SourceSnapshot,VOID.Dataset,EX.ActionGenre,EX.DramaGenre}
    for a,p,v in original:
        if p==EX.retrievedAt:v=timestamp_literal(str(v))
        if p==EX.title:continue # rdfs:label already carries the same title.
        if p==EX.runtimeMinutes:p=DBO.runtime;v=Literal(float(Decimal(str(v))*60),datatype=XSD.double)
        else:p=mapping.get(p,p);v=mapping.get(v,v)
        if p==RDF.type and v not in allowed_types and v!=OWL.NamedIndividual:continue
        data.add((a,p,v))
    # Retain only declared custom properties plus standard predicates; no obsolete inverses.
    allowed={URIRef(p['uri']) for p in PROPERTIES}|{RDF.type,RDFS.label,OWL.sameAs,PROV.wasDerivedFrom,DCT.title,DCT.license,DCT.source,VOID.dataDump,RDFS.seeAlso}
    for t in list(data):
        if t[1] not in allowed:data.remove(t)
    # Every source date is retained at its stated precision in a source audit, not invented day/month.
    if persist:
        write_json(OUT/'source_mapping.json',{'schema_reference':(ROOT/'evidence/dbpedia_reference_url.txt').read_text().strip(),'reference_sha256':hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),'reference_version':'Official 2016-10 schema + official extraction-framework development vocabulary (790 classes); live starring/runtime/MovieGenre cross-checked 2026-10-09','classes':CLASSES,'properties':PROPERTIES,'removed':'FeatureFilm (Q11424 means film, not necessarily feature); unsupported Documentary/FictionGenre; blanket FilmAward fallback; duplicate vocabulary','preserved_entities':len(set(data.subjects(OWL.sameAs,None))),'base_dataset_sha256':hashlib.sha256((ROOT/'data/processed/movies.ttl').read_bytes()).hexdigest()})
        s.serialize(OUT/'schema.ttl',format='turtle');data.serialize(OUT/'asserted.ttl',format='turtle');(s+data).serialize(OUT/'complete.ttl',format='turtle')
    return s,data

def manchester(e):
    if e is None:return '—'
    if isinstance(e,URIRef):return compact(e)
    op,*a=e
    if op in ('and','or'):return '('+(' and ' if op=='and' else ' or ').join(manchester(x) for x in a)+')'
    if op in ('some','value'):return compact(a[0])+' '+op+' '+compact(a[1])
    return compact(a[0])+' '+('min' if op=='min' else 'exactly')+' '+str(a[1])+' '+compact(a[2])

def schema_hierarchy(schema, output):
    h=Graph()
    for a,_,b in schema.triples((None,RDFS.subClassOf,None)):
        if isinstance(a,URIRef) and isinstance(b,URIRef):h.add((a,RDFS.subClassOf,b))
    for a,b in re.findall(r'SubClassOf\(\s*<([^>]+)>\s*<([^>]+)>\s*\)',output):h.add((URIRef(a),RDFS.subClassOf,URIRef(b)))
    return h

def reason(java, reuse_classification=False):
    s,data=build_design();combined=s+data
    from rdflib.compare import to_isomorphic
    graph_digest=str(to_isomorphic(combined).graph_digest())
    old_manifest=OUT/'classification_input.json'
    if reuse_classification:
        assert old_manifest.exists() and json.loads(old_manifest.read_text())['graph_digest']==graph_digest,'Cached classification does not match input'
    else:write_json(old_manifest,{'graph_digest':graph_digest,'schema_reference_sha256':hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),'development_reference_sha256':hashlib.sha256((ROOT/'evidence/dbpedia_development_reference.owl').read_bytes()).hexdigest()})
    import tempfile
    with tempfile.TemporaryDirectory(prefix='movie-design-') as tmp:
        file=Path(tmp)/'validated.owl';combined.serialize(file,format='xml')
        cp=str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit')+':'+str(__import__('pathlib').Path(__import__('owlready2').__file__).parent/'hermit/HermiT.jar')
        r=subprocess.CompletedProcess([],0,(OUT/'hermit.log').read_text()) if reuse_classification else subprocess.run([java,'-Xmx2048M','-cp',cp,'org.semanticweb.HermiT.cli.CommandLine','-k','-U','-c','-I',str(file)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    (OUT/'hermit.log').write_text(r.stdout)
    if r.returncode!=0 or 'Exception' in r.stdout:raise RuntimeError(r.stdout[-3000:])
    inferred=Graph()
    for person,typ in re.findall(r'Type\(\s*<([^>]+)>\s*<([^>]+)>\s*\)',r.stdout):inferred.add((URIRef(person),RDF.type,URIRef(typ)))
    # The CLI exports direct individual types. Expand its entailed named-class hierarchy,
    # otherwise a ThreeCreditContributor would be missing its MultiCreditContributor type.
    hierarchy=schema_hierarchy(s, r.stdout)
    for individual, _, typ in list(inferred):
        for parent in hierarchy.transitive_objects(typ, RDFS.subClassOf):
            if isinstance(parent,URIRef):inferred.add((individual,RDF.type,parent))
    # ABox class exports from HermiT omit inferred object-property assertions. Obtain those using
    # OWL RL rules only; never emulate DL cardinality by COUNT.
    from owlrl import DeductiveClosure,OWLRL_Semantics
    closure=s+data;DeductiveClosure(OWLRL_Semantics).expand(closure)
    for a,p,v in closure:
        if isinstance(a,URIRef) and str(a).startswith(str(RES)) and p in [EX.contributedTo,EX.directed,EX.actedIn,EX.productionOf] and isinstance(v,URIRef) and str(v).startswith(str(RES)):
            inferred.add((a,p,v))
    inferred.serialize(OUT/'inferred.ttl',format='turtle')
    reasoned=s+data+inferred
    named=[URIRef(c['uri']) for c in CLASSES]
    def local_values(g,c):return sorted({str(x) for x in g.subjects(RDF.type,c) if str(x).startswith(str(RES))})
    counts={compact(c):{'asserted':len(local_values(data,c)),'reasoned':len(local_values(reasoned,c)),'new':len(set(local_values(reasoned,c))-set(local_values(data,c))),'examples':local_values(reasoned,c)[:3]} for c in named}
    for c in CLASSES:
        if c['definition']:
            assert counts[c['name']]['asserted']==0
            assert counts[c['name']]['reasoned']>0,c['name']
    expected={'MultiCreditContributor':2,'ThreeCreditContributor':3}
    for n,k in expected.items():
        # Distinct roles guarantee distinct functional-role credit records; count only witnesses
        # of different roles, not distinct IRIs, for independent lower-bound verification.
        witnesses={p for p in data.subjects(RDF.type,DBO.Person) if len({data.value(c,EX.hasRole) for c in data.objects(p,EX.hasContribution)})>=k}
        actual={URIRef(x) for x in local_values(reasoned,EX[n])}
        assert witnesses<=actual,(n,len(witnesses),len(actual))
    # Test the unprovable MultiGenreFilm independently; do not keep an empty inferred class.
    mg=URIRef(str(EX)+'MultiGenreFilm');extra=Graph();b=BNode();h=BNode();restriction=BNode()
    extra.add((mg,RDF.type,OWL.Class));extra.add((mg,OWL.equivalentClass,b));extra.add((b,OWL.intersectionOf,h));Collection(extra,h,[DBO.Film,restriction]);extra.add((restriction,RDF.type,OWL.Restriction));extra.add((restriction,OWL.onProperty,DBO.genre));extra.add((restriction,OWL.onClass,DBO.Genre));extra.add((restriction,OWL.minQualifiedCardinality,Literal(2,datatype=XSD.nonNegativeInteger)))
    with tempfile.TemporaryDirectory(prefix='movie-cardinality-') as tmp:
        f=Path(tmp)/'cardinality.owl';(combined+extra).serialize(f,format='xml')
        rr=subprocess.run([java,'-Xmx2048M','-cp',cp,'org.semanticweb.HermiT.cli.CommandLine','-k','-I',str(f)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300)
    (OUT/'cardinality_negative.log').write_text(rr.stdout)
    assert rr.returncode==0 and 'Exception' not in rr.stdout
    mg_members=[a for a,c in re.findall(r'Type\(\s*<([^>]+)>\s*<([^>]+)>\s*\)',rr.stdout) if c==str(mg) and a.startswith(str(RES))]
    assert not mg_members,'Unexpected genre distinctness must be investigated'
    report={'consistent':"http://www.w3.org/2002/07/owl#Thing is satisfiable." in r.stdout,'hermit_exit_code':r.returncode,'graph_digest':graph_digest,'unsatisfiable_named_classes':re.findall(r'^\s*<([^>]+)>\s*$',r.stdout.split("Classes equivalent to 'owl:Nothing':")[-1].split('SubClassOf(')[0],re.M),'counts':counts,'cardinality':{'min2_contributions':counts['ex:MultiCreditContributor']['new'],'min3_contributions':counts['ex:ThreeCreditContributor']['new'],'MultiGenreFilm':0,'note':'No unique-name assumption. Functional hasRole plus four genuinely different controlled roles prove credit-record distinctness. Genre/Award/Film entities are not blanket AllDifferent.'},'object_property_method':'OWL RL inverse/subproperty/chain closure; class results from HermiT, no SPARQL aggregate classification','video_status':'Removed at user request; no recording generated'}
    write_json(OUT/'reasoning.json',report)
    create_queries(data,reasoned);create_document(s,data,reasoned,report)
    print(json.dumps({'class_counts':counts,'cardinality':report['cardinality']},ensure_ascii=False,indent=2))

PREFIX=f'''PREFIX ex: <{EX}>\nPREFIX dbo: <{DBO}>\nPREFIX res: <{RES}>\nPREFIX rdfs: <{RDFS}>\nPREFIX rdf: <{RDF}>\n'''
QUERIES=[]
def create_queries(data,reasoned):
    QUERIES.clear()
    questions=[
    ('List films','A','?s a dbo:Film .'),('Inception: year, duration and director','A','res:film-Q25188 dbo:genre ?s .'),('Directors of Inception','A','res:film-Q25188 dbo:director ?s .'),('Inception credits and roles','A','res:film-Q25188 dbo:starring ?s .'),('Films directed by Nolan','A','?s dbo:director res:person-Q25191 .'),('Companies credited on Inception','A','res:film-Q25188 dbo:productionCompany ?s .'),('Awards of Inception','A','res:film-Q25188 dbo:award ?s .'),('Runtime in seconds','A','res:film-Q25188 dbo:runtime ?s .'),
    ('Film genres through the parent class','B','?f a dbo:Film ; dbo:genre ?s . ?s a dbo:Genre .'),('Persons through Agent hierarchy','B','?s a dbo:Agent . FILTER EXISTS { ?s a dbo:Person }'),('Production companies','B','?s a dbo:Company .'),('Film subclasses','B','?s rdfs:subClassOf+ dbo:Film .'),('Actors through Artist hierarchy','B','?s a dbo:Artist . FILTER EXISTS { ?s a dbo:Actor }'),
    ('Inferred Actors','C','?s a dbo:Actor .'),('Inferred Filmmakers','C','?s a ex:Filmmaker .'),('Inferred Action films','C','?s a ex:ActionFilm .'),('Award-winning films','C','?s a ex:AwardWinningFilm .'),('People with at least two provably distinct credits','C','?s a ex:MultiCreditContributor .'),('People with at least three provably distinct credits','C','?s a ex:ThreeCreditContributor .'),('Writer-directors','C','?s a ex:WriterDirector .'),('Actor-filmmakers','C','?s a ex:ActorFilmmaker .'),('Award-winning filmmakers','C','?s a ex:AwardWinningFilmmaker .'),('Award-winning action films','C','?s a ex:AwardWinningActionFilm .'),('Action/drama crossing films','C','?s a ex:GenreCrossingFilm .'),('Nolan contributions through property chain','C','res:person-Q25191 ex:contributedTo ?s .'),('Nolan films through inverse director','C','res:person-Q25191 ex:directed ?s .')]
    results=[]
    for i,(question,group,body) in enumerate(questions,1):
        query=PREFIX+'SELECT DISTINCT ?s ?label WHERE { '+body+(' FILTER(STRSTARTS(STR(?s), "'+str(RES)+'"))' if i not in [8,12] else '')+' OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s'
        if i==2:
            query=PREFIX+'SELECT ?title ?year ?runtimeSeconds ?director WHERE { res:film-Q25188 rdfs:label ?title ; ex:releaseYear ?year ; dbo:runtime ?runtimeSeconds ; dbo:director ?person . ?person rdfs:label ?director }'
        if i==4:
            query=PREFIX+'SELECT ?personName ?roleName WHERE { res:film-Q25188 ex:contributionOf ?credit . ?credit ex:contributionBy ?person ; ex:hasRole ?role . ?person rdfs:label ?personName . ?role rdfs:label ?roleName } ORDER BY ?roleName ?personName'
        file=ROOT/'queries'/f'{i:02}.rq';file.write_text(query+'\n')
        asserted=list(data.query(query));rows=list(reasoned.query(query));results.append(dict(number=i,question=question,group=group,asserted_rows=len(asserted),reasoned_rows=len(rows),results=[{str(k):str(v) for k,v in r.asdict().items()} for r in rows],query=query))
        QUERIES.append(results[-1])
    # Named graphs preserve asserted vs entailed separation for a genuine inference-only query.
    from rdflib import Dataset
    ds=Dataset();ag=ds.graph(URIRef('urn:movie:asserted'));rg=ds.graph(URIRef('urn:movie:reasoned'))
    for t in data:ag.add(t)
    for t in reasoned:rg.add(t)
    query=PREFIX+'''SELECT DISTINCT ?s ?type WHERE {
 GRAPH <urn:movie:reasoned> { ?s a ?type }
 FILTER(STRSTARTS(STR(?s), "'''+str(RES)+'''") && STRSTARTS(STR(?type), "'''+str(EX)+'''"))
 FILTER NOT EXISTS { GRAPH <urn:movie:asserted> { ?s a ?type } }
} ORDER BY ?type ?s'''
    rr=list(ds.query(query));(ROOT/'queries/27.rq').write_text(query+'\n');results.append(dict(number=27,question='Types present only after reasoning',group='C',asserted_rows=0,reasoned_rows=len(rr),query=query,results=[{'s':str(r.s),'type':str(r.type)} for r in rr]))
    QUERIES.append(results[-1]);write_json(OUT/'query_results.json',results);ds.serialize(OUT/'before_after.trig',format='trig')

def create_document(schema,data,reasoned,report):
    lines=['# DBpedia-based Movie Ontology: Evidence-driven Design','', 'This design is grounded in the existing crawled dataset. Domain facts are not invented. The native build, application and query modes share these version-three definitions and canonical exports.','', '## 1. Findings and semantic decisions','',
      '- Reuse dbo:Film, Person, Actor, Writer, MovieDirector, ScreenWriter, Producer, Company, Organisation, Award, MovieGenre, Genre, Country, Language, Work, Artist and Agent. Actor follows the original dbo:starring range; no equivalent-class override of dbo:Actor.',
      '- Reuse dbo:director, starring, writer, producer, productionCompany, award, genre, country, language and runtime. Preserve reference domain/range: starring ranges over Actor, producer over Agent, productionCompany over Company.',
      '- dbo:MovieDirector, ScreenWriter and Producer are reused for occupation-level inferences from the corresponding credits. One-way subclass axioms suffice; their global definitions are not overridden. - dbo:runtime is seconds (xsd:double); Inception has 8880 seconds, converted from the crawled 148 minutes. Titles reuse rdfs:label (annotation property, not a custom datatype property).',
      '- P577 has varying precision. Keep a documented local releaseYear summary instead of inventing a full dbo:releaseDate. Budget, gross, IMDb, distributors and ratings are excluded because they are not in the collected field set.',
      '- Remove unsupported Documentary/Fiction hierarchy and FeatureFilm assertions: Wikidata Q11424 means film and does not justify feature-film classification. Award labels alone do not justify treating every unrecognized award as a film award.',
      '- ActionGenre and DramaGenre are transparent label-normalization buckets, not source-provided OWL classes. The author-specified classification rule is separate from the crawled facts; fiction/non-fiction is not guessed.',
      '- Contribution and four role individuals represent P57/P161/P58/P162 credits. Each record has exactly one person, film and role. Missing values remain an open-world validation issue, not automatic inconsistency.',
      '- MultiCreditContributor / ThreeCreditContributor mean at least two/three distinct credit records. Different roles provide witnesses; these class names do not prove exactly two/three unique roles across an entire career. More precise display names: MultiCreditContributor / ThreeCreditContributor.',
      '- MultiGenreFilm, MultiAwardFilm and FrequentProductionCompany are not included as inferred classes: different genre/award/film IRIs alone do not establish inequality. COUNT DISTINCT can answer a database-style question, but cannot be presented as OWL DL entailment.',
      '', '### Reference scope','',f"The official 2016-10 reference and official extraction-framework development vocabulary (790 classes) were checked. Semantic alternatives reviewed include Actor, MovieDirector, ScreenWriter, Producer, Writer, ArtisticGenre, LiteraryGenre, MovieGenre; dbo:occupation ranges over PersonFunction, while dbo:role and artistFunction are strings and cannot replace the local credit-to-role entity link. dbo:year (gYear) is generic, whereas ex:releaseYear explicitly represents an integer earliest-release summary; it does not claim equivalence to dbo:year or a complete releaseDate. The archived reference hash is: {hashlib.sha256(REFERENCE.read_bytes()).hexdigest()}. The current official runtime, starring and MovieGenre pages were cross-checked. Absence in this version is not proof that no equivalent vocabulary exists anywhere; local CREATE/EXTEND decisions are scoped to the checked DBpedia vocabulary and the stated meanings.",
      '', '### Target size','', 'The overview uses 14 main concepts: dbo:Film, Person, Actor, Company, Award, MovieGenre, Country, Language; ex:Contribution, ContributionRole, Filmmaker, ActionFilm, AwardWinningFilm and MultiCreditContributor. Supporting hierarchy, provenance and inferred subsets are listed separately. There are 10 domain inferred classes, including seven additional classes requested in section 13, plus four supporting credit subclasses and the reused Actor inference. This deliberately exceeds the approximate 5–8 final target to satisfy the stronger requirement of seven additional supported classes; no empty classes were added to reach a count.',
      '', '## 2. TABLE 1 — Class inventory','', '| Class / URI | DBpedia equivalent | Action | Parent | Explicit / Inferred | Manchester definition | Source and meaning |','|---|---|---|---|---|---|---|']
    for c in CLASSES:
        lines.append('| '+ ' | '.join([c['name'],c['name'] if c['action']=='REUSE' else 'No matching meaning in checked reference',c['action'],c['parent'],'Inferred' if c['definition'] or c['name'] in ['dbo:Actor','dbo:MovieDirector','dbo:ScreenWriter','dbo:Producer','dbo:Writer'] else 'Base / hierarchy',manchester(c['definition']),c['source']+'; '+c['reason']])+' |')
    lines+=['','## 3. TABLE 2 — Object properties','', '| Property / URI | Reuse / Create | Domain | Range | Inverse | Subproperty | Characteristics | Source / meaning |','|---|---|---|---|---|---|---|---|']
    for p in PROPERTIES:
        if p['kind']=='Object':lines.append('| '+' | '.join([p['name'],p['action'],p['domain'],p['range'],p['inverse'],p['subproperty'],'Functional' if p['functional'] else 'No extra characteristic',p['source']])+' |')
    lines+=['','No symmetric, transitive or inverse-functional flags are added. contributedTo is non-simple because it has a property chain; cardinality is placed on the simple hasContribution property, not contributedTo. Standard owl:sameAs and prov:wasDerivedFrom remain as identity/provenance predicates; they are not custom domain properties.','', '## 4. TABLE 3 — Data properties','', '| Property | Reuse / Create | Domain | Datatype | Cardinality | Crawled source | Meaning |','|---|---|---|---|---|---|---|']
    for p in PROPERTIES:
        if p['kind']=='Data':lines.append('| '+' | '.join([p['name'],p['action'],p['domain'],p['range'],'No global max; one normalized value in this export',p['source'],'Seconds' if p['name']=='dbo:runtime' else p['source']])+' |')
    lines+=['','rdfs:label is reused as an annotation property with language-tagged text; it is intentionally not declared owl:DatatypeProperty. There are 19 object + 5 datatype properties in the design, excluding built-in and metadata predicates.','', '## 5. TABLE 4 — Inferred classes and actual results','', '| Class | DBpedia equivalent | OWL restriction | Real example | Initial facts | New knowledge / local count |','|---|---|---|---|---|---|']
    for c in CLASSES:
        if c['definition'] or c['name'] in ['dbo:Actor','dbo:MovieDirector','dbo:ScreenWriter','dbo:Producer','dbo:Writer']:
            count=report['counts'][c['name']];ex=count['examples'][0] if count['examples'] else 'No member'
            label=str(data.value(URIRef(ex),RDFS.label) or compact(URIRef(ex)))
            lines.append('| '+' | '.join([c['name'],c['name'] if c['action']=='REUSE' else 'No equivalent checked',manchester(c['definition']) if c['definition'] else ('Range(dbo:starring)=dbo:Actor' if c['name']=='dbo:Actor' else 'Credit existential / reused superclass inference'),label+' ('+compact(URIRef(ex))+')','Source triples shown below',f"0 asserted → {count['new']} newly entailed"])+' |')
    chains=[
      ('Film starring Person','dbo:starring range → Actor','Actor ⊑ Artist','Artist ⊑ Person','Person ⊑ Agent'),
      ('Contribution hasRole DirectorRole','hasValue → DirectingContribution','inverse contributionBy → hasContribution','some DirectingContribution → Filmmaker','Person/Agent hierarchy'),
      ('Film genre typed ActionGenre','ActionGenre ⊑ MovieGenre','MovieGenre ⊑ Genre','some ActionGenre → ActionFilm','Parent genre query matches'),
      ('Person directing + writing credits','Role → Directing/WritingContribution','Inverse produces hasContribution','Two existential restrictions → WriterDirector','Filmmaker also follows'),
      ('Person with three credit roles','Different controlled roles','Functional hasRole proves records different','min 3 → ThreeCreditContributor','min 2 → MultiCreditContributor'),
      ('Film ActionGenre + award','Genre hierarchy and award range','ActionFilm / AwardWinningFilm','Intersection → AwardWinningActionFilm','New type absent before'),
      ('Credit person and film links','Inverse hasContribution','hasContribution ∘ contributionTo → contributedTo','dbo:director inverse → directed','directed ⊑ contributedTo')]
    lines+=['','## 6. TABLE 5 — Multi-step chains','', '| Initial facts | Step 1 | Step 2 | Step 3 | Final inference |','|---|---|---|---|---|']
    lines += ['| '+' | '.join(row)+' |' for row in chains]
    lines+=['','## 7. TABLE 6 — Executed SPARQL competency questions','', '| # / Question | SPARQL file | Direct / Reasoned | Before → After rows | Reasoning value |','|---|---|---|---|---|']
    for q in QUERIES:lines.append(f"| {q['number']}. {q['question']} | queries/{q['number']:02}.rq | {q['group']} | {q['asserted_rows']} → {q['reasoned_rows']} | "+('Shared inferred types / relationships' if q['group']=='C' else 'Hierarchy closure' if q['group']=='B' else 'Source facts')+' |')
    lines+=['','Group A queries use asserted.ttl. Group B needs schema and hierarchy closure; group C uses inferred.ttl together with schema + asserted data. Query 27 uses the named graphs in before_after.trig. Entity-result queries restrict results to local resource IRIs and exclude sameAs aliases; the class-count table uses the same local identity scope. Query 8 returns a literal and query 12 returns class URIs, so they use the corresponding value/class scope.','', '## 8. TABLE 7 — Five strongest verified demos','', '| Question | Initial data | DBpedia reuse | Custom rule | Inferred result | Why it matters |','|---|---|---|---|---|---|']
    demos=[('Who is an Actor?','dbo:Actor',14),('Who is a Filmmaker?','ex:Filmmaker',15),('Which films are ActionFilm?','ex:ActionFilm',16),('Who has three provably distinct credits?','ex:ThreeCreditContributor',19),('Which action films received an award?','ex:AwardWinningActionFilm',23)]
    for question,typ,num in demos:
        lines.append('| '+' | '.join([question,'Real source triples below','dbo:Film / Person / Actor / genre / award',manchester(DEFINITIONS.get(typ)) if typ!='dbo:Actor' else 'starring range + hierarchy',str(report['counts'][typ]['new'])+' newly entailed local members','Reusable explicit semantics; before/after verified'])+' |')
    lines+=['','MultiGenreFilm was a preferred demo, but the real DL run inferred zero members. The fourth demo uses genuine min 3 reasoning instead. This meets the cardinality objective without inventing genre inequality.','', '## 9. Five complete Semantic Web demonstrations','']
    for question,typ,num in demos:
        example=URIRef(report['counts'][typ]['examples'][0]);example=RES['person-Q25191'] if typ in ['ex:Filmmaker','ex:ThreeCreditContributor'] else example
        if (example,RDF.type,URIRef(str(DBO if typ.startswith('dbo:') else EX)+typ.split(':')[1])) not in reasoned:raise AssertionError(typ)
        facts=set(data.triples((example,None,None)))
        if typ=='dbo:Actor':facts|=set(data.triples((None,DBO.starring,example)))
        for credit in data.objects(example,EX.hasContribution):facts|=set(data.triples((credit,None,None)))
        for genre in data.objects(example,DBO.genre):facts|=set(data.triples((genre,None,None)))
        keep={RDF.type,EX.hasRole,EX.contributionBy,EX.contributionTo,EX.hasContribution,DBO.starring,DBO.genre,DBO.award}
        selected=[t for t in facts if t[1] in keep]
        # Compact credit witness set: one record per different role is sufficient for the demo.
        if typ in ['ex:Filmmaker','ex:ThreeCreditContributor']:
            credits={};
            for c in sorted(data.objects(example,EX.hasContribution),key=str):credits.setdefault(data.value(c,EX.hasRole),c)
            chosen=set(credits.values());selected=[t for t in selected if (t[0]==example and (t[1]!=EX.hasContribution or t[2] in chosen)) or t[0] in chosen]
        lines+=['### '+question,'','QUESTION: '+question,'','INITIAL TRIPLES:','', '```turtle']
        lines+=sorted(compact(a)+' '+compact(p)+' '+compact(v)+' .' for a,p,v in selected)
        lines+=['```','', 'DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.','', 'ONTOLOGY RULE: '+(manchester(DEFINITIONS.get(typ)) if typ!='dbo:Actor' else 'dbo:starring rdfs:range dbo:Actor; Actor subclass Artist subclass Person subclass Agent.'),'', 'REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.','', 'INFERRED KNOWLEDGE: `'+compact(example)+' rdf:type '+typ+'`. This type has zero direct assertions in the input graph.','', 'SPARQL:','', '```sparql',QUERIES[num-1]['query'],'```','', f"RESULT: {report['counts'][typ]['new']} newly entailed local individuals; example {data.value(example,RDFS.label)} ({compact(example)}).",'', 'WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.','']
    lines+=['## 10. Full definitions, source witnesses and OWL expressions','']
    for c in CLASSES:
        if not c['definition']:continue
        u=URIRef(c['uri']);example=URIRef(report['counts'][c['name']]['examples'][0]);lines+=['### '+c['name'],'', 'REUSE/EXTEND rationale: '+c['reason'],'', 'CRAWLED SUPPORT: '+c['source'],'', 'MANCHESTER: `'+manchester(c['definition'])+'`','', 'OWL EXPRESSION: EquivalentClasses('+c['name']+' '+functional(c['definition'])+')','', 'REAL INDIVIDUAL: '+str(data.value(example,RDFS.label))+' (`'+compact(example)+'`).','', 'ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.','', 'INITIAL FACTS:','', '```turtle']
        facts=[]
        for p in [RDF.type,DBO.genre,DBO.award,DBO.starring]:facts+=list(data.triples((example,p,None)))
        if 'Person' in str(c['parent']) or c['name'] in ['ex:Filmmaker','ex:WriterDirector','ex:ActorFilmmaker','ex:AwardWinningFilmmaker','ex:MultiCreditContributor','ex:ThreeCreditContributor']:
            perrole={}
            for credit in sorted(data.objects(example,EX.hasContribution),key=str):perrole.setdefault(data.value(credit,EX.hasRole),credit)
            for credit in perrole.values():
                facts.append((example,EX.hasContribution,credit));facts+=list(data.triples((credit,EX.hasRole,None)));facts+=list(data.triples((credit,EX.contributionTo,None)));facts+=list(data.triples((credit,RDF.type,None)))
        if c['name']=='ex:ActorFilmmaker':facts+=list(data.triples((None,DBO.starring,example)))
        for genre in data.objects(example,DBO.genre):facts+=list(data.triples((genre,RDF.type,None)))
        if c['name'].endswith('Contribution'):facts+=list(data.triples((example,EX.hasRole,None)))
        lines+=sorted(set(compact(a)+' '+compact(p)+' '+compact(v)+' .' for a,p,v in facts));lines+=['```','', 'NEW KNOWLEDGE: `'+compact(example)+' rdf:type '+c['name']+'`.','']
    lines+=['## 11. Cardinality and validation limitations','', 'Exactly 1 constrains each Contribution endpoint and role. It does not validate completeness under the open-world assumption: an absent filler may exist without an explicit assertion. Structural checks must separately enforce that the exported record contains its three fields.','', 'At least 2 / at least 3 are genuine HermiT results on hasContribution. Example: Christopher Nolan has distinct directing, writing and producing credit records; those records cannot collapse into one because hasRole is functional and DirectorRole, WriterRole and ProducerRole are distinct. No inequality is fabricated for people, genres, awards, companies or films.','', 'The negative MultiGenreFilm test separately adds the requested min 2 genre definition and obtains zero DL members. A production class is excluded because the dataset cannot prove two genre fillers distinct. Future additions require source-supported inequality or a justified identity model; a blanket AllDifferent on Wikidata IDs is not justified by syntax.','', '## 12. Checklist and reproduction','', '- [x] Official DBpedia reference checked and hashed; reused term meanings, domain/range preserved.', '- [x] No ex:Film, Person, Actor, Award, Genre, Language, Country, Company or Organisation clones.', '- [x] Every extension maps to crawled claims or documented source-record metadata.', '- [x] All demo individuals exist in the crawled dataset.', '- [x] All retained defined classes have genuinely inferred members.', '- [x] Equivalent classes, existential/value/cardinality restrictions and hierarchy present.', '- [x] Inverse, subproperty and chain reasoning present; no gratuitous property characteristics.', '- [x] Seven explanatory inference chains and 27 executed competency questions.', '- [x] Five verified demo cases with no false claim that SQL cannot reproduce them.', '- [x] Genuine min 2/min 3 DL results and explicit negative genre-cardinality test.', '- [x] No MP4 videos included; removed at user request.', '- [ ] Zero-result MultiGenreFilm / MultiAwardFilm / FrequentProductionCompany: require additional justified evidence before inclusion.', '- [x] Archived official ontology, official development vocabulary and relevant live term meanings checked; equivalence decisions remain scoped to these references.','', 'Run:','', '```sh', 'make build', 'make reason JAVA=/path/to/java', 'make validate', 'make test', '```','', 'Open ontology/Movie_Knowledge_Graph.owl directly in Protégé; it combines the schema and asserted facts without pre-asserting inferred classes. Start HermiT and inspect the example types; inferred.ttl is exported entailment evidence, not source assertions. before_after.trig supports query 27. Temporary RDF/XML reasoner inputs are removed after each run, preserving one authoritative full OWL export.','', '## References','', '- [Official DBpedia ontology download](https://downloads.dbpedia.org/2016-10/dbpedia_2016-10.owl)', '- [dbo:starring](https://dbpedia.org/ontology/starring)', '- [dbo:runtime](https://dbpedia.org/ontology/runtime)', '- [dbo:MovieGenre](https://dbpedia.org/ontology/MovieGenre)', '- [DBpedia Actor meaning](https://mappings.dbpedia.org/server/ontology/classes/Actor)', '- [W3C OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/)', '- [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)']
    lines += ['', '## Appendix — All executable competency queries', '', 'Namespace identifiers in the tables expand using these prefixes:', '', '```sparql', PREFIX.strip(), '```', '']
    for query in QUERIES:
        lines += ['### Query '+str(query['number'])+' — '+query['question'], '', 'Before / after rows: '+str(query['asserted_rows'])+' / '+str(query['reasoned_rows']), '', '```sparql', query['query'], '```', '']
    (ROOT/'docs/DBpedia_OWL_Design.md').write_text('\n'.join(lines)+'\n')

def functional(e):
    if isinstance(e,URIRef):return compact(e)
    op,*a=e
    if op in ['and','or']:return ('ObjectIntersectionOf' if op=='and' else 'ObjectUnionOf')+'('+' '.join(functional(x) for x in a)+')'
    if op=='some':return 'ObjectSomeValuesFrom('+compact(a[0])+' '+compact(a[1])+')'
    if op=='value':return 'ObjectHasValue('+compact(a[0])+' '+compact(a[1])+')'
    return ('ObjectMinCardinality' if op=='min' else 'ObjectExactCardinality')+'('+str(a[1])+' '+compact(a[0])+' '+compact(a[2])+')'

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--java',required=True);p.add_argument('--reuse-classification',action='store_true');a=p.parse_args();reason(a.java,a.reuse_classification)
