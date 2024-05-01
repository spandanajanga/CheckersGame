import copy
from checkersboard import *
from game import *



def main():
    game = CheckersGame()
    game.display_board()

    while not game.is_game_over():
        if game.get_legal_moves(WHITE):
            # Player 1 (User) Move
            print("White's move: ")
            while True:
                try:
                    start_row = int(input("Enter starting row: "))
                    start_col = int(input("Enter starting column: "))
                    end_row = int(input("Enter ending row: "))
                    end_col = int(input("Enter ending column: "))
                    move = ((start_row, start_col), (end_row, end_col))
                    if move in game.get_legal_moves(WHITE):
                        break
                    else:
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Invalid input! Please enter integers.")
            game.make_move(move)
            game.display_board()

        if game.get_legal_moves(BLACK):
            # Player 2 (AI) Move
            print("Black's(AI) move: ")
            move, _ = game.minmax(3, False)
            if move:
                game.make_move(move)
                print("AI's move: ", move)
                game.display_board()

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
    elif black_count > white_count:
        winner = "Black"

    if winner:
        print(f"{winner} wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()

