# MovieLOD — Đối chiếu yêu cầu 3.0.0

Năm yêu cầu cốt lõi đều có minh chứng trong cùng model 3.0.0. Đây là đối chiếu kỹ thuật, không phải điểm do giảng viên chấm.

| Yêu cầu | Minh chứng | Kết quả |
|---|---|---|
| Ontology | 37 named classes, DBpedia reuse, restrictions, inverse/chain, HermiT | Đáp ứng về kỹ thuật |
| Dữ liệu nguồn | 76 phản hồi giữ nguyên byte/hash, 30 phim, provenance | Đáp ứng trong mẫu |
| Công bố RDF | HTTP IRI, Turtle/JSON-LD/OWL, license, public graph equality | Đồng bộ 3.0.0 |
| Liên kết | 1.727 sameAs, Wikidata/DBpedia; scope đếm rõ | Đáp ứng; chưa đo precision/recall |
| SPARQL | 27 competency questions, ba graph scopes trong trình duyệt, SELECT/ASK/CONSTRUCT/DESCRIBE | Đáp ứng; query không tự chạy DL reasoner |

## Minh chứng suy luận

Actor 769; Filmmaker 89; WriterDirector 10; min 2 credit: 17 người; min 3: 7 người; 965 chain pairs. Min cardinality dựa controlled-role distinctness và hasRole functional. Negative MultiGenreFilm = 0 được ghi rõ, không thay bằng COUNT DISTINCT.

16 tests kiểm tra model và endpoint. Các file evidence ghi hash của OWL, kết quả truy vấn, browser và đồ thị công khai. Kiểm tra trực tiếp bằng `src/validate.py`, `pytest`, `src/public_query_check.py` và `src/check_publication.py`.

## Phần cần bổ sung khi nộp

11 ô ảnh Protégé trong slide cần screenshot thật theo checklist. Các ảnh web đã chụp; sơ đồ tác giả không giả làm giao diện Protégé. MP4 đã xoá theo yêu cầu; demo bằng thao tác trực tiếp. Nếu rubric riêng bắt buộc video hoặc ảnh đã điền, phần đó chưa hoàn tất. Số lớp và số triple không tự quyết định điểm. Mẫu có chủ đích, mapping nhãn và identity matching chưa có ground truth vẫn là giới hạn học thuật.

Hosting công khai là GitHub Pages (web tĩnh, Comunica trong browser). Endpoint HTTP SPARQL bằng Flask có ở bản local; không khẳng định GitHub Pages chạy backend Python.
