"""Set a new canonical publication origin before rebuilding RDF and documents."""
import argparse
import json
from urllib.parse import urlsplit
from common import ROOT,CONFIG,write_json

def rebase(origin):
    origin=origin.rstrip('/')
    url=urlsplit(origin)
    if url.scheme not in ['http','https'] or not url.hostname or url.query or url.fragment:
        raise ValueError('Provide an HTTP(S) base URL without a query or fragment')
    old=CONFIG['base_url'].rstrip('/')
    files=[ROOT/'README.md',ROOT/'web/dist/app.js',ROOT/'evidence/publication.json']
    files+=list((ROOT/'queries').glob('*.rq'))
    for path in files:
        if path.exists():path.write_text(path.read_text(encoding='utf-8').replace(old,origin),encoding='utf-8')
    CONFIG['base_url']=origin;write_json(ROOT/'config.json',CONFIG)
    print('Canonical origin:',origin)
    print('Next: build.py, prepare_web.py, validate.py, make_docs.py')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('origin');rebase(p.parse_args().origin)
