import math
import numpy as np
import matplotlib.pyplot as plt

# Initialize the game board
AI = 'O'
YOU = 'X'

# Function to print the game board in the terminal
def print_board_terminal(board):
    for i in range(0, 9, 3):
        print(board[i] + ' | ' + board[i+1] + ' | ' + board[i+2])
    print()

# Set up the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

# Plot the 2D Tic-Tac-Toe board
def plot_board_2d(board):
    ax.clear()  # Clear the previous plot

    # Draw the grid
    ax.set_xticks(np.arange(0.5, 3.5, step=1))
    ax.set_yticks(np.arange(0.5, 3.5, step=1))
    ax.grid(True)

    # Set axis limits and turn off axis labels
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Plot the moves on the 2D board
    for i, cell in enumerate(board):
        x = i % 3  # Column
        y = 2 - (i // 3)  # Row (inverted for proper board display)
        if cell == YOU:
            ax.text(x + 0.5, y + 0.5, 'X', fontsize=40, ha='center', va='center', color='red')
        elif cell == AI:
            ax.text(x + 0.5, y + 0.5, 'O', fontsize=40, ha='center', va='center', color='blue')

    plt.draw()  # Redraw the updated plot
    plt.pause(0.001)  # Pause briefly to allow updates and input collection

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return all(cell != '-' for cell in board)

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if check_winner(board, AI):
        return 1
    elif check_winner(board, YOU):
        return -1
    elif is_board_full(board):
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = AI
                eval = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                board[i] = '-'
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = YOU
                eval = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                board[i] = '-'
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def find_best_move(board):
    best_move = -1
    best_eval = -math.inf
    for i in range(9):
        if board[i] == '-':
            board[i] = AI
            eval = minimax_alpha_beta(board, 0, -math.inf, math.inf, False)
            board[i] = '-'
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

def play_game():
    board = ['-'] * 9  # Initialize the board

    # Main game loop
    while True:
        print_board_terminal(board)  # Print the board in the terminal
        plot_board_2d(board)         # Plot the 2D board
        try:
            move = int(input("Select your choice (1-9): "))  # Ask for 1-based input
            if move < 1 or move > 9:
                print("Invalid input. Please choose a number between 1 and 9.")
                continue
            move -= 1  # Convert to 0-based index
            if board[move] == '-':
                board[move] = YOU
                if check_winner(board, YOU):
                    print_board_terminal(board)
                    plot_board_2d(board)
                    print("You win!")
                    break
                elif is_board_full(board):
                    print_board_terminal(board)
                    plot_board_2d(board)
                    print("It's a draw!")
                    break
                ai_move = find_best_move(board)
                board[ai_move] = AI
                if check_winner(board, AI):
                    print_board_terminal(board)
                    plot_board_2d(board)
                    print("AI wins!")
                    break
                elif is_board_full(board):
                    print_board_terminal(board)
                    plot_board_2d(board)
                    print("It's a draw!")
                    break
            else:
                print("Cell already filled. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 9.")

# Game restart loop
while True:
    play_game()  # Start the game
    restart = input("Game over. Do you want to play again? (y/n): ").lower()
    if restart != 'y':
        print("Thanks for playing!")
        break
