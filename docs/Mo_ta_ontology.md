# MovieLOD — Mô tả ontology cuối 3.0.0

> **Phiên bản:** Ontology, dữ liệu, web và truy vấn dùng chung 3.0.0. MP4 đã được xoá theo yêu cầu; tài liệu demo dùng cho trình diễn trực tiếp.

## Lớp và căn cứ

| Lớp | Hành động | Lớp cha | Căn cứ / ý nghĩa |
|---|---|---|---|
| dbo:Work | REUSE | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Film | REUSE | dbo:Work | P31; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Agent | REUSE | — | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Person | REUSE | dbo:Agent | P31=Q5; P57/P161/P58/P162; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Artist | REUSE | dbo:Person | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Actor | REUSE | dbo:Artist | P161; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Writer | REUSE | dbo:Person | P58 via ScreenWriter; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:MovieDirector | REUSE | dbo:Person | P57; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:ScreenWriter | REUSE | dbo:Writer | P58; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Producer | REUSE | dbo:Person | P162; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Organisation | REUSE | dbo:Agent | DBpedia supertype of supported entities; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Company | REUSE | dbo:Organisation | P272; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Genre | REUSE | — | P136; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:MovieGenre | REUSE | dbo:Genre | P136 in film context; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Award | REUSE | — | P166; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Country | REUSE | — | P495; Reuse DBpedia meaning and its supported superclass; no local clone. |
| dbo:Language | REUSE | — | P364; Reuse DBpedia meaning and its supported superclass; no local clone. |
| ex:Contribution | CREATE | — | P57/P161/P58/P162; A local credit association with one person, film and role; not the person or film itself. |
| ex:ContributionRole | CREATE | — | The four crawled credit predicates; Local controlled role values, not subclasses of Person. |
| ex:SourceSnapshot | CREATE | — | snapshots.json URL/time/hash; A retrieved response record, not a domain entity. |
| void:Dataset | REUSE | — | Published collection of crawled film records; Reuse VoID dataset, remove ex:Dataset clone. |
| ex:ActionGenre | EXTEND | dbo:MovieGenre | P136 target English label; Local normalized film-genre bucket selected by matching the crawled English label; no DBpedia class of this narrow meaning in reference module. |
| ex:DramaGenre | EXTEND | dbo:MovieGenre | P136 target English label; Local normalized film-genre bucket selected by matching the crawled English label; no DBpedia class of this narrow meaning in reference module. |
| ex:ActingContribution | EXTEND | ex:Contribution | Credit claim corresponding to Actor; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:DirectingContribution | EXTEND | ex:Contribution | Credit claim corresponding to Director; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:WritingContribution | EXTEND | ex:Contribution | Credit claim corresponding to Writer; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:ProducingContribution | EXTEND | ex:Contribution | Credit claim corresponding to Producer; Local credit record classified by a fixed role; DBpedia Actor describes a person, not this record. |
| ex:Filmmaker | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:ActionFilm | EXTEND | dbo:Film | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningFilm | EXTEND | dbo:Film | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:MultiCreditContributor | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; At least two semantically distinct credit records. Different roles prove their distinctness; the name is shorthand and does not exclude repeated same-role credits. |
| ex:ThreeCreditContributor | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; At least three distinct credit records; three different role fillers prove distinctness. Not exactly three roles or an exhaustive career description. |
| ex:WriterDirector | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; A person with both directing and writing credits in this dataset; classification is never manually asserted. |
| ex:ActorFilmmaker | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningFilmmaker | EXTEND | dbo:Person | P57/P161/P58/P162; P166 when award-based; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:AwardWinningActionFilm | EXTEND | dbo:Film | P136/P166; Local dataset-specific OWL-defined subset; not a replacement for a DBpedia base class. |
| ex:GenreCrossingFilm | EXTEND | dbo:Film | P136/P166; Film carrying both action and drama genre memberships; this is not an unproved two-distinct-genre cardinality claim. |

## Quan hệ và datatype

| Property | Kiểu | Domain | Range | Inverse / subproperty | Căn cứ |
|---|---|---|---|---|---|
| dbo:director | Object | dbo:Film | dbo:Person | — / — | P57 |
| dbo:starring | Object | dbo:Work | dbo:Actor | — / — | P161 |
| dbo:writer | Object | dbo:Work | dbo:Person | — / — | P58 |
| dbo:producer | Object | dbo:Work | dbo:Agent | — / — | P162 |
| dbo:productionCompany | Object | dbo:Work | dbo:Company | — / — | P272 |
| dbo:award | Object | — | dbo:Award | — / — | P166 |
| dbo:genre | Object | — | dbo:Genre | — / — | P136 |
| dbo:country | Object | — | dbo:Country | — / — | P495 |
| dbo:language | Object | — | dbo:Language | — / — | P364 |
| ex:hasContribution | Object | dbo:Person | ex:Contribution | ex:contributionBy / — | Derived credit association |
| ex:contributionBy | Object | ex:Contribution | dbo:Person | — / — | P57/P161/P58/P162 |
| ex:contributionTo | Object | ex:Contribution | dbo:Film | ex:contributionOf / — | Containing source film |
| ex:contributionOf | Object | dbo:Film | ex:Contribution | — / — | Inverse of contributionTo |
| ex:hasRole | Object | ex:Contribution | ex:ContributionRole | — / — | Credit predicate to controlled role |
| ex:contributedTo | Object | dbo:Person | dbo:Film | — / — | OWL property chain |
| ex:directed | Object | dbo:Person | dbo:Film | dbo:director / ex:contributedTo | Inverse P57 |
| ex:actedIn | Object | dbo:Actor | dbo:Film | dbo:starring / ex:contributedTo | Inverse P161 |
| ex:productionOf | Object | dbo:Company | dbo:Work | dbo:productionCompany / — | Inverse P272 |
| ex:sourceSnapshot | Object | — | ex:SourceSnapshot | — / — | Crawled entity response provenance |
| dbo:runtime | Data | dbo:Work | xsd:double | — / — | P2047; normalize to seconds |
| ex:releaseYear | Data | dbo:Film | xsd:integer | — / — | Earliest Gregorian P577 year, precision >=9 |
| ex:sourceUrl | Data | ex:SourceSnapshot | xsd:anyURI | — / — | Snapshot manifest sourceUrl |
| ex:retrievedAt | Data | ex:SourceSnapshot | xsd:dateTime | — / — | Snapshot manifest retrievedAt |
| ex:sha256 | Data | ex:SourceSnapshot | xsd:string | — / — | Snapshot manifest sha256 |

## Ngữ nghĩa và kết quả

Reuse 17 lớp DBpedia và một lớp VoID; 19 lớp riêng mở rộng theo facts. Actor dùng range của starring. Contribution có ba endpoint functional/exactly 1. Chain hasContribution rồi contributionTo tạo contributedTo; cardinality đặt trên hasContribution.

Không có FeatureFilm/DocumentaryFilm/FictionGenre hoặc fallback FilmAward thiếu căn cứ. ActionGenre/DramaGenre là bucket nhãn. GenreCrossing không chứng minh hai genre filler khác nhau. HermiT: consistent; 17 người min 2 credit, 7 người min 3, 10 WriterDirector.

Định nghĩa Manchester/OWL và từng ví dụ thật nằm trong DBpedia_OWL_Design.md/html. Hướng dẫn học nền và thực hành nằm trong Huong_dan_doc_hieu_project.pdf.
