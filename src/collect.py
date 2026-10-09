"""Download real source responses; keep originals, hashes, and retrieval times."""
import argparse
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from urllib.parse import quote
import requests
from common import ROOT, CONFIG, write_json

RAW = ROOT / 'data/raw'
HEADERS = {'User-Agent': 'MovieLOD-CourseProject/1.0 (educational RDF snapshot)', 'Accept': 'application/json'}
_last_wikidata_request = 0.0

def pace_wikidata(provider):
    """Respect the public API's rate limits; cache hits do not incur a delay."""
    global _last_wikidata_request
    if provider != 'Wikidata':
        return
    delay = 6 - (time.monotonic() - _last_wikidata_request)
    if delay > 0:
        time.sleep(delay)
    _last_wikidata_request = time.monotonic()

def fetch(url, provider, refresh=False):
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    path, meta = RAW / (key + '.json'), RAW / (key + '.meta.json')
    if not refresh and path.exists() and meta.exists():
        info = json.loads(meta.read_text())
        if hashlib.sha256(path.read_bytes()).hexdigest() == info['sha256']:
            return json.loads(path.read_bytes()), info
    last_error = None
    for attempt in range(6):
        try:
            pace_wikidata(provider)
            r = requests.get(url, headers=HEADERS, timeout=45)
            if r.status_code == 429:
                try:
                    retry_after = float(r.headers.get('Retry-After', '35'))
                except ValueError:
                    retry_after = 35
                time.sleep(max(35, retry_after))
                raise requests.RequestException('429 rate limited; respected Retry-After')
            r.raise_for_status()
            data = r.json()
            if 'error' in data:
                raise ValueError(str(data['error']))
            info = {'url': url, 'provider': provider,
                    'retrieved_at': datetime.now(timezone.utc).isoformat(),
                    'sha256': hashlib.sha256(r.content).hexdigest(),
                    'path': str(path.relative_to(ROOT)), 'http_status': r.status_code}
            path.write_bytes(r.content)
            write_json(meta, info)
            return data, info
        except (requests.RequestException, ValueError) as e:
            last_error = str(e)
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(provider + ': ' + last_error)

def wd_url(**kwargs):
    params = {'action': 'wbgetentities', 'format': 'json', 'languages': 'en', **kwargs}
    return 'https://www.wikidata.org/w/api.php?' + requests.compat.urlencode(params)

def claim_ids(entity, prop):
    result = []
    for claim in entity.get('claims', {}).get(prop, []):
        if claim.get('rank') == 'deprecated':
            continue
        value = claim.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(value, dict) and value.get('id'):
            result.append(value['id'])
    return sorted(set(result))

def collect(refresh=False):
    RAW.mkdir(parents=True, exist_ok=True)
    snapshots, films, entities, errors = {}, [], {}, []
    titles = CONFIG['seed_titles']
    # Identity is resolved by the exact English Wikipedia sitelink, never fuzzy labels.
    for start in range(0, len(titles), 10):
        batch = titles[start:start+10]
        data, info = fetch(wd_url(sites='enwiki', titles='|'.join(batch), props='labels|descriptions|sitelinks|claims'), 'Wikidata', refresh)
        snapshots[info['url']] = info
        for qid, entity in data.get('entities', {}).items():
            if 'missing' not in entity:
                entities[qid] = entity
                title = entity.get('sitelinks', {}).get('enwiki', {}).get('title')
                if title in batch:
                    films.append({'qid': qid, 'wiki_title': title, 'wikidata_snapshot': info['url']})
        print('Wikidata film batch:', start + len(batch), '/', len(titles), flush=True)
    missing = sorted(set(titles) - {f['wiki_title'] for f in films})
    if missing:
        errors.append({'stage': 'identity', 'missing_titles': missing})
    needed = set()
    for f in films:
        for prop in ['P57', 'P161', 'P58', 'P162', 'P136', 'P495', 'P364', 'P166', 'P272']:
            needed.update(claim_ids(entities[f['qid']], prop))
    for start in range(0, len(needed), 40):
        batch = sorted(needed)[start:start+40]
        data, info = fetch(wd_url(ids='|'.join(batch), props='labels|descriptions|claims'), 'Wikidata', refresh)
        snapshots[info['url']] = info
        for qid, entity in data.get('entities', {}).items():
            if 'missing' not in entity:
                entity['_snapshot_url'] = info['url']
                entities[qid] = entity
        print('Wikidata related batch:', start+len(batch), '/', len(needed), flush=True)
    # Second hop: people can hold their own awards (e.g. Best Actor), distinct from awards the film itself received.
    person_award_ids = set()
    for qid in needed:
        if qid in entities and 'Q5' in claim_ids(entities[qid], 'P31'):
            person_award_ids.update(claim_ids(entities[qid], 'P166'))
    person_award_ids -= set(entities)
    person_award_ids = sorted(person_award_ids)
    for start in range(0, len(person_award_ids), 40):
        batch = person_award_ids[start:start+40]
        data, info = fetch(wd_url(ids='|'.join(batch), props='labels|descriptions'), 'Wikidata', refresh)
        snapshots[info['url']] = info
        for qid, entity in data.get('entities', {}).items():
            if 'missing' not in entity:
                entity['_snapshot_url'] = info['url']
                entities[qid] = entity
        print('Wikidata person-award batch:', start+len(batch), '/', len(person_award_ids), flush=True)
    def get_dbpedia(f):
        uri = 'http://dbpedia.org/resource/' + f['wiki_title'].replace(' ', '_')
        url = 'https://dbpedia.org/data/' + quote(f['wiki_title'].replace(' ', '_'), safe='') + '.json'
        try:
            data, info = fetch(url, 'DBpedia', refresh)
            root = data.get(uri, {})
            types = [v.get('value') for v in root.get('http://www.w3.org/1999/02/22-rdf-syntax-ns#type', [])]
            ok = 'http://dbpedia.org/ontology/Film' in types
            return f, info, uri if ok else None, None if ok else 'DBpedia root is not explicitly Film'
        except RuntimeError as e:
            return f, None, None, str(e)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(get_dbpedia, f) for f in films]
        for future in as_completed(futures):
            f, info, uri, err = future.result()
            if info:
                snapshots[info['url']] = info
                f['dbpedia_snapshot'] = info['url']
            if uri:
                f['dbpedia_uri'] = uri
            if err:
                errors.append({'stage': 'dbpedia', 'film': f['wiki_title'], 'message': err})
            print('DBpedia:', f['wiki_title'], 'OK' if uri else 'not linked', flush=True)
    # Film claims and related labels have their own response-level provenance.
    write_json(ROOT/'data/raw/snapshots.json', sorted(snapshots.values(), key=lambda x:x['url']))
    # Full responses stay in raw/. The normalized staging file keeps only fields used here.
    normalized_entities = {}
    for qid, entity in entities.items():
        normalized_entities[qid] = {
            'id': qid, 'labels': entity.get('labels',{}),
            'sitelinks': {'enwiki':entity.get('sitelinks',{}).get('enwiki',{})},
            'claims': {p:entity.get('claims',{}).get(p,[]) for p in ['P31','P57','P161','P58','P162','P136','P495','P364','P577','P2047','P166','P272']},
            '_snapshot_url': entity.get('_snapshot_url')}
    write_json(ROOT/'data/processed/collected.json', {'films': sorted(films,key=lambda x:x['qid']), 'entities': normalized_entities})
    write_json(ROOT/'evidence/collection.json', {'requested_films': len(titles), 'resolved_films': len(films),
               'snapshots': len(snapshots), 'dbpedia_links': sum(bool(f.get('dbpedia_uri')) for f in films), 'errors': errors})
    if not films:
        raise RuntimeError('No films collected')
    return films

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--refresh', action='store_true', help='Download again instead of using verified cached originals')
    collect(p.parse_args().refresh)
