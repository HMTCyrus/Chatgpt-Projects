# Historical Constellation (Prototype: Nhà Trần)

Phiên bản quy mô nhỏ đầu tiên của Historical Constellation, tập trung vào giai đoạn **nhà Trần ở Việt Nam**.

## Tính năng hiện có
- Hiển thị graph quan hệ lịch sử theo node/edge.
- Dataset mẫu gồm nhân vật, sự kiện, triều đại, tư tưởng liên quan đến nhà Trần.
- Timeline slider để lọc quan hệ theo từng mốc năm (1225-1400).
- Chọn nhân vật/thực thể để xem thông tin chi tiết + quan hệ đang hoạt động + confidence.

## Cài đặt
```bash
python -m venv .venv
source .venv/bin/activate
pip install PyQt6
```

## Chạy ứng dụng
```bash
python app.py
```

## Gợi ý mở rộng tiếp theo
- Đưa dữ liệu ra file JSON/Neo4j thay vì hard-coded.
- Thêm bộ lọc theo loại quan hệ (ally, enemy, successor...).
- Tích hợp ingestion từ Wikipedia/Wikidata cho giai đoạn nhà Trần.
