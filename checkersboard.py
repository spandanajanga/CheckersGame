import math
import copy

class Board:
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.B_left = self.w_left = 12  #B= black and W= white
        self.B_kings = self.w_kings = 0
        self.features = []
        self.rewards = []

    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self, rows, cols, piece):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(piece(row, col, W))
                    elif row > 4:
                        self.board[row].append(piece(row, col, B))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def display_board(self):
        self.board.print_board()

    def get_legal_moves(self):
        return self.board.get_possible_next_moves()

    def make_move(self, move):
        self.board.make_move(move)
        self.current_player = 1 if self.current_player == 2 else 2

    def is_game_over(self):
        return self.board.is_game_over()
    
    def not_spot(self, loc):
        if len(loc) == 0 or loc[0] < 0 or loc[0] > self.HEIGHT - 1 or loc[1] < 0 or loc[1] > self.WIDTH - 1:
            return True
        return False    
    
    def get_spot_info(self, loc):
        return self.spots[loc[0]][loc[1]]
    
    def forward_n_locations(self, start_loc, n, backwards=False):
        if n % 2 == 0:
            temp1 = 0
            temp2 = 0
        elif start_loc[0] % 2 == 0:
            temp1 = 0
            temp2 = 1 
        else:
            temp1 = 1
            temp2 = 0
        answer = [[start_loc[0], start_loc[1] + math.floor(n / 2) + temp1], [start_loc[0], start_loc[1] - math.floor(n / 2) - temp2]]
        if backwards: 
            answer[0][0] = answer[0][0] - n
            answer[1][0] = answer[1][0] - n
        else:
            answer[0][0] = answer[0][0] + n
            answer[1][0] = answer[1][0] + n
        if self.not_spot(answer[0]):
            answer[0] = []
        if self.not_spot(answer[1]):
            answer[1] = []
        return answer

    def extract_features(self, state, action):
        # Define your feature extraction logic here
        features = [...]  # Extract features from the state and action
        self.features.append(features)

    def calculate_reward(self, state, action, next_state):
        # Define your reward calculation logic here
        reward = [...]  # Calculate reward based on the state, action, and next state
        self.rewards.append(reward)

def main():
    game = board()
    game.display_board()

    while not game.is_game_over():
        legal_moves = game.get_legal_moves()
        if legal_moves:
            print("Player", game.current_player, "'s move:")
            print("Legal Moves:", legal_moves)
            # Implement the move selection logic here
            selected_move = legal_moves[0]  # For now, just select the first legal move
            game.make_move(selected_move)
            game.display_board()
            # Extract features and calculate reward for the current state-action pair
            game.extract_features(game.board, selected_move)
            game.calculate_reward(game.board, selected_move, game.board)  # Assuming no change in state for now
        else:
            print("No legal moves for Player", game.current_player)
            break

    # Determine the winner
    if game.current_player == 1:
        winner = "Player 2"
    elif game.current_player == 2:
        winner = "Player 1"
    else:
        winner = "No one"

    print("Game over. Winner:", winner)

if __name__ == "__main__":
    main()
