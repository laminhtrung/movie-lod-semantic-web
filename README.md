# MovieLOD — Movie ontology and linked data 3.0.0

Ontology, dữ liệu, các giao diện truy vấn và tài liệu cùng sử dụng model **3.0.0**. MP4 đã được xoá theo yêu cầu; không ghi hoặc chỉnh sửa video. Website: https://laminhtrung.github.io/movie-lod-semantic-web/.

File đầy đủ để mở trong Protégé: [Movie_Knowledge_Graph.owl](ontology/Movie_Knowledge_Graph.owl). File [Movie_Ontology.owl](ontology/Movie_Ontology.owl) chỉ chứa schema. HermiT chạy trực tiếp trên full OWL: consistent, không có named class bất khả thỏa. Hash file và kết quả tại [final_owl_checks.json](evidence/ontology_design/final_owl_checks.json).

## Tài liệu

| Sản phẩm | Nội dung |
|---|---|
| [Slide PPTX](docs/Slide.pptx) / [PDF](docs/Slide.pdf) | 24 trang tiếng Anh; 11 khung chờ ảnh Protégé có hướng dẫn tiếng Việt |
| [Script thuyết trình](docs/Script_thuyet_trinh.pdf) | Lời tiếng Việt khớp từng slide |
| [Bộ ngắn 13 trang](docs/Slide_ngan_13.pptx) / [PDF](docs/Slide_ngan_13.pdf) | Tóm tắt cùng model; [script riêng](docs/Script_thuyet_trinh_ngan_13.pdf) |
| [Báo cáo PDF](docs/Bao_cao.pdf) / [Word](docs/Bao_cao.docx) | Tiếng Anh, 15 trang; Times New Roman 13, giãn dòng 1,5; logo HUST, bìa nhóm và mục lục riêng |
| [Hướng dẫn đọc hiểu](docs/Huong_dan_doc_hieu_project.pdf) / [Word](docs/Huong_dan_doc_hieu_project.docx) | Tiếng Việt; RDF/OWL/SPARQL, sơ đồ, ví dụ và câu hỏi ôn tập |
| [A–Z](docs/Huong_dan_A_Z.pdf) / [thao tác](docs/Huong_dan_thao_tac_chi_tiet.pdf) | Tái lập, ba query scopes và Protégé |
| [Mô tả ontology](docs/Mo_ta_ontology.pdf) / [thiết kế chi tiết](docs/DBpedia_OWL_Design.html) | Class/property inventory, Manchester expressions, căn cứ nguồn và 27 queries |
| [Kết quả reasoner](docs/Ket_qua_reasoner.pdf) | Kết quả trên đúng full OWL và giới hạn diễn giải |
| [Checklist ảnh](docs/Checklist_anh_Protege.pdf) | Vị trí ảnh Protégé cần bổ sung; không phải ảnh đã chụp |
| [Demo trực tiếp](docs/Kich_ban_video.pdf) | Kịch bản thao tác; giữ tên file để tương thích liên kết, không chứa video |
| [Đối chiếu yêu cầu](CHAM_DIEM.pdf) | Minh chứng kỹ thuật và các giới hạn; không phải điểm chính thức |
| Gói bàn giao ZIP | Tạo ngoài repo bằng `src/sync_document_assets.py`; không commit ZIP vào Git |

`docs/Slide_full.pptx.pdf` là PDF nguồn nhóm cung cấp, được giữ để truy nguyên ảnh. Deck hiện tại là Slide.pptx/pdf. Sơ đồ tác giả và bảng log không được gọi là screenshot Protégé. Báo cáo giữ trọng tâm học thuật.

## Số liệu và suy luận

- Full OWL: **19.025 triple**, 37 named classes (17 DBpedia + 1 VoID + 19 lớp riêng), 19 object và 5 datatype property.
- Facts: 18.595 triple; schema: 442 triple; 12 triple nhãn role có trong cả hai nên tổng là 19.025.
- 30 phim, 851 người, 1.010 credit, 45 công ty, 75 genre, 672 award entity; 76 phản hồi nguồn có SHA-256.
- 1.727 sameAs: 1.699 Wikidata và 28 DBpedia; lọc IRI local khi đếm cá thể.
- HermiT: dbo:Actor 769, Filmmaker 89, WriterDirector 10, MultiCreditContributor 17, ThreeCreditContributor 7.
- 965 cặp contributedTo được materialize bằng OWL RL; cardinality do HermiT suy ra, không gán bằng COUNT DISTINCT.

Inception: 2010, dbo:runtime **8.880 giây** (=148 phút), Nolan; 25 credit. Nolan đạo diễn 8 phim trong mẫu. ActionGenre/DramaGenre là bucket nhãn tác giả. Không thêm AllDifferent cho mọi QID; negative MultiGenreFilm có 0 DL members.

## Chạy và tái lập

```bash
make setup
# Cần Java 17; JAVA phải là executable Java thật.
make all JAVA=/path/to/java
.venv/bin/python src/server.py --port 8000
```

`make all` chạy collect → build 3.0.0 → HermiT/OWL RL → validate → pytest. Nếu chỉ tái lập từ corpus đang có, dùng `make build`, `make reason JAVA=/path/to/java`, `make validate`, `make test`. Collect có thể cần mạng; không cần thu thập lại để đọc bộ đã bàn giao. Restart server sau khi thay graph.

```bash
.venv/bin/python src/query.py queries/02.rq
.venv/bin/python src/query.py queries/20.rq --mode asserted
.venv/bin/python src/query.py queries/20.rq --reasoned
.venv/bin/python src/query.py queries/27.rq --mode dataset
```

WriterDirector: 0 trước, 10 sau. Query 01–08 dùng source facts; 09–26 dùng inference; 27 dùng Dataset/TriG. Web tự chọn scope theo mẫu, đổi scope rồi bấm Run để so sánh. Endpoint Flask cục bộ `/sparql?mode=asserted|reasoned|dataset` đọc cùng exports. GitHub Pages phục vụ web tĩnh; truy vấn công khai chạy trong trình duyệt bằng Comunica, không có backend Flask công khai. Browser Comunica tải các graph đã tính; không chạy reasoner cho từng request.

```bash
.venv/bin/python src/make_slides_video.py --slides-only
.venv/bin/python src/make_short_slides.py
.venv/bin/python src/make_report.py
.venv/bin/python src/make_docs.py
.venv/bin/python src/sync_document_assets.py
```

Các trình tạo tài liệu không cần video. Evidence hiện tại gồm 15 tests, 27 competency queries, browser/query checks và đối chiếu public RDF. Consistency không chứng minh factual accuracy hay completeness; source matching chưa có annotated ground truth. Lịch sử Git không được viết lại khi xoá MP4.

## Repo và gói bàn giao

Source, corpus đang dùng, tài liệu cuối và evidence hiện tại nằm trong repo. Gói ZIP và archive deploy được tạo ở `../movie_lod_github_deliverables/`; ảnh preview, cache và log build là file sinh tự động. Mỗi query chỉ có một bản ở `queries/`. Nguồn thiết kế duy nhất là `docs/DBpedia_OWL_Design.md`.

## GitHub Pages

Repo mới: https://github.com/laminhtrung/movie-lod-semantic-web
Website: https://laminhtrung.github.io/movie-lod-semantic-web/

GitHub Actions deploy thư mục `web/dist` khi có thay đổi trên nhánh `main`. Settings → Pages → Source chọn **GitHub Actions**. Không dùng thư mục `docs` làm nguồn website. Không có submodule: toàn bộ frontend nằm trong repo này. `.nojekyll` giữ nguyên các file RDF và tài nguyên tĩnh.

URL canonical và các IRI đều chứa `/movie-lod-semantic-web`. Khi chạy local, có thể mở `http://127.0.0.1:8000/movie-lod-semantic-web/`; Flask cũng hỗ trợ đường dẫn gốc để thuận tiện kiểm thử. Các link tĩnh giữ đúng prefix như trên Pages.

Sau đổi ontology hoặc dữ liệu: chạy build → reason → validate → tests; sau sửa tài liệu: chạy các trình tạo tương ứng và `src/sync_document_assets.py`, rồi commit/push thư mục `web/dist`. GitHub Actions sẽ xuất bản bản mới. Không chứa hoặc tạo video demo.
