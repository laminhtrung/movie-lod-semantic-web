"""Record semantic alternatives for every proposed property."""
def main():
    import sys,json,hashlib
    from pathlib import Path
    sys.path.insert(0,'src')
    from common import ROOT,write_json
    out=ROOT/'evidence/ontology_design';m=json.load(open(out/'source_mapping.json'))
    reason={
    'ex:hasContribution':'dbo:occupation links a PersonFunction, not a film-credit record. The local property refers to n-ary source credits.',
    'ex:contributionBy':'dbo:director/writer/starring refer from Work/Film to people; this relation originates from a credit record, so they are not semantically interchangeable.',
    'ex:contributionTo':'The domain is a credit association, not an Agent or Work. This is the film endpoint of the n-ary model.',
    'ex:contributionOf':'Inverse of the film endpoint of the local n-ary association; not a Film-to-Person relation.',
    'ex:hasRole':'dbo:role and dbo:artistFunction have string ranges; the controlled-role entity of a functional credit record has distinct object semantics.',
    'ex:contributedTo':'Covers every collected credit role through a shared chain. director/starring/writer/producer are narrower and opposite-direction properties.',
    'ex:directed':'Inverse of dbo:director; cannot reuse that forward predicate with its arguments reversed. It is also a subproperty of the broader local contributedTo.',
    'ex:actedIn':'Inverse of dbo:starring; forward dbo:starring cannot denote the reversed relation.',
    'ex:productionOf':'Inverse of dbo:productionCompany; preserving direction is necessary for semantic equivalence.',
    'ex:sourceSnapshot':'More specific than prov:wasDerivedFrom: points to a locally saved response record with retrieval timestamp and content hash, not merely any source entity.',
    'ex:releaseYear':'Derived earliest-release-year integer summary from P577. dbo:releaseDate requires a date; dbo:year is a generic gYear and does not express the earliest-release summary. No equivalence or invented full date is asserted.',
    'ex:sourceUrl':'Literal lexical request endpoint stored in the snapshot manifest. DBpedia has no matching request-metadata datatype property in the checked vocabulary; prov:wasDerivedFrom is separately retained as an IRI relation.',
    'ex:retrievedAt':'Retrieval instant of a local response snapshot, not a film releaseDate, generic date, or creation time of the original remote entity.',
    'ex:sha256':'SHA-256 checksum of the exact crawled response bytes, not a generic title, name, code or identifier of the represented film/person.'}
    for p in m['properties']:
     p['semantic_reuse_reason']=reason.get(p['name'],'Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds.')
    m['reference_versions']={'official_archive_sha256':hashlib.sha256((ROOT/'evidence/dbpedia_reference.owl').read_bytes()).hexdigest(),'official_development_url':'https://raw.githubusercontent.com/dbpedia/extraction-framework/master/ontology.owl','official_development_sha256':hashlib.sha256((ROOT/'evidence/dbpedia_development_reference.owl').read_bytes()).hexdigest()}
    write_json(out/'source_mapping.json',m)
    p=ROOT/'docs/DBpedia_OWL_Design.md';s=p.read_text();start=s.find('## Property-by-property semantic reuse audit')
    if start>=0:s=s[:start]+s[s.index('## References',start):]
    section=['## Property-by-property semantic reuse audit','','The comparison checks the relation meaning, argument direction, entity level, range and units; lexical resemblance alone is insufficient.','','| Property | Decision | Semantic comparison |','|---|---|---|']
    section+=['| '+q['name']+' | '+q['action']+' | '+q['semantic_reuse_reason']+' |' for q in m['properties']]
    s=s.replace('## References','\n'.join(section)+'\n\n## References')
    p.write_text(s)

if __name__=="__main__":main()
