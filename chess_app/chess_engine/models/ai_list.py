from chess_engine.models.ai_algorithm.randomAI import RandomAI
from chess_engine.models.base import AI
from chess_engine.models.ai_algorithm.pieceCountH import PieceCountH


AI_LIST: dict[str, type[AI]] = {
    "random": RandomAI,
}