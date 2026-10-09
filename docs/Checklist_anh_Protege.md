---
title: "MovieLOD: checklist ảnh minh chứng Protégé"
date: "11 vị trí trong bộ 24 slide · 09/10/2026"
---

## Cách chèn

Có 11 khung ảnh ghi rõ mã, tên file và thao tác ngay trên slide. Lần tạo này không có ảnh Protégé thật: chưa có ảnh giao diện đã xác minh cho ontology mới; không dùng ảnh dựng làm screenshot. Ảnh ứng dụng Web trong slide là ảnh chụp thực.

Cách 1: chèn ảnh vào PowerPoint và che/xóa khung chờ cùng phần hướng dẫn của khung đó. Cách 2: lưu đúng tên ở `evidence/protege/` (PNG/JPG/JPEG cùng stem), chạy `.venv/bin/python src/make_slides.py --slides-only`; khung chờ tự thay bằng ảnh. Speaker Notes giữ quy trình chụp.

Chụp đúng cửa sổ/view, chữ đủ lớn (gợi ý 1440×900 trở lên); không lấy cả desktop có ứng dụng khác. Giữ tên ontology và IRI/thông tin cần chứng minh. Ảnh cây khai báo không được ghi nhãn inferred.

## Danh sách ảnh

### P00 — Slide 05: IRI và phiên bản 3.0.0

**Tên file:** `P00_ontology_header.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở ontology/Movie_Knowledge_Graph.owl.
2. Chọn Active Ontology / Ontology Header.
3. Giữ IRI và versionInfo 3.0.0 trong ảnh.

**Mục cần thấy:** 37 lớp có tên; không đếm biểu thức anonymous như lớp có tên.

### P01 — Slide 06: Cây Work / Film

**Tên file:** `P01_film_hierarchy.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Classes → dbo:Work → dbo:Film.
2. Hiện ActionFilm, AwardWinningFilm và các lớp giao.
3. Giữ IRI DBpedia của Film trong Description.

**Mục cần thấy:** Không có FeatureFilm/AnimatedFilm/DocumentaryFilm trong module cuối.

### P02 — Slide 07: Cây chủ thể DBpedia

**Tên file:** `P02_agent_hierarchy.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở dbo:Agent → dbo:Person và dbo:Organisation.
2. Hiện Artist → Actor; Organisation → Company.
3. Mở MovieDirector / Writer → ScreenWriter.

**Mục cần thấy:** Reuse lớp DBpedia; không tạo ex:Actor hoặc ex:Organization.

### P03 — Slide 08: MovieGenre và Award

**Tên file:** `P03_genre_award_hierarchy.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở dbo:Genre → dbo:MovieGenre.
2. Hiện ActionGenre / DramaGenre; chọn dbo:Award.
3. Giữ Description để đọc IRI và lớp cha.

**Mục cần thấy:** Không có FictionGenre hoặc các nhóm award suy đoán theo nhãn.

### P04 — Slide 09: Ràng buộc Contribution

**Tên file:** `P04_contribution_restrictions.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:Contribution.
2. Hiện exactly 1 cho contributionBy, contributionTo, hasRole.
3. Chọn hasRole để thấy Functional và role individual.

**Mục cần thấy:** Ba endpoint đúng 1; dữ liệu thiếu cần structural validation riêng.

### P05 — Slide 10: Domain / range / inverse

**Tên file:** `P05_object_property.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn contributionBy: Contribution → dbo:Person.
2. Hiện Functional và inverse hasContribution.
3. Có thể chụp contributedTo với property chain.

**Mục cần thấy:** Chain hasContribution rồi contributionTo; không đặt cardinality trên contributedTo.

### P06 — Slide 13: Định nghĩa Filmmaker

**Tên file:** `P06_filmmaker_equivalent_class.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:Filmmaker.
2. Hiện Equivalent To với Person AND các nhánh SOME.
3. Đọc các nhánh Directing / Writing / ProducingContribution.

**Mục cần thấy:** Công thức không tự chứng minh reasoner đã chạy.

### P07 — Slide 14: Cardinality trên Contribution

**Tên file:** `P07_three_credit_cardinality.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn ex:ThreeCreditContributor; hiện min 3 hasContribution Contribution.
2. Chạy HermiT; chọn Nolan ở inferred view.
3. Chụp thêm Functional hasRole và AllDifferent của bốn role.

**Mục cần thấy:** 7 người đạt min 3; 17 người đạt min 2; không phải COUNT DISTINCT.

### P08 — Slide 16: Thời lượng theo DBpedia

**Tên file:** `P08_runtime_datatype.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn dbo:runtime trong Data properties.
2. Hiện domain dbo:Work và range xsd:double.
3. Chọn Inception: runtime = 8880 giây.

**Mục cần thấy:** 8880 giây = 148 phút; rdfs:label là annotation property.

### P09 — Slide 18: Cá thể Inception bản mới

**Tên file:** `P09_inception_individual.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Mở Movie_Knowledge_Graph.owl 3.0.0.
2. Chọn film-Q25188; hiện label, releaseYear 2010, runtime 8880.
3. Hiện dbo:director, genre, productionCompany và award.

**Mục cần thấy:** Cá thể trong OWL khớp trang resource 3.0.0; runtime là 8880 giây.

### P10 — Slide 21: Các type suy luận của Nolan

**Tên file:** `P10_nolan_inferred_types.png`. **Mở:** `ontology/Movie_Knowledge_Graph.owl`.

1. Chọn HermiT → Start reasoner, chờ hoàn tất.
2. Chọn person-Q25191; mở inferred types.
3. Giữ WriterDirector, Filmmaker, ThreeCreditContributor trong ảnh.

**Mục cần thấy:** Type mới không được gán trực tiếp trong asserted graph; giữ trạng thái reasoner.

## Kiểm tra trước khi dùng làm minh chứng

- Đúng ontology 3.0.0 của bài; không dùng ảnh 2.0 làm minh chứng mô hình mới.
- Ảnh cá thể dùng Knowledge Graph; ảnh mô hình dùng schema OWL.
- IRI lớp DBpedia, cardinality và datatype đọc được.
- Không nói HermiT/Pellet đã chứng minh DL nếu chỉ chụp công thức hoặc chọn menu.
- Nếu chạy reasoner, giữ tên và trạng thái; ghi cả lỗi nếu có.

Nguồn hướng dẫn giao diện: [Protégé Views](https://protegeproject.github.io/protege/views/). Ngữ nghĩa cần nhớ: [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/). Nội dung lớp/thuộc tính/cá thể lấy từ OWL của bài.