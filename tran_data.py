from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Node:
    node_id: str
    name: str
    kind: str
    start_year: int
    end_year: int
    summary: str
    x: float
    y: float


@dataclass(frozen=True)
class Edge:
    source_id: str
    target_id: str
    relation: str
    start_year: int
    end_year: int
    confidence: float
    source: str


NODES: Dict[str, Node] = {
    "tran_dynasty": Node(
        node_id="tran_dynasty",
        name="Nhà Trần",
        kind="Dynasty",
        start_year=1225,
        end_year=1400,
        summary="Triều đại lãnh đạo Đại Việt và nổi bật với 3 lần kháng chiến chống Nguyên Mông.",
        x=0,
        y=0,
    ),
    "tran_thai_tong": Node(
        node_id="tran_thai_tong",
        name="Trần Thái Tông",
        kind="Person",
        start_year=1218,
        end_year=1277,
        summary="Vị vua đầu tiên của nhà Trần, đặt nền tảng chính trị và quân sự.",
        x=-230,
        y=-160,
    ),
    "tran_thanh_tong": Node(
        node_id="tran_thanh_tong",
        name="Trần Thánh Tông",
        kind="Person",
        start_year=1240,
        end_year=1290,
        summary="Cùng Thái Thượng Hoàng điều hành triều chính và chuyển giao quyền lực ổn định.",
        x=-60,
        y=-210,
    ),
    "tran_nhan_tong": Node(
        node_id="tran_nhan_tong",
        name="Trần Nhân Tông",
        kind="Person",
        start_year=1258,
        end_year=1308,
        summary="Lãnh đạo kháng chiến chống Nguyên lần 2, 3 và sáng lập Thiền phái Trúc Lâm.",
        x=120,
        y=-180,
    ),
    "tran_hung_dao": Node(
        node_id="tran_hung_dao",
        name="Trần Hưng Đạo",
        kind="Person",
        start_year=1228,
        end_year=1300,
        summary="Quốc công Tiết chế, danh tướng chủ chốt trong kháng chiến chống Nguyên Mông.",
        x=260,
        y=-40,
    ),
    "battle_bach_dang": Node(
        node_id="battle_bach_dang",
        name="Chiến thắng Bạch Đằng (1288)",
        kind="Event",
        start_year=1288,
        end_year=1288,
        summary="Trận quyết định đánh bại đạo thủy quân Nguyên trên sông Bạch Đằng.",
        x=270,
        y=180,
    ),
    "mongol_invasions": Node(
        node_id="mongol_invasions",
        name="Kháng chiến chống Nguyên Mông",
        kind="Event",
        start_year=1258,
        end_year=1288,
        summary="Ba lần kháng chiến 1258, 1285, 1287-1288 của Đại Việt trước Nguyên Mông.",
        x=90,
        y=170,
    ),
    "truc_lam": Node(
        node_id="truc_lam",
        name="Thiền phái Trúc Lâm",
        kind="Idea",
        start_year=1299,
        end_year=1400,
        summary="Dòng thiền mang bản sắc Đại Việt, do Trần Nhân Tông sáng lập.",
        x=-130,
        y=170,
    ),
}


EDGES: List[Edge] = [
    Edge("tran_dynasty", "tran_thai_tong", "FOUNDED_BY", 1225, 1277, 0.96, "Đại Việt sử ký toàn thư"),
    Edge("tran_thai_tong", "tran_thanh_tong", "SUCCESSOR_OF", 1258, 1278, 0.95, "Wikipedia tiếng Việt"),
    Edge("tran_thanh_tong", "tran_nhan_tong", "SUCCESSOR_OF", 1278, 1293, 0.94, "Wikipedia tiếng Việt"),
    Edge("tran_nhan_tong", "truc_lam", "FOUNDER_OF", 1299, 1308, 0.91, "Thiền uyển tập anh"),
    Edge("tran_nhan_tong", "mongol_invasions", "LED", 1278, 1288, 0.92, "Việt Nam sử lược"),
    Edge("tran_hung_dao", "mongol_invasions", "COMMANDER_OF", 1258, 1288, 0.97, "Hịch tướng sĩ"),
    Edge("battle_bach_dang", "mongol_invasions", "PART_OF", 1288, 1288, 0.98, "Đại Việt sử ký toàn thư"),
    Edge("tran_hung_dao", "battle_bach_dang", "STRATEGIST_OF", 1288, 1288, 0.95, "Wikipedia tiếng Việt"),
    Edge("tran_dynasty", "mongol_invasions", "DEFENDED_AGAINST", 1258, 1288, 0.93, "Đại Việt sử ký toàn thư"),
]
