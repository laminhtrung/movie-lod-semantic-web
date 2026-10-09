# DBpedia-based Movie Ontology: Evidence-driven Design

This design is grounded in the existing crawled dataset. Domain facts are not invented. The native build, application and query modes share these version-three definitions and canonical exports.

## 1. Findings and semantic decisions

- Reuse dbo:Film, Person, Actor, Writer, MovieDirector, ScreenWriter, Producer, Company, Organisation, Award, MovieGenre, Genre, Country, Language, Work, Artist and Agent. Actor follows the original dbo:starring range; no equivalent-class override of dbo:Actor.
- Reuse dbo:director, starring, writer, producer, productionCompany, award, genre, country, language and runtime. Preserve reference domain/range: starring ranges over Actor, producer over Agent, productionCompany over Company.
- dbo:MovieDirector, ScreenWriter and Producer are reused for occupation-level inferences from the corresponding credits. One-way subclass axioms suffice; their global definitions are not overridden. - dbo:runtime is seconds (xsd:double); Inception has 8880 seconds, converted from the crawled 148 minutes. Titles reuse rdfs:label (annotation property, not a custom datatype property).
- P577 has varying precision. Keep a documented local releaseYear summary instead of inventing a full dbo:releaseDate. Budget, gross, IMDb, distributors and ratings are excluded because they are not in the collected field set.
- Remove unsupported Documentary/Fiction hierarchy and FeatureFilm assertions: Wikidata Q11424 means film and does not justify feature-film classification. Award labels alone do not justify treating every unrecognized award as a film award.
- ActionGenre and DramaGenre are transparent label-normalization buckets, not source-provided OWL classes. The author-specified classification rule is separate from the crawled facts; fiction/non-fiction is not guessed.
- Contribution and four role individuals represent P57/P161/P58/P162 credits. Each record has exactly one person, film and role. Missing values remain an open-world validation issue, not automatic inconsistency.
- MultiCreditContributor / ThreeCreditContributor mean at least two/three distinct credit records. Different roles provide witnesses; these class names do not prove exactly two/three unique roles across an entire career. More precise display names: MultiCreditContributor / ThreeCreditContributor.
- MultiGenreFilm, MultiAwardFilm and FrequentProductionCompany are not included as inferred classes: different genre/award/film IRIs alone do not establish inequality. COUNT DISTINCT can answer a database-style question, but cannot be presented as OWL DL entailment.

### Reference scope

The official 2016-10 reference and official extraction-framework development vocabulary (790 classes) were checked. Semantic alternatives reviewed include Actor, MovieDirector, ScreenWriter, Producer, Writer, ArtisticGenre, LiteraryGenre, MovieGenre; dbo:occupation ranges over PersonFunction, while dbo:role and artistFunction are strings and cannot replace the local credit-to-role entity link. dbo:year (gYear) is generic, whereas ex:releaseYear explicitly represents an integer earliest-release summary; it does not claim equivalence to dbo:year or a complete releaseDate. The archived reference hash is: a0ca30c8f25cf2d2957639dcad4fd1115f37a856d6d542fd50bba3bf9fa6bf9f. The current official runtime, starring and MovieGenre pages were cross-checked. Absence in this version is not proof that no equivalent vocabulary exists anywhere; local CREATE/EXTEND decisions are scoped to the checked DBpedia vocabulary and the stated meanings.

### Target size

The overview uses 14 main concepts: dbo:Film, Person, Actor, Company, Award, MovieGenre, Country, Language; ex:Contribution, ContributionRole, Filmmaker, ActionFilm, AwardWinningFilm and MultiCreditContributor. Supporting hierarchy, provenance and inferred subsets are listed separately. There are 10 domain inferred classes, including seven additional classes requested in section 13, plus four supporting credit subclasses and the reused Actor inference. This deliberately exceeds the approximate 5–8 final target to satisfy the stronger requirement of seven additional supported classes; no empty classes were added to reach a count.

## 2. TABLE 1 — Class inventory

| Class / URI | DBpedia equivalent | Action | Parent | Explicit / Inferred | Manchester definition | Source and meaning |
|---|---|---|---|---|---|---|
| dbo:Work | dbo:Work | REUSE | — | Base / hierarchy | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Film | dbo:Film | REUSE | dbo:Work | Base / hierarchy | — | P31; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Agent | dbo:Agent | REUSE | — | Base / hierarchy | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Person | dbo:Person | REUSE | dbo:Agent | Base / hierarchy | — | P31=Q5; P57/P161/P58/P162; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Artist | dbo:Artist | REUSE | dbo:Person | Base / hierarchy | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Actor | dbo:Actor | REUSE | dbo:Artist | Inferred | — | P161; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Writer | dbo:Writer | REUSE | dbo:Person | Inferred | — | P58 via ScreenWriter; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:MovieDirector | dbo:MovieDirector | REUSE | dbo:Person | Inferred | — | P57; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:ScreenWriter | dbo:ScreenWriter | REUSE | dbo:Writer | Inferred | — | P58; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Producer | dbo:Producer | REUSE | dbo:Person | Inferred | — | P162; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Organisation | dbo:Organisation | REUSE | dbo:Agent | Base / hierarchy | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Company | dbo:Company | REUSE | dbo:Organisation | Base / hierarchy | — | P272; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Genre | dbo:Genre | REUSE | — | Base / hierarchy | — | P136; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:MovieGenre | dbo:MovieGenre | REUSE | dbo:Genre | Base / hierarchy | — | P136 in film context; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Award | dbo:Award | REUSE | — | Base / hierarchy | — | P166; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Country | dbo:Country | REUSE | — | Base / hierarchy | — | P495; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Language | dbo:Language | REUSE | — | Base / hierarchy | — | P364; Reuse DBpedia meaning and its supported superclass; no local clone. |
| ex:Contribution | No matching meaning in checked reference | CREATE | — | Base / hierarchy | — | P57/P161/P58/P162; A local credit association with one person, film and role; not the person or film itself. |
| ex:ContributionRole | No matching meaning in checked reference | CREATE | — | Base / hierarchy | — | The four crawled credit predicates; Local controlled role values, not subclasses of Person. |
| ex:SourceSnapshot | No matching meaning in checked reference | CREATE | — | Base / hierarchy | — | snapshots.json URL/time/hash; A retrieved response record, not a domain entity. |
| void:Dataset | void:Dataset | REUSE | — | Base / hierarchy | — | Published collection of crawled film records; Reuse VoID dataset, remove ex:Dataset clone. |
| ex:ActionGenre | No matching meaning in checked reference | EXTEND | dbo:MovieGenre | Base / hierarchy | — | P136 target English label; Local normalized film-genre bucket selected by matching the crawled English label; no DBpedia class of this narrow meaning in reference module. |
| ex:DramaGenre | No matching meaning in checked reference | EXTEND | dbo:MovieGenre | Base / hierarchy | — | P136 target English label; Local normalized film-genre bucket selected by matching the crawled English label; no DBpedia class of this narrow meaning in reference module. |
| ex:ActingContribution | No matching meaning in checked reference | EXTEND | ex:Contribution | Inferred | (ex:Contribution and ex:hasRole value ex:ActorRole) | Credit claim corresponding to Actor; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:DirectingContribution | No matching meaning in checked reference | EXTEND | ex:Contribution | Inferred | (ex:Contribution and ex:hasRole value ex:DirectorRole) | Credit claim corresponding to Director; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:WritingContribution | No matching meaning in checked reference | EXTEND | ex:Contribution | Inferred | (ex:Contribution and ex:hasRole value ex:WriterRole) | Credit claim corresponding to Writer; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:ProducingContribution | No matching meaning in checked reference | EXTEND | ex:Contribution | Inferred | (ex:Contribution and ex:hasRole value ex:ProducerRole) | Credit claim corresponding to Producer; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:Filmmaker | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (dbo:Person and (ex:hasContribution some ex:DirectingContribution or ex:hasContribution some ex:WritingContribution or ex:hasContribution some ex:ProducingContribution)) | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:ActionFilm | No matching meaning in checked reference | EXTEND | dbo:Film | Inferred | (dbo:Film and dbo:genre some ex:ActionGenre) | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningFilm | No matching meaning in checked reference | EXTEND | dbo:Film | Inferred | (dbo:Film and dbo:award some dbo:Award) | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:MultiCreditContributor | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (dbo:Person and ex:hasContribution min 2 ex:Contribution) | P57/P161/P58/P162; P166 when award-based; At least two semantically distinct credit records. Different roles prove their distinctness; the name is shorthand and does not exclude repeated same-role credits. |
| ex:ThreeCreditContributor | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (dbo:Person and ex:hasContribution min 3 ex:Contribution) | P57/P161/P58/P162; P166 when award-based; At least three distinct credit records; three different role fillers prove distinctness. Not exactly three roles or an exhaustive career description. |
| ex:WriterDirector | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (dbo:MovieDirector and dbo:ScreenWriter) | P57/P161/P58/P162; P166 when award-based; A person with both directing and writing credits in this dataset; classification is never manually asserted. |
| ex:ActorFilmmaker | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (dbo:Actor and ex:Filmmaker) | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningFilmmaker | No matching meaning in checked reference | EXTEND | dbo:Person | Inferred | (ex:Filmmaker and dbo:award some dbo:Award) | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningActionFilm | No matching meaning in checked reference | EXTEND | dbo:Film | Inferred | (ex:ActionFilm and ex:AwardWinningFilm) | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:GenreCrossingFilm | No matching meaning in checked reference | EXTEND | dbo:Film | Inferred | (dbo:Film and dbo:genre some ex:ActionGenre and dbo:genre some ex:DramaGenre) | P136/P166; Film carrying both action and drama genre memberships; this is not an unproved two-distinct-genre cardinality claim. |

## 3. TABLE 2 — Object properties

| Property / URI | Reuse / Create | Domain | Range | Inverse | Subproperty | Characteristics | Source / meaning |
|---|---|---|---|---|---|---|---|
| dbo:director | REUSE | dbo:Film | dbo:Person | — | — | No extra characteristic | P57 |
| dbo:starring | REUSE | dbo:Work | dbo:Actor | — | — | No extra characteristic | P161 |
| dbo:writer | REUSE | dbo:Work | dbo:Person | — | — | No extra characteristic | P58 |
| dbo:producer | REUSE | dbo:Work | dbo:Agent | — | — | No extra characteristic | P162 |
| dbo:productionCompany | REUSE | dbo:Work | dbo:Company | — | — | No extra characteristic | P272 |
| dbo:award | REUSE | — | dbo:Award | — | — | No extra characteristic | P166 |
| dbo:genre | REUSE | — | dbo:Genre | — | — | No extra characteristic | P136 |
| dbo:country | REUSE | — | dbo:Country | — | — | No extra characteristic | P495 |
| dbo:language | REUSE | — | dbo:Language | — | — | No extra characteristic | P364 |
| ex:hasContribution | CREATE | dbo:Person | ex:Contribution | ex:contributionBy | — | No extra characteristic | Derived credit association |
| ex:contributionBy | CREATE | ex:Contribution | dbo:Person | — | — | Functional | P57/P161/P58/P162 |
| ex:contributionTo | CREATE | ex:Contribution | dbo:Film | ex:contributionOf | — | Functional | Containing source film |
| ex:contributionOf | CREATE | dbo:Film | ex:Contribution | — | — | No extra characteristic | Inverse of contributionTo |
| ex:hasRole | CREATE | ex:Contribution | ex:ContributionRole | — | — | Functional | Credit predicate to controlled role |
| ex:contributedTo | CREATE | dbo:Person | dbo:Film | — | — | No extra characteristic | OWL property chain |
| ex:directed | CREATE | dbo:Person | dbo:Film | dbo:director | ex:contributedTo | No extra characteristic | Inverse P57 |
| ex:actedIn | CREATE | dbo:Actor | dbo:Film | dbo:starring | ex:contributedTo | No extra characteristic | Inverse P161 |
| ex:productionOf | CREATE | dbo:Company | dbo:Work | dbo:productionCompany | — | No extra characteristic | Inverse P272 |
| ex:sourceSnapshot | CREATE | — | ex:SourceSnapshot | — | — | No extra characteristic | Crawled entity response provenance |

No symmetric, transitive or inverse-functional flags are added. contributedTo is non-simple because it has a property chain; cardinality is placed on the simple hasContribution property, not contributedTo. Standard owl:sameAs and prov:wasDerivedFrom remain as identity/provenance predicates; they are not custom domain properties.

## 4. TABLE 3 — Data properties

| Property | Reuse / Create | Domain | Datatype | Cardinality | Crawled source | Meaning |
|---|---|---|---|---|---|---|
| dbo:runtime | REUSE | dbo:Work | xsd:double | No global max; one normalized value in this export | P2047; normalize to seconds | Seconds |
| ex:releaseYear | CREATE | dbo:Film | xsd:integer | No global max; one normalized value in this export | Earliest Gregorian P577 year, precision >=9 | Earliest Gregorian P577 year, precision >=9 |
| ex:sourceUrl | CREATE | ex:SourceSnapshot | xsd:anyURI | No global max; one normalized value in this export | Snapshot manifest sourceUrl | Snapshot manifest sourceUrl |
| ex:retrievedAt | CREATE | ex:SourceSnapshot | xsd:dateTime | No global max; one normalized value in this export | Snapshot manifest retrievedAt | Snapshot manifest retrievedAt |
| ex:sha256 | CREATE | ex:SourceSnapshot | xsd:string | No global max; one normalized value in this export | Snapshot manifest sha256 | Snapshot manifest sha256 |

rdfs:label is reused as an annotation property with language-tagged text; it is intentionally not declared owl:DatatypeProperty. There are 19 object + 5 datatype properties in the design, excluding built-in and metadata predicates.

## 5. TABLE 4 — Inferred classes and actual results

| Class | DBpedia equivalent | OWL restriction | Real example | Initial facts | New knowledge / local count |
|---|---|---|---|---|---|
| dbo:Actor | dbo:Actor | Range(dbo:starring)=dbo:Actor | Burr Steers (res:person-Q1016897) | Source triples shown below | 0 asserted → 769 newly entailed |
| dbo:Writer | dbo:Writer | Credit existential / reused superclass inference | Philippa Boyens (res:person-Q116854) | Source triples shown below | 0 asserted → 34 newly entailed |
| dbo:MovieDirector | dbo:MovieDirector | Credit existential / reused superclass inference | Damien Chazelle (res:person-Q18350026) | Source triples shown below | 0 asserted → 17 newly entailed |
| dbo:ScreenWriter | dbo:ScreenWriter | Credit existential / reused superclass inference | Philippa Boyens (res:person-Q116854) | Source triples shown below | 0 asserted → 34 newly entailed |
| dbo:Producer | dbo:Producer | Credit existential / reused superclass inference | Fran Walsh (res:person-Q116861) | Source triples shown below | 0 asserted → 57 newly entailed |
| ex:ActingContribution | No equivalent checked | (ex:Contribution and ex:hasRole value ex:ActorRole) | Alien — actor — Sigourney Weaver (res:contribution-Q103569-Q102124-actor) | Source triples shown below | 0 asserted → 855 newly entailed |
| ex:DirectingContribution | No equivalent checked | (ex:Contribution and ex:hasRole value ex:DirectorRole) | Alien — director — Ridley Scott (res:contribution-Q103569-Q56005-director) | Source triples shown below | 0 asserted → 31 newly entailed |
| ex:WritingContribution | No equivalent checked | (ex:Contribution and ex:hasRole value ex:WriterRole) | Alien — writer — Ronald Shusett (res:contribution-Q103569-Q3056094-writer) | Source triples shown below | 0 asserted → 51 newly entailed |
| ex:ProducingContribution | No equivalent checked | (ex:Contribution and ex:hasRole value ex:ProducerRole) | Alien — producer — Gordon Carroll (res:contribution-Q103569-Q1537983-producer) | Source triples shown below | 0 asserted → 73 newly entailed |
| ex:Filmmaker | No equivalent checked | (dbo:Person and (ex:hasContribution some ex:DirectingContribution or ex:hasContribution some ex:WritingContribution or ex:hasContribution some ex:ProducingContribution)) | Philippa Boyens (res:person-Q116854) | Source triples shown below | 0 asserted → 89 newly entailed |
| ex:ActionFilm | No equivalent checked | (dbo:Film and dbo:genre some ex:ActionGenre) | Alien (res:film-Q103569) | Source triples shown below | 0 asserted → 12 newly entailed |
| ex:AwardWinningFilm | No equivalent checked | (dbo:Film and dbo:award some dbo:Award) | Alien (res:film-Q103569) | Source triples shown below | 0 asserted → 26 newly entailed |
| ex:MultiCreditContributor | No equivalent checked | (dbo:Person and ex:hasContribution min 2 ex:Contribution) | Fran Walsh (res:person-Q116861) | Source triples shown below | 0 asserted → 17 newly entailed |
| ex:ThreeCreditContributor | No equivalent checked | (dbo:Person and ex:hasContribution min 3 ex:Contribution) | Christopher Nolan (res:person-Q25191) | Source triples shown below | 0 asserted → 7 newly entailed |
| ex:WriterDirector | No equivalent checked | (dbo:MovieDirector and dbo:ScreenWriter) | Damien Chazelle (res:person-Q18350026) | Source triples shown below | 0 asserted → 10 newly entailed |
| ex:ActorFilmmaker | No equivalent checked | (dbo:Actor and ex:Filmmaker) | Quentin Tarantino (res:person-Q3772) | Source triples shown below | 0 asserted → 7 newly entailed |
| ex:AwardWinningFilmmaker | No equivalent checked | (ex:Filmmaker and dbo:award some dbo:Award) | Philippa Boyens (res:person-Q116854) | Source triples shown below | 0 asserted → 65 newly entailed |
| ex:AwardWinningActionFilm | No equivalent checked | (ex:ActionFilm and ex:AwardWinningFilm) | Alien (res:film-Q103569) | Source triples shown below | 0 asserted → 10 newly entailed |
| ex:GenreCrossingFilm | No equivalent checked | (dbo:Film and dbo:genre some ex:ActionGenre and dbo:genre some ex:DramaGenre) | Pulp Fiction (res:film-Q104123) | Source triples shown below | 0 asserted → 8 newly entailed |

## 6. TABLE 5 — Multi-step chains

| Initial facts | Step 1 | Step 2 | Step 3 | Final inference |
|---|---|---|---|---|
| Film starring Person | dbo:starring range → Actor | Actor ⊑ Artist | Artist ⊑ Person | Person ⊑ Agent |
| Contribution hasRole DirectorRole | hasValue → DirectingContribution | inverse contributionBy → hasContribution | some DirectingContribution → Filmmaker | Person/Agent hierarchy |
| Film genre typed ActionGenre | ActionGenre ⊑ MovieGenre | MovieGenre ⊑ Genre | some ActionGenre → ActionFilm | Parent genre query matches |
| Person directing + writing credits | Role → Directing/WritingContribution | Inverse produces hasContribution | Two existential restrictions → WriterDirector | Filmmaker also follows |
| Person with three credit roles | Different controlled roles | Functional hasRole proves records different | min 3 → ThreeCreditContributor | min 2 → MultiCreditContributor |
| Film ActionGenre + award | Genre hierarchy and award range | ActionFilm / AwardWinningFilm | Intersection → AwardWinningActionFilm | New type absent before |
| Credit person and film links | Inverse hasContribution | hasContribution ∘ contributionTo → contributedTo | dbo:director inverse → directed | directed ⊑ contributedTo |

## 7. TABLE 6 — Executed SPARQL competency questions

| # / Question | SPARQL file | Direct / Reasoned | Before → After rows | Reasoning value |
|---|---|---|---|---|
| 1. List films | queries/01.rq | A | 30 → 30 | Source facts |
| 2. Inception: year, duration and director | queries/02.rq | A | 1 → 1 | Source facts |
| 3. Directors of Inception | queries/03.rq | A | 1 → 1 | Source facts |
| 4. Inception credits and roles | queries/04.rq | A | 25 → 25 | Source facts |
| 5. Films directed by Nolan | queries/05.rq | A | 8 → 8 | Source facts |
| 6. Companies credited on Inception | queries/06.rq | A | 4 → 4 | Source facts |
| 7. Awards of Inception | queries/07.rq | A | 7 → 7 | Source facts |
| 8. Runtime in seconds | queries/08.rq | A | 1 → 1 | Source facts |
| 9. Film genres through the parent class | queries/09.rq | B | 0 → 75 | Hierarchy closure |
| 10. Persons through Agent hierarchy | queries/10.rq | B | 0 → 851 | Hierarchy closure |
| 11. Production companies | queries/11.rq | B | 45 → 45 | Hierarchy closure |
| 12. Film subclasses | queries/12.rq | B | 0 → 4 | Hierarchy closure |
| 13. Actors through Artist hierarchy | queries/13.rq | B | 0 → 769 | Hierarchy closure |
| 14. Inferred Actors | queries/14.rq | C | 0 → 769 | Shared inferred types / relationships |
| 15. Inferred Filmmakers | queries/15.rq | C | 0 → 89 | Shared inferred types / relationships |
| 16. Inferred Action films | queries/16.rq | C | 0 → 12 | Shared inferred types / relationships |
| 17. Award-winning films | queries/17.rq | C | 0 → 26 | Shared inferred types / relationships |
| 18. People with at least two provably distinct credits | queries/18.rq | C | 0 → 17 | Shared inferred types / relationships |
| 19. People with at least three provably distinct credits | queries/19.rq | C | 0 → 7 | Shared inferred types / relationships |
| 20. Writer-directors | queries/20.rq | C | 0 → 10 | Shared inferred types / relationships |
| 21. Actor-filmmakers | queries/21.rq | C | 0 → 7 | Shared inferred types / relationships |
| 22. Award-winning filmmakers | queries/22.rq | C | 0 → 65 | Shared inferred types / relationships |
| 23. Award-winning action films | queries/23.rq | C | 0 → 10 | Shared inferred types / relationships |
| 24. Action/drama crossing films | queries/24.rq | C | 0 → 8 | Shared inferred types / relationships |
| 25. Nolan contributions through property chain | queries/25.rq | C | 0 → 8 | Shared inferred types / relationships |
| 26. Nolan films through inverse director | queries/26.rq | C | 0 → 8 | Shared inferred types / relationships |
| 27. Types present only after reasoning | queries/27.rq | C | 0 → 1261 | Shared inferred types / relationships |

Group A queries use asserted.ttl. Group B needs schema and hierarchy closure; group C uses inferred.ttl together with schema + asserted data. Query 27 uses the named graphs in before_after.trig. Entity-result queries restrict results to local resource IRIs and exclude sameAs aliases; the class-count table uses the same local identity scope. Query 8 returns a literal and query 12 returns class URIs, so they use the corresponding value/class scope.

## 8. TABLE 7 — Five strongest verified demos

| Question | Initial data | DBpedia reuse | Custom rule | Inferred result | Why it matters |
|---|---|---|---|---|---|
| Who is an Actor? | Real source triples below | dbo:Film / Person / Actor / genre / award | starring range + hierarchy | 769 newly entailed local members | Reusable explicit semantics; before/after verified |
| Who is a Filmmaker? | Real source triples below | dbo:Film / Person / Actor / genre / award | (dbo:Person and (ex:hasContribution some ex:DirectingContribution or ex:hasContribution some ex:WritingContribution or ex:hasContribution some ex:ProducingContribution)) | 89 newly entailed local members | Reusable explicit semantics; before/after verified |
| Which films are ActionFilm? | Real source triples below | dbo:Film / Person / Actor / genre / award | (dbo:Film and dbo:genre some ex:ActionGenre) | 12 newly entailed local members | Reusable explicit semantics; before/after verified |
| Who has three provably distinct credits? | Real source triples below | dbo:Film / Person / Actor / genre / award | (dbo:Person and ex:hasContribution min 3 ex:Contribution) | 7 newly entailed local members | Reusable explicit semantics; before/after verified |
| Which action films received an award? | Real source triples below | dbo:Film / Person / Actor / genre / award | (ex:ActionFilm and ex:AwardWinningFilm) | 10 newly entailed local members | Reusable explicit semantics; before/after verified |

MultiGenreFilm was a preferred demo, but the real DL run inferred zero members. The fourth demo uses genuine min 3 reasoning instead. This meets the cardinality objective without inventing genre inequality.

## 9. Five complete Semantic Web demonstrations

### Who is an Actor?

QUESTION: Who is an Actor?

INITIAL TRIPLES:

```turtle
res:contribution-Q104123-Q1016897-actor ex:contributionBy res:person-Q1016897 .
res:contribution-Q104123-Q1016897-actor ex:contributionTo res:film-Q104123 .
res:contribution-Q104123-Q1016897-actor ex:hasRole ex:ActorRole .
res:contribution-Q104123-Q1016897-actor http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:film-Q104123 dbo:starring res:person-Q1016897 .
res:person-Q1016897 ex:hasContribution res:contribution-Q104123-Q1016897-actor .
res:person-Q1016897 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.

ONTOLOGY RULE: dbo:starring rdfs:range dbo:Actor; Actor subclass Artist subclass Person subclass Agent.

REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.

INFERRED KNOWLEDGE: `res:person-Q1016897 rdf:type dbo:Actor`. This type has zero direct assertions in the input graph.

SPARQL:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Actor . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

RESULT: 769 newly entailed local individuals; example Burr Steers (res:person-Q1016897).

WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.

### Who is a Filmmaker?

QUESTION: Who is a Filmmaker?

INITIAL TRIPLES:

```turtle
res:contribution-Q13417189-Q25191-director ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-director ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-director ex:hasRole ex:DirectorRole .
res:contribution-Q13417189-Q25191-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-producer ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-producer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-producer ex:hasRole ex:ProducerRole .
res:contribution-Q13417189-Q25191-producer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-writer ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-writer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-writer ex:hasRole ex:WriterRole .
res:contribution-Q13417189-Q25191-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q25191 dbo:award res:award-Q102427 .
res:person-Q25191 dbo:award res:award-Q103360 .
res:person-Q25191 dbo:award res:award-Q105447 .
res:person-Q25191 dbo:award res:award-Q1056240 .
res:person-Q25191 dbo:award res:award-Q12143912 .
res:person-Q25191 dbo:award res:award-Q12201477 .
res:person-Q25191 dbo:award res:award-Q16058279 .
res:person-Q25191 dbo:award res:award-Q3405197 .
res:person-Q25191 dbo:award res:award-Q586356 .
res:person-Q25191 dbo:award res:award-Q787131 .
res:person-Q25191 dbo:award res:award-Q833154 .
res:person-Q25191 dbo:award res:award-Q833163 .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-director .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-producer .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-writer .
res:person-Q25191 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.

ONTOLOGY RULE: (dbo:Person and (ex:hasContribution some ex:DirectingContribution or ex:hasContribution some ex:WritingContribution or ex:hasContribution some ex:ProducingContribution))

REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.

INFERRED KNOWLEDGE: `res:person-Q25191 rdf:type ex:Filmmaker`. This type has zero direct assertions in the input graph.

SPARQL:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:Filmmaker . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

RESULT: 89 newly entailed local individuals; example Christopher Nolan (res:person-Q25191).

WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.

### Which films are ActionFilm?

QUESTION: Which films are ActionFilm?

INITIAL TRIPLES:

```turtle
res:film-Q103569 dbo:award res:award-Q1131772 .
res:film-Q103569 dbo:award res:award-Q1257399 .
res:film-Q103569 dbo:award res:award-Q1265702 .
res:film-Q103569 dbo:award res:award-Q3414212 .
res:film-Q103569 dbo:award res:award-Q393686 .
res:film-Q103569 dbo:award res:award-Q739633 .
res:film-Q103569 dbo:genre res:genre-Q102260466 .
res:film-Q103569 dbo:genre res:genre-Q10663882 .
res:film-Q103569 dbo:genre res:genre-Q11304653 .
res:film-Q103569 dbo:genre res:genre-Q1200678 .
res:film-Q103569 dbo:genre res:genre-Q1342372 .
res:film-Q103569 dbo:genre res:genre-Q157394 .
res:film-Q103569 dbo:genre res:genre-Q1776156 .
res:film-Q103569 dbo:genre res:genre-Q188473 .
res:film-Q103569 dbo:genre res:genre-Q200092 .
res:film-Q103569 dbo:genre res:genre-Q20656232 .
res:film-Q103569 dbo:genre res:genre-Q2484376 .
res:film-Q103569 dbo:genre res:genre-Q319221 .
res:film-Q103569 dbo:genre res:genre-Q471839 .
res:film-Q103569 dbo:starring res:person-Q102124 .
res:film-Q103569 dbo:starring res:person-Q200405 .
res:film-Q103569 dbo:starring res:person-Q223091 .
res:film-Q103569 dbo:starring res:person-Q266270 .
res:film-Q103569 dbo:starring res:person-Q283872 .
res:film-Q103569 dbo:starring res:person-Q3047302 .
res:film-Q103569 dbo:starring res:person-Q314290 .
res:film-Q103569 dbo:starring res:person-Q320093 .
res:film-Q103569 dbo:starring res:person-Q323185 .
res:film-Q103569 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q102260466 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q10663882 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1200678 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1342372 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q157394 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1776156 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q200092 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q319221 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q471839 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.

ONTOLOGY RULE: (dbo:Film and dbo:genre some ex:ActionGenre)

REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.

INFERRED KNOWLEDGE: `res:film-Q103569 rdf:type ex:ActionFilm`. This type has zero direct assertions in the input graph.

SPARQL:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:ActionFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

RESULT: 12 newly entailed local individuals; example Alien (res:film-Q103569).

WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.

### Who has three provably distinct credits?

QUESTION: Who has three provably distinct credits?

INITIAL TRIPLES:

```turtle
res:contribution-Q13417189-Q25191-director ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-director ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-director ex:hasRole ex:DirectorRole .
res:contribution-Q13417189-Q25191-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-producer ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-producer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-producer ex:hasRole ex:ProducerRole .
res:contribution-Q13417189-Q25191-producer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-writer ex:contributionBy res:person-Q25191 .
res:contribution-Q13417189-Q25191-writer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-writer ex:hasRole ex:WriterRole .
res:contribution-Q13417189-Q25191-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q25191 dbo:award res:award-Q102427 .
res:person-Q25191 dbo:award res:award-Q103360 .
res:person-Q25191 dbo:award res:award-Q105447 .
res:person-Q25191 dbo:award res:award-Q1056240 .
res:person-Q25191 dbo:award res:award-Q12143912 .
res:person-Q25191 dbo:award res:award-Q12201477 .
res:person-Q25191 dbo:award res:award-Q16058279 .
res:person-Q25191 dbo:award res:award-Q3405197 .
res:person-Q25191 dbo:award res:award-Q586356 .
res:person-Q25191 dbo:award res:award-Q787131 .
res:person-Q25191 dbo:award res:award-Q833154 .
res:person-Q25191 dbo:award res:award-Q833163 .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-director .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-producer .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-writer .
res:person-Q25191 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.

ONTOLOGY RULE: (dbo:Person and ex:hasContribution min 3 ex:Contribution)

REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.

INFERRED KNOWLEDGE: `res:person-Q25191 rdf:type ex:ThreeCreditContributor`. This type has zero direct assertions in the input graph.

SPARQL:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:ThreeCreditContributor . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

RESULT: 7 newly entailed local individuals; example Christopher Nolan (res:person-Q25191).

WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.

### Which action films received an award?

QUESTION: Which action films received an award?

INITIAL TRIPLES:

```turtle
res:film-Q103569 dbo:award res:award-Q1131772 .
res:film-Q103569 dbo:award res:award-Q1257399 .
res:film-Q103569 dbo:award res:award-Q1265702 .
res:film-Q103569 dbo:award res:award-Q3414212 .
res:film-Q103569 dbo:award res:award-Q393686 .
res:film-Q103569 dbo:award res:award-Q739633 .
res:film-Q103569 dbo:genre res:genre-Q102260466 .
res:film-Q103569 dbo:genre res:genre-Q10663882 .
res:film-Q103569 dbo:genre res:genre-Q11304653 .
res:film-Q103569 dbo:genre res:genre-Q1200678 .
res:film-Q103569 dbo:genre res:genre-Q1342372 .
res:film-Q103569 dbo:genre res:genre-Q157394 .
res:film-Q103569 dbo:genre res:genre-Q1776156 .
res:film-Q103569 dbo:genre res:genre-Q188473 .
res:film-Q103569 dbo:genre res:genre-Q200092 .
res:film-Q103569 dbo:genre res:genre-Q20656232 .
res:film-Q103569 dbo:genre res:genre-Q2484376 .
res:film-Q103569 dbo:genre res:genre-Q319221 .
res:film-Q103569 dbo:genre res:genre-Q471839 .
res:film-Q103569 dbo:starring res:person-Q102124 .
res:film-Q103569 dbo:starring res:person-Q200405 .
res:film-Q103569 dbo:starring res:person-Q223091 .
res:film-Q103569 dbo:starring res:person-Q266270 .
res:film-Q103569 dbo:starring res:person-Q283872 .
res:film-Q103569 dbo:starring res:person-Q3047302 .
res:film-Q103569 dbo:starring res:person-Q314290 .
res:film-Q103569 dbo:starring res:person-Q320093 .
res:film-Q103569 dbo:starring res:person-Q323185 .
res:film-Q103569 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q102260466 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q10663882 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1200678 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1342372 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q157394 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1776156 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q200092 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q319221 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q471839 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

DBPEDIA VOCABULARY: dbo:Film, dbo:Person, dbo:Actor and the source-supported properties in Table 2.

ONTOLOGY RULE: (ex:ActionFilm and ex:AwardWinningFilm)

REASONING: The source relation supplies existential witnesses. Supporting credit classes follow role hasValue restrictions. For min 3, the three role individuals are distinct by their controlled meanings; functional hasRole forces the corresponding credits to be distinct. HermiT classified the complete graph.

INFERRED KNOWLEDGE: `res:film-Q103569 rdf:type ex:AwardWinningActionFilm`. This type has zero direct assertions in the input graph.

SPARQL:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:AwardWinningActionFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

RESULT: 10 newly entailed local individuals; example Alien (res:film-Q103569).

WHY THIS DEMONSTRATES SEMANTIC WEB: The ontology makes the classification and shared vocabulary explicit and reusable across consumers. SQL joins, recursive queries and rule systems can reproduce many of these answers; the advantage is declared semantics, interoperable identifiers, open-world entailment and consistency checking, not an inability of databases to compute them.

## 10. Full definitions, source witnesses and OWL expressions

### ex:ActingContribution

REUSE/EXTEND rationale: Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record.

CRAWLED SUPPORT: Credit claim corresponding to Actor

MANCHESTER: `(ex:Contribution and ex:hasRole value ex:ActorRole)`

OWL EXPRESSION: EquivalentClasses(ex:ActingContribution ObjectIntersectionOf(ex:Contribution ObjectHasValue(ex:hasRole ex:ActorRole)))

REAL INDIVIDUAL: Alien — actor — Sigourney Weaver (`res:contribution-Q103569-Q102124-actor`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q103569-Q102124-actor ex:hasRole ex:ActorRole .
res:contribution-Q103569-Q102124-actor http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
```

NEW KNOWLEDGE: `res:contribution-Q103569-Q102124-actor rdf:type ex:ActingContribution`.

### ex:DirectingContribution

REUSE/EXTEND rationale: Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record.

CRAWLED SUPPORT: Credit claim corresponding to Director

MANCHESTER: `(ex:Contribution and ex:hasRole value ex:DirectorRole)`

OWL EXPRESSION: EquivalentClasses(ex:DirectingContribution ObjectIntersectionOf(ex:Contribution ObjectHasValue(ex:hasRole ex:DirectorRole)))

REAL INDIVIDUAL: Alien — director — Ridley Scott (`res:contribution-Q103569-Q56005-director`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q103569-Q56005-director ex:hasRole ex:DirectorRole .
res:contribution-Q103569-Q56005-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
```

NEW KNOWLEDGE: `res:contribution-Q103569-Q56005-director rdf:type ex:DirectingContribution`.

### ex:WritingContribution

REUSE/EXTEND rationale: Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record.

CRAWLED SUPPORT: Credit claim corresponding to Writer

MANCHESTER: `(ex:Contribution and ex:hasRole value ex:WriterRole)`

OWL EXPRESSION: EquivalentClasses(ex:WritingContribution ObjectIntersectionOf(ex:Contribution ObjectHasValue(ex:hasRole ex:WriterRole)))

REAL INDIVIDUAL: Alien — writer — Ronald Shusett (`res:contribution-Q103569-Q3056094-writer`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q103569-Q3056094-writer ex:hasRole ex:WriterRole .
res:contribution-Q103569-Q3056094-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
```

NEW KNOWLEDGE: `res:contribution-Q103569-Q3056094-writer rdf:type ex:WritingContribution`.

### ex:ProducingContribution

REUSE/EXTEND rationale: Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record.

CRAWLED SUPPORT: Credit claim corresponding to Producer

MANCHESTER: `(ex:Contribution and ex:hasRole value ex:ProducerRole)`

OWL EXPRESSION: EquivalentClasses(ex:ProducingContribution ObjectIntersectionOf(ex:Contribution ObjectHasValue(ex:hasRole ex:ProducerRole)))

REAL INDIVIDUAL: Alien — producer — Gordon Carroll (`res:contribution-Q103569-Q1537983-producer`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q103569-Q1537983-producer ex:hasRole ex:ProducerRole .
res:contribution-Q103569-Q1537983-producer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
```

NEW KNOWLEDGE: `res:contribution-Q103569-Q1537983-producer rdf:type ex:ProducingContribution`.

### ex:Filmmaker

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(dbo:Person and (ex:hasContribution some ex:DirectingContribution or ex:hasContribution some ex:WritingContribution or ex:hasContribution some ex:ProducingContribution))`

OWL EXPRESSION: EquivalentClasses(ex:Filmmaker ObjectIntersectionOf(dbo:Person ObjectUnionOf(ObjectSomeValuesFrom(ex:hasContribution ex:DirectingContribution) ObjectSomeValuesFrom(ex:hasContribution ex:WritingContribution) ObjectSomeValuesFrom(ex:hasContribution ex:ProducingContribution))))

REAL INDIVIDUAL: Philippa Boyens (`res:person-Q116854`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q127367-Q116854-writer ex:contributionTo res:film-Q127367 .
res:contribution-Q127367-Q116854-writer ex:hasRole ex:WriterRole .
res:contribution-Q127367-Q116854-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q116854 dbo:award res:award-Q1056240 .
res:person-Q116854 dbo:award res:award-Q107258 .
res:person-Q116854 dbo:award res:award-Q1075366 .
res:person-Q116854 dbo:award res:award-Q23050104 .
res:person-Q116854 dbo:award res:award-Q3414212 .
res:person-Q116854 dbo:award res:award-Q430910 .
res:person-Q116854 dbo:award res:award-Q644077 .
res:person-Q116854 dbo:award res:award-Q739694 .
res:person-Q116854 ex:hasContribution res:contribution-Q127367-Q116854-writer .
res:person-Q116854 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q116854 rdf:type ex:Filmmaker`.

### ex:ActionFilm

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P136/P166

MANCHESTER: `(dbo:Film and dbo:genre some ex:ActionGenre)`

OWL EXPRESSION: EquivalentClasses(ex:ActionFilm ObjectIntersectionOf(dbo:Film ObjectSomeValuesFrom(dbo:genre ex:ActionGenre)))

REAL INDIVIDUAL: Alien (`res:film-Q103569`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:film-Q103569 dbo:award res:award-Q1131772 .
res:film-Q103569 dbo:award res:award-Q1257399 .
res:film-Q103569 dbo:award res:award-Q1265702 .
res:film-Q103569 dbo:award res:award-Q3414212 .
res:film-Q103569 dbo:award res:award-Q393686 .
res:film-Q103569 dbo:award res:award-Q739633 .
res:film-Q103569 dbo:genre res:genre-Q102260466 .
res:film-Q103569 dbo:genre res:genre-Q10663882 .
res:film-Q103569 dbo:genre res:genre-Q11304653 .
res:film-Q103569 dbo:genre res:genre-Q1200678 .
res:film-Q103569 dbo:genre res:genre-Q1342372 .
res:film-Q103569 dbo:genre res:genre-Q157394 .
res:film-Q103569 dbo:genre res:genre-Q1776156 .
res:film-Q103569 dbo:genre res:genre-Q188473 .
res:film-Q103569 dbo:genre res:genre-Q200092 .
res:film-Q103569 dbo:genre res:genre-Q20656232 .
res:film-Q103569 dbo:genre res:genre-Q2484376 .
res:film-Q103569 dbo:genre res:genre-Q319221 .
res:film-Q103569 dbo:genre res:genre-Q471839 .
res:film-Q103569 dbo:starring res:person-Q102124 .
res:film-Q103569 dbo:starring res:person-Q200405 .
res:film-Q103569 dbo:starring res:person-Q223091 .
res:film-Q103569 dbo:starring res:person-Q266270 .
res:film-Q103569 dbo:starring res:person-Q283872 .
res:film-Q103569 dbo:starring res:person-Q3047302 .
res:film-Q103569 dbo:starring res:person-Q314290 .
res:film-Q103569 dbo:starring res:person-Q320093 .
res:film-Q103569 dbo:starring res:person-Q323185 .
res:film-Q103569 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q102260466 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q10663882 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1200678 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1342372 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q157394 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1776156 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q200092 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q319221 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q471839 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

NEW KNOWLEDGE: `res:film-Q103569 rdf:type ex:ActionFilm`.

### ex:AwardWinningFilm

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P136/P166

MANCHESTER: `(dbo:Film and dbo:award some dbo:Award)`

OWL EXPRESSION: EquivalentClasses(ex:AwardWinningFilm ObjectIntersectionOf(dbo:Film ObjectSomeValuesFrom(dbo:award dbo:Award)))

REAL INDIVIDUAL: Alien (`res:film-Q103569`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:film-Q103569 dbo:award res:award-Q1131772 .
res:film-Q103569 dbo:award res:award-Q1257399 .
res:film-Q103569 dbo:award res:award-Q1265702 .
res:film-Q103569 dbo:award res:award-Q3414212 .
res:film-Q103569 dbo:award res:award-Q393686 .
res:film-Q103569 dbo:award res:award-Q739633 .
res:film-Q103569 dbo:genre res:genre-Q102260466 .
res:film-Q103569 dbo:genre res:genre-Q10663882 .
res:film-Q103569 dbo:genre res:genre-Q11304653 .
res:film-Q103569 dbo:genre res:genre-Q1200678 .
res:film-Q103569 dbo:genre res:genre-Q1342372 .
res:film-Q103569 dbo:genre res:genre-Q157394 .
res:film-Q103569 dbo:genre res:genre-Q1776156 .
res:film-Q103569 dbo:genre res:genre-Q188473 .
res:film-Q103569 dbo:genre res:genre-Q200092 .
res:film-Q103569 dbo:genre res:genre-Q20656232 .
res:film-Q103569 dbo:genre res:genre-Q2484376 .
res:film-Q103569 dbo:genre res:genre-Q319221 .
res:film-Q103569 dbo:genre res:genre-Q471839 .
res:film-Q103569 dbo:starring res:person-Q102124 .
res:film-Q103569 dbo:starring res:person-Q200405 .
res:film-Q103569 dbo:starring res:person-Q223091 .
res:film-Q103569 dbo:starring res:person-Q266270 .
res:film-Q103569 dbo:starring res:person-Q283872 .
res:film-Q103569 dbo:starring res:person-Q3047302 .
res:film-Q103569 dbo:starring res:person-Q314290 .
res:film-Q103569 dbo:starring res:person-Q320093 .
res:film-Q103569 dbo:starring res:person-Q323185 .
res:film-Q103569 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q102260466 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q10663882 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1200678 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1342372 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q157394 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1776156 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q200092 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q319221 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q471839 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

NEW KNOWLEDGE: `res:film-Q103569 rdf:type ex:AwardWinningFilm`.

### ex:MultiCreditContributor

REUSE/EXTEND rationale: At least two semantically distinct credit records. Different roles prove their distinctness; the name is shorthand and does not exclude repeated same-role credits.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(dbo:Person and ex:hasContribution min 2 ex:Contribution)`

OWL EXPRESSION: EquivalentClasses(ex:MultiCreditContributor ObjectIntersectionOf(dbo:Person ObjectMinCardinality(2 ex:hasContribution ex:Contribution)))

REAL INDIVIDUAL: Fran Walsh (`res:person-Q116861`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q127367-Q116861-producer ex:contributionTo res:film-Q127367 .
res:contribution-Q127367-Q116861-producer ex:hasRole ex:ProducerRole .
res:contribution-Q127367-Q116861-producer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q127367-Q116861-writer ex:contributionTo res:film-Q127367 .
res:contribution-Q127367-Q116861-writer ex:hasRole ex:WriterRole .
res:contribution-Q127367-Q116861-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q116861 dbo:award res:award-Q102427 .
res:person-Q116861 dbo:award res:award-Q1056240 .
res:person-Q116861 dbo:award res:award-Q107258 .
res:person-Q116861 dbo:award res:award-Q1075366 .
res:person-Q116861 dbo:award res:award-Q112243 .
res:person-Q116861 dbo:award res:award-Q131837474 .
res:person-Q116861 dbo:award res:award-Q139184 .
res:person-Q116861 dbo:award res:award-Q1472235 .
res:person-Q116861 dbo:award res:award-Q23049782 .
res:person-Q116861 dbo:award res:award-Q23050104 .
res:person-Q116861 dbo:award res:award-Q3414212 .
res:person-Q116861 dbo:award res:award-Q428808 .
res:person-Q116861 dbo:award res:award-Q430910 .
res:person-Q116861 dbo:award res:award-Q4824149 .
res:person-Q116861 dbo:award res:award-Q5569374 .
res:person-Q116861 dbo:award res:award-Q644077 .
res:person-Q116861 dbo:award res:award-Q739694 .
res:person-Q116861 ex:hasContribution res:contribution-Q127367-Q116861-producer .
res:person-Q116861 ex:hasContribution res:contribution-Q127367-Q116861-writer .
res:person-Q116861 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q116861 rdf:type ex:MultiCreditContributor`.

### ex:ThreeCreditContributor

REUSE/EXTEND rationale: At least three distinct credit records; three different role fillers prove distinctness. Not exactly three roles or an exhaustive career description.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(dbo:Person and ex:hasContribution min 3 ex:Contribution)`

OWL EXPRESSION: EquivalentClasses(ex:ThreeCreditContributor ObjectIntersectionOf(dbo:Person ObjectMinCardinality(3 ex:hasContribution ex:Contribution)))

REAL INDIVIDUAL: Christopher Nolan (`res:person-Q25191`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q13417189-Q25191-director ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-director ex:hasRole ex:DirectorRole .
res:contribution-Q13417189-Q25191-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-producer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-producer ex:hasRole ex:ProducerRole .
res:contribution-Q13417189-Q25191-producer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q13417189-Q25191-writer ex:contributionTo res:film-Q13417189 .
res:contribution-Q13417189-Q25191-writer ex:hasRole ex:WriterRole .
res:contribution-Q13417189-Q25191-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q25191 dbo:award res:award-Q102427 .
res:person-Q25191 dbo:award res:award-Q103360 .
res:person-Q25191 dbo:award res:award-Q105447 .
res:person-Q25191 dbo:award res:award-Q1056240 .
res:person-Q25191 dbo:award res:award-Q12143912 .
res:person-Q25191 dbo:award res:award-Q12201477 .
res:person-Q25191 dbo:award res:award-Q16058279 .
res:person-Q25191 dbo:award res:award-Q3405197 .
res:person-Q25191 dbo:award res:award-Q586356 .
res:person-Q25191 dbo:award res:award-Q787131 .
res:person-Q25191 dbo:award res:award-Q833154 .
res:person-Q25191 dbo:award res:award-Q833163 .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-director .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-producer .
res:person-Q25191 ex:hasContribution res:contribution-Q13417189-Q25191-writer .
res:person-Q25191 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q25191 rdf:type ex:ThreeCreditContributor`.

### ex:WriterDirector

REUSE/EXTEND rationale: A person with both directing and writing credits in this dataset; classification is never manually asserted.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(dbo:MovieDirector and dbo:ScreenWriter)`

OWL EXPRESSION: EquivalentClasses(ex:WriterDirector ObjectIntersectionOf(dbo:MovieDirector dbo:ScreenWriter))

REAL INDIVIDUAL: Damien Chazelle (`res:person-Q18350026`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q15648198-Q18350026-director ex:contributionTo res:film-Q15648198 .
res:contribution-Q15648198-Q18350026-director ex:hasRole ex:DirectorRole .
res:contribution-Q15648198-Q18350026-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q15648198-Q18350026-writer ex:contributionTo res:film-Q15648198 .
res:contribution-Q15648198-Q18350026-writer ex:hasRole ex:WriterRole .
res:contribution-Q15648198-Q18350026-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q18350026 dbo:award res:award-Q103360 .
res:person-Q18350026 dbo:award res:award-Q3774974 .
res:person-Q18350026 dbo:award res:award-Q787131 .
res:person-Q18350026 ex:hasContribution res:contribution-Q15648198-Q18350026-director .
res:person-Q18350026 ex:hasContribution res:contribution-Q15648198-Q18350026-writer .
res:person-Q18350026 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q18350026 rdf:type ex:WriterDirector`.

### ex:ActorFilmmaker

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(dbo:Actor and ex:Filmmaker)`

OWL EXPRESSION: EquivalentClasses(ex:ActorFilmmaker ObjectIntersectionOf(dbo:Actor ex:Filmmaker))

REAL INDIVIDUAL: Quentin Tarantino (`res:person-Q3772`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q104123-Q3772-actor ex:contributionTo res:film-Q104123 .
res:contribution-Q104123-Q3772-actor ex:hasRole ex:ActorRole .
res:contribution-Q104123-Q3772-actor http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q104123-Q3772-director ex:contributionTo res:film-Q104123 .
res:contribution-Q104123-Q3772-director ex:hasRole ex:DirectorRole .
res:contribution-Q104123-Q3772-director http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:contribution-Q104123-Q3772-writer ex:contributionTo res:film-Q104123 .
res:contribution-Q104123-Q3772-writer ex:hasRole ex:WriterRole .
res:contribution-Q104123-Q3772-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:film-Q104123 dbo:starring res:person-Q3772 .
res:person-Q3772 dbo:award res:award-Q1011547 .
res:person-Q3772 dbo:award res:award-Q105447 .
res:person-Q3772 dbo:award res:award-Q113068 .
res:person-Q3772 dbo:award res:award-Q13452531 .
res:person-Q3772 dbo:award res:award-Q1789102 .
res:person-Q3772 dbo:award res:award-Q179808 .
res:person-Q3772 dbo:award res:award-Q17985761 .
res:person-Q3772 dbo:award res:award-Q24051550 .
res:person-Q3772 dbo:award res:award-Q25405526 .
res:person-Q3772 dbo:award res:award-Q311836 .
res:person-Q3772 dbo:award res:award-Q3404975 .
res:person-Q3772 dbo:award res:award-Q3703457 .
res:person-Q3772 dbo:award res:award-Q41375 .
res:person-Q3772 dbo:award res:award-Q41417 .
res:person-Q3772 dbo:award res:award-Q4743376 .
res:person-Q3772 dbo:award res:award-Q5211225 .
res:person-Q3772 dbo:award res:award-Q52382875 .
res:person-Q3772 dbo:award res:award-Q670282 .
res:person-Q3772 dbo:award res:award-Q716909 .
res:person-Q3772 dbo:award res:award-Q727282 .
res:person-Q3772 dbo:award res:award-Q833154 .
res:person-Q3772 dbo:award res:award-Q849124 .
res:person-Q3772 dbo:award res:award-Q849771 .
res:person-Q3772 ex:hasContribution res:contribution-Q104123-Q3772-actor .
res:person-Q3772 ex:hasContribution res:contribution-Q104123-Q3772-director .
res:person-Q3772 ex:hasContribution res:contribution-Q104123-Q3772-writer .
res:person-Q3772 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q3772 rdf:type ex:ActorFilmmaker`.

### ex:AwardWinningFilmmaker

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P57/P161/P58/P162; P166 when award-based

MANCHESTER: `(ex:Filmmaker and dbo:award some dbo:Award)`

OWL EXPRESSION: EquivalentClasses(ex:AwardWinningFilmmaker ObjectIntersectionOf(ex:Filmmaker ObjectSomeValuesFrom(dbo:award dbo:Award)))

REAL INDIVIDUAL: Philippa Boyens (`res:person-Q116854`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:contribution-Q127367-Q116854-writer ex:contributionTo res:film-Q127367 .
res:contribution-Q127367-Q116854-writer ex:hasRole ex:WriterRole .
res:contribution-Q127367-Q116854-writer http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:Contribution .
res:person-Q116854 dbo:award res:award-Q1056240 .
res:person-Q116854 dbo:award res:award-Q107258 .
res:person-Q116854 dbo:award res:award-Q1075366 .
res:person-Q116854 dbo:award res:award-Q23050104 .
res:person-Q116854 dbo:award res:award-Q3414212 .
res:person-Q116854 dbo:award res:award-Q430910 .
res:person-Q116854 dbo:award res:award-Q644077 .
res:person-Q116854 dbo:award res:award-Q739694 .
res:person-Q116854 ex:hasContribution res:contribution-Q127367-Q116854-writer .
res:person-Q116854 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Person .
```

NEW KNOWLEDGE: `res:person-Q116854 rdf:type ex:AwardWinningFilmmaker`.

### ex:AwardWinningActionFilm

REUSE/EXTEND rationale: Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class.

CRAWLED SUPPORT: P136/P166

MANCHESTER: `(ex:ActionFilm and ex:AwardWinningFilm)`

OWL EXPRESSION: EquivalentClasses(ex:AwardWinningActionFilm ObjectIntersectionOf(ex:ActionFilm ex:AwardWinningFilm))

REAL INDIVIDUAL: Alien (`res:film-Q103569`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:film-Q103569 dbo:award res:award-Q1131772 .
res:film-Q103569 dbo:award res:award-Q1257399 .
res:film-Q103569 dbo:award res:award-Q1265702 .
res:film-Q103569 dbo:award res:award-Q3414212 .
res:film-Q103569 dbo:award res:award-Q393686 .
res:film-Q103569 dbo:award res:award-Q739633 .
res:film-Q103569 dbo:genre res:genre-Q102260466 .
res:film-Q103569 dbo:genre res:genre-Q10663882 .
res:film-Q103569 dbo:genre res:genre-Q11304653 .
res:film-Q103569 dbo:genre res:genre-Q1200678 .
res:film-Q103569 dbo:genre res:genre-Q1342372 .
res:film-Q103569 dbo:genre res:genre-Q157394 .
res:film-Q103569 dbo:genre res:genre-Q1776156 .
res:film-Q103569 dbo:genre res:genre-Q188473 .
res:film-Q103569 dbo:genre res:genre-Q200092 .
res:film-Q103569 dbo:genre res:genre-Q20656232 .
res:film-Q103569 dbo:genre res:genre-Q2484376 .
res:film-Q103569 dbo:genre res:genre-Q319221 .
res:film-Q103569 dbo:genre res:genre-Q471839 .
res:film-Q103569 dbo:starring res:person-Q102124 .
res:film-Q103569 dbo:starring res:person-Q200405 .
res:film-Q103569 dbo:starring res:person-Q223091 .
res:film-Q103569 dbo:starring res:person-Q266270 .
res:film-Q103569 dbo:starring res:person-Q283872 .
res:film-Q103569 dbo:starring res:person-Q3047302 .
res:film-Q103569 dbo:starring res:person-Q314290 .
res:film-Q103569 dbo:starring res:person-Q320093 .
res:film-Q103569 dbo:starring res:person-Q323185 .
res:film-Q103569 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q102260466 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q10663882 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1200678 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1342372 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q157394 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1776156 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q200092 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q20656232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q319221 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q471839 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

NEW KNOWLEDGE: `res:film-Q103569 rdf:type ex:AwardWinningActionFilm`.

### ex:GenreCrossingFilm

REUSE/EXTEND rationale: Film carrying both action and drama genre memberships; this is not an unproved two-distinct-genre cardinality claim.

CRAWLED SUPPORT: P136/P166

MANCHESTER: `(dbo:Film and dbo:genre some ex:ActionGenre and dbo:genre some ex:DramaGenre)`

OWL EXPRESSION: EquivalentClasses(ex:GenreCrossingFilm ObjectIntersectionOf(dbo:Film ObjectSomeValuesFrom(dbo:genre ex:ActionGenre) ObjectSomeValuesFrom(dbo:genre ex:DramaGenre)))

REAL INDIVIDUAL: Pulp Fiction (`res:film-Q104123`).

ASSERTED / INFERRED: No direct assertion of this type; HermiT entails membership. The role→credit→person classes need approximately 2–4 explanatory steps; OWL semantics is not procedural and does not prescribe evaluation order.

INITIAL FACTS:

```turtle
res:film-Q104123 dbo:award res:award-Q1170507 .
res:film-Q104123 dbo:award res:award-Q1315008 .
res:film-Q104123 dbo:award res:award-Q1720784 .
res:film-Q104123 dbo:award res:award-Q1789102 .
res:film-Q104123 dbo:award res:award-Q179808 .
res:film-Q104123 dbo:award res:award-Q1868950 .
res:film-Q104123 dbo:award res:award-Q1966965 .
res:film-Q104123 dbo:award res:award-Q2295041 .
res:film-Q104123 dbo:award res:award-Q2544859 .
res:film-Q104123 dbo:award res:award-Q3404523 .
res:film-Q104123 dbo:award res:award-Q3841643 .
res:film-Q104123 dbo:award res:award-Q41375 .
res:film-Q104123 dbo:award res:award-Q41417 .
res:film-Q104123 dbo:award res:award-Q503034 .
res:film-Q104123 dbo:award res:award-Q505449 .
res:film-Q104123 dbo:award res:award-Q5211226 .
res:film-Q104123 dbo:award res:award-Q540977 .
res:film-Q104123 dbo:award res:award-Q548389 .
res:film-Q104123 dbo:award res:award-Q696972 .
res:film-Q104123 dbo:award res:award-Q696998 .
res:film-Q104123 dbo:award res:award-Q6978541 .
res:film-Q104123 dbo:award res:award-Q849124 .
res:film-Q104123 dbo:award res:award-Q952914 .
res:film-Q104123 dbo:genre res:genre-Q11304653 .
res:film-Q104123 dbo:genre res:genre-Q113485322 .
res:film-Q104123 dbo:genre res:genre-Q130232 .
res:film-Q104123 dbo:genre res:genre-Q157443 .
res:film-Q104123 dbo:genre res:genre-Q1788980 .
res:film-Q104123 dbo:genre res:genre-Q188473 .
res:film-Q104123 dbo:genre res:genre-Q19367312 .
res:film-Q104123 dbo:genre res:genre-Q2421031 .
res:film-Q104123 dbo:genre res:genre-Q2484376 .
res:film-Q104123 dbo:genre res:genre-Q3990883 .
res:film-Q104123 dbo:genre res:genre-Q459290 .
res:film-Q104123 dbo:genre res:genre-Q5778924 .
res:film-Q104123 dbo:genre res:genre-Q7444356 .
res:film-Q104123 dbo:genre res:genre-Q859369 .
res:film-Q104123 dbo:genre res:genre-Q959790 .
res:film-Q104123 dbo:starring res:person-Q1016897 .
res:film-Q104123 dbo:starring res:person-Q104061 .
res:film-Q104123 dbo:starring res:person-Q109232 .
res:film-Q104123 dbo:starring res:person-Q1209753 .
res:film-Q104123 dbo:starring res:person-Q125017 .
res:film-Q104123 dbo:starring res:person-Q1368224 .
res:film-Q104123 dbo:starring res:person-Q1563838 .
res:film-Q104123 dbo:starring res:person-Q164534 .
res:film-Q104123 dbo:starring res:person-Q172678 .
res:film-Q104123 dbo:starring res:person-Q185051 .
res:film-Q104123 dbo:starring res:person-Q191132 .
res:film-Q104123 dbo:starring res:person-Q203804 .
res:film-Q104123 dbo:starring res:person-Q2263306 .
res:film-Q104123 dbo:starring res:person-Q235115 .
res:film-Q104123 dbo:starring res:person-Q238483 .
res:film-Q104123 dbo:starring res:person-Q240774 .
res:film-Q104123 dbo:starring res:person-Q2434817 .
res:film-Q104123 dbo:starring res:person-Q254431 .
res:film-Q104123 dbo:starring res:person-Q270774 .
res:film-Q104123 dbo:starring res:person-Q2924399 .
res:film-Q104123 dbo:starring res:person-Q2926038 .
res:film-Q104123 dbo:starring res:person-Q310315 .
res:film-Q104123 dbo:starring res:person-Q318267 .
res:film-Q104123 dbo:starring res:person-Q3193117 .
res:film-Q104123 dbo:starring res:person-Q3241353 .
res:film-Q104123 dbo:starring res:person-Q356541 .
res:film-Q104123 dbo:starring res:person-Q3772 .
res:film-Q104123 dbo:starring res:person-Q3856171 .
res:film-Q104123 dbo:starring res:person-Q3973186 .
res:film-Q104123 dbo:starring res:person-Q432437 .
res:film-Q104123 dbo:starring res:person-Q453973 .
res:film-Q104123 dbo:starring res:person-Q514913 .
res:film-Q104123 dbo:starring res:person-Q7647898 .
res:film-Q104123 dbo:starring res:person-Q80938 .
res:film-Q104123 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:Film .
res:genre-Q11304653 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q113485322 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q113485322 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:DramaGenre .
res:genre-Q130232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q130232 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:DramaGenre .
res:genre-Q157443 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q1788980 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q188473 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q19367312 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q2421031 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q2484376 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q3990883 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q3990883 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:ActionGenre .
res:genre-Q459290 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q5778924 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q7444356 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q859369 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
res:genre-Q859369 http://www.w3.org/1999/02/22-rdf-syntax-ns#type ex:DramaGenre .
res:genre-Q959790 http://www.w3.org/1999/02/22-rdf-syntax-ns#type dbo:MovieGenre .
```

NEW KNOWLEDGE: `res:film-Q104123 rdf:type ex:GenreCrossingFilm`.

## 11. Cardinality and validation limitations

Exactly 1 constrains each Contribution endpoint and role. It does not validate completeness under the open-world assumption: an absent filler may exist without an explicit assertion. Structural checks must separately enforce that the exported record contains its three fields.

At least 2 / at least 3 are genuine HermiT results on hasContribution. Example: Christopher Nolan has distinct directing, writing and producing credit records; those records cannot collapse into one because hasRole is functional and DirectorRole, WriterRole and ProducerRole are distinct. No inequality is fabricated for people, genres, awards, companies or films.

The negative MultiGenreFilm test separately adds the requested min 2 genre definition and obtains zero DL members. A production class is excluded because the dataset cannot prove two genre fillers distinct. Future additions require source-supported inequality or a justified identity model; a blanket AllDifferent on Wikidata IDs is not justified by syntax.

## 12. Checklist and reproduction

- [x] Official DBpedia reference checked and hashed; reused term meanings, domain/range preserved.
- [x] No ex:Film, Person, Actor, Award, Genre, Language, Country, Company or Organisation clones.
- [x] Every extension maps to crawled claims or documented source-record metadata.
- [x] All demo individuals exist in the crawled dataset.
- [x] All retained defined classes have genuinely inferred members.
- [x] Equivalent classes, existential/value/cardinality restrictions and hierarchy present.
- [x] Inverse, subproperty and chain reasoning present; no gratuitous property characteristics.
- [x] Seven explanatory inference chains and 27 executed competency questions.
- [x] Five verified demo cases with no false claim that SQL cannot reproduce them.
- [x] Genuine min 2/min 3 DL results and explicit negative genre-cardinality test.
- [x] No MP4 videos included; removed at user request.
- [ ] Zero-result MultiGenreFilm / MultiAwardFilm / FrequentProductionCompany: require additional justified evidence before inclusion.
- [x] Archived official ontology, official development vocabulary and relevant live term meanings checked; equivalence decisions remain scoped to these references.

Run:

```sh
make build
make reason JAVA=/path/to/java
make validate
make test
```

Open ontology/Movie_Knowledge_Graph.owl directly in Protégé; it combines the schema and asserted facts without pre-asserting inferred classes. Start HermiT and inspect the example types; inferred.ttl is exported entailment evidence, not source assertions. before_after.trig supports query 27. Temporary RDF/XML reasoner inputs are removed after each run, preserving one authoritative full OWL export.

## Property-by-property semantic reuse audit

The comparison checks the relation meaning, argument direction, entity level, range and units; lexical resemblance alone is insufficient.

| Property | Decision | Semantic comparison |
|---|---|---|
| dbo:director | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:starring | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:writer | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:producer | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:productionCompany | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:award | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:genre | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:country | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| dbo:language | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| ex:hasContribution | CREATE | dbo:occupation links a PersonFunction, not a film-credit record. The local property refers to n-ary source credits. |
| ex:contributionBy | CREATE | dbo:director/writer/starring refer from Work/Film to people; this relation originates from a credit record, so they are not semantically interchangeable. |
| ex:contributionTo | CREATE | The domain is a credit association, not an Agent or Work. This is the film endpoint of the n-ary model. |
| ex:contributionOf | CREATE | Inverse of the film endpoint of the local n-ary association; not a Film-to-Person relation. |
| ex:hasRole | CREATE | dbo:role and dbo:artistFunction have string ranges; the controlled-role entity of a functional credit record has distinct object semantics. |
| ex:contributedTo | CREATE | Covers every collected credit role through a shared chain. director/starring/writer/producer are narrower and opposite-direction properties. |
| ex:directed | CREATE | Inverse of dbo:director; cannot reuse that forward predicate with its arguments reversed. It is also a subproperty of the broader local contributedTo. |
| ex:actedIn | CREATE | Inverse of dbo:starring; forward dbo:starring cannot denote the reversed relation. |
| ex:productionOf | CREATE | Inverse of dbo:productionCompany; preserving direction is necessary for semantic equivalence. |
| ex:sourceSnapshot | CREATE | More specific than prov:wasDerivedFrom: points to a locally saved response record with retrieval timestamp and content hash, not merely any source entity. |
| dbo:runtime | REUSE | Same relation/value semantics as the checked DBpedia property, with its original domain and range. Runtime is converted to the reference unit of seconds. |
| ex:releaseYear | CREATE | Derived earliest-release-year integer summary from P577. dbo:releaseDate requires a date; dbo:year is a generic gYear and does not express the earliest-release summary. No equivalence or invented full date is asserted. |
| ex:sourceUrl | CREATE | Literal lexical request endpoint stored in the snapshot manifest. DBpedia has no matching request-metadata datatype property in the checked vocabulary; prov:wasDerivedFrom is separately retained as an IRI relation. |
| ex:retrievedAt | CREATE | Retrieval instant of a local response snapshot, not a film releaseDate, generic date, or creation time of the original remote entity. |
| ex:sha256 | CREATE | SHA-256 checksum of the exact crawled response bytes, not a generic title, name, code or identifier of the represented film/person. |

## References

- [Official DBpedia ontology download](https://downloads.dbpedia.org/2016-10/dbpedia_2016-10.owl)
- [dbo:starring](https://dbpedia.org/ontology/starring)
- [dbo:runtime](https://dbpedia.org/ontology/runtime)
- [dbo:MovieGenre](https://dbpedia.org/ontology/MovieGenre)
- [DBpedia Actor meaning](https://mappings.dbpedia.org/server/ontology/classes/Actor)
- [W3C OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/)
- [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/)

## Appendix — All executable competency queries

Namespace identifiers in the tables expand using these prefixes:

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```

### Query 1 — List films

Before / after rows: 30 / 30

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Film . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 2 — Inception: year, duration and director

Before / after rows: 1 / 1

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?title ?year ?runtimeSeconds ?director WHERE { res:film-Q25188 rdfs:label ?title ; ex:releaseYear ?year ; dbo:runtime ?runtimeSeconds ; dbo:director ?person . ?person rdfs:label ?director }
```

### Query 3 — Directors of Inception

Before / after rows: 1 / 1

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:film-Q25188 dbo:director ?s . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 4 — Inception credits and roles

Before / after rows: 25 / 25

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?personName ?roleName WHERE { res:film-Q25188 ex:contributionOf ?credit . ?credit ex:contributionBy ?person ; ex:hasRole ?role . ?person rdfs:label ?personName . ?role rdfs:label ?roleName } ORDER BY ?roleName ?personName
```

### Query 5 — Films directed by Nolan

Before / after rows: 8 / 8

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s dbo:director res:person-Q25191 . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 6 — Companies credited on Inception

Before / after rows: 4 / 4

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:film-Q25188 dbo:productionCompany ?s . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 7 — Awards of Inception

Before / after rows: 7 / 7

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:film-Q25188 dbo:award ?s . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 8 — Runtime in seconds

Before / after rows: 1 / 1

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:film-Q25188 dbo:runtime ?s . OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 9 — Film genres through the parent class

Before / after rows: 0 / 75

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?f a dbo:Film ; dbo:genre ?s . ?s a dbo:Genre . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 10 — Persons through Agent hierarchy

Before / after rows: 0 / 851

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Agent . FILTER EXISTS { ?s a dbo:Person } FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 11 — Production companies

Before / after rows: 45 / 45

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Company . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 12 — Film subclasses

Before / after rows: 0 / 4

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s rdfs:subClassOf+ dbo:Film . OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 13 — Actors through Artist hierarchy

Before / after rows: 0 / 769

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Artist . FILTER EXISTS { ?s a dbo:Actor } FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 14 — Inferred Actors

Before / after rows: 0 / 769

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a dbo:Actor . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 15 — Inferred Filmmakers

Before / after rows: 0 / 89

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:Filmmaker . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 16 — Inferred Action films

Before / after rows: 0 / 12

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:ActionFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 17 — Award-winning films

Before / after rows: 0 / 26

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:AwardWinningFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 18 — People with at least two provably distinct credits

Before / after rows: 0 / 17

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:MultiCreditContributor . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 19 — People with at least three provably distinct credits

Before / after rows: 0 / 7

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:ThreeCreditContributor . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 20 — Writer-directors

Before / after rows: 0 / 10

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:WriterDirector . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 21 — Actor-filmmakers

Before / after rows: 0 / 7

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:ActorFilmmaker . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 22 — Award-winning filmmakers

Before / after rows: 0 / 65

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:AwardWinningFilmmaker . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 23 — Award-winning action films

Before / after rows: 0 / 10

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:AwardWinningActionFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 24 — Action/drama crossing films

Before / after rows: 0 / 8

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { ?s a ex:GenreCrossingFilm . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 25 — Nolan contributions through property chain

Before / after rows: 0 / 8

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:person-Q25191 ex:contributedTo ?s . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 26 — Nolan films through inverse director

Before / after rows: 0 / 8

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?label WHERE { res:person-Q25191 ex:directed ?s . FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/")) OPTIONAL { ?s rdfs:label ?label } } ORDER BY ?s
```

### Query 27 — Types present only after reasoning

Before / after rows: 0 / 1261

```sparql
PREFIX ex: <https://laminhtrung.github.io/movie-lod-semantic-web/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX res: <https://laminhtrung.github.io/movie-lod-semantic-web/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?s ?type WHERE {
 GRAPH <urn:movie:reasoned> { ?s a ?type }
 FILTER(STRSTARTS(STR(?s), "https://laminhtrung.github.io/movie-lod-semantic-web/resource/") && STRSTARTS(STR(?type), "https://laminhtrung.github.io/movie-lod-semantic-web/ontology#"))
 FILTER NOT EXISTS { GRAPH <urn:movie:asserted> { ?s a ?type } }
} ORDER BY ?type ?s
```

