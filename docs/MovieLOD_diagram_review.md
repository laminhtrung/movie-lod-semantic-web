# Kiểm tra sơ đồ MovieLOD

Bản vẽ: `MovieLOD_entity_diagram.png`, `.svg` và `.pdf`.

Sơ đồ dùng ký pháp UML cho các lớp chính (A/B), view range của OWL (C) và một ví dụ liên kết RDF giữa các cá thể (D). Phạm vi gồm toàn bộ 19 object properties, 5 datatype properties và ví dụ `owl:sameAs`; không liệt kê toàn bộ 37 lớp hoặc mọi biểu thức anonymous/restriction trong OWL.

## Tài liệu chuẩn đối chiếu

- [OMG UML 2.5.1, tài liệu normative](https://www.omg.org/spec/UML/2.5.1/PDF): §9.2.4.2 (generalization), §11.5.4 (association/navigability/multiplicity), §9.8.4 (instance specification). Đã đọc trực tiếp PDF của OMG.
- [W3C OWL 2 Structural Specification](https://www.w3.org/TR/owl2-syntax/): khai báo lớp, property, domain/range, qualified cardinality và cá thể.
- [W3C OWL 2 Primer](https://www.w3.org/TR/owl2-primer/): lớp/cá thể, ràng buộc property, đồng nhất và khác nhau của cá thể.

## Những sửa đổi sau đối chiếu

1. `Film → Work`: nét liền và tam giác rỗng hướng về lớp cha, thay cho nét đứt ở bản trước.
2. Object property: đường liền với đầu mũi tên mở, tên property ghi trên đường nối; tên và chiều đối chiếu trực tiếp với domain/range trong OWL.
3. Bội số `1` đặt ở đầu đích cho `contributionBy`, `contributionTo`, `hasRole`. Kiểm tra qualified cardinality bằng 1 và range tương ứng của lớp Contribution. Các bội số association khác không hiển thị, do đó không diễn giải chúng thành 1. Đây là quy tắc nêu ở UML §11.5.4.
4. Datatype property đặt trong ngăn thuộc tính, theo dạng `property : datatype [0..*]`. Trình tạo kiểm tra không có FunctionalProperty hay restriction cho các property này. `runtime` có đơn vị giây.
5. ActorRole/DirectorRole/WriterRole/ProducerRole xuất hiện trong UML Comment, ghi rõ là OWL individuals; không đặt trong ngăn thuộc tính. `owl:AllDifferent` được kiểm tra trong OWL. Không suy diễn rằng ContributionRole chỉ có đúng bốn cá thể.
6. View C ghi rõ không có domain axiom. “Unspecified subject” là ký hiệu hỗ trợ đọc range, không phải lớp mới của ontology.
7. View D dùng cá thể Inception có tên/type gạch chân theo ký pháp instance; hai IRI bên ngoài là các node RDF. Hai triple `owl:sameAs` được kiểm tra có thật trong file OWL. Chúng không được biểu diễn thành quan hệ giữa các lớp.

## Kiểm tra nội dung và bố cục

Trình tạo `src/draw_movielod_entities.py` kiểm tra trực tiếp nguồn OWL, rồi đo chữ sau khi trình duyệt nạp font để phát hiện:

- property thiếu hoặc sai domain/range;
- bội số không khớp restriction;
- chữ vượt khung ảnh hoặc tràn khỏi ô;
- hai nhãn chồng nhau;
- nhãn đè lên ô hay bị đường nối xuyên qua;
- đường nối đi vào bên trong ô không liên quan.

Kết quả cuối: các danh sách lỗi đều rỗng. Đã xem lại trực quan PNG và bản render của PDF. PDF có một trang, nhúng font Arial Regular/Bold; SVG cũng nhúng font. PNG kích thước 2800 × 3410 px. Bản SVG/PDF phù hợp để phóng to và in; toàn bộ nhãn được giữ dưới dạng chữ.

Dữ liệu kiểm tra: `evidence/entity_diagram_checks.json`. File OWL không thay đổi; SHA-256 vẫn là `c75fb9caad895cbc18ba316e4bfb7bc1be1ef7f3701ff214276a1a21acc4eecd`.
