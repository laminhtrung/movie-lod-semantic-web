"""Run with an environment containing Playwright + Chromium; app must be on port 8000."""
import json
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence/screenshots';OUT.mkdir(parents=True,exist_ok=True)
checks=[]
parser=argparse.ArgumentParser()
parser.add_argument('--port',type=int,default=8000)
args=parser.parse_args()
APP_URL=f'http://127.0.0.1:{args.port}'
with sync_playwright() as p:
    chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    browser=p.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None)
    context=browser.new_context(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page=context.new_page();errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(APP_URL+'/',wait_until='networkidle')
    page.wait_for_function("!document.querySelector('#run').disabled && document.querySelector('#results tbody')")
    assert 'Christopher Nolan' in page.locator('#results').inner_text()
    assert page.locator('html').get_attribute('lang')=='en'
    assert 'Run query' in page.locator('#run').inner_text()
    assert page.locator('#results th').all_text_contents()==['title','year','runtimeSeconds','director']
    page.screenshot(path=str(OUT/'01_app.png'),full_page=False)
    checks.append({'check':'local endpoint UI, Inception','passed':True})
    page.select_option('#sample','3')
    page.wait_for_function("!document.querySelector('#run').disabled")
    assert 'Director' in page.locator('#results').inner_text()
    assert 'Writer' in page.locator('#results').inner_text()
    page.locator('#query-text').fill('not SPARQL')
    page.click('#run');page.wait_for_function("!document.querySelector('#run').disabled")
    assert page.locator('#status').inner_text().startswith('Query error:')
    assert page.locator('#results').inner_text()=='Check the syntax or choose a sample query.'
    page.locator('#query-text').fill('')
    page.click('#run')
    assert page.locator('#status').inner_text()=='Enter a SPARQL query.'
    page.locator('#search').fill('__no_matching_film__')
    assert page.locator('#film-list').inner_text()=='No matching films found.'
    page.locator('#search').fill('')
    page.select_option('#sample','4')
    page.wait_for_function("!document.querySelector('#run').disabled")
    assert page.locator('#results tbody tr').count()>=5
    page.screenshot(path=str(OUT/'02_nolan.png'),full_page=False)
    checks.append({'check':'Nolan query through endpoint','passed':True})
    page.goto(APP_URL+'/resource/film-Q25188',wait_until='networkidle')
    assert page.locator('h1').inner_text()=='Inception'
    assert page.locator('html').get_attribute('lang')=='en'
    assert 'Download RDF (Turtle)' in page.locator('main').inner_text()
    page.screenshot(path=str(OUT/'03_resource.png'),full_page=False)
    checks.append({'check':'IRI HTML and linked-data navigation','passed':True})
    page.goto(APP_URL+'/?browser',wait_until='networkidle')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert 'Christopher Nolan' in page.locator('#results').inner_text(),page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica SELECT','passed':True})
    page.locator('#query-text').fill('PREFIX dbo: <http://dbpedia.org/ontology/> SELECT (COUNT(?f) AS ?count) WHERE { ?f a dbo:Film }'); page.click('#run')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert page.locator('#results tbody tr').count()>0,page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica GROUP BY / COUNT','passed':True})
    page.locator('#query-text').fill('ASK { <https://laminhtrung.github.io/movie-lod-semantic-web/resource/film-Q25188> a <http://dbpedia.org/ontology/Film> }'); page.click('#run')
    page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert 'True' in page.locator('#results').inner_text(),page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica ASK','passed':True})
    page.locator('#query-text').fill('CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 3')
    page.click('#run');page.wait_for_function("!document.querySelector('#run').disabled",timeout=45000)
    assert page.locator('#results pre').count()==1,page.locator('#status').inner_text()
    checks.append({'check':'browser Comunica CONSTRUCT','passed':True})
    page.set_viewport_size({'width':390,'height':844})
    page.goto(APP_URL+'/',wait_until='networkidle')
    page.wait_for_function("!document.querySelector('#run').disabled")
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
    page.screenshot(path=str(OUT/'04_mobile.png'),full_page=True)
    checks.append({'check':'mobile 390px, no page overflow','passed':True})
    assert not errors,errors
    checks.append({'check':'no uncaught browser exceptions','passed':True})
    context.close();browser.close()
(ROOT/'evidence/browser_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
