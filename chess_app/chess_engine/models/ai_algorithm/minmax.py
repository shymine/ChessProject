from typing import Dict
from chess import Board, Move
from chess_engine.models.base import InitPlayer, AI, Heuristic
import math
import time
import random
import chess

class MinMax(AI):
    def __init__(self, player: InitPlayer, heuristic: Heuristic, depth: int) -> None:
        self.depth = depth
        self.tree_log = []
        self.count = 0
        self.heuristic = heuristic
        super().__init__(player)
    
    def makeMove(self, board: Board) -> Move:
        start = time.time()
        self.tree_log = []

        best_score = -math.inf
        best_moves = []
        board_table = {}

        for move in board.legal_moves:
            child = self._create_child(board, move)
            score = self.minmax(child, self.depth, False, board.turn, board_table)
            if score == best_score:
                best_moves.append(move)
            if score > best_score:
                best_score = score
                best_moves = [move]
        
        end = time.time()
        print("best moves: (", best_score, ")", [x.uci() for x in best_moves])
        print("Time spend for minmax: ", end-start)
        with open("./tree_debug/{}.txt".format(self.count), "w") as f:
            f.write("\n".join(self.tree_log))
        self.count += 1

        r = random.randint(0, len(best_moves)-1)
        return best_moves[r]
    
    def minmax(self, node: Board, depth: int, player: bool, player_color: chess.Color, lookup_table: Dict[str, float]) -> float:
        if depth == 0 :
            v = self.heuristic(node, player_color)
            self.tree_log.append("-    "*(self.depth-depth)+node.peek().uci()+" ("+str(v)+")")
            return v
        if node.is_checkmate():
            v = -math.inf if player else math.inf
            self.tree_log.append("-    "*(self.depth-depth)+node.peek().uci()+" ("+str(v)+")")
            return v
        if node.is_game_over(claim_draw=True): # all draw because checkmate answered before
            self.tree_log.append("-    "*(self.depth-depth)+node.peek().uci()+" (draw)")
            return 0
        
        node_hash = node.fen()

        if node_hash in lookup_table:
            return lookup_table[node_hash]
        
        curr_lvl = len(self.tree_log)
        self.tree_log.append("-    "*(self.depth-depth)+node.peek().uci())

        children = [self._create_child(node, move) for move in node.legal_moves]
        if player:
            v = -math.inf     
            for child in children:
                v = max(v, self.minmax(child, depth-1, not player, player_color, lookup_table))
            lookup_table[node_hash] = v
            self.tree_log[curr_lvl] = self.tree_log[curr_lvl]+" ("+str(v)+") max"
            return v
        else:
            v = math.inf
            for child in children:
                v = min(v, self.minmax(child, depth-1, not player, player_color, lookup_table))
            lookup_table[node_hash] = v
            self.tree_log[curr_lvl] = self.tree_log[curr_lvl]+" ("+str(v)+") min"
            return v
    
    def _create_child(self, node: Board, move: Move) -> Board:
        c = node.copy()
        c.push(move)
        return c
    