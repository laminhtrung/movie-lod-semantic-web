---
title: "MovieLOD: lời thuyết trình cho bộ 24 slide"
date: "Bản đầy đủ · 09/10/2026"
---

## Cách dùng

Bộ chính có **24 slide**, thuyết trình đầy đủ khoảng **18–22 phút**. Nội dung slide và Speaker Notes bằng tiếng Anh; script riêng giữ lời tiếng Việt tương ứng để tập nói. Hướng dẫn trong ô chờ ảnh vẫn bằng tiếng Việt. Bản ngắn 13 trang được cập nhật cùng model mới ở Slide_ngan_13.pptx/pdf và Script_thuyet_trinh_ngan_13.md/pdf. MP4 đã được loại theo yêu cầu; trình bày demo trực tiếp trên ứng dụng.

Tập theo 3 phần: thành viên A slide 1–10; B slide 11–18; C slide 19–24. Nếu chỉ có 2 người, chia sau slide 14. Các con số lấy từ dữ liệu và evidence hiện tại. Khung ảnh Protégé chưa có ảnh thực; không đọc ghi chú chờ bổ sung như kết quả đã chứng minh.

## Luồng rút gọn 12–15 phút

Ưu tiên slide 1–5, 9–10, 12–13, 15–17, 19–23. Các trang cây lớp, công thức cardinality và tra cứu IRI có thể dùng khi trả lời câu hỏi.

## Mục lục

| Slide | Nội dung |
|:--|:--|
| 01 | MovieLOD |
| 02 | Objectives and synchronized evidence |
| 03 | Architecture and knowledge layers |
| 04 | Dataset: units and counting scope |
| 05 | Ontology inventory: reuse before extension |
| 06 | Work and Film: meaningful inferred subsets |
| 07 | People and companies: reuse DBpedia hierarchy |
| 08 | Genre, awards and provenance |
| 09 | Contribution: person, film and role |
| 10 | Properties: reuse, inverse and chain |
| 11 | OWL axioms: what each statement means |
| 12 | Verified domain classes after HermiT |
| 13 | Nolan: facts → credit type → Filmmaker |
| 14 | Genuine minimum-cardinality reasoning |
| 15 | Source claims and reproducibility |
| 16 | RDF literals and DBpedia units |
| 17 | Linked data: identity and publication |
| 18 | Inception: RDF resource and OWL |
| 19 | SPARQL: choose the knowledge scope |
| 20 | Credit records and competency questions |
| 21 | Before / after: Nolan and WriterDirector |
| 22 | Verification of the final OWL |
| 23 | Coverage and limitations |
| 24 | Evidence capture and submission checklist |

## Slide 01 — MovieLOD

**Lời nói:**

Nhóm trình bày MovieLOD, một knowledge graph về điện ảnh. File OWL cuối hiện là bản 3.0.0, có 30 phim, 37 lớp có tên và 1.727 liên kết danh tính. Ví dụ xuyên suốt là Inception và Christopher Nolan. Chúng ta cần phân biệt ontology mới đã chạy HermiT với ứng dụng web vẫn dùng snapshot trước đó. Vì vậy, mỗi kết quả trong bài sẽ được gắn với đúng phiên bản và phạm vi kiểm tra.

**Chuyển trang:** Sau đây nhóm chuyển sang objectives and synchronized evidence.

## Slide 02 — Objectives and synchronized evidence

**Lời nói:**

Năm yêu cầu cốt lõi đã dùng chung ontology 3.0.0. Graph nguồn, graph suy luận và dataset trước/sau có trên web, endpoint và terminal. Slide, báo cáo và kết quả truy vấn khớp cùng model. MP4 đã xóa theo yêu cầu, không dựng lại video.

**Chuyển trang:** Sau đây nhóm chuyển sang architecture and knowledge layers.

## Slide 03 — Architecture and knowledge layers

**Lời nói:**

Collect cung cấp corpus đã crawl; build xuất model 3.0.0. HermiT phân loại OWL canonical; OWL RL bổ sung inverse, subproperty và chain. Validate chạy 27 câu hỏi. Web, endpoint và terminal dùng chung graph nguồn, graph suy luận và dataset so sánh.

**Chuyển trang:** Sau đây nhóm chuyển sang dataset: units and counting scope.

## Slide 04 — Dataset: units and counting scope

**Lời nói:**

Mẫu có 30 phim, 851 người, 1.010 credit record, 45 công ty và 672 thực thể giải thưởng. OWL đầy đủ chứa 19.025 triple, gồm schema và facts khai báo, chưa phải toàn bộ closure suy luận. Cần đọc đúng đơn vị: credit không phải số người, award entity không phải số lần trao giải. Các thống kê membership chỉ đếm IRI local để tránh tăng số do alias sameAs.

**Chuyển trang:** Sau đây nhóm chuyển sang ontology inventory: reuse before extension.

## Slide 05 — Ontology inventory: reuse before extension

**Lời nói:**

37 lớp gồm 17 lớp DBpedia, một lớp VoID Dataset và 19 lớp riêng. Các lớp riêng mô tả credit, nguồn, hai bucket thể loại và những subset suy luận có nghĩa rõ. Mười lớp domain có membership suy ra; bốn subclass credit hỗ trợ các chain. Nhóm không tạo lại Actor, Genre, Award hoặc Company dưới namespace riêng chỉ để tăng số lượng lớp.

**Ảnh cần bổ sung — P00:** `P00_ontology_header.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở ontology/Movie_Knowledge_Graph.owl.
2. Chọn Active Ontology / Ontology Header.
3. Giữ IRI và versionInfo 3.0.0 trong ảnh.

**Cần thấy:** 37 lớp có tên; không đếm biểu thức anonymous như lớp có tên.

**Chuyển trang:** Sau đây nhóm chuyển sang work and film: meaningful inferred subsets.

## Slide 06 — Work and Film: meaningful inferred subsets

**Lời nói:**

Film reuse DBpedia và nằm dưới Work. ActionFilm dựa vào genre; AwardWinningFilm dựa vào award; lớp giao kết hợp hai điều kiện. GenreCrossingFilm yêu cầu action và drama membership, nhưng chưa chứng minh có hai genre khác nhau. Các khai báo FeatureFilm, AnimatedFilm và DocumentaryFilm thiếu căn cứ trong model cuối đã được bỏ. Vì vậy cây lớp mới khác ảnh Protégé của bộ tài liệu cũ.

**Ảnh cần bổ sung — P01:** `P01_film_hierarchy.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Classes → dbo:Work → dbo:Film.
2. Hiện ActionFilm, AwardWinningFilm và các lớp giao.
3. Giữ IRI DBpedia của Film trong Description.

**Cần thấy:** Không có FeatureFilm/AnimatedFilm/DocumentaryFilm trong module cuối.

**Chuyển trang:** Sau đây nhóm chuyển sang people and companies: reuse dbpedia hierarchy.

## Slide 07 — People and companies: reuse DBpedia hierarchy

**Lời nói:**

Actor được suy ra từ range của starring và giữ nguyên IRI DBpedia. Nhóm cũng reuse MovieDirector, Writer, ScreenWriter và Producer. Restriction của credit hỗ trợ suy luận nghề theo một chiều, không định nghĩa lại toàn bộ class chuẩn. Company nằm dưới Organisation. Một người có thể đồng thời thỏa nhiều nghề và nhiều subset; Actor và Filmmaker không bị ép disjoint.

**Ảnh cần bổ sung — P02:** `P02_agent_hierarchy.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở dbo:Agent → dbo:Person và dbo:Organisation.
2. Hiện Artist → Actor; Organisation → Company.
3. Mở MovieDirector / Writer → ScreenWriter.

**Cần thấy:** Reuse lớp DBpedia; không tạo ex:Actor hoặc ex:Organization.

**Chuyển trang:** Sau đây nhóm chuyển sang genre, awards and provenance.

## Slide 08 — Genre, awards and provenance

**Lời nói:**

Genre và MovieGenre là lớp chuẩn. ActionGenre và DramaGenre là bucket dựa trên nhãn genre đã crawl, theo chính sách ánh xạ của nhóm. Chúng không phải taxonomy OWL mà nguồn đã cung cấp. Nhóm không đoán FictionGenre và không gán mọi award chưa nhận diện thành FilmAward. SourceSnapshot phục vụ truy nguồn; void:Dataset mô tả tập dữ liệu. Cách phân biệt này giúp tránh suy diễn ngoài nguồn.

**Ảnh cần bổ sung — P03:** `P03_genre_award_hierarchy.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở dbo:Genre → dbo:MovieGenre.
2. Hiện ActionGenre / DramaGenre; chọn dbo:Award.
3. Giữ Description để đọc IRI và lớp cha.

**Cần thấy:** Không có FictionGenre hoặc các nhóm award suy đoán theo nhãn.

**Chuyển trang:** Sau đây nhóm chuyển sang contribution: person, film and role.

## Slide 09 — Contribution: person, film and role

**Lời nói:**

Contribution là record nối một người, một phim và một role. Ba endpoint có tính functional và qualified exactly-one restrictions. Nolan có ba credit riêng trên Inception cho directing, writing và producing. Role là individual của vocabulary kiểm soát, không phải Person. Các subclass credit được suy ra từ hasRole value. Exactly one không tự báo dữ liệu thiếu dưới giả định thế giới mở; cần structural validation riêng.

**Ảnh cần bổ sung — P04:** `P04_contribution_restrictions.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:Contribution.
2. Hiện exactly 1 cho contributionBy, contributionTo, hasRole.
3. Chọn hasRole để thấy Functional và role individual.

**Cần thấy:** Ba endpoint đúng 1; dữ liệu thiếu cần structural validation riêng.

**Chuyển trang:** Sau đây nhóm chuyển sang properties: reuse, inverse and chain.

## Slide 10 — Properties: reuse, inverse and chain

**Lời nói:**

Các quan hệ phim phổ biến dùng DBpedia. Inverse của contributionBy cho đường đi hasContribution từ người đến credit. Chain hasContribution rồi contributionTo suy ra contributedTo từ người đến phim. Directed và actedIn là quan hệ cụ thể hơn. Property chain làm contributedTo trở thành non-simple, nên cardinality đặt trên hasContribution, không đặt trên contributedTo. Kết quả có 965 cặp người–phim local.

**Ảnh cần bổ sung — P05:** `P05_object_property.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn contributionBy: Contribution → dbo:Person.
2. Hiện Functional và inverse hasContribution.
3. Có thể chụp contributedTo với property chain.

**Cần thấy:** Chain hasContribution rồi contributionTo; không đặt cardinality trên contributedTo.

**Tra cứu khi bảo vệ (không đọc toàn bộ):**

Reference: all 19 object properties (not intended to be read aloud in full):
| Property | Domain | Range | Inverse / characteristics |
|:--|:--|:--|:--|
| dbo:award | — | dbo:Award | — |
| dbo:country | — | dbo:Country | — |
| dbo:director | dbo:Film | dbo:Person | ex:directed |
| dbo:genre | — | dbo:Genre | — |
| dbo:language | — | dbo:Language | — |
| dbo:producer | dbo:Work | dbo:Agent | — |
| dbo:productionCompany | dbo:Work | dbo:Company | ex:productionOf |
| dbo:starring | dbo:Work | dbo:Actor | ex:actedIn |
| dbo:writer | dbo:Work | dbo:Person | — |
| ex:actedIn | dbo:Actor | dbo:Film | dbo:starring |
| ex:contributedTo | dbo:Person | dbo:Film | — |
| ex:contributionBy | ex:Contribution | dbo:Person | ex:hasContribution · functional |
| ex:contributionOf | dbo:Film | ex:Contribution | ex:contributionTo |
| ex:contributionTo | ex:Contribution | dbo:Film | ex:contributionOf · functional |
| ex:directed | dbo:Person | dbo:Film | dbo:director |
| ex:hasContribution | dbo:Person | ex:Contribution | ex:contributionBy |
| ex:hasRole | ex:Contribution | ex:ContributionRole | — · functional |
| ex:productionOf | dbo:Company | dbo:Work | dbo:productionCompany |
| ex:sourceSnapshot | — | ex:SourceSnapshot | — |

**Chuyển trang:** Sau đây nhóm chuyển sang owl axioms: what each statement means.

## Slide 11 — OWL axioms: what each statement means

**Lời nói:**

EquivalentClass phát biểu điều kiện cần và đủ; SubClassOf chỉ một chiều. SOME nhận diện sự tồn tại của filler, VALUE trỏ đến role cụ thể. Functional có thể buộc hai filler đồng nhất; nó không đơn thuần là quy tắc từ chối nhập liệu. Thiếu triple không tự là phủ định, và IRI khác nhau không tự chứng minh cá thể khác nhau. Đây là các điểm phải nhớ khi đọc kết quả reasoner.

**Chuyển trang:** Sau đây nhóm chuyển sang verified domain classes after hermit.

## Slide 12 — Verified domain classes after HermiT

**Lời nói:**

Bảng liệt kê mười subset domain có membership HermiT thật. Trong đó có bảy lớp bổ sung ngoài Filmmaker, ActionFilm và AwardWinningFilm. Actor dùng range chuẩn của DBpedia, còn bốn loại Contribution là bước trung gian. Tất cả type subset ở bảng đều có zero assertion trong đầu vào. Nhóm không dùng COUNT DISTINCT để gán các class này rồi gọi đó là entailment OWL DL.

**Chuyển trang:** Sau đây nhóm chuyển sang nolan: facts → credit type → filmmaker.

## Slide 13 — Nolan: facts → credit type → Filmmaker

**Lời nói:**

Credit của Nolan có DirectorRole nên thỏa DirectingContribution. Inverse tạo hasContribution; điều kiện SOME và OR của Filmmaker nhận diện Nolan. Credit writing tạo ScreenWriter, directing tạo MovieDirector, rồi giao hai nghề tạo WriterDirector. Các type này không được gán thủ công. Đây là chain giải thích nhiều bước dựa trên cùng facts; OWL không bắt reasoner chạy theo đúng thứ tự trình bày trên sơ đồ.

**Ảnh cần bổ sung — P06:** `P06_filmmaker_equivalent_class.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:Filmmaker.
2. Hiện Equivalent To với Person AND các nhánh SOME.
3. Đọc các nhánh Directing / Writing / ProducingContribution.

**Cần thấy:** Công thức không tự chứng minh reasoner đã chạy.

**Chuyển trang:** Sau đây nhóm chuyển sang genuine minimum-cardinality reasoning.

## Slide 14 — Genuine minimum-cardinality reasoning

**Lời nói:**

Ba credit của Nolan có DirectorRole, WriterRole và ProducerRole khác nhau. hasRole là functional; các role được khai báo AllDifferent theo nghĩa của vocabulary kiểm soát. Nếu hai credit đồng nhất, một record phải có hai role khác nhau và gây mâu thuẫn. Vì vậy HermiT chứng minh ít nhất ba credit khác nhau. Có 7 người đạt min 3 và 17 người đạt min 2. Genre vẫn thiếu bằng chứng inequality.

**Ảnh cần bổ sung — P07:** `P07_three_credit_cardinality.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:ThreeCreditContributor; hiện min 3 hasContribution Contribution.
2. Chạy HermiT; chọn Nolan ở inferred view.
3. Chụp thêm Functional hasRole và AllDifferent của bốn role.

**Cần thấy:** 7 người đạt min 3; 17 người đạt min 2; không phải COUNT DISTINCT.

**Chuyển trang:** Sau đây nhóm chuyển sang source claims and reproducibility.

## Slide 15 — Source claims and reproducibility

**Lời nói:**

Dữ liệu thực tế có người và role, genre, award, company, country, language, năm và thời lượng. Không bổ sung budget hoặc ratings nếu chưa crawl. 76 phản hồi giữ URL, thời điểm và checksum. Hash chỉ kiểm tra byte nguyên vẹn, không chứng minh mọi claim đúng ngoài đời. Ánh xạ genre theo nhãn là chính sách nhóm, cần được đánh giá chất lượng riêng khi mở rộng mẫu.

**Chuyển trang:** Sau đây nhóm chuyển sang rdf literals and dbpedia units.

## Slide 16 — RDF literals and DBpedia units

**Lời nói:**

Inception có label, năm 2010 và runtime 8.880 giây, tương đương 148 phút. Runtime reuse DBpedia với range double. Model có năm datatype property; rdfs:label là annotation, không phải một custom title datatype. releaseYear là summary theo chính sách chọn năm từ nguồn, không phải ngày phát hành đầy đủ. Điều quan trọng khi reuse là giữ đúng nghĩa, kiểu dữ liệu và đơn vị.

**Ảnh cần bổ sung — P08:** `P08_runtime_datatype.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn dbo:runtime trong Data properties.
2. Hiện domain dbo:Work và range xsd:double.
3. Chọn Inception: runtime = 8880 giây.

**Cần thấy:** 8880 giây = 148 phút; rdfs:label là annotation property.

**Chuyển trang:** Sau đây nhóm chuyển sang linked data: identity and publication.

## Slide 17 — Linked data: identity and publication

**Lời nói:**

Website cung cấp RDF, schema, full OWL và inference 3.0.0. HTTP IRI và giấy phép hỗ trợ reuse. Có 1.699 link Wikidata và 28 link DBpedia. Reuse dbo:Film, sameAs và provenance có ba ý nghĩa khác nhau.

**Chuyển trang:** Sau đây nhóm chuyển sang inception: rdf resource and owl.

## Slide 18 — Inception: RDF resource and OWL

**Lời nói:**

Trang resource mô tả Inception bằng property DBpedia, năm, thời lượng giây, identity và provenance. Khung ảnh yêu cầu cùng cá thể trong Protégé. Ảnh web và screenshot ontology là hai loại minh chứng khác nhau.

**Ảnh cần bổ sung — P09:** `P09_inception_individual.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Movie_Knowledge_Graph.owl 3.0.0.
2. Chọn film-Q25188; hiện label, releaseYear 2010, runtime 8880.
3. Hiện dbo:director, genre, productionCompany và award.

**Cần thấy:** Cá thể trong OWL khớp trang resource 3.0.0; runtime là 8880 giây.

**Chuyển trang:** Sau đây nhóm chuyển sang sparql: choose the knowledge scope.

## Slide 19 — SPARQL: choose the knowledge scope

**Lời nói:**

Query Inception trả 2010, 8.880 giây và Nolan. Chọn scope dữ liệu nguồn, graph inference đã tính hoặc named graph trước/sau. Browser dùng Comunica; endpoint dùng RDFLib. Cả hai truy vấn chung exports, không chạy HermiT lại mỗi lần.

**Chuyển trang:** Sau đây nhóm chuyển sang credit records and competency questions.

## Slide 20 — Credit records and competency questions

**Lời nói:**

Inception có 25 credit: 21 acting, một directing, một writing và hai producing. Ảnh truy vấn Nolan thể hiện ba vai trò của một người. Web có 27 mẫu query và chọn scope đúng theo mẫu. Khi đếm, giới hạn IRI local để loại alias; phân biệt record, người và cặp người–phim.

**Chuyển trang:** Sau đây nhóm chuyển sang before / after: nolan and writerdirector.

## Slide 21 — Before / after: Nolan and WriterDirector

**Lời nói:**

WriterDirector có zero assertion và 10 người sau inference. Chọn scope để so sánh cùng query trước/sau. Query 27 dùng named graph; terminal có --mode asserted, reasoned, dataset. Cardinality do HermiT suy ra, không gán bằng đếm IRI.

**Ảnh cần bổ sung — P10:** `P10_nolan_inferred_types.png`; mở `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn HermiT → Start reasoner, chờ hoàn tất.
2. Chọn person-Q25191; mở inferred types.
3. Giữ WriterDirector, Filmmaker, ThreeCreditContributor trong ảnh.

**Cần thấy:** Type mới không được gán trực tiếp trong asserted graph; giữ trạng thái reasoner.

**Tra cứu khi bảo vệ (không đọc toàn bộ):**

Reference: 27 design queries, asserted versus reasoned results:
1. List films: 30 → 30
2. Inception: year, duration and director: 1 → 1
3. Directors of Inception: 1 → 1
4. Inception credits and roles: 25 → 25
5. Films directed by Nolan: 8 → 8
6. Companies credited on Inception: 4 → 4
7. Awards of Inception: 7 → 7
8. Runtime in seconds: 1 → 1
9. Film genres through the parent class: 0 → 75
10. Persons through Agent hierarchy: 0 → 851
11. Production companies: 45 → 45
12. Film subclasses: 0 → 4
13. Actors through Artist hierarchy: 0 → 769
14. Inferred Actors: 0 → 769
15. Inferred Filmmakers: 0 → 89
16. Inferred Action films: 0 → 12
17. Award-winning films: 0 → 26
18. People with at least two provably distinct credits: 0 → 17
19. People with at least three provably distinct credits: 0 → 7
20. Writer-directors: 0 → 10
21. Actor-filmmakers: 0 → 7
22. Award-winning filmmakers: 0 → 65
23. Award-winning action films: 0 → 10
24. Action/drama crossing films: 0 → 8
25. Nolan contributions through property chain: 0 → 8
26. Nolan films through inverse director: 0 → 8
27. Types present only after reasoning: 0 → 1261

**Chuyển trang:** Sau đây nhóm chuyển sang verification of the final owl.

## Slide 22 — Verification of the final OWL

**Lời nói:**

HermiT kiểm tra đúng full OWL: consistent, không có named class bất khả thỏa. 27 competency queries chạy theo scope rõ ràng; 965 chain pairs được materialize riêng. 16 tests kiểm tra model và endpoint. Browser kiểm tra SELECT, ASK, CONSTRUCT, DESCRIBE và phục hồi sau query sai cú pháp.

**Chuyển trang:** Sau đây nhóm chuyển sang coverage and limitations.

## Slide 23 — Coverage and limitations

**Lời nói:**

Ontology, data, các giao diện query và tài liệu cùng 3.0.0. Consistency, toàn vẹn nguồn và before/after được kiểm tra riêng. Mẫu có chủ đích, label mapping và matching chưa có ground truth vẫn là giới hạn. MP4 đã loại theo yêu cầu; kiểm tra kỹ thuật không phải điểm chính thức.

**Chuyển trang:** Sau đây nhóm chuyển sang evidence capture and submission checklist.

## Slide 24 — Evidence capture and submission checklist

**Lời nói:**

Các ô còn lại yêu cầu screenshot Protégé thật. Script Việt khớp slide Anh; báo cáo học thuật giữ 15 trang. Ảnh web hiện tại và log reasoner hỗ trợ trình bày. MP4 đã xóa, không chỉnh nội dung hoặc dựng lại video.

**Chuyển trang:** Nhóm xin mời thầy cô đặt câu hỏi.

## Câu hỏi bảo vệ ngắn

**37 lớp khác gì 30 phim?** 37 là lớp có tên; 30 là cá thể Film trong mẫu. Protégé Metrics có thể tính thêm lớp ngoài được tham chiếu.

**Vì sao cần Contribution?** Một người có nhiều vai trò trong nhiều phim; mỗi bộ người–phim–vai trò có bản ghi riêng.

**Vì sao exact cardinality chưa thay Python?** OWL dùng thế giới mở; Python kiểm tra trường bắt buộc của ứng dụng.

**COUNT DISTINCT có phải suy luận DL không?** Đếm tên IRI là quy tắc ứng dụng; OWL không mặc định tên khác nhau chỉ cá thể khác nhau.

**Endpoint thiếu lớp mới có phải lỗi OWL?** Chọn scope source/inference/named graphs phù hợp; HermiT không chạy lại cho mỗi query.

**sameAs khác nguồn thế nào?** sameAs là cùng danh tính; sourceSnapshot là xuất xứ; dbo:Film là tái dùng từ vựng.

**SQL có trả được các câu hỏi không?** Có, bằng JOIN/view/quy tắc. Giá trị của bài là IRI, từ vựng chung, liên kết, nguồn và định nghĩa ngữ nghĩa.

**Ảnh Protégé có chứng minh reasoner đã chạy không?** Ảnh cây asserted/định nghĩa chỉ chứng minh khai báo. Muốn dùng ảnh inferred, phải ghi rõ reasoner và trạng thái/kết quả thật.
