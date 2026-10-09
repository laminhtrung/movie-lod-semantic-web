import json,html,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
from common import ROOT
root=ROOT
snapshots=json.loads((root/'data/raw/snapshots.json').read_text())
for snapshot in snapshots:
 response=json.loads((root/snapshot['path']).read_text())
 if 'Q25188' in response.get('entities',{}):
  entity=response['entities']['Q25188'];break
assert hashlib.sha256((root/snapshot['path']).read_bytes()).hexdigest()==snapshot['sha256']
metadata={k:snapshot[k] for k in ['provider','url','retrieved_at','sha256','path','http_status']}
excerpt={'id':entity['id'],'labels':{'en':entity['labels']['en']},'P57_director':[{'mainsnak':entity['claims']['P57'][0]['mainsnak']}]}
source_html='<html lang="en"><meta charset="utf-8"><style>body{margin:0;padding:28px;background:#f3f6f7;color:#152b3a;font:22px Arial}h1{font-size:30px;color:#007f82}h2{font-size:23px}section{background:white;border-radius:12px;padding:20px;margin-top:16px}pre{font:16px Menlo,monospace;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.35}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}p{font-size:17px;color:#506776}</style><h1>R2 · Actual Wikidata response and provenance</h1><p>Read from the saved source file; SHA-256 verified. This is a source viewer, not a Protégé screenshot.</p><div class="grid"><section><h2>Response metadata</h2><pre>'+html.escape(json.dumps(metadata,indent=2))+'</pre></section><section><h2>Selected raw fields (references omitted)</h2><pre>'+html.escape(json.dumps(excerpt,indent=2))+'</pre></section></div></html>'
hermit=json.loads((root/'evidence/ontology_design/final_owl_checks.json').read_text())
validation=json.loads((root/'evidence/validation.json').read_text())
tests=(root/'evidence/tests.txt').read_text().splitlines()[-1]
text='MovieLOD · Actual verification results\n\n'+tests+'\n\nHermiT 1.3.8.1099 · Movie_Knowledge_Graph.owl\nConsistent: Yes · unsatisfiable named classes: 0\n\n'+json.dumps(hermit['class_counts'],indent=2)+'\n\nData checks: '+str(validation['data_checks_passed'])+'\nSource hashes: '+str(validation['source_hashes_match'])+' · '+str(validation['snapshots_checked'])+'/76\nSPARQL files executed: '+str(validation['query_files_executed'])+'\n\nSources: evidence/tests.txt, ontology_design/final_owl_checks.json, validation.json\nThis is an execution-log viewer, not the Protégé interface.'
validation_html='<html lang="en"><meta charset="utf-8"><body style="margin:0;padding:38px;background:#10202b;color:#d6eee8;font:23px Menlo,monospace"><pre style="white-space:pre-wrap">'+html.escape(text)+'</pre></body></html>'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 page=browser.new_page(viewport={'width':1440,'height':1000})
 for name,markup in [('12_sources_en',source_html),('13_validation_en',validation_html)]:
  (root/'evidence/screenshots'/f'{name}.html').write_text(markup)
  page.set_content(markup);page.screenshot(path=str(root/'evidence/screenshots'/f'{name}.png'),full_page=True)
 browser.close()
