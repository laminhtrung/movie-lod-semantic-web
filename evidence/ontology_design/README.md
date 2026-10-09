# Cách sử dụng bản thiết kế đã kiểm chứng

Canonical OWL local đã được xuất thành 3.0.0 và kiểm tra trực tiếp bằng HermiT; ứng dụng và các graph đã đồng bộ 3.0.0.

- Đọc docs/DBpedia_OWL_Design.html để xem đủ 7 bảng, định nghĩa OWL, 5 demo và kết quả truy vấn. Bảng rộng có thể cuộn ngang.
- schema.ttl chứa các tiên đề; asserted.ttl chỉ chứa dữ liệu đầu vào; inferred.ttl chứa kết quả suy luận.
- Trong Protégé: mở complete.ttl rồi chọn HermiT → Start reasoner. Đây là đồ thị đầy đủ chứa schema + facts, chưa gán thủ công các lớp suy luận.
- Có thể tạo tạm một OWL đầy đủ từ `Graph().parse("schema.ttl") + Graph().parse("asserted.ttl")` bằng RDFLib. Tắt normalization của xsd:dateTime hoặc chuyển lexical timestamp về 3 chữ số thập phân trước khi serialize để tương thích HermiT cũ.
- Query 01–08 chạy với asserted.ttl. Query 09–26 chạy với tổng schema + asserted + inferred. Query 27 chạy trên before_after.trig (hai named graph).
- reasoning.json ghi số lượng local URI; query_results.json ghi số dòng truy vấn; các query thực thể giới hạn IRI local để loại alias. Query literal và class URI có scope riêng.
- hermit.log là log thật; cardinality_negative.log xác nhận MultiGenreFilm không có member suy luận. Không thêm AllDifferent cho genre/film/award để ép điểm.
- exactly 1 không thay cho kiểm tra dữ liệu thiếu trong mô hình thế giới mở.
- MP4 đã được loại bỏ theo yêu cầu; dùng duy nhất full OWL canonical.
