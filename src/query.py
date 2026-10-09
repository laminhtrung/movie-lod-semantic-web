"""SPARQL terminal: python src/query.py queries/01.rq [--reasoned]"""
import argparse
from pathlib import Path
from rdflib import Graph, Dataset
from common import ROOT

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('file',type=Path)
    p.add_argument('--reasoned',action='store_true',help='also load ontology/movie.ttl (class hierarchy) and data/processed/inferred_classes.ttl (run src/reason.py first)')
    p.add_argument('--mode',choices=['asserted','reasoned','dataset'])
    args=p.parse_args()
    mode=args.mode or ('reasoned' if args.reasoned else 'asserted')
    g=Graph().parse(ROOT/'data/processed/movies.ttl')
    if mode=='dataset':g=Dataset().parse(ROOT/'data/processed/before_after.trig',format='trig')
    if mode=='reasoned':
        g.parse(ROOT/'ontology/movie.ttl')
        g.parse(ROOT/'data/processed/inferred_classes.ttl')
    result=g.query(args.file.read_text(encoding='utf-8'))
    serialized=result.serialize(format='json' if result.type in ['SELECT','ASK'] else 'turtle')
    print(serialized.decode() if isinstance(serialized,bytes) else serialized)
