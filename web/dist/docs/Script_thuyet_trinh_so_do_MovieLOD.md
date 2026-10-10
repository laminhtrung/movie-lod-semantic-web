# Script thuyết trình sơ đồ MovieLOD

Hình sử dụng: `MovieLOD_entity_diagram.png`. Ngôn ngữ: tiếng Việt. Thời lượng dự kiến: khoảng 5–6 phút, tùy tốc độ nói.

**Phạm vi đã kiểm tra:** ontology có **37 lớp được đặt tên**; hình hiện tại thể hiện **13 lớp chính**, **19 object properties**, **5 datatype properties**, cùng ví dụ liên kết `owl:sameAs`. **24 lớp chưa xuất hiện trong hình.** Các ô trùng tên là cùng một lớp. Bốn tên ActorRole/DirectorRole/WriterRole/ProducerRole là cá thể; “Unspecified subject” là ký hiệu hỗ trợ đọc domain/range, không phải lớp bổ sung.

Các đoạn trong ngoặc vuông là chỉ dẫn thao tác, không đọc thành lời.

## 1. Giới thiệu và cách đọc hình

[Chỉ tiêu đề, sau đó lướt qua bốn vùng A, B, C, D.]

“Đây là sơ đồ mô hình thực thể chính của MovieLOD. Ontology đầy đủ có 37 lớp; hình này chọn 13 lớp chính để làm rõ cấu trúc dữ liệu và các quan hệ. Vì vậy, đây chưa phải sơ đồ toàn bộ phân cấp lớp.

Trong hình, ô chữ nhật có tên như Film hoặc Person biểu diễn lớp. Mũi tên mở biểu diễn object property, với tên quan hệ ghi trên đường nối. Tam giác rỗng biểu diễn kế thừa: Film là lớp con của Work. Những dòng trong ngăn thuộc tính là datatype property, tức các giá trị như năm phát hành hoặc thời lượng.

Hình gồm mô hình đóng góp, quan hệ phim và người, mô tả nguồn dữ liệu, và ví dụ liên kết tới dữ liệu bên ngoài.”

## 2. Vùng A — đóng góp và vai trò

[Chỉ Person → Contribution → Film, rồi ContributionRole.]

“Phần A thể hiện cách một người tham gia vào một bộ phim thông qua một Contribution, tức một đóng góp cụ thể.

Person có `hasContribution` trỏ tới Contribution. Theo chiều ngược lại, `contributionBy` cho biết đóng góp đó thuộc về người nào. `contributionTo` cho biết đóng góp dành cho bộ phim nào; `contributionOf` cho phép đi từ phim tới các đóng góp.

Mỗi Contribution gắn với đúng một người, một phim và một vai trò. Bội số 1 được đặt tại các đầu đích tương ứng, dựa trên ràng buộc trong OWL.

Bốn vai trò diễn viên, đạo diễn, biên kịch và nhà sản xuất là các cá thể của ContributionRole. Chúng được khai báo khác nhau bằng AllDifferent. Khai báo này không giới hạn lớp chỉ được có bốn vai trò.

Từ chuỗi Person → Contribution → Film, ontology có thể suy ra quan hệ `contributedTo`. Mô hình này giúp biểu diễn một người đảm nhiệm nhiều vai trò trong cùng một phim.”

## 3. Vùng B — phim, người và đơn vị sản xuất

[Chỉ tam giác Film → Work; tiếp theo các mũi tên director, writer, starring, productionCompany, producer.]

“Ở phần B, Film kế thừa Work, tức một bộ phim là một loại tác phẩm. Vì vậy, phim cũng thuộc phạm vi của những thuộc tính được khai báo cho Work.

`director` nối Film với Person; `directed` đi từ Person tới Film. `writer` nối Work với Person, `starring` nối Work với Actor, còn `actedIn` đi từ Actor tới Film.

`productionCompany` nối tác phẩm với công ty sản xuất; `productionOf` cung cấp chiều truy cập ngược lại. `producer` có đích là Agent theo khai báo trong ontology.

Về giá trị dữ liệu, Film có năm phát hành kiểu integer, còn Work có thời lượng kiểu double, tính bằng giây. Những thuộc tính này không được khai báo là bắt buộc hoặc chỉ có một giá trị trong OWL hiện tại. Chúng ta không tự thêm bội số 1.”

## 4. Vùng C — thuộc tính mô tả và nguồn dữ liệu

[Chỉ Unspecified subject, rồi Genre/Award/Country/Language và SourceSnapshot.]

“Phần C gồm thể loại, giải thưởng, quốc gia, ngôn ngữ và nguồn dữ liệu. Các property ở đây đã có range, nhưng chưa khai báo domain.

Vì vậy, hình dùng ký hiệu Unspecified subject. Ký hiệu này không phải một lớp mới, và cũng không có nghĩa rằng các quan hệ này chỉ được dùng cho Film.

SourceSnapshot lưu thông tin về bản dữ liệu nguồn: URL nguồn, thời điểm thu thập và mã SHA-256. Các thông tin này hỗ trợ truy xuất nguồn gốc và kiểm tra dữ liệu. Chúng có các kiểu anyURI, dateTime và string tương ứng.”

## 5. Vùng D — liên kết dữ liệu và query minh chứng

[Chỉ cá thể res:film-Q25188 và hai IRI bên ngoài. Nếu demo web, chọn query “Inception links to DBpedia and Wikidata”.]

“Phần D chuyển từ mô hình lớp sang một ví dụ dữ liệu cụ thể. Cá thể `film-Q25188` biểu diễn phim Inception trong MovieLOD và có kiểu Film.

Cá thể này được nối bằng `owl:sameAs` tới tài nguyên Inception của DBpedia và Q25188 của Wikidata. Đây là khai báo cùng một thực thể, mạnh hơn một liên kết tham khảo thông thường.

Query mẫu trên web đọc các liên kết này và trả về hai nguồn: DBpedia và Wikidata. Ví dụ cho thấy dữ liệu nội bộ có thể liên kết với định danh được dùng trong những bộ dữ liệu khác.”

## 6. Kết thúc và phạm vi của hình

[Chỉ lại các vùng A/B, rồi nhắc phần lớp suy luận chưa vẽ.]

“Sơ đồ làm rõ cách MovieLOD tổ chức phim, người, đóng góp, vai trò và nguồn dữ liệu, đồng thời khai báo các quan hệ để truy vấn và suy luận.

Ontology còn có những lớp như Filmmaker, WriterDirector, AwardWinningFilm và ThreeCreditContributor. Các lớp này cùng những lớp còn lại chưa được thể hiện đầy đủ trong hình hiện tại. Khi trình bày toàn bộ ontology hoặc kết quả phân loại của reasoner, nhóm cần dùng thêm phần phân cấp lớp và các định nghĩa OWL tương ứng.”

## Câu hỏi có thể được hỏi

**Hình có đủ 37 lớp chưa?**

Chưa. Hình có 13 lớp chính; ontology có 37 lớp được đặt tên. Hình bao phủ 19 object properties và 5 datatype properties được khai báo, nhưng không biểu diễn toàn bộ lớp và axiom.

**Vì sao Person và Film xuất hiện ở nhiều vùng?**

Đó là các ô lặp lại của cùng một lớp để giảm đường nối giao nhau; chúng không được đếm thành nhiều lớp.

**ContributionRole có đúng bốn cá thể không?**

Có bốn cá thể vai trò được nêu trong hình và khai báo AllDifferent. Không có nghĩa rằng lớp này chỉ được có đúng bốn cá thể.

**Unspecified subject có được tính trong 37 lớp không?**

Không. Đây là ký hiệu cho phần domain chưa được khai báo, không phải một lớp mới trong ontology.

**Bội số 1 có nghĩa dữ liệu phải có sẵn một triple không?**

Đây là ràng buộc ngữ nghĩa OWL về đúng một giá trị, với kiểu đích tương ứng. Theo giả định thế giới mở, thiếu triple trong file không tự động chứng minh rằng cá thể vi phạm ràng buộc; đây không phải kiểm tra trường bắt buộc như một biểu mẫu hoặc SHACL.

**Có nên nói hình này chứng minh toàn bộ reasoning không?**

Không. Hình minh họa mô hình và một số cơ chế, như property chain. Muốn chứng minh phân loại các lớp suy luận cần trình bày axiom, kết quả reasoner hoặc query trước/sau reasoning.

## Đối chiếu lớp để chuẩn bị câu trả lời

13 lớp xuất hiện trong hình:

- `dbo:Actor`, `dbo:Agent`, `dbo:Award`, `dbo:Company`, `dbo:Country`, `dbo:Film`, `dbo:Genre`, `dbo:Language`, `dbo:Person`, `dbo:Work`.
- `ex:Contribution`, `ex:ContributionRole`, `ex:SourceSnapshot`.

24 lớp chưa xuất hiện:

- Vocabulary DBpedia: `dbo:Artist`, `dbo:MovieDirector`, `dbo:MovieGenre`, `dbo:Organisation`, `dbo:Producer`, `dbo:ScreenWriter`, `dbo:Writer`.
- Credit subclasses: `ex:ActingContribution`, `ex:DirectingContribution`, `ex:ProducingContribution`, `ex:WritingContribution`.
- Genre subclasses: `ex:ActionGenre`, `ex:DramaGenre`.
- Film subclasses: `ex:ActionFilm`, `ex:AwardWinningActionFilm`, `ex:AwardWinningFilm`, `ex:GenreCrossingFilm`.
- Person subclasses: `ex:ActorFilmmaker`, `ex:AwardWinningFilmmaker`, `ex:Filmmaker`, `ex:MultiCreditContributor`, `ex:ThreeCreditContributor`, `ex:WriterDirector`.
- Dataset: `void:Dataset`.

Nguồn đối chiếu: `ontology/Movie_Knowledge_Graph.owl` phiên bản 3.0.0. SHA-256: `c75fb9caad895cbc18ba316e4bfb7bc1be1ef7f3701ff214276a1a21acc4eecd`.
