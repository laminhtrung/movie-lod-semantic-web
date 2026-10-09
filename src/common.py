import json
import re
from urllib.parse import urlsplit
from pathlib import Path
from rdflib import Namespace

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
BASE = CONFIG['base_url'].rstrip('/')
EX = Namespace(BASE + '/ontology#')
RES = Namespace(BASE + '/resource/')
DBO = Namespace('http://dbpedia.org/ontology/')
PROV = Namespace('http://www.w3.org/ns/prov#')
VOID = Namespace('http://rdfs.org/ns/void#')
DCT = Namespace('http://purl.org/dc/terms/')

def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

SITE_PATH = urlsplit(BASE).path.rstrip('/')

def site_path(path):
    """Absolute URL path inside this deployment, including a Pages project prefix."""
    if not path.startswith('/'):
        raise ValueError('Expected a root-relative path')
    if SITE_PATH and (path == SITE_PATH or path.startswith(SITE_PATH + '/')):
        return path
    return SITE_PATH + path

def prefix_html_links(markup):
    """Keep local links within the project when deployed below a domain root."""
    return re.sub(r'((?:href|src)=[\"\'])(/(?!/)[^\"\']*)', lambda m:m.group(1)+site_path(m.group(2)), markup)
