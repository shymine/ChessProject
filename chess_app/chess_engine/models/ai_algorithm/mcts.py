from typing import List, Optional
from chess import Board, Move, Color
from chess_engine.models.base import InitPlayer, AI
from tqdm import tqdm
import math
import time
import random
import jsonpickle

class MCTS(AI):
    def __init__(self, player: InitPlayer, iterations: int) -> None:
        self.iterations = iterations
        super().__init__(player)

    def makeMove(self, board: Board) -> Move:
        start = time.time()
        root = MCTSNode(board, None, None, board.turn)
        for _ in tqdm(range(self.iterations)):
            node = root
            while not (node.is_terminal() or node.is_fully_expanded() or len(node.children) == 0):
                # print("node: ", jsonpickle.encode(node))
                node = node.best_child()
            if not (node.is_terminal() or node.is_fully_expanded()):
                node = node.expand()
            result = node.rollout()
            node.backpropagate(result)
        end = time.time()
        print("Time spend for mcts: ", end-start)
        return root.best_child(c=0).action

class MCTSNode:
    def __init__(self, board: Board, parent, action: Optional[Move], root_color: Color) -> None:
        self.state = board
        self.parent = parent
        self.children: List[MCTSNode] = []
        self.action = action
        self.visits = 0
        self.score = 0
        self.untried_actions = list(self.state.legal_moves)
        self.root_color = root_color
        random.shuffle(self.untried_actions)

    def is_fully_expanded(self) -> bool :
        return len(self.untried_actions) == 0
    
    def is_terminal(self) -> bool:
        return self.state.is_game_over(claim_draw=True)

    def expand(self):
        """Add a remaining action as a children"""
        action = self.untried_actions.pop()
        new_state = self.state.copy()
        new_state.push(action)
        child = MCTSNode(new_state, self, action, self.root_color)
        self.children.append(child)
        return child
    
    def best_child(self, c=1.4):
        def select(child: MCTSNode) -> float:
            # print("select: child score {}; child visit {}; self visit {}".format(child.score, child.visits, self.visits))
            perf_score = child.score / child.visits
            exp_score = math.sqrt(math.log(self.visits) / child.visits)
            return perf_score + c * exp_score
        
        return max(self.children, key=select)
    
    def rollout(self) -> float:
        """play random moves until game ends"""
        def random_move(moves: List[Move]) -> Move:
            if len(moves) == 0:
                raise Exception("there are no moves")
            if len(moves) == 1:
                return moves[0]
            el = random.randint(0, len(moves)-1)
            return moves[el]
        
        new_state = self.state.copy()

        while not new_state.is_game_over(claim_draw=True):
            try:
                move = random_move(list(new_state.legal_moves))
            except Exception as e:
                print("no moves in {}".format(new_state.legal_moves))
                raise e
            new_state.push(move)
        result = 0
        outcome = new_state.outcome(claim_draw=True)
        if outcome is not None:
            if outcome.winner is None:
                result = 0.5
            elif outcome.winner == self.root_color:
                result = 1
            else:
                result = 0
        else :
            raise Exception("outcome is None: ", new_state.fen())

        return result
    
    def backpropagate(self, result):
        """update the stats up the tree"""
        self.visits += 1
        self.score += result
        if not self.parent is None:
            self.parent.backpropagate(result)
    
