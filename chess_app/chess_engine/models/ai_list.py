from chess_engine.models.ai_algorythm.randomAI import RandomAI
from chess_engine.models.playerBase import Player, InitPlayer


AI_LIST: dict[str, Player] = {
    "random": RandomAI(InitPlayer("random", True))
}