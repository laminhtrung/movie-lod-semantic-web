# MovieLOD — Kịch bản demo trực tiếp 3.0.0

MP4 đã được xoá theo yêu cầu. Tài liệu dùng cho trình diễn trực tiếp; không tạo video.

## Chuẩn bị

Mở full OWL `ontology/Movie_Knowledge_Graph.owl` trong Protégé. Start HermiT trước buổi demo. Chạy `.venv/bin/python src/server.py --port 8000` hoặc mở website public. Mở snapshots.json, movies.ttl, final_owl_checks.json và query_results.json trong editor. Tăng font để người xem đọc được. Không gọi schematic là screenshot Protégé.

## Luồng demo khoảng 5 phút

| Thời gian | Thao tác | Minh chứng / lời giải thích |
|---|---|---|
| 0:00–0:25 | Trang chủ, statistics và query Inception | 30 phim, 37 lớp; 2010 / 8880 giây / Nolan. RDF lưu giây, UI có thể hiển thị phút. |
| 0:25–1:15 | Protégé: dbo:Film, Contribution, hasRole | Reuse DBpedia; credit có đúng một người, phim và role; role controlled và khác nhau. |
| 1:15–1:45 | snapshots.json và phản hồi gốc | 76 phản hồi có URL/time/hash; SHA kiểm tra byte, không chứng minh mọi claim đúng. |
| 1:45–2:20 | Trang resource Inception, tải Turtle/JSON-LD/OWL và license | HTTP IRI, open RDF, CC BY-SA; public RDF khớp local exports. |
| 2:20–2:45 | Resource Inception: owl:sameAs | Hai IRI Wikidata/DBpedia của Inception; toàn bộ dataset có 1727 sameAs. Phân biệt identity và provenance. |
| 2:45–3:25 | Query 04: 25 credit Inception; 05: 8 phim Nolan | Credit khác với người; Nolan có directing/writing/producing records riêng. Download kết quả. |
| 3:25–4:10 | Query 20: Source facts rồi Inference, bấm Run mỗi lần | WriterDirector 0 → 10; query đọc entailments đã tính, không chạy HermiT. |
| 4:10–4:35 | Protégé Nolan, ThreeCreditContributor; query 27 | Ba role khác nhau + hasRole functional chứng minh ba credit khác nhau; named graph ghi before/after. |
| 4:35–5:00 | Evidence: HermiT, tests, public graphs | Consistent, không unsatisfiable named class, 16 tests; nêu mẫu có chủ đích và giới hạn OWA. |

## Các lệnh dự phòng

```bash
.venv/bin/python src/query.py queries/02.rq
.venv/bin/python src/query.py queries/05.rq
.venv/bin/python src/query.py queries/20.rq --mode asserted
.venv/bin/python src/query.py queries/20.rq --reasoned
.venv/bin/python src/query.py queries/27.rq --mode dataset
curl -G 'http://127.0.0.1:8000/sparql' --data-urlencode mode=reasoned --data-urlencode query@queries/20.rq
```

Nếu query mới không có type, kiểm tra scope trước. ASK false trên graph nguồn là không thấy assertion, không phải OWL phủ định. Không thêm AllDifferent cho mọi QID để ép cardinality. Nếu cần giải thích MultiGenreFilm, negative test cho 0 DL members dù COUNT DISTINCT có thể lớn hơn một. Điểm chính thức do giảng viên quyết định.


## Hosting GitHub Pages

Website: https://laminhtrung.github.io/movie-lod-semantic-web/
Repo độc lập: https://github.com/laminhtrung/movie-lod-semantic-web

Bản công khai dùng Comunica để truy vấn ngay trong trình duyệt. GitHub Pages không chạy Flask và không cung cấp API `/sparql` của Python. Endpoint và content negotiation 303 chỉ được kiểm tra trên server cục bộ; Pages cung cấp trang resource và các liên kết tải RDF tĩnh. Chọn source facts / inference / before-after theo câu hỏi. IRI dùng URL GitHub Pages canonical; không bỏ prefix tên repo khi chép đường dẫn. Push `main` kích hoạt workflow Pages. Không có video demo.
