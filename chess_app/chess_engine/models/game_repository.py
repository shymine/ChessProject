from chess_engine.models.game import Game
from chess_engine.models.playerBase import InitPlayer

class GameRepository:

    def __init__(self) -> None:
        self.default = Game(InitPlayer("", False), InitPlayer("", False))
        self.current_game = self.default
        self.game_history = []
        
    
    def setCurrentGame(self, game: Game):
        self.current_game = game
    
    def pushHistory(self):
        if self.current_game.players[True].name == "":
            self.game_history.append(self.current_game)
            self.current_game = self.default
