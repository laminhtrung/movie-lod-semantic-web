import json
import sys
from pathlib import Path
import pytest
from rdflib import Graph, RDF, URIRef
from rdflib.plugins.sparql import prepareQuery
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from common import EX,RES,DBO,SITE_PATH,site_path
from server import app, DATA

@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()

def query_text(name):return (ROOT/'queries'/name).read_text()

def test_inception_identity_and_normalized_data():
    rows=list(DATA.query(query_text('02.rq')))
    assert rows and all(str(r.title)=='Inception' and str(r.director)=='Christopher Nolan' for r in rows)
    assert all(int(r.year)==2010 and float(r.runtimeSeconds)==8880 for r in rows)

def test_credits_include_role_labels():
    rows=list(DATA.query(query_text('04.rq')))
    assert rows
    assert any(str(r.personName)=='Christopher Nolan' and str(r.roleName)=='Director' for r in rows)
    assert any(str(r.personName)=='Christopher Nolan' and str(r.roleName)=='Writer' for r in rows)

def test_get_and_post_sparql_protocol(client):
    q=query_text('02.rq')
    responses=[client.get('/sparql',query_string={'query':q}),
               client.post('/sparql',data={'query':q}),
               client.post('/sparql',data=q,content_type='application/sparql-query')]
    for r in responses:
        assert r.status_code==200
        assert r.mimetype=='application/sparql-results+json'
        assert r.json['results']['bindings'][0]['title']['value']=='Inception'

def test_ask_and_construct(client):
    assert client.post('/sparql',data='ASK { <https://laminhtrung.github.io/movie-lod-semantic-web/resource/film-Q25188> <http://www.w3.org/2002/07/owl#sameAs> <http://www.wikidata.org/entity/Q25188> }',content_type='application/sparql-query').json['boolean'] is True
    q='CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 3'
    r=client.get('/sparql',query_string={'query':q})
    assert r.status_code==200 and r.mimetype=='text/turtle'
    assert len(Graph().parse(data=r.text,format='turtle'))==3

def test_invalid_and_remote_queries_are_rejected(client):
    assert client.get('/sparql',query_string={'query':'not SPARQL'}).status_code==400
    assert client.get('/sparql',query_string={'query':'SELECT * WHERE { SERVICE <http://example.com/sparql> { ?s ?p ?o } }'}).status_code==400
    assert client.get('/sparql',query_string={'query':'SELECT * FROM <http://example.com/data.ttl> WHERE {?s ?p ?o}'}).status_code==400
    assert client.post('/sparql',data='INSERT DATA { <urn:a> <urn:b> <urn:c> }',content_type='application/sparql-query').status_code==400

def test_real_resource_dereferencing(client):
    r=client.get('/resource/film-Q25188',headers={'Accept':'text/turtle'})
    assert r.status_code==303 and r.headers['Location']==site_path('/describe/film-Q25188.ttl')
    rdf=client.get(r.headers['Location'])
    g=Graph().parse(data=rdf.text,format='turtle')
    assert (RES['film-Q25188'],RDF.type,DBO.Film) in g
    page=client.get('/resource/film-Q25188')
    assert page.status_code==200 and 'application/ld+json' in page.text
    assert client.get('/resource/does-not-exist').status_code==404

def test_dbpedia_class_queries_and_owl_inverse_rule():
    g=Graph().parse(ROOT/'ontology/movie.ttl') + DATA
    person=next(g.objects(RES['film-Q25188'],DBO.director))
    # Standard DBpedia class queries work on the stored graph without inference.
    counts=list(DATA.query('''
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT (COUNT(DISTINCT ?film) AS ?films)
               (COUNT(DISTINCT ?person) AS ?people)
               (COUNT(DISTINCT ?country) AS ?countries)
        WHERE {
          { ?film a dbo:Film }
          UNION { ?person a dbo:Person }
          UNION { ?country a dbo:Country }
        }
    '''))[0]
    assert (int(counts.films),int(counts.people),int(counts.countries)) == (30,851,11)
    assert (person,EX.directed,RES['film-Q25188']) not in DATA
    DeductiveClosure(OWLRL_Semantics).expand(g)
    assert (person,EX.directed,RES['film-Q25188']) in g
    # The director range is still inferred from the reused dbo:Person class.
    probe=Graph().parse(ROOT/'ontology/movie.ttl')
    probe.add((URIRef('urn:test:film'),DBO.director,URIRef('urn:test:director')))
    DeductiveClosure(OWLRL_Semantics).expand(probe)
    assert (URIRef('urn:test:director'),RDF.type,DBO.Person) in probe

def test_data_checks_catch_missing_contribution_person_and_empty_graph():
    from validate import check_data
    g=Graph().parse(ROOT/'data/processed/movies.ttl')
    assert not check_data(g)
    contribution=next(g.subjects(RDF.type,EX.Contribution))
    g.remove((contribution,EX.contributionBy,None))
    assert any(str(contribution) in error and 'contributionBy' in error for error in check_data(g))
    assert check_data(Graph())==['Dataset has no films.']


def test_query_modes_return_genuine_before_after_membership(client):
    q=query_text('20.rq')
    before=client.post('/sparql?mode=asserted',data=q,content_type='application/sparql-query')
    after=client.post('/sparql?mode=reasoned',data=q,content_type='application/sparql-query')
    assert len(before.json['results']['bindings'])==0
    assert len(after.json['results']['bindings'])==10
    named=client.post('/sparql?mode=dataset',data=query_text('27.rq'),content_type='application/sparql-query')
    assert named.status_code==200 and len(named.json['results']['bindings'])==1261
    assert client.get('/sparql',query_string={'mode':'invalid','query':'ASK {}'}).status_code==400


def test_pages_project_prefix_preserves_assets_and_endpoint(client):
    page=client.get(SITE_PATH+'/')
    assert page.status_code==200
    assert 'src="'+SITE_PATH+'/app.js"' in page.text
    assert client.get(SITE_PATH+'/app.js').status_code==200
    result=client.post(SITE_PATH+'/sparql?mode=reasoned',data=query_text('20.rq'),content_type='application/sparql-query')
    assert result.status_code==200 and len(result.json['results']['bindings'])==10
