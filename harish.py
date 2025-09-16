import tkinter as tk
from tkinter import messagebox
import math
import random

class FlameXOGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔥 XO - Specially made for angry bird 🐤")
        
        # Get screen dimensions for proper fitting
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window size based on screen size
        if screen_width < 600:  # Mobile screens
            width = int(screen_width * 0.95)
            height = int(screen_height * 0.85)
        else:  # Desktop screens
            width = int(screen_width * 0.4)
            height = int(screen_height * 0.7)
        
        # Ensure minimum usable size
        width = max(width, 350)
        height = max(height, 500)
        
        # Center window on screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg='#0D0D0D')
        
        self.selected_level = None
        self.show_mode_selection()

    def show_mode_selection(self):
        """Show difficulty selection screen first"""
        self.clear_root()
        
        frame = tk.Frame(self.root, bg='#1A0A00', relief='ridge', bd=5)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title
        title_text = "🔥 Choose Your Challenge 🔥"
        title_label = tk.Label(frame, text=title_text,
                               font=('Impact', 18, 'bold'),
                               fg='#FFD700', bg='#1A0A00')
        title_label.pack(pady=20)
        
        # Special message from Harish
        description = tk.Label(frame, 
                               text="Dare to challenge if you are a boy win!\n- Harish",
                               font=('Comic Sans MS', 12, 'italic'),
                               fg='#FF6347', bg='#1A0A00')
        description.pack(pady=10)
        
        # Difficulty levels
        levels = [
            ("🟢 Easy", "Easy", '#00FF00'),
            ("🟡 Medium", "Medium", '#FFFF00'),
            ("🟠 Hard", "Hard", '#FF8000'),
            ("🔴 Impossible", "Impossible", '#FF0000')
        ]
        
        self.level_var = tk.StringVar(value="Medium")
        
        # Radio buttons for difficulty
        for text, value, color in levels:
            rb = tk.Radiobutton(frame, text=text, variable=self.level_var, value=value,
                               font=('Comic Sans MS', 14, 'bold'), 
                               fg=color, bg='#1A0A00',
                               selectcolor='#FF4500', 
                               activebackground='#1A0A00', 
                               activeforeground=color)
            rb.pack(anchor='w', padx=40, pady=5)
        
        # Special label below Impossible - ONLY shows "angry bird"
        angry_bird_label = tk.Label(frame, text="angry bird",
                                   font=('Comic Sans MS', 12, 'bold'),
                                   fg='#FF6347', bg='#1A0A00')
        angry_bird_label.pack(pady=8)
        
        # Start game button
        start_btn = tk.Button(frame, text="🎮 START GAME 🎮", 
                             font=('Impact', 14, 'bold'),
                             bg='#FF4500', fg='white', 
                             relief='raised', bd=4, 
                             padx=30, pady=10,
                             command=self.start_game)
        start_btn.pack(pady=20)

    def start_game(self):
        """Start the game with selected difficulty"""
        self.selected_level = self.level_var.get()
        
        if self.selected_level == 'Impossible':
            messagebox.showinfo("🔥 IMPOSSIBLE MODE SELECTED! 🔥", 
                              "WARNING: Computer will ALWAYS win in this mode!\n" +
                              "Dare to challenge if you are a boy win!\n- Harish 🔥")
        
        self.clear_root()
        self.setup_game_ui()

    def clear_root(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_game_ui(self):
        """Setup the main game interface"""
        # Initialize game state
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.game_active = True
        self.player_turn = True
        
        # Title with current mode
        title_frame = tk.Frame(self.root, bg='#2D1100', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text=f"🔥 XO - {self.selected_level} Mode 🔥",
                              font=('Impact', 16, 'bold'), 
                              fg='#FFD700', bg='#2D1100')
        title_label.pack(pady=15)
        
        # Flame decorative elements
        flame_label = tk.Label(self.root, text="🔥" * 18, 
                              font=('Arial', 12), fg='#FF4500', bg='#0D0D0D')
        flame_label.pack(pady=5)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='#330000', relief='sunken', bd=3)
        self.board_frame.pack(padx=20, pady=15)
        
        # Create 3x3 button grid with responsive sizing
        button_size = 80  # Base size for buttons
        font_size = 24    # Base font size
        
        # Adjust for smaller screens
        if self.root.winfo_reqwidth() < 400:
            button_size = 60
            font_size = 20
        
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(self.board_frame, text="", 
                               width=6, height=3,
                               font=('Impact', font_size, 'bold'),
                               bg='#4A1A1A', fg='white',
                               activebackground='#6A2A2A',
                               relief='raised', bd=5,
                               command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j, padx=3, pady=3)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        # Status label
        self.status_label = tk.Label(self.root, 
                                    text="🎯 Your Move! You are X 🎯",
                                    font=('Comic Sans MS', 12, 'bold'), 
                                    fg='#00FF88', bg='#0D0D0D',
                                    wraplength=300, justify='center')
        self.status_label.pack(pady=10)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#0D0D0D')
        control_frame.pack(pady=10)
        
        # Restart button
        self.restart_btn = tk.Button(control_frame, text="🔄 Restart",
                                    font=('Arial', 10, 'bold'),
                                    bg='#FF4500', fg='white',
                                    relief='raised', bd=3, 
                                    padx=15, pady=5,
                                    command=self.reset_game)
        self.restart_btn.pack(side='left', padx=10)
        
        # Change Mode button
        mode_btn = tk.Button(control_frame, text="🎮 Mode",
                            font=('Arial', 10, 'bold'),
                            bg='#FF8000', fg='white',
                            relief='raised', bd=3, 
                            padx=15, pady=5,
                            command=self.show_mode_selection)
        mode_btn.pack(side='left', padx=5)
        
        # Quit button
        quit_btn = tk.Button(control_frame, text="🚪 Quit",
                            font=('Arial', 10, 'bold'),
                            bg='#8B0000', fg='white',
                            relief='raised', bd=3, 
                            padx=15, pady=5,
                            command=self.root.quit)
        quit_btn.pack(side='right', padx=10)

    def player_move(self, row, col):
        """Handle player's move"""
        if not self.game_active or not self.player_turn or self.board[row][col] != "":
            return
        
        # Player makes move
        self.board[row][col] = "X"
        self.buttons[row][col].config(text="X", bg='#00BFFF', fg='white', state='disabled')
        self.player_turn = False
        
        # Check if player won (but NEVER in Impossible mode)
        if self.check_winner("X") and self.selected_level != 'Impossible':
            self.highlight_winner("X")
            self.status_label.config(text="🎉 You Won! 🎉", fg='#00FF00')
            self.game_active = False
            messagebox.showinfo("Victory!", f"You won {self.selected_level} mode!")
            return
        
        # Check for draw
        if self.is_board_full():
            if self.selected_level == 'Impossible':
                # Special message for Impossible mode draw
                self.status_label.config(text="🤝 DRAW!\nHence proved you are a girl!\n- Harish", fg='#FF4500')
                self.animate_dancing_girl()
                self.game_active = False
                messagebox.showinfo("Draw!", "It's a draw!\nHence proved you are a girl! - Harish 😄")
            else:
                self.status_label.config(text="🤝 It's a Draw! 🤝", fg='#FFFF00')
                self.game_active = False
                messagebox.showinfo("Draw", "Game ended in a draw!")
            return
        
        # Computer's turn
        self.status_label.config(text="🤖 Computer thinking... 🤖", fg='#FF4500')
        self.root.after(600, self.computer_move)

    def computer_move(self):
        """Handle computer's move based on difficulty"""
        if not self.game_active:
            return
        
        # Select AI strategy based on difficulty
        if self.selected_level == 'Easy':
            move = self.random_move()
        elif self.selected_level == 'Medium':
            move = self.medium_move()
        elif self.selected_level == 'Hard':
            move = self.best_move()
        else:  # Impossible mode - Computer MUST win
            move = self.impossible_move()
        
        if move:
            row, col = move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O", bg='#FF4500', fg='white', state='disabled')
            
            # Check if computer won
            if self.check_winner("O"):
                self.highlight_winner("O")
                if self.selected_level == 'Impossible':
                    # Special message for Impossible mode win with dancing girl
                    self.status_label.config(text="🔥 COMPUTER WINS!\nHence proved you are a girl!\n- Harish", fg='#FF0000')
                    self.animate_dancing_girl()
                    messagebox.showinfo("CRUSHED!", "Computer wins IMPOSSIBLE mode!\nHence proved you are a girl! - Harish 😆")
                else:
                    self.status_label.config(text="🔥 COMPUTER WINS! 🔥", fg='#FF0000')
                    messagebox.showinfo("Defeated!", f"Computer won {self.selected_level} mode!")
                self.game_active = False
                return
            
            # Check for draw
            if self.is_board_full():
                if self.selected_level == 'Impossible':
                    # Special message for Impossible mode draw with dancing girl
                    self.status_label.config(text="🤝 DRAW!\nHence proved you are a girl!\n- Harish", fg='#FF4500')
                    self.animate_dancing_girl()
                    messagebox.showinfo("Draw!", "It's a draw!\nHence proved you are a girl! - Harish 😄")
                else:
                    self.status_label.config(text="🤝 It's a Draw! 🤝", fg='#FFFF00')
                    messagebox.showinfo("Draw", "Game ended in a draw!")
                self.game_active = False
                return
        
        self.player_turn = True
        self.status_label.config(text="🎯 Your Move! Fight Back! 🎯", fg='#00FF88')

    def animate_dancing_girl(self):
        """Dancing girl animation for computer wins/draws in Impossible mode"""
        # Dancing girl frames with different poses
        dance_frames = [
            "💃 Girl is dancing! 💃\nIt was Harish! 🕺",
            "🕺 Girl is dancing! 🕺\nIt was Harish! 💃", 
            "💃🎵 Girl is dancing! 🎵💃\nIt was Harish! 🕺🎵",
            "🕺🎶 Girl is dancing! 🎶🕺\nIt was Harish! 💃🎶",
            "💃✨ Girl is dancing! ✨💃\nIt was Harish! 🕺✨",
            "🕺🌟 Girl is dancing! 🌟🕺\nIt was Harish! 💃🌟",
            "💃🎭 Girl is dancing! 🎭💃\nIt was Harish! 🕺🎭",
            "🕺🎪 Girl is dancing! 🎪🕺\nIt was Harish! 💃🎪"
        ]
        
        self.dance_frame = 0
        self.original_text = self.status_label.cget('text')
        
        def animate_dance():
            if not hasattr(self, 'status_label') or not self.status_label.winfo_exists():
                return
            
            if self.dance_frame < len(dance_frames) * 3:  # Loop 3 times
                current_frame = dance_frames[self.dance_frame % len(dance_frames)]
                
                # Color cycle for extra effect
                colors = ['#FF69B4', '#FF1493', '#FF6347', '#FFD700', '#00FF7F', '#00BFFF', '#DA70D6']
                color = colors[self.dance_frame % len(colors)]
                
                self.status_label.config(text=current_frame, fg=color)
                self.dance_frame += 1
                
                # Continue animation
                self.root.after(400, animate_dance)
            else:
                # Reset to original text after animation
                self.status_label.config(text=self.original_text, fg='#FF4500')
        
        # Start the dancing animation
        animate_dance()

    def random_move(self):
        """Easy mode - Random move"""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        return random.choice(empty_cells) if empty_cells else None

    def medium_move(self):
        """Medium mode - Win if possible, block sometimes, else random"""
        # Try to win first
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = ""
                        return (i, j)
                    self.board[i][j] = ""
        
        # Try to block player (70% chance)
        if random.random() < 0.7:
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        if self.check_winner("X"):
                            self.board[i][j] = ""
                            return (i, j)
                        self.board[i][j] = ""
        
        # Random move
        return self.random_move()

    def best_move(self):
        """Hard mode - Optimal minimax strategy"""
        best_score = -math.inf
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.minimax(0, False)
                    self.board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move

    def impossible_move(self):
        """Impossible mode - Computer ALWAYS wins, player can NEVER win"""
        # First priority: Win immediately if possible
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.board[i][j] = ""
                        return (i, j)  # Winning move!
                    self.board[i][j] = ""
        
        # Second priority: Block player from winning
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = ""
                        return (i, j)  # Block player
                    self.board[i][j] = ""
        
        # Third priority: Use enhanced minimax
        return self.get_killer_move()

    def get_killer_move(self):
        """Enhanced minimax for Impossible mode"""
        best_score = -math.inf
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    score = self.killer_minimax(0, True)
                    self.board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        return best_move

    def killer_minimax(self, depth, is_maximizing):
        """Enhanced minimax that heavily penalizes draws and favors wins"""
        if self.check_winner("O"):
            return 1000 - depth  # Huge reward for winning
        if self.check_winner("X"):
            return -1000 + depth  # Huge penalty for losing
        if self.is_board_full():
            return -50  # Penalty for draws - we want to WIN!
        
        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.killer_minimax(depth + 1, False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.killer_minimax(depth + 1, True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def minimax(self, depth, is_maximizing):
        """Standard minimax algorithm for Hard mode"""
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = -math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "O"
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == "":
                        self.board[i][j] = "X"
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        """Check if the specified player has won"""
        # Check rows, columns, and diagonals
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]):
                return True
            if all([self.board[j][i] == player for j in range(3)]):
                return True
        
        if all([self.board[i][i] == player for i in range(3)]):
            return True
        if all([self.board[i][2-i] == player for i in range(3)]):
            return True
        
        return False

    def is_board_full(self):
        """Check if the board is completely filled"""
        return all([cell != "" for row in self.board for cell in row])

    def highlight_winner(self, player):
        """Highlight winning combination with glow effect"""
        win_color = '#00FFFF' if player == "X" else '#FFD700'
        
        # Find and highlight winning cells
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == player:
                    if self.is_winning_cell(i, j, player):
                        self.buttons[i][j].config(bg=win_color, relief='sunken')

    def is_winning_cell(self, row, col, player):
        """Check if a cell is part of the winning combination"""
        # Check row
        if all([self.board[row][j] == player for j in range(3)]):
            return True
        # Check column
        if all([self.board[j][col] == player for j in range(3)]):
            return True
        # Check main diagonal
        if row == col and all([self.board[i][i] == player for i in range(3)]):
            return True
        # Check anti-diagonal
        if row + col == 2 and all([self.board[i][2-i] == player for i in range(3)]):
            return True
        return False

    def reset_game(self):
        """Reset the current game"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_active = True
        self.player_turn = True
        
        # Reset all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", bg='#4A1A1A', fg='white', 
                                        state='normal', relief='raised')
        
        self.status_label.config(text="🎯 Your Move! You are X 🎯", fg='#00FF88')

    def run(self):
        """Start the application"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = FlameXOGame()
    game.run()
