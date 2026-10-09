"""Verify the deployed browser query engine, including hosting MIME regression."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--url', default='https://laminhtrung.github.io/movie-lod-semantic-web/')
args = parser.parse_args()
samples = json.loads((ROOT/'web/dist/data/queries.json').read_text())
expected = {x['file']: x['result'] for x in json.loads((ROOT/'evidence/query_results.json').read_text())}
checks, errors, responses = [], [], []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    page = browser.new_page(viewport={'width':1440, 'height':1000})
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: responses.append({'url':response.url, 'status':response.status, 'content_type':response.headers.get('content-type')}) if '/data/movies.ttl' in response.url else None)
    page.goto(args.url, wait_until='networkidle', timeout=60000)
    page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
    assert 'Christopher Nolan' in page.locator('#results').inner_text(), page.locator('#status').inner_text()
    for i, sample in enumerate(samples):
        page.select_option('#sample', str(i))
        page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
        status = page.locator('#status').inner_text()
        assert not status.startswith('Query error:'), status
        result = expected[sample['file']]
        if 'boolean' in result:
            assert page.locator('#results').inner_text() == ('True' if result['boolean'] else 'False')
        else:
            assert page.locator('#results tbody tr').count() == len(result['results']['bindings']), sample['file']
        assert not page.locator('#export').is_disabled()
        checks.append({'query':sample['file'], 'status':status, 'passed':True})
    page.select_option('#query-mode','asserted')
    page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
    for query in ['CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 3', 'DESCRIBE <https://laminhtrung.github.io/movie-lod-semantic-web/resource/film-Q25188>']:
        page.locator('#query-text').fill(query)
        page.click('#run')
        page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
        assert page.locator('#results pre').count() == 1, page.locator('#status').inner_text()
        assert page.locator('#results pre').inner_text().strip()
        with page.expect_download() as download:
            page.click('#export')
        assert download.value.suggested_filename == 'query_results.ttl'
        checks.append({'query':query.split()[0], 'status':page.locator('#status').inner_text(), 'passed':True})
    # The same minimum-cardinality ASK must differ between source facts and inference.
    for mode, answer in [('asserted','False'),('reasoned','True')]:
        page.select_option('#query-mode',mode)
        page.locator('#query-text').fill('ASK { <https://laminhtrung.github.io/movie-lod-semantic-web/resource/person-Q25191> a <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#ThreeCreditContributor> }')
        page.click('#run')
        page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
        assert page.locator('#results').inner_text()==answer
        checks.append({'query':'ASK min3 '+mode,'status':answer,'passed':True})
    page.locator('#query-text').fill('not SPARQL')
    page.click('#run')
    page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
    assert page.locator('#status').inner_text().startswith('Query error:')
    assert page.locator('#export').is_disabled()
    page.select_option('#sample', '0')
    page.wait_for_function("!document.querySelector('#run').disabled", timeout=45000)
    assert 'Christopher Nolan' in page.locator('#results').inner_text()
    page.screenshot(path=str(ROOT/'evidence/screenshots/10_public_query_fixed.png'))
    assert not errors, errors
    browser.close()
report = {'url':args.url, 'checked_at':datetime.now(timezone.utc).isoformat(), 'checks':checks, 'invalid_query_recovery':True, 'uncaught_errors':errors, 'dataset_responses':responses}
(ROOT/'evidence/public_query_checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
