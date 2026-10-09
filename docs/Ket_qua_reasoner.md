# MovieLOD — Kết quả reasoner của OWL cuối

> **Phiên bản:** Ontology, dữ liệu, web và truy vấn dùng chung 3.0.0. MP4 đã được xoá theo yêu cầu; tài liệu demo dùng cho trình diễn trực tiếp.

HermiT 1.3.8.1099 đọc trực tiếp RDF/XML, exit code 0; consistent, không có named class bất khả thỏa. Kết quả class membership khớp thiết kế đã kiểm chứng. Đây không phải kiểm chứng Pellet mới; log Pellet cũ thuộc model trước.

File: `ontology/Movie_Knowledge_Graph.owl`. SHA-256: `c75fb9caad895cbc18ba316e4bfb7bc1be1ef7f3701ff214276a1a21acc4eecd`. Lần kiểm tra và thời gian chạy được ghi trong `evidence/ontology_design/final_owl_checks.json`.

| Class | Thành viên local sau reasoning |
|---|---:|
| dbo:Work | 30 |
| dbo:Film | 30 |
| dbo:Agent | 896 |
| dbo:Person | 851 |
| dbo:Artist | 769 |
| dbo:Actor | 769 |
| dbo:Writer | 34 |
| dbo:MovieDirector | 17 |
| dbo:ScreenWriter | 34 |
| dbo:Producer | 57 |
| dbo:Organisation | 45 |
| dbo:Company | 45 |
| dbo:Genre | 75 |
| dbo:MovieGenre | 75 |
| dbo:Award | 672 |
| dbo:Country | 11 |
| dbo:Language | 15 |
| ex:Contribution | 1010 |
| ex:ContributionRole | 0 |
| ex:SourceSnapshot | 76 |
| ex:ActionGenre | 3 |
| ex:DramaGenre | 9 |
| ex:ActingContribution | 855 |
| ex:DirectingContribution | 31 |
| ex:WritingContribution | 51 |
| ex:ProducingContribution | 73 |
| ex:Filmmaker | 89 |
| ex:ActionFilm | 12 |
| ex:AwardWinningFilm | 26 |
| ex:MultiCreditContributor | 17 |
| ex:ThreeCreditContributor | 7 |
| ex:WriterDirector | 10 |
| ex:ActorFilmmaker | 7 |
| ex:AwardWinningFilmmaker | 65 |
| ex:AwardWinningActionFilm | 10 |
| ex:GenreCrossingFilm | 8 |

ContributionRole hiển thị 0 trong cột local res: vì bốn role individual thuộc ex:. Tổng thực tế là 4. Các type domain suy luận không được asserted trong facts đầu vào. HermiT CLI xuất direct types; các superclass entailments được mở rộng theo hierarchy để đếm đầy đủ.

Ba role khác nhau cộng hasRole functional chứng minh ba credit khác nhau. MultiGenreFilm negative test trả 0, không được giữ như lớp suy luận có population. 965 quan hệ contributedTo được kiểm tra bằng inverse/subproperty/chain closure OWL RL; không dùng COUNT để giả lập cardinality.

Log: evidence/ontology_design/final_owl_hermit.log; bảng query: query_results.json. Consistency không chứng minh tất cả source claims đúng hoặc đầy đủ. MP4 đã được xoá theo yêu cầu.
