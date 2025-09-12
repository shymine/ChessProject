import chess
import torch.nn as nn
import torch
from torch import optim, argmax
from torch.nn import MSELoss

from chess_engine.models.ai_algorithm.modelHeuristic import transform_board_to_tensor


class TrainModelHeuristic:
    def __init__(self, model: nn.Module, config, device: torch.device):
        self.model = model
        self.config = config
        self.device = device
        self.model.to(device)

        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.losses = []


def train(self, epochs: int, gamma: float) -> float:
    for epoch in range(epochs):
        episode = []
        g = 0
        tot_g = []
        tot_pred = []
        for recomp, pred in reversed(episode):
            g = recomp + gamma * g
            tot_g.append(g)
            tot_pred.append(pred)
        tot_g = reversed(tot_g)
        tot_pred = reversed(tot_pred)
        loss = MSELoss(torch.tensor(tot_pred), torch.tensor(tot_g))
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        self.losses.append(loss.item())


def reward(game: chess.Board, move: chess.Move):
    reward = 0
    opposent = not game.turn
    value = pieces_value(game, opposent)
    game.push(move)
    if game.is_checkmate():
        reward = 39
        if not game.turn :
            reward *= -1
    elif not game.is_game_over(claim_draw=True):
        reward = value - pieces_value(game, opposent)
    game.pop()
    return reward

def pieces_value(node: chess.Board, color: chess.Color) -> float:
    nb_pawn = len(node.pieces(chess.PAWN, color))
    nb_rook = len(node.pieces(chess.ROOK, color))
    nb_knight = len(node.pieces(chess.KNIGHT, color))
    nb_bishop = len(node.pieces(chess.BISHOP, color))
    nb_queen = len(node.pieces(chess.QUEEN, color))
    total_player = nb_pawn * 1 + nb_rook * 5 + nb_knight * 3 + nb_bishop * 3 + nb_queen * 9
    return total_player

def generate_episode(model):
    game = chess.Board()
    while not game.is_game_over(claim_draw=True):
        move_value = []
        for move in game.legal_moves:
            game.push(move)
            eval = model(transform_board_to_tensor(game))
            move_value.append(eval)
            game.pop()
        best_move = argmax(torch.stack(move_value, 0))
        move_reward = reward(game, game.legal_moves[best_move])
        yield move_reward, max(move_value)
