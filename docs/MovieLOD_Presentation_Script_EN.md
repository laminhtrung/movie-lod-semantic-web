# MovieLOD — English Presentation Script

## Presenter guidance

This script follows the 24-slide presentation. The main talk takes approximately 15–18 minutes at a measured pace. The optional diagram walkthrough takes another 4–5 minutes; use it instead of the detailed explanations on slides 9–10 if time is limited. Instructions in square brackets are stage directions and should not be read aloud.

Suggested division: Presenter 1 covers slides 1–6; Presenter 2 covers slides 7–12; Presenter 3 covers slides 13–18; Presenter 4 covers slides 19–24. Use the diagram appendix wherever the diagram is displayed.

The current ontology has 37 named classes. The entity diagram shows 13 of them, all 19 declared object properties and all five datatype properties. It does not show the complete class hierarchy. The website now offers 28 sample queries: the original 27 competency queries and the additional Inception identity-link query. Unfilled Protégé screenshot placeholders are instructions to collect evidence, not completed evidence.

## Slide 01 — MovieLOD

“Good morning. Today, we will present MovieLOD, a movie knowledge graph built with RDF, OWL and SPARQL.

Our project connects movie information with reusable vocabulary from DBpedia and external identifiers from Wikidata and DBpedia. It also uses explicit ontology definitions to infer classifications that are not directly asserted in the source data.

We will use Inception and Christopher Nolan as our running examples, moving from source facts to ontology modeling, reasoning and queries.”

## Slide 02 — Objectives and synchronized evidence

“The project has five main objectives: collect movie data, construct an ontology, connect resources to external datasets, demonstrate reasoning, and provide meaningful SPARQL queries.

These objectives are supported by separate forms of evidence. Source records support the factual input. OWL axioms explain the model. Reasoner results support logical entailments. Query results demonstrate how the knowledge can be retrieved.

We keep these forms of evidence distinct, because a successful query alone does not prove that a reasoner produced the answer.”

## Slide 03 — Architecture and knowledge layers

“The processing pipeline has four main stages: collection, construction, reasoning and validation.

Collected responses are preserved with their source metadata. The construction stage produces the asserted graph and the ontology. HermiT checks the full OWL model and classifies individuals. Additional materialized relationships support querying.

The application exposes three knowledge scopes: source facts, facts with inference, and named graphs for before-and-after comparison. The browser uses Comunica; the local endpoint uses RDFLib.”

## Slide 04 — Dataset: units and counting scope

“Our sample contains 30 films, 851 people, 1,010 contribution records and 45 production companies. It also contains 672 award entities and 76 source snapshots.

The full OWL graph contains 19,025 triples. This count includes the declared model and facts; it is not the size of the complete inferred closure.

These units matter. A contribution record is not a person, and an award entity is not an award ceremony. Entity statistics are scoped to local identifiers to avoid double-counting external aliases.”

## Slide 05 — Ontology inventory: reuse before extension

“The ontology has 37 named classes: 17 reused DBpedia classes, 19 local classes and the VoID Dataset class.

We reuse established concepts such as Film, Person, Actor, Company and Genre. Local classes address needs specific to this project, including contribution records, source snapshots and classes defined by reasoning conditions.

The class count refers to named classes. Anonymous restrictions and other OWL expressions are part of the model, but they should not be counted as additional named classes.”

## Slide 06 — Work and Film: meaningful inferred subsets

“Film is a subclass of Work. This allows films to participate in relationships and attributes declared for works, while retaining movie-specific information.

Our local film classes describe subsets with explicit conditions. For example, ActionFilm depends on an action-genre relationship, and AwardWinningFilm depends on the existence of an award relationship. Their intersection supports AwardWinningActionFilm.

The purpose of these classes is to make their meaning explicit and reusable. A class name should be supported by an ontology definition, rather than added only to increase the inventory.”

## Slide 07 — People and companies: reuse DBpedia hierarchy

“The people and organization model also reuses DBpedia. Person belongs to the Agent hierarchy, while Company belongs to the organization branch.

Specialized occupations include Actor, MovieDirector, ScreenWriter and Producer. The ontology can connect these occupations with contribution evidence and other declared relationships.

For example, WriterDirector combines the director and screenwriter classifications. This gives us a meaningful class whose members can be inferred from the model, instead of manually adding a label to each person.”

## Slide 08 — Genre, awards and provenance

“Movie descriptions include genres, awards, countries and languages. These are represented as linked resources rather than repeated text fields.

Our local genre categories include action and drama, with an explicit mapping policy. The quality of that mapping remains a separate evaluation issue.

Some properties declare a range without declaring a domain. We preserve that distinction in the ontology and the diagram. We do not invent a domain restriction saying that every such property can only be used on Film.”

## Slide 09 — Contribution: person, film and role

“A contribution represents one person's participation in one film in one role.

Each Contribution has exactly one contributing Person, one target Film and one ContributionRole. The role individuals represent acting, directing, writing and producing. They are explicitly declared different.

This intermediate entity preserves information that a simple person-to-film link cannot express by itself. The same person may contribute to the same film in several roles, and those contributions remain separate records with their own meaning.”

## Slide 10 — Properties: reuse, inverse and chain

“The model contains 19 declared object properties and five datatype properties.

Inverse properties allow us to traverse related information in the opposite direction. For example, contributionBy goes from a contribution to its person, while hasContribution provides the inverse view.

The property chain hasContribution followed by contributionTo entails contributedTo. This expresses a reusable semantic rule: if a person has a contribution and that contribution targets a film, the person contributed to that film.”

## Slide 11 — OWL axioms: what each statement means

“An equivalent-class definition gives necessary and sufficient conditions. A subclass axiom gives a one-way implication.

Existential restrictions state that a suitable related individual exists. A has-value restriction refers to a particular individual, such as DirectorRole. Functional properties limit the number of distinct values; they may lead a reasoner to identify values rather than reject a record.

OWL follows the open-world assumption. Missing information is not automatically false, and different identifiers do not automatically prove that their individuals are different.”

## Slide 12 — Verified domain classes after HermiT

“This slide summarizes ten domain classifications with inferred memberships in the checked model.

The examples include Filmmaker, ActionFilm, AwardWinningFilm and several more specific classes. Four contribution subclasses support the reasoning, while Actor also uses the range of the reused starring property.

The domain classifications shown here were not directly asserted as input types. Their memberships follow from the facts and axioms. The displayed results should therefore be associated with the reasoner evidence, not just with the existence of the class definitions.”

## Slide 13 — Nolan: facts to credit type to Filmmaker

“Consider Christopher Nolan. A contribution with DirectorRole satisfies the definition of DirectingContribution. The inverse relationship connects that contribution to Nolan through hasContribution.

The Filmmaker definition recognizes people with a suitable directing, writing or producing contribution. Other axioms support MovieDirector and ScreenWriter. Their intersection supports WriterDirector.

This explanation follows a convenient teaching sequence. It does not imply that the reasoner must execute rules in that exact order; the classifications follow from the combined logical meaning of the ontology.”

## Slide 14 — Genuine minimum-cardinality reasoning

“Nolan has contributions with director, writer and producer roles. The role individuals are declared different, and hasRole is functional.

If two of these contributions were the same individual, that individual would have two different role values, contradicting functionality. The model therefore provides evidence that these contributions are distinct.

This supports minimum-cardinality reasoning. The checked results include 17 people in the two-credit class and seven in the three-credit class. Counting different identifier strings alone would not provide the same OWL proof.”

## Slide 15 — Source claims and reproducibility

“Source preservation supports reproducibility. The project retains 76 source responses with their URLs, retrieval times and checksums.

A checksum helps verify that the stored bytes have not changed. It does not prove that every source claim is correct in the real world.

Our sample and mapping rules also limit the conclusions we can draw. Genre categorization and external-identifier matching would benefit from a larger evaluation dataset and manually checked reference answers.”

## Slide 16 — RDF literals and DBpedia units

“Inception provides a concrete example of datatype modeling. Its selected release year is 2010, and its runtime is 8,880 seconds, equivalent to 148 minutes.

We reuse the DBpedia runtime property with the double datatype and preserve its unit. The releaseYear property stores an integer summary rather than a complete release-date history.

SourceSnapshot uses anyURI, dateTime and string for its source URL, retrieval timestamp and checksum. Labels are annotations, so they are not counted as additional datatype properties in this inventory.”

## Slide 17 — Linked data: identity and publication

“The published data includes 1,727 identity links: 1,699 to Wikidata and 28 to DBpedia.

We distinguish three ideas. Reusing dbo:Film shares vocabulary. An owl:sameAs statement declares that two identifiers denote the same individual. Source metadata records where information came from.

The GitHub Pages website publishes resource descriptions and RDF downloads. These identifiers and exports allow other consumers to inspect and reuse the data independently of the application interface.”

## Slide 18 — Inception: RDF resource and OWL

“The Inception resource page shows its label, year, runtime, movie relationships, identity links and source metadata.

The same resource can be inspected in the OWL file. Matching values across these views helps demonstrate that the interface is presenting the published model.

A browser screenshot demonstrates application behavior. A Protégé screenshot demonstrates a particular ontology view. To demonstrate inferred types, the screenshot must also show the relevant reasoning result rather than only an asserted definition.”

## Slide 19 — SPARQL: choose the knowledge scope

“Before running a query, we choose the knowledge scope.

Source facts retrieve the asserted data. With OWL inference includes exported inferred knowledge. Before-and-after named graphs support comparisons between the two.

The Inception query retrieves the year, duration and director. The application queries prepared data; it does not run HermiT again for every browser request. This distinction explains why selecting the correct scope is necessary when demonstrating a newly inferred class.”

## Slide 20 — Credit records and competency questions

“Inception has 25 contribution records: 21 acting contributions, one directing contribution, one writing contribution and two producing contributions.

These are contribution records, not 25 different people. One person can hold several roles.

The website currently contains 28 sample queries. The original 27 address our competency questions and reasoning comparisons. The additional query, named ‘Inception links to DBpedia and Wikidata’, retrieves the film's two external identity links.”

[For a live demonstration, select “Inception links to DBpedia and Wikidata”. Confirm that the table contains DBpedia/Inception and Wikidata/Q25188.]

## Slide 21 — Before and after: Nolan and WriterDirector

“The WriterDirector class has no directly asserted memberships in the input graph. After reasoning, the checked local result contains ten members.

We compare the same classification question across the source and inferred scopes. The named-graph query can explicitly retrieve types present only after reasoning.

This is a clearer demonstration of entailment than displaying a class name alone. It connects the original evidence, the class definition and the newly available classification.”

## Slide 22 — Verification of the final OWL

“The full OWL file has been checked with HermiT. The recorded result is consistent, with no unsatisfiable named classes.

The original competency queries were validated in their intended scopes. The additional identity query has also been checked and returns the two expected links. Application checks cover query forms and recovery from invalid syntax.

These checks answer different questions. Logical consistency checks the ontology, query validation checks retrieval, and source hashes check file integrity. None of them alone establishes that every real-world statement is true.”

## Slide 23 — Coverage and limitations

“The project demonstrates vocabulary reuse, linked identifiers, provenance, OWL definitions, reasoning and SPARQL retrieval.

Its limitations include the small, selected sample, the genre-mapping policy and the absence of a complete ground-truth evaluation for external matching.

The current entity diagram also has a defined scope: it shows 13 of the 37 named classes and all declared object and datatype properties. It should not be described as the complete class hierarchy or a drawing of every OWL axiom.”

## Slide 24 — Evidence capture and submission checklist

“To complete the presentation evidence, we need genuine Protégé screenshots for the requested ontology and inferred views. Any remaining placeholders should be replaced with screenshots captured from the correct file and reasoner state.

The main contribution of MovieLOD is the explicit, reusable meaning of its data: shared vocabulary, linked identity, traceable sources and logical definitions that support new classifications.

Thank you for listening. We welcome your questions.”

## Optional diagram walkthrough — approximately 4–5 minutes

[Display MovieLOD_entity_diagram.png. This explanation can replace parts of slides 9–10; do not add a new slide unless the deck is being revised.]

“This diagram presents the main MovieLOD classes and their relationships. The ontology contains 37 named classes, while this drawing shows 13 core classes. Repeated boxes refer to the same class.

In the class view, rectangles represent classes. Open arrows indicate object properties, with the property name written on the connection. A solid line with a hollow triangle represents generalization. Here, Film is a subclass of Work. Fields inside the class compartments represent datatype properties.

Let us start with section A. A Person has a Contribution, and the Contribution targets a Film. The inverse properties let us navigate back from a contribution to its person, or from a film to its contributions.

A Contribution has exactly one person, one film and one role. The multiplicity one is shown at the relevant target end. The four role names are individuals of ContributionRole, not attributes of that class. AllDifferent states that these four individuals are distinct; it does not state that the class can contain only those four individuals.

The contributedTo relationship is supported by a property chain: a person has a contribution, and that contribution targets a film. This connects the detailed credit model with a simpler person-to-film relationship.

Section B shows movie and production relationships. Film belongs to Work. A film can be connected to its director, while works connect to writers, actors, production companies and producers. The diagram preserves the domains and ranges declared in the ontology. It also shows that releaseYear uses an integer and runtime uses a double, measured in seconds.

Section C is a range view for properties whose domain has not been declared. The oval marked Unspecified subject is a diagram placeholder, not an additional ontology class. It prevents us from incorrectly claiming that these properties are restricted to films. Their targets include Genre, Award, Country, Language and SourceSnapshot.

SourceSnapshot records a source URL, retrieval time and checksum. These values support traceability and checking the preserved source bytes. They do not by themselves prove the factual accuracy of the source.

Section D presents an actual data example rather than another class relationship. The local individual film-Q25188 represents Inception and has type Film. Its two owl:sameAs links identify the corresponding resources in DBpedia and Wikidata. The sample query on the website retrieves these two links.

Finally, this drawing explains the core structure and all declared object and datatype properties. Other classes, including Filmmaker, WriterDirector and ThreeCreditContributor, are not shown in this diagram. To discuss all 37 classes and their reasoning definitions, we need the complete class hierarchy and the relevant OWL axioms.”

## Short answers for questions

**Does the diagram show all 37 classes?**

“No. It shows 13 core classes; 24 named classes are omitted. It covers all 19 declared object properties and all five datatype properties.”

**Why use Contribution instead of only person-to-film links?**

“A Contribution preserves the combination of person, film and role. The same person can participate in the same film in several roles.”

**Does missing data violate an exact-cardinality restriction immediately?**

“Not necessarily. OWL follows the open-world assumption. A missing triple is not automatically proof that the required value does not exist. Application completeness checks are a separate concern.”

**Does owl:sameAs mean a similar or related resource?**

“No. It asserts identity: the identifiers refer to the same individual. Matching therefore requires stronger justification than a general reference link.”

**Could a relational database answer similar questions?**

“Yes, using joins, views or rules. Our contribution is explicit semantics, shared vocabulary, interoperable identifiers, linked sources and ontology-based entailment.”

**Does a class-definition screenshot prove that reasoning ran?**

“No. It shows the definition. Evidence of inference should show the reasoner result, inferred membership or a suitable before-and-after query.”
