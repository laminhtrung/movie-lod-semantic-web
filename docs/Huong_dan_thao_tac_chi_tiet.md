# MovieLOD — Thao tác kiểm tra bản mới

> **Phiên bản:** Ontology, dữ liệu, web và truy vấn dùng chung 3.0.0. MP4 đã được xoá theo yêu cầu; tài liệu demo dùng cho trình diễn trực tiếp.

## 1. Kiểm tra đúng file

- Full OWL: ontology/Movie_Knowledge_Graph.owl.
- Schema: ontology/Movie_Ontology.owl / movie.ttl.
- Facts và inference mới: evidence/ontology_design/asserted.ttl, schema.ttl, inferred.ttl.
- So sánh named graphs: before_after.trig.

## 2. Protégé

Mở full OWL, kiểm tra 3.0.0, chọn HermiT và Start reasoner. Xem inferred types của Nolan và các credit của Nolan trên Inception. Credit có DirectorRole → DirectingContribution; người có credit này → MovieDirector / Filmmaker. Writing credit → ScreenWriter; giao hai nghề → WriterDirector.

hasRole là functional; DirectorRole, WriterRole và ProducerRole khác nhau. Ba credit không thể collapse thành một; đây là căn cứ min 3. Không thêm AllDifferent cho genre QID để ép kết quả.

## 3. Truy vấn trực tiếp và suy luận

```bash
.venv/bin/python src/query.py queries/05.rq --mode asserted
.venv/bin/python src/query.py queries/20.rq --mode asserted
.venv/bin/python src/query.py queries/20.rq --mode reasoned
.venv/bin/python src/query.py queries/27.rq --mode dataset
```

Nolan films: 8; WriterDirector: 0 trước và 10 sau. Query 27 cần Dataset/TriG, không graph phẳng. Query runner chỉ đọc graph, không chạy reasoner mới mỗi lần.

## 4. Các lỗi dễ nhầm

- Sai prefix: ex:Actor không còn ở model mới; dùng dbo:Actor.
- Sai property/đơn vị: dbo:runtime là giây, xsd:double; UI thẻ phim có thể đổi sang phút để dễ đọc; RDF vẫn lưu giây.
- Type trống: kiểm tra asserted/reasoned graph và trạng thái reasoner.
- OWL đúng nhưng query web không có lớp mới: chọn scope Inference rồi bấm Run.
- Timestamp malformed với HermiT cũ: dùng full OWL đã xuất với ba chữ số phần thập phân; không khẳng định mọi timestamp dài hơn đều sai XSD.
- COUNT DISTINCT không tự chứng minh minimum cardinality do OWL không có unique-name assumption.

## 5. Chụp ảnh và đối chiếu

Theo Checklist_anh_Protege.md/pdf; đặt ảnh đúng stem ở evidence/protege. Các ô chờ hiện không phải ảnh đã có. Hình author diagram và evidence summary không được gọi là screenshot Protégé. File nguồn Slide_full.pptx.pdf phản ánh model trước đó.

## 6. Chạy web 3.0.0

```bash
.venv/bin/python src/server.py --port 8000
```

Web local dùng RDFLib; hosted dùng Comunica. Endpoint mặc định source facts. Thêm `?mode=reasoned` để truy vấn type suy luận hoặc `?mode=dataset` cho query 27. Hosted Comunica dùng cùng exports trong web/dist/data. Sau build/reason cần restart server; không có MP4.


## Hosting GitHub Pages

Website: https://laminhtrung.github.io/movie-lod-semantic-web/
Repo độc lập: https://github.com/laminhtrung/movie-lod-semantic-web

Bản công khai dùng Comunica để truy vấn ngay trong trình duyệt. GitHub Pages không chạy Flask và không cung cấp API `/sparql` của Python. Endpoint và content negotiation 303 chỉ được kiểm tra trên server cục bộ; Pages cung cấp trang resource và các liên kết tải RDF tĩnh. Chọn source facts / inference / before-after theo câu hỏi. IRI dùng URL GitHub Pages canonical; không bỏ prefix tên repo khi chép đường dẫn. Push `main` kích hoạt workflow Pages. Không có video demo.
