"""Logic trò chơi X/O, không phụ thuộc giao diện."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TicTacToeGame:
    board: List[str] = field(default_factory=lambda: [""] * 9)
    current_player: str = "X"
    winner: Optional[str] = None
    is_draw: bool = False

    WINNING_COMBINATIONS = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    )

    def make_move(self, index: int) -> bool:
        if self.winner or self.is_draw:
            return False
        if index < 0 or index >= len(self.board):
            return False
        if self.board[index]:
            return False

        self.board[index] = self.current_player
        self._update_game_status()

        if not self.winner and not self.is_draw:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def _update_game_status(self) -> None:
        for a, b, c in self.WINNING_COMBINATIONS:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                self.winner = self.board[a]
                self.is_draw = False
                return

        if all(self.board):
            self.winner = None
            self.is_draw = True

    def reset(self) -> None:
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None
        self.is_draw = False
