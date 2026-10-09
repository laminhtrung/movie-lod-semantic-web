# MovieLOD — Hướng dẫn bắt đầu với repo hiện tại

> **Phiên bản:** Ontology, dữ liệu, web và truy vấn dùng chung 3.0.0. MP4 đã được xoá theo yêu cầu; tài liệu demo dùng cho trình diễn trực tiếp.

## Đọc đúng tài liệu

Bắt đầu bằng [hướng dẫn đọc hiểu 25 trang](Huong_dan_doc_hieu_project.pdf). Slide chính là Slide.pptx/pdf, 24 trang tiếng Anh; script tập nói bằng tiếng Việt. Báo cáo tiếng Anh đúng 15 trang. Ô chờ ảnh Protégé giữ tiếng Việt, yêu cầu ảnh mới của OWL 3.0.0.

## Chạy ontology mới

1. Mở ontology/Movie_Knowledge_Graph.owl trong Protégé. Đây là schema + facts đầy đủ.
2. Kiểm tra versionInfo 3.0.0. File Movie_Ontology.owl chỉ chứa schema.
3. Chọn HermiT → Start reasoner, đợi hoàn tất.
4. Tìm Nolan/person-Q25191. Kiểm tra Filmmaker, WriterDirector và ThreeCreditContributor ở inferred view.

HermiT xác nhận consistent và không có named class bất khả thỏa. Kết quả nằm ở evidence/ontology_design/final_owl_checks.json, gắn với hash file OWL.

## Truy vấn graph mới

```bash
.venv/bin/python src/query.py queries/20.rq --mode asserted
.venv/bin/python src/query.py queries/20.rq --mode reasoned
.venv/bin/python src/query.py queries/27.rq --mode dataset
```

Hai lệnh đầu trả lần lượt 0 và 10 người WriterDirector. Lệnh cuối so sánh type chỉ xuất hiện sau inference bằng hai named graph. SELECT/ASK trả JSON; graph query trả Turtle.

## Chạy ứng dụng hiện có

```bash
.venv/bin/python src/server.py --port 8000
```

Mở http://127.0.0.1:8000. Nếu cổng bận, chọn cổng khác và đổi URL tương ứng. Endpoint đọc exports 3.0.0: source facts, reasoned graph và named before/after dataset. Mẫu query tự chọn scope; đổi scope rồi bấm Run. Không chạy HermiT cho từng request.

## Số liệu cần nhớ

OWL cuối: 37 lớp có tên, 19 object và 5 datatype property; 19.025 triple bao gồm schema và facts. Có 30 phim, 851 người, 1.010 credit, 45 công ty, 75 genre và 672 award entity. Inception: 2010, 8.880 giây (=148 phút); Nolan đạo diễn 8 phim trong mẫu.

Actor 769; Filmmaker 89; WriterDirector 10; MultiCreditContributor 17; ThreeCreditContributor 7. Bốn role individual ở namespace ex:, không được bỏ qua chỉ vì thống kê local res: hiển thị 0 role.

## Tái lập dữ liệu và tài liệu

Trình tạo slide: src/make_slides.py --slides-only. Báo cáo: src/make_report.py. Hướng dẫn đọc hiểu: src/make_reading_guide.py. Các trình tạo này không cần ghi lại MP4.

`make build` xuất model 3.0.0 từ corpus; `make reason JAVA=/path/to/java` chạy HermiT trực tiếp trên canonical OWL và materialize OWL RL; `make validate` kiểm tra nguồn và 27 queries; `make test` chạy pytest. `make all` thực hiện cả collect trước pipeline này. Java 17 và requirements_reasoner.txt cần có để chạy HermiT.

MP4 đã xoá theo yêu cầu, không có video trong bộ bàn giao. File Slide_full.pptx.pdf là nguồn ảnh do nhóm cung cấp; Slide.pptx/pdf là deck mới nhất.


## Hosting GitHub Pages

Website: https://laminhtrung.github.io/movie-lod-semantic-web/
Repo độc lập: https://github.com/laminhtrung/movie-lod-semantic-web

Bản công khai dùng Comunica để truy vấn ngay trong trình duyệt. GitHub Pages không chạy Flask và không cung cấp API `/sparql` của Python. Endpoint và content negotiation 303 chỉ được kiểm tra trên server cục bộ; Pages cung cấp trang resource và các liên kết tải RDF tĩnh. Chọn source facts / inference / before-after theo câu hỏi. IRI dùng URL GitHub Pages canonical; không bỏ prefix tên repo khi chép đường dẫn. Push `main` kích hoạt workflow Pages. Không có video demo.
