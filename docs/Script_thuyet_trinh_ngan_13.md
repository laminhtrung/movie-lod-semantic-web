# MovieLOD — Script cho 13 slide tóm tắt

Bản 3.0.0; chữ slide/notes tiếng Anh, script này tiếng Việt. Bộ chính vẫn 24 slide; bản ngắn chọn nội dung cốt lõi. MP4 đã được loại; dùng demo ứng dụng trực tiếp.

## Slide 1 — MovieLOD

Tương ứng slide 1 của bộ chính.

Nhóm trình bày MovieLOD, một knowledge graph về điện ảnh. File OWL cuối hiện là bản 3.0.0, có 30 phim, 37 lớp có tên và 1.727 liên kết danh tính. Ví dụ xuyên suốt là Inception và Christopher Nolan. Chúng ta cần phân biệt ontology mới đã chạy HermiT với ứng dụng web vẫn dùng snapshot trước đó. Vì vậy, mỗi kết quả trong bài sẽ được gắn với đúng phiên bản và phạm vi kiểm tra.

## Slide 2 — Objectives and synchronized evidence

Tương ứng slide 2 của bộ chính.

Năm yêu cầu cốt lõi đã dùng chung ontology 3.0.0. Graph nguồn, graph suy luận và dataset trước/sau có trên web, endpoint và terminal. Slide, báo cáo và kết quả truy vấn khớp cùng model. MP4 đã xóa theo yêu cầu, không dựng lại video.

## Slide 3 — Architecture and knowledge layers

Tương ứng slide 3 của bộ chính.

Collect cung cấp corpus đã crawl; build xuất model 3.0.0. HermiT phân loại OWL canonical; OWL RL bổ sung inverse, subproperty và chain. Validate chạy 27 câu hỏi. Web, endpoint và terminal dùng chung graph nguồn, graph suy luận và dataset so sánh.

## Slide 4 — Dataset: units and counting scope

Tương ứng slide 4 của bộ chính.

Mẫu có 30 phim, 851 người, 1.010 credit record, 45 công ty và 672 thực thể giải thưởng. OWL đầy đủ chứa 19.025 triple, gồm schema và facts khai báo, chưa phải toàn bộ closure suy luận. Cần đọc đúng đơn vị: credit không phải số người, award entity không phải số lần trao giải. Các thống kê membership chỉ đếm IRI local để tránh tăng số do alias sameAs.

## Slide 5 — Ontology inventory: reuse before extension

Tương ứng slide 5 của bộ chính.

37 lớp gồm 17 lớp DBpedia, một lớp VoID Dataset và 19 lớp riêng. Các lớp riêng mô tả credit, nguồn, hai bucket thể loại và những subset suy luận có nghĩa rõ. Mười lớp domain có membership suy ra; bốn subclass credit hỗ trợ các chain. Nhóm không tạo lại Actor, Genre, Award hoặc Company dưới namespace riêng chỉ để tăng số lượng lớp.

## Slide 6 — Contribution: person, film and role

Tương ứng slide 9 của bộ chính.

Contribution là record nối một người, một phim và một role. Ba endpoint có tính functional và qualified exactly-one restrictions. Nolan có ba credit riêng trên Inception cho directing, writing và producing. Role là individual của vocabulary kiểm soát, không phải Person. Các subclass credit được suy ra từ hasRole value. Exactly one không tự báo dữ liệu thiếu dưới giả định thế giới mở; cần structural validation riêng.

## Slide 7 — Properties: reuse, inverse and chain

Tương ứng slide 10 của bộ chính.

Các quan hệ phim phổ biến dùng DBpedia. Inverse của contributionBy cho đường đi hasContribution từ người đến credit. Chain hasContribution rồi contributionTo suy ra contributedTo từ người đến phim. Directed và actedIn là quan hệ cụ thể hơn. Property chain làm contributedTo trở thành non-simple, nên cardinality đặt trên hasContribution, không đặt trên contributedTo. Kết quả có 965 cặp người–phim local.

## Slide 8 — Verified domain classes after HermiT

Tương ứng slide 12 của bộ chính.

Bảng liệt kê mười subset domain có membership HermiT thật. Trong đó có bảy lớp bổ sung ngoài Filmmaker, ActionFilm và AwardWinningFilm. Actor dùng range chuẩn của DBpedia, còn bốn loại Contribution là bước trung gian. Tất cả type subset ở bảng đều có zero assertion trong đầu vào. Nhóm không dùng COUNT DISTINCT để gán các class này rồi gọi đó là entailment OWL DL.

## Slide 9 — Nolan: facts → credit type → Filmmaker

Tương ứng slide 13 của bộ chính.

Credit của Nolan có DirectorRole nên thỏa DirectingContribution. Inverse tạo hasContribution; điều kiện SOME và OR của Filmmaker nhận diện Nolan. Credit writing tạo ScreenWriter, directing tạo MovieDirector, rồi giao hai nghề tạo WriterDirector. Các type này không được gán thủ công. Đây là chain giải thích nhiều bước dựa trên cùng facts; OWL không bắt reasoner chạy theo đúng thứ tự trình bày trên sơ đồ.

## Slide 10 — Genuine minimum-cardinality reasoning

Tương ứng slide 14 của bộ chính.

Ba credit của Nolan có DirectorRole, WriterRole và ProducerRole khác nhau. hasRole là functional; các role được khai báo AllDifferent theo nghĩa của vocabulary kiểm soát. Nếu hai credit đồng nhất, một record phải có hai role khác nhau và gây mâu thuẫn. Vì vậy HermiT chứng minh ít nhất ba credit khác nhau. Có 7 người đạt min 3 và 17 người đạt min 2. Genre vẫn thiếu bằng chứng inequality.

## Slide 11 — Linked data: identity and publication

Tương ứng slide 17 của bộ chính.

Website cung cấp RDF, schema, full OWL và inference 3.0.0. HTTP IRI và giấy phép hỗ trợ reuse. Có 1.699 link Wikidata và 28 link DBpedia. Reuse dbo:Film, sameAs và provenance có ba ý nghĩa khác nhau.

## Slide 12 — Verification of the final OWL

Tương ứng slide 22 của bộ chính.

HermiT kiểm tra đúng full OWL: consistent, không có named class bất khả thỏa. 27 competency queries chạy theo scope rõ ràng; 965 chain pairs được materialize riêng. 16 tests kiểm tra model và endpoint. Browser kiểm tra SELECT, ASK, CONSTRUCT, DESCRIBE và phục hồi sau query sai cú pháp.

## Slide 13 — Evidence capture and submission checklist

Tương ứng slide 24 của bộ chính.

Các ô còn lại yêu cầu screenshot Protégé thật. Script Việt khớp slide Anh; báo cáo học thuật giữ 15 trang. Ảnh web hiện tại và log reasoner hỗ trợ trình bày. MP4 đã xóa, không chỉnh nội dung hoặc dựng lại video.

