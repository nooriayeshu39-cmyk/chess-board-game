# game.py - Main Game Controller

from board import Board
from player import Player
from display import (
    print_board, print_message, print_game_over,
    print_controls, print_move_history, get_input, clear_screen
)


def parse_position(pos_str):
    """
    Convert chess notation (e.g., 'e4') to (row, col).
    Returns None if invalid.
    """
    pos_str = pos_str.strip().lower()
    if len(pos_str) != 2:
        return None
    
    col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
               'e': 4, 'f': 5, 'g': 6, 'h': 7}
    
    col_char = pos_str[0]
    row_char = pos_str[1]
    
    if col_char not in col_map:
        return None
    if not row_char.isdigit() or not (1 <= int(row_char) <= 8):
        return None
    
    col = col_map[col_char]
    row = 8 - int(row_char)  # Convert chess rank to array index
    return (row, col)


def position_to_notation(row, col):
    """Convert (row, col) to chess notation string"""
    col_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
               4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return f"{col_map[col]}{8 - row}"


class Game:
    """Main chess game controller"""
    
    def __init__(self):
        self.board = Board()
        self.player1 = None  # White
        self.player2 = None  # Black
        self.current_player = None
        self.move_history = []
        self.game_over = False
        self.draw_offered_by = None
    
    def setup_players(self):
        """Get player names from input"""
        clear_screen()
        print("=" * 50)
        print("         ♔  PYTHON CHESS GAME  ♚")
        print("=" * 50)
        print("\n  Welcome! Let's set up the game.\n")
        
        name1 = input("  Enter Player 1 name (White ♙): ").strip()
        if not name1:
            name1 = "Player 1"
        
        name2 = input("  Enter Player 2 name (Black ♟): ").strip()
        if not name2:
            name2 = "Player 2"
        
        self.player1 = Player(name1, 'white')
        self.player2 = Player(name2, 'black')
        self.current_player = self.player1  # White goes first
        
        print(f"\n  ✅ Game starting!")
        print(f"  {self.player1.name} plays White ♙")
        print(f"  {self.player2.name} plays Black ♟")
        print(f"\n  White moves first!")
        input("\n  Press Enter to start...")
    
    def get_other_player(self):
        """Return the player who is NOT currently playing"""
        return self.player2 if self.current_player == self.player1 else self.player1
    
    def switch_turns(self):
        """Switch to the other player"""
        self.current_player = self.get_other_player()
    
    def handle_special_commands(self, command):
        """
        Handle special commands: resign, draw, help, history.
        Returns True if command was handled, False otherwise.
        """
        if command == 'resign':
            other = self.get_other_player()
            print_game_over(str(other), f"{self.current_player.name} resigned")
            self.game_over = True
            return True
        
        elif command == 'draw':
            if self.draw_offered_by == self.get_other_player():
                # Other player already offered draw
                print_game_over(None, "Both players agreed to a draw")
                self.game_over = True
            else:
                self.draw_offered_by = self.current_player
                print_message(
                    f"{self.current_player.name} offers a draw. "
                    f"{self.get_other_player().name} type 'draw' to accept.",
                    "info"
                )
            return True
        
        elif command == 'help':
            print_controls()
            input("  Press Enter to continue...")
            return True
        
        elif command == 'history':
            print_move_history(self.move_history, last_n=10)
            input("  Press Enter to continue...")
            return True
        
        return False
    
    def get_player_move(self):
        """
        Get and validate a move from the current player.
        Returns (from_row, from_col, to_row, to_col) or None.
        """
        color = self.current_player.color
        
        # Show board with status
        print_board(self.board, self.player1, self.player2)
        
        # Show check warning
        if self.board.is_in_check(color):
            print_message(f"⚠️  {self.current_player.name}, you are in CHECK!", "check")
        
        print(f"  🎯 {self.current_player.name}'s turn ({self.current_player.color.capitalize()})")
        print(f"  Enter move (e.g., 'e2 e4') or command (help/resign/draw):")
        
        while True:
            user_input = get_input("Move")
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input in ('resign', 'draw', 'help', 'history'):
                if self.handle_special_commands(user_input):
                    if self.game_over:
                        return None
                    print_board(self.board, self.player1, self.player2)
                    if self.board.is_in_check(color):
                        print_message(f"⚠️  {self.current_player.name}, you are in CHECK!", "check")
                    print(f"  🎯 {self.current_player.name}'s turn ({self.current_player.color.capitalize()})")
                    print(f"  Enter move (e.g., 'e2 e4') or command (help/resign/draw):")
                continue
            
            # Parse the move input
            parts = user_input.split()
            if len(parts) != 2:
                print_message("Invalid format! Use: e2 e4 (from to)", "error")
                continue
            
            from_pos = parse_position(parts[0])
            to_pos = parse_position(parts[1])
            
            if from_pos is None or to_pos is None:
                print_message("Invalid squares! Use letters a-h and numbers 1-8", "error")
                continue
            
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            
            # Validate the move
            piece = self.board.get_piece(from_row, from_col)
            
            if piece is None:
                print_message("No piece at that square!", "error")
                continue
            
            if piece.color != color:
                print_message("That's not your piece!", "error")
                continue
            
            if not self.board.is_valid_move(from_row, from_col, to_row, to_col, color):
                print_message("Invalid move! Try again.", "error")
                continue
            
            return (from_row, from_col, to_row, to_col)
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Execute a move on the board"""
        piece = self.board.get_piece(from_row, from_col)
        piece_name = piece.name
        
        # Perform the move
        captured = self.board.move_piece(from_row, from_col, to_row, to_col)
        
        # Track captured piece
        if captured:
            self.current_player.add_captured_piece(captured)
            print_message(f"{self.current_player.name} captured {captured.name}!", "success")
        
        # Record move in history
        from_notation = position_to_notation(from_row, from_col)
        to_notation = position_to_notation(to_row, to_col)
        capture_symbol = "x" if captured else "-"
        move_str = f"{self.current_player.name}: {piece_name} {from_notation}{capture_symbol}{to_notation}"
        self.move_history.append(move_str)
    
    def check_game_end(self):
        """
        Check if the game has ended.
        Returns (is_over, winner, reason)
        """
        opponent_color = self.get_other_player().color
        opponent = self.get_other_player()
        
        # Check checkmate
        if self.board.is_checkmate(opponent_color):
            return True, self.current_player, "Checkmate"
        
        # Check stalemate
        if self.board.is_stalemate(opponent_color):
            return True, None, "Stalemate - Draw"
        
        return False, None, None
    
    def play(self):
        """Main game loop"""
        self.setup_players()
        print_controls()
        input("  Press Enter to start the game...")
        
        while not self.game_over:
            # Get move from current player
            move = self.get_player_move()
            
            if self.game_over:
                break
            
            if move is None:
                continue
            
            from_row, from_col, to_row, to_col = move
            
            # Execute the move
            self.make_move(from_row, from_col, to_row, to_col)
            
            # Check if opponent is in check (show message)
            opponent_color = self.get_other_player().color
            if self.board.is_in_check(opponent_color):
                if not self.board.is_checkmate(opponent_color):
                    print_message(f"{self.get_other_player().name} is in CHECK!", "check")
                    input("  Press Enter to continue...")
            
            # Check game end conditions
            is_over, winner, reason = self.check_game_end()
            if is_over:
                print_board(self.board, self.player1, self.player2)
                if winner:
                    print_game_over(str(winner), reason)
                else:
                    print_game_over(None, reason)
                self.game_over = True
                break
            
            # Switch to other player
            self.switch_turns()
        
        # Ask to play again
        print("\n  Play again? (yes/no)")
        again = input("  ➤  ").strip().lower()
        if again in ('yes', 'y'):
            self.__init__()
            self.play()
        else:
            print("\n  Thanks for playing! Goodbye! ♟\n")
