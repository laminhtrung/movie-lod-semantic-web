"""Author-generated conceptual diagram for the academic report."""
import json
import subprocess
from common import ROOT,write_json

def main():
    target=ROOT/'docs/report_images/academic_framework'
    dot='''digraph study {
      graph [rankdir=LR, bgcolor="white", pad="0.25", nodesep="0.35", ranksep="0.5", dpi=180];
      node [shape=box, style="rounded,filled", fillcolor="#EEF3F5", color="#345469", fontname="Times New Roman", fontsize=16, margin="0.18,0.14"];
      edge [color="#345469", arrowsize=0.7, fontname="Times New Roman", fontsize=13];
      sources [label="Source knowledge\\nWikidata / DBpedia"];
      alignment [label="Entity alignment\\nIdentity + provenance"];
      assertions [label="RDF assertions\\nIndividuals + relations"];
      ontology [label="OWL ontology\\nClasses + axioms", fillcolor="#E5EEE8"];
      inference [label="Semantic inference\\nEntailed membership"];
      queries [label="SPARQL questions\\nRetrieval + aggregation"];
      sources -> alignment -> assertions -> inference -> queries;
      ontology -> inference [label="defines meaning"];
      assertions -> queries [label="stated facts"];
      {rank=same; assertions; ontology;}
    }'''
    target.with_suffix('.dot').write_text(dot)
    subprocess.run(['dot','-Tpng',str(target.with_suffix('.dot')),'-o',str(target.with_suffix('.png'))],check=True)
    path=ROOT/'evidence/report_image_sources.json';report=json.loads(path.read_text())
    relative=str(target.with_suffix('.png').relative_to(ROOT))
    report['images']=[r for r in report['images'] if r['file']!=relative]
    report['images'].append({'file':relative,'source':'Author-generated conceptual framework for MovieLOD','source_type':'author_diagram'})
    write_json(path,report)

if __name__=='__main__':main()
