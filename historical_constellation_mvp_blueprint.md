# Historical Constellation – MVP Blueprint

## 1) Tuyên bố sản phẩm (Product statement)
Historical Constellation là phần mềm desktop giúp người dùng **học và ghi nhớ lịch sử theo mạng lưới ảnh hưởng**, thay vì tuyến thời gian đơn thuần.

### Vấn đề cốt lõi
- Dữ liệu lịch sử thường rời rạc (nhân vật, triều đại, sự kiện tách riêng).
- Người học khó thấy được quan hệ quyền lực và dòng chảy tư tưởng xuyên thời kỳ.

### Giá trị cốt lõi của MVP
- Tìm một nhân vật và xem ngay mạng quan hệ cấp 1–2.
- Mỗi quan hệ có **nguồn trích dẫn** + **confidence**.
- Có timeline cơ bản để lọc theo giai đoạn.

---

## 2) Phạm vi MVP (8–12 tuần)

### Bắt buộc (Must-have)
1. Search theo tên nhân vật (fuzzy + alias cơ bản).
2. Graph view: node + edge, phân loại edge theo màu.
3. Timeline slider: lọc quan hệ theo khoảng năm.
4. Panel chi tiết: mô tả, nguồn, confidence.
5. Data pipeline tự động từ Wikipedia/Wikidata (batch, không realtime).

### Nên có (Should-have)
1. Bộ lọc loại node (Person/Event/Idea).
2. Chế độ “đóng băng thời điểm” (time slice).
3. Cơ chế human review nhẹ cho edge confidence thấp.

### Chưa làm ở MVP (Out of scope)
- Đồ họa bản đồ địa lý toàn cầu nâng cao theo zoom đa tầng.
- Tự động hóa hoàn toàn extraction đa ngôn ngữ chất lượng cao.
- Collaborative editing/multi-user sync.

---

## 3) Kiến trúc kỹ thuật đề xuất

## 3.1 Desktop stack
- **Python 3.11+**
- UI: **PySide6** (ưu tiên native + Python-first)
- Graph DB: **Neo4j**
- ETL + NLP: `requests`, `wikipedia-api`, `wikidata`, `spaCy` + LLM extraction (tuỳ ngân sách)

## 3.2 Logical modules
1. `ingestion/`: lấy dữ liệu Wikipedia/Wikidata.
2. `extraction/`: trích xuất entity/relationship/time/source/confidence.
3. `graph_store/`: chuẩn hoá schema + ghi vào Neo4j.
4. `query_service/`: API nội bộ cho UI (search, subgraph, timeline filter).
5. `desktop_ui/`: graph canvas, timeline, detail panel.

## 3.3 Data flow
1. Seed nhân vật đầu vào (ví dụ 500 nhân vật nổi bật theo vùng).
2. Pull dữ liệu thô từ Wikipedia/Wikidata.
3. Extract relation candidates.
4. Score confidence.
5. Lưu vào Neo4j.
6. UI query theo person + thời gian.

---

## 4) Mô hình dữ liệu đồ thị (Neo4j)

## 4.1 Node labels
- `Person`
- `Dynasty`
- `Empire`
- `Idea`
- `Event`
- `Source`

Ví dụ thuộc tính chung:
- `id`
- `name`
- `summary`
- `start_year`, `end_year`
- `geo`
- `wikidata_id`, `wikipedia_url`
- `image_url`
- `aliases`

## 4.2 Relationship types
- `INFLUENCED_BY`
- `TEACHER_OF`
- `SUCCESSOR_OF`
- `ALLY_OF`
- `ENEMY_OF`
- `PART_OF`
- `REACTION_TO`
- `AUTHORED_BY`

Thuộc tính relationship:
- `confidence: float (0..1)`
- `start_year`, `end_year`
- `evidence_snippet`
- `source_id`
- `extracted_at`

---

## 5) Cách tính confidence (v1 đơn giản)

`confidence = 0.5 * model_score + 0.3 * source_quality + 0.2 * temporal_consistency`

Trong đó:
- `model_score`: độ chắc chắn từ mô hình extraction.
- `source_quality`: xếp hạng nguồn (Wikidata > bài wiki chưa dẫn nguồn).
- `temporal_consistency`: quan hệ có hợp logic thời gian hay không.

Ngưỡng đề xuất:
- `>= 0.75`: hiển thị mặc định.
- `0.5 - 0.75`: hiển thị nhưng gắn cảnh báo.
- `< 0.5`: ẩn khỏi view mặc định, chỉ hiện khi bật chế độ exploratory.

---

## 6) UX flow chính

1. Mở app → ô tìm kiếm + graph canvas rỗng.
2. Nhập “Napoleon Bonaparte”.
3. Tải subgraph cấp 1 (in/out).
4. Kéo timeline 1780–1820 → graph tự lọc.
5. Click edge “ALLY_OF” → panel hiện nguồn + confidence.
6. Click node “French Revolution” → chuyển trọng tâm sang event.

---

## 7) Lộ trình thực thi gợi ý

## Sprint 1 (Tuần 1–2)
- Khởi tạo project Python + Neo4j local.
- Định nghĩa graph schema + migration script.
- Seed dữ liệu thủ công 50 nhân vật để dựng UI sớm.

## Sprint 2 (Tuần 3–4)
- Search service + query subgraph depth 1–2.
- UI graph view cơ bản.
- Detail panel.

## Sprint 3 (Tuần 5–6)
- Timeline filter.
- Edge legend + confidence display.
- Caching query.

## Sprint 4 (Tuần 7–8)
- Pipeline ingestion Wikipedia/Wikidata.
- Extraction v1 + scoring.
- Scheduler cập nhật định kỳ (daily batch).

## Sprint 5 (Tuần 9–10)
- QA dữ liệu + đánh giá precision/recall mẫu.
- Tối ưu hiệu năng query.
- Đóng gói desktop app (PyInstaller).

---

## 8) KPI kiểm chứng MVP
- Thời gian từ search đến render subgraph < 2 giây (dataset thử nghiệm).
- Ít nhất 1,000 Person nodes + 5,000 edges.
- >= 80% edge trong sample audit có nguồn hợp lệ.
- User test: 70% người dùng trả lời đúng câu hỏi “ai ảnh hưởng ai” sau 10 phút dùng.

---

## 9) Rủi ro và giảm thiểu
- **Noise extraction cao** → áp dụng ngưỡng confidence + review queue.
- **Mơ hồ ngữ nghĩa quan hệ** → chuẩn hoá taxonomy edge từ đầu.
- **UI quá tải khi graph dày** → progressive reveal theo zoom + depth.
- **Chi phí LLM** → batch extraction + cache + rule-based pre-filter.

---

## 10) Next step cụ thể (ngay tuần này)
1. Chốt stack: PySide6 + Neo4j.
2. Chốt taxonomy 8 loại edge đầu tiên.
3. Làm dataset pilot 100 nhân vật (châu Âu 1750–1950).
4. Dựng prototype UI tìm kiếm + graph + panel trong 5 ngày.
5. Đo phản hồi người dùng học lịch sử lần 1.
