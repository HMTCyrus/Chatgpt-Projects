from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from tran_data import EDGES, NODES, Edge, Node


COLORS = {
    "Person": QColor("#0077b6"),
    "Dynasty": QColor("#6a4c93"),
    "Event": QColor("#f77f00"),
    "Idea": QColor("#2a9d8f"),
}


@dataclass
class RenderedNode:
    circle: QGraphicsEllipseItem
    label: QLabel


class HistoricalConstellationWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Historical Constellation - Nhà Trần (MVP)")
        self.resize(1200, 760)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints())

        self.year_label = QLabel()
        self.timeline = QSlider(Qt.Orientation.Horizontal)
        self.timeline.setMinimum(1225)
        self.timeline.setMaximum(1400)
        self.timeline.setValue(1288)
        self.timeline.valueChanged.connect(self.render_graph)

        self.search = QComboBox()
        self.search.setEditable(True)
        self.search.addItems(sorted(node.name for node in NODES.values()))
        self.search.currentTextChanged.connect(self.highlight_focus)

        self.details = QPlainTextEdit()
        self.details.setReadOnly(True)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Nhân vật / thực thể:"))
        controls.addWidget(self.search, 2)
        controls.addWidget(QLabel("Mốc năm:"))
        controls.addWidget(self.timeline, 4)
        controls.addWidget(self.year_label)

        side = QVBoxLayout()
        side.addWidget(QLabel("Thông tin chi tiết"))
        side.addWidget(self.details)

        body = QHBoxLayout()
        body.addWidget(self.view, 3)

        side_widget = QWidget()
        side_widget.setLayout(side)
        side_widget.setMaximumWidth(360)
        body.addWidget(side_widget, 1)

        root = QVBoxLayout()
        root.addLayout(controls)
        root.addLayout(body)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        self.node_items: Dict[str, RenderedNode] = {}
        self.edge_items: List[Tuple[QGraphicsLineItem, Edge]] = []
        self.render_graph(self.timeline.value())

    def _is_active(self, start: int, end: int, year: int) -> bool:
        return start <= year <= end

    def render_graph(self, year: int) -> None:
        self.year_label.setText(str(year))
        self.scene.clear()
        self.node_items.clear()
        self.edge_items.clear()

        active_nodes = {
            node_id: node
            for node_id, node in NODES.items()
            if self._is_active(node.start_year, node.end_year, year)
        }
        active_edges = [e for e in EDGES if self._is_active(e.start_year, e.end_year, year)]

        pen = QPen(QColor("#9ca3af"))
        pen.setWidth(2)

        for edge in active_edges:
            if edge.source_id not in active_nodes or edge.target_id not in active_nodes:
                continue
            source = active_nodes[edge.source_id]
            target = active_nodes[edge.target_id]
            line = self.scene.addLine(source.x, source.y, target.x, target.y, pen)
            line.setToolTip(
                f"{source.name} -> {target.name}\n"
                f"Quan hệ: {edge.relation}\n"
                f"Độ tin cậy: {edge.confidence:.2f}\n"
                f"Nguồn: {edge.source}"
            )
            self.edge_items.append((line, edge))

        for node_id, node in active_nodes.items():
            radius = 24 if node.kind == "Person" else 20
            color = COLORS.get(node.kind, QColor("#6b7280"))
            circle = self.scene.addEllipse(
                node.x - radius,
                node.y - radius,
                radius * 2,
                radius * 2,
                QPen(Qt.GlobalColor.black),
                QBrush(color),
            )
            circle.setToolTip(f"{node.name}\n{node.kind}\n{node.start_year}-{node.end_year}")
            self.node_items[node_id] = RenderedNode(circle=circle, label=QLabel(node.name))

            text_item = self.scene.addText(node.name)
            text_item.setDefaultTextColor(QColor("#111827"))
            text_item.setPos(node.x - 50, node.y + radius + 2)

        self.highlight_focus(self.search.currentText())

    def highlight_focus(self, name: str) -> None:
        selected_node = next((node for node in NODES.values() if node.name == name), None)

        for node_id, rendered in self.node_items.items():
            node = NODES[node_id]
            base_color = COLORS.get(node.kind, QColor("#6b7280"))
            rendered.circle.setBrush(QBrush(base_color))

        if not selected_node or selected_node.node_id not in self.node_items:
            self.details.setPlainText("Chọn một nhân vật hoặc thực thể để xem chi tiết.")
            return

        self.node_items[selected_node.node_id].circle.setBrush(QBrush(QColor("#ef476f")))

        connections = [
            edge
            for _, edge in self.edge_items
            if edge.source_id == selected_node.node_id or edge.target_id == selected_node.node_id
        ]
        if not connections:
            relation_summary = "Không có quan hệ nào ở mốc thời gian hiện tại."
        else:
            relation_summary = "\n".join(
                f"- {NODES[e.source_id].name} -> {NODES[e.target_id].name} ({e.relation}, conf={e.confidence:.2f})"
                for e in connections
            )

        detail = (
            f"Tên: {selected_node.name}\n"
            f"Loại: {selected_node.kind}\n"
            f"Thời gian: {selected_node.start_year}-{selected_node.end_year}\n\n"
            f"Tóm tắt:\n{selected_node.summary}\n\n"
            f"Quan hệ ở năm {self.timeline.value()}:\n{relation_summary}"
        )
        self.details.setPlainText(detail)


def main() -> None:
    app = QApplication(sys.argv)
    window = HistoricalConstellationWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
