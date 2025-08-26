from chess_engine.models.ai_algorithm.randomAI import RandomAI
from chess_engine.models.base import AI
from chess_engine.models.ai_algorithm.mcts import MCTS
from chess_engine.models.ai_algorithm.minmax import MinMax


AI_LIST: dict[str, type[AI]] = {
    "random": RandomAI,
    "minmax": MinMax,
    "mcts": MCTS
}