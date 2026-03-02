"""Trò chơi X/O với giao diện Qt (PySide6)."""

from __future__ import annotations

from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


from game_logic import TicTacToeGame


class TicTacToeWindow(QMainWindow):
    """Cửa sổ chính hiển thị bàn cờ và trạng thái."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Trò chơi X/O - Qt")
        self.setMinimumSize(420, 500)

        self.game = TicTacToeGame()
        self.buttons: List[QPushButton] = []

        self.status_label = QLabel("Lượt hiện tại: X")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; font-weight: 600; margin: 8px;")

        self._init_ui()

    def _init_ui(self) -> None:
        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(10)

        root_layout.addWidget(self.status_label)

        grid = QGridLayout()
        grid.setSpacing(8)

        for index in range(9):
            button = QPushButton("")
            button.setFixedSize(120, 120)
            button.setStyleSheet(
                "font-size: 36px; font-weight: bold;"
                "background-color: #f2f4f8; border-radius: 8px;"
            )
            button.clicked.connect(lambda _checked=False, pos=index: self._handle_move(pos))
            self.buttons.append(button)
            row, col = divmod(index, 3)
            grid.addWidget(button, row, col)

        controls = QHBoxLayout()
        controls.addStretch()

        reset_button = QPushButton("Chơi lại")
        reset_button.setStyleSheet("padding: 8px 14px; font-size: 16px;")
        reset_button.clicked.connect(self._reset_game)
        controls.addWidget(reset_button)

        controls.addStretch()

        root_layout.addLayout(grid)
        root_layout.addLayout(controls)

        self.setCentralWidget(central)

    def _handle_move(self, index: int) -> None:
        current_player = self.game.current_player
        if not self.game.make_move(index):
            return

        self.buttons[index].setText(current_player)
        self._update_status_label()

        if self.game.winner:
            self._set_board_enabled(False)
            QMessageBox.information(self, "Kết thúc", f"Người chơi {self.game.winner} đã thắng!")
        elif self.game.is_draw:
            self._set_board_enabled(False)
            QMessageBox.information(self, "Kết thúc", "Hòa! Không ai thắng.")

    def _update_status_label(self) -> None:
        if self.game.winner:
            self.status_label.setText(f"Kết quả: {self.game.winner} thắng")
        elif self.game.is_draw:
            self.status_label.setText("Kết quả: Hòa")
        else:
            self.status_label.setText(f"Lượt hiện tại: {self.game.current_player}")

    def _set_board_enabled(self, enabled: bool) -> None:
        for button in self.buttons:
            button.setEnabled(enabled)

    def _reset_game(self) -> None:
        self.game.reset()
        for button in self.buttons:
            button.setText("")
            button.setEnabled(True)
        self._update_status_label()


def main() -> None:
    app = QApplication([])
    window = TicTacToeWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
