from chess_engine.models.ai_algorithm.randomAI import RandomAI
from chess_engine.models.base import Player, InitPlayer


AI_LIST: dict[str, Player] = {
    "random": RandomAI(InitPlayer("random", True))
}