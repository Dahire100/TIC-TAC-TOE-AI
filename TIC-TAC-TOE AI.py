import math
import numpy as np
import matplotlib.pyplot as plt
import re

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
    ax.set_xticks(np.arange(0.5, 3.5, step=1))
    ax.set_yticks(np.arange(0.5, 3.5, step=1))
    ax.grid(True)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for i, cell in enumerate(board):
        x = i % 3
        y = 2 - (i // 3)
        if cell == YOU:
            ax.text(x + 0.5, y + 0.5, 'X', fontsize=40, ha='center', va='center', color='red')
        elif cell == AI:
            ax.text(x + 0.5, y + 0.5, 'O', fontsize=40, ha='center', va='center', color='blue')

    plt.draw()
    plt.pause(0.001)

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return any(all(board[i] == player for i in combo) for combo in winning_combinations)

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

def parse_input(user_input):
    """Convert natural language input into board index."""
    mapping = {
        'top left': 0, 'top center': 1, 'top right': 2,
        'middle left': 3, 'middle center': 4, 'middle right': 5,
        'bottom left': 6, 'bottom center': 7, 'bottom right': 8,
        '1': 0, '2': 1, '3': 2,
        '4': 3, '5': 4, '6': 5,
        '7': 6, '8': 7, '9': 8
    }
    user_input = user_input.lower()
    for key in mapping.keys():
        if re.search(r'\b' + re.escape(key) + r'\b', user_input):
            return mapping[key]
    return -1  # Invalid input

def play_game():
    board = ['-'] * 9

    while True:
        print_board_terminal(board)
        plot_board_2d(board)
        user_input = input("Select your choice (e.g., 'top left', 'middle center', or enter a number 1-9): ")

        move = parse_input(user_input)

        if move < 0 or move >= 9:
            print("Invalid input. Please describe your choice more clearly or enter a number between 1 and 9.")
            continue

        if board[move] == '-':
            board[move] = YOU
            print(f"You placed an 'X' in {user_input}.")
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
            print(f"AI placed an 'O' in {['top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right'][ai_move]}.")
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

# Game restart loop
while True:
    play_game()
    restart = input("Game over. Do you want to play again? (y/n): ").lower()
    if restart != 'y':
        print("Thanks for playing!")
        break
        
