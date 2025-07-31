import abc
import chess

class InitPlayer:
    def __init__(self, name: str, is_ai: bool = False) -> None:
        self.name = name
        self.is_ai = is_ai

class Player(abc.ABC):
    def __init__(self, player: InitPlayer) -> None:
        super().__init__()
        self.name = player.name
        self.is_ai = player.is_ai
    
    @abc.abstractmethod
    def play(self, moves: list[chess.Move]) -> chess.Move :
        pass