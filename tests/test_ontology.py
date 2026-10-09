import sys
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, URIRef, XSD
import re
import xml.etree.ElementTree as ET
from rdflib.compare import isomorphic
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from common import ROOT, DBO, EX, RES
from build import schema, timestamp_literal
from reason import infer, DEFINED, RL_DEFINED, CARDINALITY_DEFINED


def test_generated_schema_matches_owl_exports():
    expected = schema()
    assert isomorphic(expected, Graph().parse(ROOT / 'ontology/movie.ttl'))
    assert isomorphic(expected, Graph().parse(ROOT / 'ontology/Movie_Ontology.owl'))
    named = {c for c in expected.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)}
    assert len(named) == 37
    assert all(expected.value(c, RDFS.comment) for c in named)


def test_primary_exports_are_synchronized_and_hermit_safe():
    # Catch RDFLib silently expanding .736 to .736000 during export.
    assert str(timestamp_literal('2026-10-07T14:57:16.736805+00:00')) == '2026-10-07T14:57:16.736+00:00'
    source = ROOT / 'ontology/Movie_Knowledge_Graph.owl'
    data = Graph().parse(ROOT / 'data/processed/movies.ttl')
    assert isomorphic(data, Graph().parse(ROOT / 'data/processed/movies.jsonld', format='json-ld'))
    assert isomorphic(data + schema(), Graph().parse(source))
    values = [node.text for node in ET.parse(source).iter() if node.get('{'+str(RDF)+'}datatype') == str(XSD.dateTime)]
    assert len(values) == 76
    assert all(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}', value) for value in values)


def test_defined_classes_are_inferred_not_asserted():
    """No class in DEFINED is ever directly typed in the crawled data; membership only appears after inference."""
    data = Graph().parse(ROOT / 'data/processed/movies.ttl')
    for name in DEFINED:
        assert not any(data.subjects(RDF.type, EX[name])), f'{name} must not be asserted in the base data'


def test_real_data_classification_matches_sparql_ground_truth():
    data = Graph().parse(ROOT / 'data/processed/movies.ttl')
    g = schema() + data
    errors = infer(g)
    assert not errors

    def local(iterable):
        return {s for s in iterable if isinstance(s, URIRef) and str(s).startswith(str(RES))}

    # Contribution-kind classes must match exactly which role each ex:Contribution carries.
    for role, cls in [(EX.ActorRole, EX.ActingContribution), (EX.DirectorRole, EX.DirectingContribution),
                       (EX.WriterRole, EX.WritingContribution), (EX.ProducerRole, EX.ProducingContribution)]:
        expected = local(data.subjects(EX.hasRole, role))
        assert local(g.subjects(RDF.type, cls)) == expected

    # Person-level classes must match direct SPARQL ground truth over the asserted data.
    actors = local(data.subjects(EX.hasRole, EX.ActorRole))
    acting_people = {data.value(c, EX.contributionBy) for c in actors}
    assert local(g.subjects(RDF.type, DBO.Actor)) == acting_people

    genres = local(data.subjects(RDF.type, EX.ActionGenre))
    expected_films = {f for f in data.subjects(RDF.type,DBO.Film) if set(data.objects(f,DBO.genre)) & genres}
    assert local(g.subjects(RDF.type,EX.ActionFilm))==expected_films
    # Cardinality is loaded from a hash-bound HermiT export, never emulated by COUNT.
    import json,hashlib
    proof=json.loads((ROOT/'evidence/ontology_design/final_owl_checks.json').read_text())
    assert proof['sha256']==hashlib.sha256((ROOT/'ontology/Movie_Knowledge_Graph.owl').read_bytes()).hexdigest()
    dl=Graph().parse(ROOT/'data/processed/inferred_classes.ttl')
    for name,k in [('MultiCreditContributor',2),('ThreeCreditContributor',3)]:
        witnesses={person for person in data.subjects(RDF.type,DBO.Person)
                   if len({data.value(c,EX.hasRole) for c in data.objects(person,EX.hasContribution)})>=k}
        assert local(dl.subjects(RDF.type,EX[name]))==witnesses
    assert not list(dl.subjects(RDF.type,EX.MultiGenreFilm))

    # Known real individuals: Christopher Nolan directs and writes but never acts; Tarantino does both.
    nolan = RES['person-Q25191']
    assert (nolan, RDF.type, EX.Filmmaker) in g
    assert (nolan, RDF.type, DBO.Actor) not in g
    tarantino = RES['person-Q3772']
    assert (tarantino, RDF.type, DBO.Actor) in g
    assert (tarantino, RDF.type, EX.Filmmaker) in g


def test_multi_step_inference_chain_for_a_director():
    """Contribution(hasRole=DirectorRole) -> DirectingContribution -> Filmmaker: a 2-hop chain with no asserted rdf:type."""
    g = schema()
    person, film, contribution = map(URIRef, ['urn:test:person', 'urn:test:film', 'urn:test:contribution'])
    g.add((contribution, RDF.type, EX.Contribution))
    g.add((contribution, EX.contributionBy, person))
    g.add((contribution, EX.contributionTo, film))
    g.add((contribution, EX.hasRole, EX.DirectorRole))
    g.add((person, EX.hasContribution, contribution))
    errors = infer(g)
    assert not errors
    assert (contribution, RDF.type, EX.DirectingContribution) in g
    assert (person, RDF.type, EX.Filmmaker) in g
    assert (person, RDF.type, DBO.Actor) not in g


def test_overlap_open_world_and_disjointness():
    g = schema()
    actor_c, director_c, person = map(URIRef, ['urn:test:actor-contribution', 'urn:test:director-contribution', 'urn:test:person'])
    for contribution, role in [(actor_c, EX.ActorRole), (director_c, EX.DirectorRole)]:
        g.add((contribution, RDF.type, EX.Contribution))
        g.add((contribution, EX.contributionBy, person))
        g.add((contribution, EX.hasRole, role))
        g.add((person, EX.hasContribution, contribution))
    errors = infer(g)
    assert not errors
    # A person can hold several contributions at once: both Actor and Filmmaker, open-world style.
    assert (person, RDF.type, EX.Filmmaker) in g
    g.add((URIRef('urn:test:film'),DBO.starring,person))
    assert not infer(g)
    assert (person,RDF.type,DBO.Actor) in g
    # Conflicting role values in one functional credit produce a real inconsistency.
    g.add((actor_c,EX.hasRole,EX.DirectorRole))
    assert infer(g), 'Different controlled roles cannot collapse through functional hasRole.'
