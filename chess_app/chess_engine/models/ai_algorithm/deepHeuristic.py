import chess
import torch.nn as nn

from chess_engine.models.ai_algorithm.modelHeuristic import ModelHeuristic, transform_board_to_tensor
from chess_engine.models.base import Heuristic


class DeepHeuristic(Heuristic):
    def __init__(self, weight, default_module = ModelHeuristic()):
        super().__init__()
        self.model = default_module

    def evaluate(self, board: chess.Board, player_color: chess.Color) -> float:
        transformed_board = transform_board_to_tensor(board)
        return self.model(transformed_board).item()

