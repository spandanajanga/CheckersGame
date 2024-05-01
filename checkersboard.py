import math
import copy

EMPTY=0
WHITE=1
BLACK=2

class Board:
    def __init__(self):
    self.board = [[EMPTY] * 8 for _ in range(8)]
    self.init_board()

def init_board(self):
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 != 0:
                if row < 3:
                    self.board[row][col] = BLACK
                elif row > 4:
                    self.board[row][col] = WHITE

def display_board(self):
    print("   0 1 2 3 4 5 6 7")
    for i, row in enumerate(self.board):
        print(i, end="  ")
        for j, col in enumerate(row):
            if col == EMPTY:
                print("-", end=" ")
            elif col == WHITE:
                print("W", end=" ")
            elif col == BLACK:
                print("B", end=" ")
        print()

def get_legal_moves(self, player):
    moves = []
    for row in range(8):
        for col in range(8):
            if self.board[row][col] == player:
                moves.extend(self.get_piece_moves(row, col))
    return moves

def get_piece_moves(self, row, col):
    piece_moves = []
    if self.board[row][col] == WHITE:
        directions = [UP_LEFT, UP_RIGHT]
    elif self.board[row][col] == BLACK:
        directions = [DOWN_LEFT, DOWN_RIGHT]
    else:
        return piece_moves

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]
        if self.is_valid_square(new_row, new_col) and self.board[new_row][new_col] == EMPTY:
            piece_moves.append(((row, col), (new_row, new_col)))
        elif self.is_valid_square(new_row, new_col) and self.board[new_row][new_col] != self.board[row][col]:
            jump_row = new_row + direction[0]
            jump_col = new_col + direction[1]
            if self.is_valid_square(jump_row, jump_col) and self.board[jump_row][jump_col] == EMPTY:
                piece_moves.append(((row, col), (jump_row, jump_col)))
    return piece_moves

def is_valid_square(self, row, col):
    return 0 <= row < 8 and 0 <= col < 8

def make_move(self, move):
    start, end = move
    start_row, start_col = start
    end_row, end_col = end
    self.board[end_row][end_col] = self.board[start_row][start_col]
    self.board[start_row][start_col] = EMPTY
    if abs(start_row - end_row) == 2:
        jumped_row = (start_row + end_row) // 2
        jumped_col = (start_col + end_col) // 2
        self.board[jumped_row][jumped_col] = EMPTY

def evaluate_board(self):
    white_count = 0
    black_count = 0
    for row in range(8):
        for col in range(8):
            if self.board[row][col] == WHITE:
                white_count += 1
            elif self.board[row][col] == BLACK:
                black_count += 1
    return white_count - black_count

    def is_game_over(self):
    return not self.get_legal_moves(WHITE) or not self.get_legal_moves(BLACK)
    
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
