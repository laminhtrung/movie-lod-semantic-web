"""Run Pellet directly on the original OWL files without rewriting their axioms."""
import argparse
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
import owlready2

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--java', default='java')
parser.add_argument('--timeout', type=int, default=300)
parser.add_argument('--realize', action='store_true', help='Also classify individuals in the knowledge graph')
args = parser.parse_args()
classpath = ':'.join(str(p) for p in (Path(owlready2.__file__).parent/'pellet').glob('*.jar'))
checks = []
for name in ['Movie_Ontology', 'Movie_Knowledge_Graph']:
    source = ROOT/'ontology'/f'{name}.owl'
    for action in ['consistency', 'unsat', 'classify'] + (['realize'] if args.realize and name == 'Movie_Knowledge_Graph' else []):
        command = [args.java, '-Xmx2048M', '-cp', classpath, 'pellet.Pellet', action, '--loader', 'OWLAPI', str(source)]
        log = ROOT/'evidence'/f'pellet_{name}_{action}.txt'
        started = time.monotonic()
        with log.open('w') as output:
            result = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT, timeout=args.timeout)
        text = log.read_text()
        passed = result.returncode == 0 and {'consistency':'Consistent: Yes', 'unsat':'Found no unsatisfiable concepts.', 'classify':'owl#Thing', 'realize':'owl#Thing'}[action] in text
        check = {'file':str(source.relative_to(ROOT)), 'sha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'action':action, 'passed':passed, 'exit_code':result.returncode, 'seconds':round(time.monotonic()-started,2), 'log':str(log.relative_to(ROOT))}
        checks.append(check)
        print(json.dumps(check), flush=True)
report = {'reasoner':'Pellet 2.3.1', 'checked_at':datetime.now(timezone.utc).isoformat(), 'input':'Original RDF/XML files loaded directly with OWLAPI', 'checks':checks}
(ROOT/'evidence/pellet_run.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
if not all(c['passed'] for c in checks):
    raise SystemExit('One or more reasoner checks failed; inspect the logs.')
