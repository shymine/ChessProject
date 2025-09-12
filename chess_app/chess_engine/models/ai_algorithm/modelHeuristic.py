from typing import Any

import chess
import torch

from chess_engine.models.base import Heuristic
import torch.nn as nn
import torch.nn.functional as F

PIECE_ORDER = [
    [chess.KING, 1],
    [chess.QUEEN, 1],
    [chess.ROOK, 2],
    [chess.BISHOP, 2],
    [chess.KNIGHT, 2],
    [chess.PAWN, 8]
]

def transform_board_to_tensor(board: chess.Board) -> torch.Tensor:
    array = []
    for color in [chess.WHITE, chess.BLACK]:
        array_pop = []
        for piece_type, number in PIECE_ORDER:
            piece_count = 0
            array_piece = []
            if piece_type == chess.PAWN:
                array_piece.append(array_pop)
                piece_count = len(array_pop)
            for piece in board.pieces(piece_type, color):
                piece_count += 1
                array_piece.append(transform_piece(color, piece, piece_type))
            if piece_count < number:
                for _ in range(number-piece_count):
                    array_piece.append(neutral_piece(color, piece_type))
            elif piece_count > number:
                for _ in range(piece_count-number):
                    array_pop.append(array_piece.pop())
            array.append(array_piece)

    flattened_data = []
    for piece_data in array:
        flattened_data.extend(piece_data)
    flattened_data.append(int(board.turn))

    return torch.tensor(flattened_data, dtype=torch.float32)




def transform_piece(color, piece, piece_type):
    return [(chess.square_file(piece) + 1) / 8,
            (chess.square_rank(piece) + 1) / 8,
            int(color),
            1,
            piece_type / 6]

def neutral_piece(color, piece_type):
    return [0,
            0,
            int(color),
            0,
            piece_type / 6]


class ModelHeuristic(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.lin1 = nn.Linear(161, 64)
        self.lin2 = nn.Linear(64, 16)
        self.lin3 = nn.Linear(16, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.lin1(x))
        x = F.relu(self.lin2(x))
        return F.tanh(self.lin3(x))



