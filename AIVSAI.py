import random
import copy
from checkersboard import *
from game import *

    def minmax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            return None, self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            legal_moves = self.get_legal_moves(WHITE)
            for move in legal_moves:
                new_board = copy.deepcopy(self)
                new_board.make_move(move)
                _, eval = new_board.minmax(depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            legal_moves = self.get_legal_moves(BLACK)
            for move in legal_moves:
                new_board = copy.deepcopy(self)
                new_board.make_move(move)
                _, eval = new_board.minmax(depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return best_move, min_eval

    def is_game_over(self):
        return not self.get_legal_moves(WHITE) or not self.get_legal_moves(BLACK)


class QLearningAgent:
    def __init__(self):
        self.q_values = {}

    def get_q_value(self, state, action):
        return self.q_values.get((state, action), 0.0)

    def update(self, state, action, next_state, reward, alpha, gamma):
        max_q_next = max([self.get_q_value(next_state, a) for a in next_state.get_legal_moves(BLACK)] or [0.0])
        self.q_values[(state, action)] = (1 - alpha) * self.get_q_value(state, action) + alpha * (reward + gamma * max_q_next)

    def get_action(self, state, epsilon):
        legal_moves = state.get_legal_moves(WHITE)
        if not legal_moves:
            return None

        if random.random() < epsilon:
            return random.choice(legal_moves)
        else:
            q_values = [self.get_q_value(state, a) for a in legal_moves]
            return legal_moves[q_values.index(max(q_values))]


def main():
    games_played = 0
    white_wins = 0
    black_wins = 0
    total_moves = 0

    while True:
        games_played += 1
        moves = 0
        game = CheckersGame()
        game.display_board()

        q_agent = QLearningAgent()

        epsilon = 0.1
        alpha = 0.1
        gamma = 0.9

        while not game.is_game_over():
            moves += 1
            if game.get_legal_moves(WHITE):
                move, _ = game.minmax(3, True)
                if move:
                    game.make_move(move)
                    print("White's move: ", move)
                    game.display_board()
                    next_state = copy.deepcopy(game)
                    reward = game.evaluate_board()
                    q_agent.update(game, move, next_state, reward, alpha, gamma)
            if game.get_legal_moves(BLACK):
                move = q_agent.get_action(game, epsilon)
                if move:
                    game.make_move(move)
                    print("Black's move: ", move)
                    game.display_board()
        
        total_moves += moves

        winner = None
        white_count = 0
        black_count = 0
        for row in range(8):
            for col in range(8):
                if game.board[row][col] == WHITE:
                    white_count += 1
                elif game.board[row][col] == BLACK:
                    black_count += 1
        if white_count > black_count:
            winner = "White"
            white_wins += 1
        elif black_count > white_count:
            winner = "Black"
            black_wins += 1

        if winner:
            print(f"{winner} wins!")
        else:
            print("It's a draw!")

        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != "yes":
            break

    print(f"Number of games played: {games_played}")
    print(f"Number of games won by White: {white_wins}")
    print(f"Number of games won by Black: {black_wins}")
    print(f"Average number of moves per game: {total_moves / games_played}")


if __name__ == "__main__":
    main()
