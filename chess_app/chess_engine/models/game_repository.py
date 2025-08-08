from typing import List
from chess_engine.models.game import Game, AI_LIST
from chess_engine.models.playerBase import InitPlayer
from os import listdir
from os.path import isfile, join

import chess.pgn as pgn


class GameRepository:

    ROOT="./games"

    def __init__(self) -> None:
        self.default = Game(InitPlayer("", False), InitPlayer("", False))
        self.current_game = self.default
        self.game_history: List[Game] = []

        print("loading history:")
        filenames = [join(self.ROOT, f) for f in listdir(self.ROOT) if isfile(join(self.ROOT, f))]
        for file in filenames:
            self.game_history.append(
                self._fromPGN(file)
            )
    
    def setCurrentGame(self, game: Game):
        self.current_game = game
    
    def pushHistory(self): # must be called only if game is finished
        if self.current_game.players[True].name != "":
            self.game_history.append(self.current_game)
            self._toPGN()
            print("game pushed to history")
            self.current_game = self.default
        else:
            print("current: ", self.current_game.players[True].name)

    def _toPGN(self): # must be called only if game is finished
        game = pgn.Game()
        white = self.current_game.players[True].name
        black = self.current_game.players[False].name
        game.headers["White"] = white
        game.headers["Black"] = black
        result = self.current_game.gameResultString()
        game.headers["Result"] = result

        node = game
        for move in self.current_game.getHistory():
            node = node.add_main_variation(move)
        
        filename = "./games/{}_{}.pgn".format(white, black)
        with open(filename, "w") as file:
            file.write(str(game))
    
    def _fromPGN(self, filename: str) -> Game:
        with open(filename, "r") as file:
            pgn_game: pgn.Game = pgn.read_game(file)
        print(filename)
        wname = pgn_game.headers["White"]
        wis_ai = wname in AI_LIST
        bname = pgn_game.headers["Black"]
        bis_ai = bname in AI_LIST
        white = InitPlayer(wname, wis_ai)
        black = InitPlayer(bname, bis_ai)
        game = Game(white, black)

        for move in pgn_game.mainline_moves():
            game.play(move)
        
        return game
