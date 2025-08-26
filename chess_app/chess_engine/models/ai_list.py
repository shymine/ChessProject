from chess_engine.models.ai_algorithm.randomAI import RandomAI
from chess_engine.models.ai_algorithm.minmax import MinMax
from chess_engine.models.ai_algorithm.mcts import MCTS
from chess_engine.models.base import Player, InitPlayer
from chess_engine.models.ai_algorithm.pieceCountH import PieceCountH


AI_LIST: dict[str, Player] = {
    "random": RandomAI(InitPlayer("random", True)),
    "minmax": MinMax(InitPlayer("minmax", True), PieceCountH()),
    "mcts": MCTS(InitPlayer("mcts", True), 200),
}