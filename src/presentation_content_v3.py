"""Canonical version-three slide content; English slides and Vietnamese photo instructions."""
SLIDES = [{'number': 1,
  'title': 'MovieLOD',
  'subtitle': 'DBpedia reuse · OWL reasoning · linked movie knowledge',
  'kind': 'cover',
  'section': 'MovieLOD',
  'speech': 'We present the final local ontology, version 3.0.0. It contains 30 films, 37 named classes and 1,727 '
            'identity links. We distinguish the verified ontology from the web application, which now uses the '
            'same canonical vocabulary. Our examples use real Inception and Christopher Nolan records.',
  'speech_vi': 'Nhóm trình bày MovieLOD, một knowledge graph về điện ảnh. File OWL cuối hiện là bản 3.0.0, có 30 '
               'phim, 37 lớp có tên và 1.727 liên kết danh tính. Ví dụ xuyên suốt là Inception và Christopher '
               'Nolan. Chúng ta cần phân biệt ontology mới đã chạy HermiT với ứng dụng web vẫn dùng snapshot '
               'trước đó. Vì vậy, mỗi kết quả trong bài sẽ được gắn với đúng phiên bản và phạm vi kiểm tra.'},
 {'number': 2,
  'title': 'Objectives and synchronized evidence',
  'subtitle': 'Ontology, data, publication, linking and SPARQL access',
  'kind': 'requirements',
  'section': 'Objectives and synchronized evidence',
  'speech': 'The five core requirements share ontology version 3.0.0. The source graph, inferred graph and named '
            'before/after dataset are available in the browser and local endpoint. The report, slides and query results '
            'describe the same model. MP4 files were removed at the user’s request; no video was regenerated.',
  'rows': [['R1', 'DBpedia-based ontology', '37 named classes; HermiT consistency'],
           ['R2', 'Source-supported data', '76 retained responses and provenance'],
           ['R3', 'RDF publication', 'Canonical RDF / OWL 3.0.0'],
           ['R4', 'Identity alignment', '1,699 Wikidata + 28 DBpedia links'],
           ['R5', 'SPARQL access', '27 questions; source / inferred / named graph modes']],
  'speech_vi': 'Năm yêu cầu cốt lõi đã dùng chung ontology 3.0.0. Graph nguồn, graph suy luận và dataset '
               'trước/sau có trên web, endpoint và terminal. Slide, báo cáo và kết quả truy vấn khớp cùng model. '
               'MP4 đã xóa theo yêu cầu, không dựng lại video.'},
 {'number': 3,
  'title': 'Architecture and knowledge layers',
  'subtitle': 'One reproducible pipeline across every interface',
  'kind': 'pipeline',
  'section': 'Architecture and knowledge layers',
  'speech': 'The source collector feeds a native version-3 build. HermiT classifies the canonical OWL, and OWL RL '
            'materializes inverse, subproperty and chain relations. Validation executes all 27 competency '
            'questions. Source facts, inferred knowledge and named-graph comparisons are shared by the browser, '
            'endpoint and terminal.',
  'stages': [['01', 'SOURCE FACTS', '76 retained responses\n+ provenance'],
             ['02', 'BUILD 3.0.0', 'Canonical RDF / OWL\n+ resource pages'],
             ['03', 'REASON / CHECK', 'HermiT + OWL RL\n27 query checks'],
             ['04', 'QUERY MODES', 'Source / inference\nBefore / after']],
  'speech_vi': 'Collect cung cấp corpus đã crawl; build xuất model 3.0.0. HermiT phân loại OWL canonical; OWL RL '
               'bổ sung inverse, subproperty và chain. Validate chạy 27 câu hỏi. Web, endpoint và terminal dùng '
               'chung graph nguồn, graph suy luận và dataset so sánh.'},
 {'number': 4,
  'title': 'Dataset: units and counting scope',
  'subtitle': 'Final OWL: 19,025 triples including schema and asserted facts',
  'kind': 'metrics',
  'section': 'Dataset: units and counting scope',
  'speech': 'The selected sample has 30 films, 851 people, 1,010 credit records, 45 companies and 672 award '
            'entities. The final OWL contains 19,025 triples including schema and asserted data, not a complete '
            'reasoning closure. There are 75 genres, 11 countries, 15 languages and 76 source responses. Counts '
            'refer to local resource identifiers; the four role individuals use the ontology namespace.',
  'metrics': [['30', 'films'],
              ['851', 'people'],
              ['1,010', 'credit records'],
              ['45', 'companies'],
              ['672', 'award entities'],
              ['76', 'source responses']],
  'footer': '37 named classes · 19 object + 5 datatype properties · 4 controlled role individuals',
  'speech_vi': 'Mẫu có 30 phim, 851 người, 1.010 credit record, 45 công ty và 672 thực thể giải thưởng. OWL đầy '
               'đủ chứa 19.025 triple, gồm schema và facts khai báo, chưa phải toàn bộ closure suy luận. Cần đọc '
               'đúng đơn vị: credit không phải số người, award entity không phải số lần trao giải. Các thống kê '
               'membership chỉ đếm IRI local để tránh tăng số do alias sameAs.'},
 {'number': 5,
  'title': 'Ontology inventory: reuse before extension',
  'subtitle': '17 DBpedia classes + 1 VoID class + 19 local classes',
  'kind': 'ontology_overview',
  'section': 'Ontology inventory: reuse before extension',
  'speech': 'The module has 37 named classes: 17 DBpedia classes, one VoID Dataset and 19 local classes. The '
            'local classes comprise source records, the contribution model, two label-based genre buckets and ten '
            'domain inferred classes. Four additional inferred credit subclasses support the reasoning chains. No '
            'local clone of Actor, Genre, Award or Company remains.',
  'photo': 'P00',
  'groups': [['17 classes', 'DBpedia classes and hierarchy'],
             ['1 class', 'void:Dataset'],
             ['3 classes', 'Contribution / Role / SourceSnapshot'],
             ['2 classes', 'ActionGenre / DramaGenre'],
             ['4 classes', 'Role-defined credit subclasses'],
             ['10 classes', 'Domain inferred subsets']],
  'speech_vi': '37 lớp gồm 17 lớp DBpedia, một lớp VoID Dataset và 19 lớp riêng. Các lớp riêng mô tả credit, '
               'nguồn, hai bucket thể loại và những subset suy luận có nghĩa rõ. Mười lớp domain có membership '
               'suy ra; bốn subclass credit hỗ trợ các chain. Nhóm không tạo lại Actor, Genre, Award hoặc Company '
               'dưới namespace riêng chỉ để tăng số lượng lớp.'},
 {'number': 6,
  'title': 'Work and Film: meaningful inferred subsets',
  'subtitle': 'No unsupported feature, animation or documentary declarations',
  'kind': 'hierarchy',
  'section': 'Work and Film: meaningful inferred subsets',
  'speech': 'Film reuses DBpedia and is a Work. ActionFilm and AwardWinningFilm follow genre and award facts. '
            'AwardWinningActionFilm combines those memberships. GenreCrossingFilm requires action and drama '
            'membership but does not prove two distinct genre fillers. Unsupported release-kind assertions and '
            'empty documentary classes were removed.',
  'photo': 'P01',
  'tree': [(0, 'dbo:Work'),
           (1, 'dbo:Film · 30'),
           (2, 'ActionFilm · 12'),
           (2, 'AwardWinningFilm · 26'),
           (2, 'AwardWinningActionFilm · 10'),
           (2, 'GenreCrossingFilm · 8')],
  'footer': 'Membership is inferred from source-supported facts; genre buckets are explicit author mappings.',
  'speech_vi': 'Film reuse DBpedia và nằm dưới Work. ActionFilm dựa vào genre; AwardWinningFilm dựa vào award; '
               'lớp giao kết hợp hai điều kiện. GenreCrossingFilm yêu cầu action và drama membership, nhưng chưa '
               'chứng minh có hai genre khác nhau. Các khai báo FeatureFilm, AnimatedFilm và DocumentaryFilm '
               'thiếu căn cứ trong model cuối đã được bỏ. Vì vậy cây lớp mới khác ảnh Protégé của bộ tài liệu '
               'cũ.'},
 {'number': 7,
  'title': 'People and companies: reuse DBpedia hierarchy',
  'subtitle': 'Actor and Filmmaker may overlap; roles remain individuals',
  'kind': 'hierarchy',
  'section': 'People and companies: reuse DBpedia hierarchy',
  'speech': 'Actor is inferred using the range of starring and remains the DBpedia class. The module also reuses '
            'MovieDirector, Writer, ScreenWriter and Producer. Contribution restrictions support one-way '
            'occupation inferences without redefining these global classes. Company is a subclass of '
            'Organisation. A person may satisfy several occupations and local subsets.',
  'photo': 'P02',
  'tree': [(0, 'dbo:Agent'),
           (1, 'dbo:Person · 851'),
           (2, 'dbo:Artist → dbo:Actor · 769'),
           (2, 'dbo:MovieDirector · 17'),
           (2, 'dbo:Writer → ScreenWriter · 34'),
           (2, 'dbo:Producer · 57'),
           (2, 'Filmmaker · 89; WriterDirector · 10'),
           (1, 'dbo:Organisation'),
           (2, 'dbo:Company · 45')],
  'footer': 'No ex:Actor / Organization / ProductionCompany clones; four role values describe credit records.',
  'speech_vi': 'Actor được suy ra từ range của starring và giữ nguyên IRI DBpedia. Nhóm cũng reuse MovieDirector, '
               'Writer, ScreenWriter và Producer. Restriction của credit hỗ trợ suy luận nghề theo một chiều, '
               'không định nghĩa lại toàn bộ class chuẩn. Company nằm dưới Organisation. Một người có thể đồng '
               'thời thỏa nhiều nghề và nhiều subset; Actor và Filmmaker không bị ép disjoint.'},
 {'number': 8,
  'title': 'Genre, awards and provenance',
  'subtitle': 'Explicit label mappings are distinguished from logical entailment',
  'kind': 'genre_award',
  'section': 'Genre, awards and provenance',
  'speech': 'Genre and MovieGenre are reused. The two local buckets ActionGenre and DramaGenre use crawled '
            'English genre labels. No fiction hierarchy is guessed, and unrecognized awards are not automatically '
            'called FilmAward. Award remains a reused entity class. SourceSnapshot records retrieval provenance, '
            'while void:Dataset describes the collection.',
  'photo': 'P03',
  'genre': ['dbo:Genre',
            '  dbo:MovieGenre',
            '    ex:ActionGenre · 3 genre entities',
            '    ex:DramaGenre · 9 genre entities'],
  'awards': ['dbo:Award · 672 entities', '  Film and person award facts', '  No guessed award subclasses'],
  'footer': 'Supporting vocabulary: dbo:Country / Language · ex:SourceSnapshot · void:Dataset',
  'speech_vi': 'Genre và MovieGenre là lớp chuẩn. ActionGenre và DramaGenre là bucket dựa trên nhãn genre đã '
               'crawl, theo chính sách ánh xạ của nhóm. Chúng không phải taxonomy OWL mà nguồn đã cung cấp. Nhóm '
               'không đoán FictionGenre và không gán mọi award chưa nhận diện thành FilmAward. SourceSnapshot '
               'phục vụ truy nguồn; void:Dataset mô tả tập dữ liệu. Cách phân biệt này giúp tránh suy diễn ngoài '
               'nguồn.'},
 {'number': 9,
  'title': 'Contribution: person, film and role',
  'subtitle': 'Exactly one endpoint of each kind per credit record',
  'kind': 'contribution',
  'section': 'Contribution: person, film and role',
  'speech': 'Each Contribution relates one person, one film and one role, with functional endpoints and qualified '
            'exactly-one restrictions. Nolan has directing, writing and producing credits for Inception. '
            'Role-specific credit subclasses are inferred using hasRole value restrictions. Missing fields still '
            'require structural validation under open-world semantics.',
  'photo': 'P04',
  'points': ['4 role individuals',
             'Nolan: 3 roles on Inception',
             '1,010 credit records',
             'Keep association-level provenance'],
  'speech_vi': 'Contribution là record nối một người, một phim và một role. Ba endpoint có tính functional và '
               'qualified exactly-one restrictions. Nolan có ba credit riêng trên Inception cho directing, '
               'writing và producing. Role là individual của vocabulary kiểm soát, không phải Person. Các '
               'subclass credit được suy ra từ hasRole value. Exactly one không tự báo dữ liệu thiếu dưới giả '
               'định thế giới mở; cần structural validation riêng.'},
 {'number': 10,
  'title': 'Properties: reuse, inverse and chain',
  'subtitle': '19 object properties; custom relations describe credit context',
  'kind': 'properties',
  'section': 'Properties: reuse, inverse and chain',
  'speech': 'Direct film relations reuse DBpedia. The inverse of contributionBy supports hasContribution. '
            'contributedTo is entailed through the hasContribution/contributionTo property chain. Directed and '
            'actedIn are narrower subproperties. The chain property is non-simple, so the cardinality model uses '
            'the simple hasContribution relation.',
  'photo': 'P05',
  'rows': [['contributionBy', 'Credit → Person', 'hasContribution'],
           ['contributionTo', 'Credit → Film', 'contributionOf'],
           ['hasRole', 'Credit → Role', 'functional'],
           ['dbo:director', 'Film → Person', 'ex:directed'],
           ['dbo:starring', 'Work → Actor', 'ex:actedIn'],
           ['contributedTo', 'Person → Film', 'property chain']],
  'speech_vi': 'Các quan hệ phim phổ biến dùng DBpedia. Inverse của contributionBy cho đường đi hasContribution '
               'từ người đến credit. Chain hasContribution rồi contributionTo suy ra contributedTo từ người đến '
               'phim. Directed và actedIn là quan hệ cụ thể hơn. Property chain làm contributedTo trở thành '
               'non-simple, nên cardinality đặt trên hasContribution, không đặt trên contributedTo. Kết quả có '
               '965 cặp người–phim local.'},
 {'number': 11,
  'title': 'OWL axioms: what each statement means',
  'subtitle': 'Model semantics and structural data validation answer different questions',
  'kind': 'owl_rules',
  'section': 'OWL axioms: what each statement means',
  'speech': 'Equivalent classes express necessary and sufficient conditions; subclass axioms have one direction. '
            'Existential and value restrictions classify credits and people. Functional properties can force '
            'equality, while different role values provide distinctness witnesses. Missing facts do not imply '
            'negation, and different IRIs alone do not prove different individuals.',
  'cards': [['Class definitions',
             'AND / OR / SOME / VALUE\nConditions produce types not asserted in source facts.'],
            ['Exactly one endpoint',
             'Contribution: one person, film and role.\nMissing-field checks are separate.'],
            ['Inverse and property chain',
             'hasContribution o contributionTo → contributedTo\n965 local person–film pairs.'],
            ['Open world and identity',
             'Missing facts do not imply falsehood.\nDifferent IRIs do not establish inequality.']],
  'speech_vi': 'EquivalentClass phát biểu điều kiện cần và đủ; SubClassOf chỉ một chiều. SOME nhận diện sự tồn '
               'tại của filler, VALUE trỏ đến role cụ thể. Functional có thể buộc hai filler đồng nhất; nó không '
               'đơn thuần là quy tắc từ chối nhập liệu. Thiếu triple không tự là phủ định, và IRI khác nhau không '
               'tự chứng minh cá thể khác nhau. Đây là các điểm phải nhớ khi đọc kết quả reasoner.'},
 {'number': 12,
  'title': 'Verified domain classes after HermiT',
  'subtitle': 'All listed types have zero assertions in the input data',
  'kind': 'defined_table',
  'section': 'Verified domain classes after HermiT',
  'speech': 'Ten domain subsets have genuine HermiT members, including seven additional subsets beyond Filmmaker, '
            'ActionFilm and AwardWinningFilm. The four credit subclasses are supporting definitions. Actor uses '
            'DBpedia range reasoning. Counts are local identifiers only. No COUNT DISTINCT aggregate is used to '
            'produce these domain class memberships.',
  'footer': 'Supporting credit types: Acting 855 · Directing 31 · Writing 51 · Producing 73; dbo:Actor 769.',
  'speech_vi': 'Bảng liệt kê mười subset domain có membership HermiT thật. Trong đó có bảy lớp bổ sung ngoài '
               'Filmmaker, ActionFilm và AwardWinningFilm. Actor dùng range chuẩn của DBpedia, còn bốn loại '
               'Contribution là bước trung gian. Tất cả type subset ở bảng đều có zero assertion trong đầu vào. '
               'Nhóm không dùng COUNT DISTINCT để gán các class này rồi gọi đó là entailment OWL DL.'},
 {'number': 13,
  'title': 'Nolan: facts → credit type → Filmmaker',
  'subtitle': 'A multi-step explanation grounded in real records',
  'kind': 'nolan_chain',
  'section': 'Nolan: facts → credit type → Filmmaker',
  'speech': 'A directing record with DirectorRole becomes DirectingContribution. The inverse property supplies '
            'hasContribution for Nolan. The existential and union definition yields Filmmaker. Writing credits '
            'additionally support ScreenWriter; directing credits support MovieDirector, and their intersection '
            'yields WriterDirector. These types are not manually asserted.',
  'photo': 'P06',
  'steps': [['SOURCE FACTS', 'Nolan a dbo:Person; credit hasRole DirectorRole.'],
            ['CREDIT CLASS', 'credit a DirectingContribution; inverse yields hasContribution.'],
            ['PERSON CLASS', 'Nolan a Filmmaker; directing + writing also yield WriterDirector.']],
  'footer': 'Nolan: 8 directed films, 22 credit IRIs in the sample; three roles on Inception.',
  'speech_vi': 'Credit của Nolan có DirectorRole nên thỏa DirectingContribution. Inverse tạo hasContribution; '
               'điều kiện SOME và OR của Filmmaker nhận diện Nolan. Credit writing tạo ScreenWriter, directing '
               'tạo MovieDirector, rồi giao hai nghề tạo WriterDirector. Các type này không được gán thủ công. '
               'Đây là chain giải thích nhiều bước dựa trên cùng facts; OWL không bắt reasoner chạy theo đúng thứ '
               'tự trình bày trên sơ đồ.'},
 {'number': 14,
  'title': 'Genuine minimum-cardinality reasoning',
  'subtitle': 'Functional hasRole + different roles prove distinct credits',
  'kind': 'cardinality',
  'section': 'Genuine minimum-cardinality reasoning',
  'speech': 'Nolan has directing, writing and producing credits with different controlled role values. Because '
            'hasRole is functional and the roles are AllDifferent, these records cannot be the same individual. '
            'HermiT entails at least three distinct Contributions. Seven people satisfy min three and seventeen '
            'min two. Genre cardinality still lacks inequality witnesses; MultiGenreFilm is not retained as a '
            'populated inferred class.',
  'photo': 'P07',
  'cards': [['MultiCreditContributor · 17',
             'Person and hasContribution min 2 Contribution.\nDistinctness needs semantic evidence.'],
            ['ThreeCreditContributor · 7',
             'Person and hasContribution min 3 Contribution.\nNolan supplies three different-role witnesses.']],
  'footer': 'Negative test: min 2 genres gives 0 DL members; SQL/SPARQL counting is a different claim.',
  'speech_vi': 'Ba credit của Nolan có DirectorRole, WriterRole và ProducerRole khác nhau. hasRole là functional; '
               'các role được khai báo AllDifferent theo nghĩa của vocabulary kiểm soát. Nếu hai credit đồng '
               'nhất, một record phải có hai role khác nhau và gây mâu thuẫn. Vì vậy HermiT chứng minh ít nhất ba '
               'credit khác nhau. Có 7 người đạt min 3 và 17 người đạt min 2. Genre vẫn thiếu bằng chứng '
               'inequality.'},
 {'number': 15,
  'title': 'Source claims and reproducibility',
  'subtitle': 'Real crawl fields; no fabricated budget, ratings or awards',
  'kind': 'collection',
  'section': 'Source claims and reproducibility',
  'speech': 'The collector contains credit claims, genres, awards, companies, countries, languages, dates and '
            'durations. We exclude fields that were not collected. Seventy-six saved responses provide retrieval '
            'URLs, timestamps and checksums. Label-based genre normalization is an author policy, not a '
            'source-provided OWL taxonomy. Hashes establish byte integrity, not factual truth.',
  'image': 'evidence/screenshots/12_sources_en.png',
  'cards': [['Source-supported relations',
             'P57 / P161 / P58 / P162: credits.\nP136 / P166 / P272: genre, award, company.'],
            ['Normalized values', 'P2047 duration → seconds.\nP577 → earliest Gregorian release-year summary.'],
            ['Traceability',
             '76 responses; retrieval URL / time / SHA-256.\n'
             'Identity links and provenance have different meanings.']],
  'speech_vi': 'Dữ liệu thực tế có người và role, genre, award, company, country, language, năm và thời lượng. '
               'Không bổ sung budget hoặc ratings nếu chưa crawl. 76 phản hồi giữ URL, thời điểm và checksum. '
               'Hash chỉ kiểm tra byte nguyên vẹn, không chứng minh mọi claim đúng ngoài đời. Ánh xạ genre theo '
               'nhãn là chính sách nhóm, cần được đánh giá chất lượng riêng khi mở rộng mẫu.'},
 {'number': 16,
  'title': 'RDF literals and DBpedia units',
  'subtitle': 'runtime is seconds; labels are annotations',
  'kind': 'rdf',
  'section': 'RDF literals and DBpedia units',
  'speech': 'Inception has label Inception, release-year summary 2010 and runtime 8880 seconds. Runtime reuses '
            'DBpedia with xsd:double. The model has five datatype properties; rdfs:label is an annotation '
            'property, not an extra custom title datatype. We preserve the source precision rather than inventing '
            'a full release date.',
  'photo': 'P08',
  'code': 'res:film-Q25188 a dbo:Film ;\n'
          '  rdfs:label "Inception"@en ;\n'
          '  ex:releaseYear 2010 ;\n'
          '  dbo:runtime "8880.0"^^xsd:double ;\n'
          '  dbo:director res:person-Q25191 .',
  'rows': [['dbo:runtime', 'double · seconds'],
           ['ex:releaseYear', 'integer'],
           ['ex:sourceUrl', 'anyURI'],
           ['ex:retrievedAt', 'dateTime'],
           ['ex:sha256', 'string']],
  'speech_vi': 'Inception có label, năm 2010 và runtime 8.880 giây, tương đương 148 phút. Runtime reuse DBpedia '
               'với range double. Model có năm datatype property; rdfs:label là annotation, không phải một custom '
               'title datatype. releaseYear là summary theo chính sách chọn năm từ nguồn, không phải ngày phát '
               'hành đầy đủ. Điều quan trọng khi reuse là giữ đúng nghĩa, kiểu dữ liệu và đơn vị.'},
 {'number': 17,
  'title': 'Linked data: identity and publication',
  'subtitle': 'Canonical identifiers, graph exports and external identity links',
  'kind': 'lod',
  'section': 'Linked data: identity and publication',
  'speech': 'The website distributes the version-3 RDF, schema, full OWL and inference exports. HTTP identifiers '
            'and CC BY-SA support reuse. Identity alignment retains 1699 Wikidata and 28 DBpedia links. Reusing '
            'dbo:Film, identity sameAs and source provenance are three distinct semantic operations.',
  'stars': [['1★', 'Open license', 'CC BY-SA 4.0'],
            ['2★', 'Structured source descriptions', 'Claims, identifiers, values'],
            ['3★', 'Open RDF serializations', 'RDF/XML, Turtle, JSON-LD'],
            ['4★', 'HTTP identifiers and RDF', 'Canonical version 3.0.0'],
            ['5★', 'External identity links', '1,699 Wikidata + 28 DBpedia']],
  'footer': 'Public graphs and local canonical exports are checked for semantic equality.',
  'speech_vi': 'Website cung cấp RDF, schema, full OWL và inference 3.0.0. HTTP IRI và giấy phép hỗ trợ reuse. Có '
               '1.699 link Wikidata và 28 link DBpedia. Reuse dbo:Film, sameAs và provenance có ba ý nghĩa khác '
               'nhau.'},
 {'number': 18,
  'title': 'Inception: RDF resource and OWL',
  'subtitle': 'The web description and final OWL share the same source facts',
  'kind': 'resource',
  'section': 'Inception: RDF resource and OWL',
  'speech': 'The resource page displays the canonical description of Inception: DBpedia properties, its '
            'release-year summary, duration in seconds, identities and provenance. The photo slot requests the '
            'same individual in Protégé. It distinguishes a live resource description from a genuine ontology '
            'screenshot.',
  'photo': 'P09',
  'image': 'evidence/screenshots/09_inception_resource.png',
  'footer': 'Left: current version-3 web description. Right: capture the same individual in Protégé.',
  'speech_vi': 'Trang resource mô tả Inception bằng property DBpedia, năm, thời lượng giây, identity và '
               'provenance. Khung ảnh yêu cầu cùng cá thể trong Protégé. Ảnh web và screenshot ontology là hai '
               'loại minh chứng khác nhau.'},
 {'number': 19,
  'title': 'SPARQL: choose the knowledge scope',
  'subtitle': 'Source facts, OWL inference or before/after named graphs',
  'kind': 'query',
  'section': 'SPARQL: choose the knowledge scope',
  'speech': 'The default Inception query returns 2010, 8880 seconds and Nolan. The knowledge-scope selector '
            'chooses source facts, the precomputed inference graph or the named before/after dataset. The browser '
            'uses Comunica; the local endpoint uses RDFLib. Both modes query the same exports rather than '
            'executing a reasoner for every request.',
  'image': 'evidence/screenshots/05_inception_current.png',
  'code': 'SELECT ?year ?seconds ?director WHERE {\n'
          '  res:film-Q25188 ex:releaseYear ?year ;\n'
          '    dbo:runtime ?seconds ; dbo:director ?person .\n'
          '  ?person rdfs:label ?director .\n'
          '}',
  'footer': 'The sample chooses its required scope automatically; change scope to compare before and after.',
  'speech_vi': 'Query Inception trả 2010, 8.880 giây và Nolan. Chọn scope dữ liệu nguồn, graph inference đã tính '
               'hoặc named graph trước/sau. Browser dùng Comunica; endpoint dùng RDFLib. Cả hai truy vấn chung '
               'exports, không chạy HermiT lại mỗi lần.'},
 {'number': 20,
  'title': 'Credit records and competency questions',
  'subtitle': '27 design queries; counts use local identities',
  'kind': 'roles',
  'section': 'Credit records and competency questions',
  'speech': 'Inception has 25 credit records: 21 acting, one directing, one writing and two producing. The '
            'current application image shows Nolan’s three roles, not all 25 records. The new competency suite '
            'contains 27 queries and tests before/after reasoning, including WriterDirector and property-chain '
            'results.',
  'image': 'evidence/screenshots/06_nolan_roles.png',
  'cards': [['25 Inception credits', '21 acting + 1 directing + 1 writing + 2 producing.'],
            ['8 / 4 / 7', 'Nolan films / Inception companies / Godfather awards.'],
            ['27 design queries', 'Direct facts / hierarchy / inferred knowledge.']],
  'speech_vi': 'Inception có 25 credit: 21 acting, một directing, một writing và hai producing. Ảnh truy vấn '
               'Nolan thể hiện ba vai trò của một người. Web có 27 mẫu query và chọn scope đúng theo mẫu. Khi '
               'đếm, giới hạn IRI local để loại alias; phân biệt record, người và cặp người–phim.'},
 {'number': 21,
  'title': 'Before / after: Nolan and WriterDirector',
  'subtitle': 'The same result is available in web, local endpoint and terminal',
  'kind': 'endpoint',
  'section': 'Before / after: Nolan and WriterDirector',
  'speech': 'WriterDirector has zero asserted members and ten inferred local members. The scope selector lets '
            'readers compare the same query before and after reasoning. Query 27 uses explicit named graphs. The '
            'terminal supports --mode asserted, reasoned or dataset; no distinct-term count is used to classify '
            'the cardinality subsets.',
  'photo': 'P10',
  'code': '.venv/bin/python src/query.py queries/20.rq\n'
          '.venv/bin/python src/query.py queries/20.rq --reasoned\n'
          '.venv/bin/python src/query.py queries/27.rq --mode dataset',
  'rows': [['Asserted', 'WriterDirector 0; Nolan min 3: false'],
           ['Reasoned', 'WriterDirector 10; Nolan min 3: true']],
  'speech_vi': 'WriterDirector có zero assertion và 10 người sau inference. Chọn scope để so sánh cùng query '
               'trước/sau. Query 27 dùng named graph; terminal có --mode asserted, reasoned, dataset. Cardinality '
               'do HermiT suy ra, không gán bằng đếm IRI.'},
 {'number': 22,
  'title': 'Verification of the final OWL',
  'subtitle': 'Direct HermiT run; evidence bound to the file hash',
  'kind': 'validation',
  'section': 'Verification of the final OWL',
  'speech': 'HermiT checked the canonical RDF/XML OWL: consistent, no unsatisfiable named classes. All 27 '
            'competency questions execute against explicit graph scopes; 965 chain pairs are materialized '
            'separately. Sixteen tests verify the model and endpoint. Browser checks exercise SELECT, ASK, '
            'CONSTRUCT, DESCRIBE and recovery from malformed queries.',
  'image': 'docs/sync_images/verification.png',
  'checks': [['PASS', 'HermiT consistency'],
             ['0', 'unsatisfiable named classes'],
             ['27', 'design queries executed'],
             ['965', 'chain pairs verified']],
  'speech_vi': 'HermiT kiểm tra đúng full OWL: consistent, không có named class bất khả thỏa. 27 competency '
               'queries chạy theo scope rõ ràng; 965 chain pairs được materialize riêng. 16 tests kiểm tra model '
               'và endpoint. Browser kiểm tra SELECT, ASK, CONSTRUCT, DESCRIBE và phục hồi sau query sai cú '
               'pháp.'},
 {'number': 23,
  'title': 'Coverage and limitations',
  'subtitle': 'Verified functional requirements; evidence scope remains explicit',
  'kind': 'score_limits',
  'section': 'Coverage and limitations',
  'speech': 'The ontology, dataset, query interfaces and document exports share version 3.0.0. Consistency, '
            'source integrity and before/after query behavior are checked independently. Selection bias, label '
            'mappings and unannotated identity matching still limit generalization. MP4 files are excluded as '
            'requested; an official assignment grade is not inferred from technical checks.',
  'rows': [['R1', 'Canonical OWL + HermiT', 'Verified'],
           ['R2', 'Source facts + provenance', 'Verified'],
           ['R3', 'Public RDF / OWL', 'Aligned'],
           ['R4', 'Retained identity links', 'Verified'],
           ['R5', 'Three query scopes', 'Verified']],
  'cards': [['Inference scope', 'Consistency does not prove completeness or factual accuracy.'],
            ['Source and identity', 'No blanket inequality for QIDs; genre buckets are author mappings.'],
            ['Deliverables', 'Slides, report and guides are current. No MP4 files are included.']],
  'speech_vi': 'Ontology, data, các giao diện query và tài liệu cùng 3.0.0. Consistency, toàn vẹn nguồn và '
               'before/after được kiểm tra riêng. Mẫu có chủ đích, label mapping và matching chưa có ground truth '
               'vẫn là giới hạn. MP4 đã loại theo yêu cầu; kiểm tra kỹ thuật không phải điểm chính thức.'},
 {'number': 24,
  'title': 'Evidence capture and submission checklist',
  'subtitle': 'Report: 15 pages · main deck: 24 slides · no MP4 included',
  'kind': 'closing',
  'section': 'Evidence capture and submission checklist',
  'speech': 'The remaining slots request genuine Protégé screenshots of the final ontology. The Vietnamese '
            'speaker script matches the English deck. The report keeps its fifteen-page academic format. Current '
            'web captures and reasoner logs support the presentation; MP4 files have been removed without editing '
            'or generating video content.',
  'footer': 'Use the canonical OWL for Protégé evidence; source facts and inferred knowledge have separate '
            'scopes.',
  'speech_vi': 'Các ô còn lại yêu cầu screenshot Protégé thật. Script Việt khớp slide Anh; báo cáo học thuật giữ '
               '15 trang. Ảnh web hiện tại và log reasoner hỗ trợ trình bày. MP4 đã xóa, không chỉnh nội dung '
               'hoặc dựng lại video.'}]
PROTEGE_SHOTS = {'P00': {'file': 'P00_ontology_header.png',
         'title': 'IRI và phiên bản 3.0.0',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Mở ontology/Movie_Knowledge_Graph.owl.',
                   'Chọn Active Ontology / Ontology Header.',
                   'Giữ IRI và versionInfo 3.0.0 trong ảnh.'],
         'expect': '37 lớp có tên; không đếm biểu thức anonymous như lớp có tên.',
         'title_en': 'Ontology 3.0.0 header'},
 'P01': {'file': 'P01_film_hierarchy.png',
         'title': 'Cây Work / Film',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Mở Classes → dbo:Work → dbo:Film.',
                   'Hiện ActionFilm, AwardWinningFilm và các lớp giao.',
                   'Giữ IRI DBpedia của Film trong Description.'],
         'expect': 'Không có FeatureFilm/AnimatedFilm/DocumentaryFilm trong module cuối.',
         'title_en': 'Work and Film hierarchy'},
 'P02': {'file': 'P02_agent_hierarchy.png',
         'title': 'Cây chủ thể DBpedia',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Mở dbo:Agent → dbo:Person và dbo:Organisation.',
                   'Hiện Artist → Actor; Organisation → Company.',
                   'Mở MovieDirector / Writer → ScreenWriter.'],
         'expect': 'Reuse lớp DBpedia; không tạo ex:Actor hoặc ex:Organization.',
         'title_en': 'DBpedia agent hierarchy'},
 'P03': {'file': 'P03_genre_award_hierarchy.png',
         'title': 'MovieGenre và Award',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Mở dbo:Genre → dbo:MovieGenre.',
                   'Hiện ActionGenre / DramaGenre; chọn dbo:Award.',
                   'Giữ Description để đọc IRI và lớp cha.'],
         'expect': 'Không có FictionGenre hoặc các nhóm award suy đoán theo nhãn.',
         'title_en': 'MovieGenre and Award'},
 'P04': {'file': 'P04_contribution_restrictions.png',
         'title': 'Ràng buộc Contribution',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn ex:Contribution.',
                   'Hiện exactly 1 cho contributionBy, contributionTo, hasRole.',
                   'Chọn hasRole để thấy Functional và role individual.'],
         'expect': 'Ba endpoint đúng 1; dữ liệu thiếu cần structural validation riêng.',
         'title_en': 'Contribution restrictions'},
 'P05': {'file': 'P05_object_property.png',
         'title': 'Domain / range / inverse',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn contributionBy: Contribution → dbo:Person.',
                   'Hiện Functional và inverse hasContribution.',
                   'Có thể chụp contributedTo với property chain.'],
         'expect': 'Chain hasContribution rồi contributionTo; không đặt cardinality trên contributedTo.',
         'title_en': 'Inverse and functional properties'},
 'P06': {'file': 'P06_filmmaker_equivalent_class.png',
         'title': 'Định nghĩa Filmmaker',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn ex:Filmmaker.',
                   'Hiện Equivalent To với Person AND các nhánh SOME.',
                   'Đọc các nhánh Directing / Writing / ProducingContribution.'],
         'expect': 'Công thức không tự chứng minh reasoner đã chạy.',
         'title_en': 'Filmmaker equivalent class'},
 'P07': {'file': 'P07_three_credit_cardinality.png',
         'title': 'Cardinality trên Contribution',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn ex:ThreeCreditContributor; hiện min 3 hasContribution Contribution.',
                   'Chạy HermiT; chọn Nolan ở inferred view.',
                   'Chụp thêm Functional hasRole và AllDifferent của bốn role.'],
         'expect': '7 người đạt min 3; 17 người đạt min 2; không phải COUNT DISTINCT.',
         'title_en': 'Three-credit cardinality'},
 'P08': {'file': 'P08_runtime_datatype.png',
         'title': 'Thời lượng theo DBpedia',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn dbo:runtime trong Data properties.',
                   'Hiện domain dbo:Work và range xsd:double.',
                   'Chọn Inception: runtime = 8880 giây.'],
         'expect': '8880 giây = 148 phút; rdfs:label là annotation property.',
         'title_en': 'DBpedia runtime in seconds'},
 'P09': {'file': 'P09_inception_individual.png',
         'title': 'Cá thể Inception bản mới',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Mở Movie_Knowledge_Graph.owl 3.0.0.',
                   'Chọn film-Q25188; hiện label, releaseYear 2010, runtime 8880.',
                   'Hiện dbo:director, genre, productionCompany và award.'],
         'expect': 'Cá thể trong OWL khớp trang resource 3.0.0; runtime là 8880 giây.',
         'title_en': 'Inception in the final OWL'},
 'P10': {'file': 'P10_nolan_inferred_types.png',
         'title': 'Các type suy luận của Nolan',
         'owl': 'Movie_Knowledge_Graph.owl',
         'steps': ['Chọn HermiT → Start reasoner, chờ hoàn tất.',
                   'Chọn person-Q25191; mở inferred types.',
                   'Giữ WriterDirector, Filmmaker, ThreeCreditContributor trong ảnh.'],
         'expect': 'Type mới không được gán trực tiếp trong asserted graph; giữ trạng thái reasoner.',
         'title_en': 'Nolan inferred types'}}
