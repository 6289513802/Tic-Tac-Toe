import tkinter as tk
from tkinter import messagebox
import math

def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    return None

def is_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def ai_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.configure(bg='black')
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.create_widgets()
        self.center_window()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg='black', bd=5, relief='ridge')
        self.frame.pack(expand=True, padx=10, pady=10)
        
        self.create_buttons()
        self.replay_button = tk.Button(self.root, text='Replay', font='Arial 15 bold', bg='orange', fg='white', command=self.reset_board, bd=3, relief='raised')
        self.replay_button.pack(pady=20)

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.frame, text=' ', font='Arial 20 bold', width=5, height=2, bg='lightgrey', bd=2, relief='solid',
                                               command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    def on_button_click(self, i, j):
        if self.buttons[i][j]['text'] == ' ' and self.current_player == 'X':
            self.buttons[i][j]['text'] = 'X'
            self.buttons[i][j]['fg'] = 'blue'
            self.buttons[i][j]['bg'] = 'lightblue'
            self.board[i][j] = 'X'
            if self.check_game_over():
                return
            self.current_player = 'O'
            self.ai_turn()

    def ai_turn(self):
        move = ai_move(self.board)
        if move:
            i, j = move
            self.buttons[i][j]['text'] = 'O'
            self.buttons[i][j]['fg'] = 'red'
            self.buttons[i][j]['bg'] = 'lightcoral'
            self.board[i][j] = 'O'
            if self.check_game_over():
                return
            self.current_player = 'X'

    def check_game_over(self):
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Tic-Tac-Toe", f"{winner} wins!")
            self.reset_board()
            return True
        elif is_full(self.board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            self.reset_board()
            return True
        return False

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ' '
                self.buttons[i][j]['bg'] = 'lightgrey'
        self.current_player = 'X'
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
