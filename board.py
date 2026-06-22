# board.py - Chess Board Setup and State Management

from pieces import Pawn, Rook, Knight, Bishop, Queen, King
import copy


class Board:
    """Chess board - manages piece positions and move validation"""
    
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
    
    def setup_board(self):
        """Place all pieces in their starting positions"""
        
        # Black pieces (top - rows 0 and 1)
        self.grid[0] = [
            Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
            King('black'), Bishop('black'), Knight('black'), Rook('black')
        ]
        self.grid[1] = [Pawn('black') for _ in range(8)]
        
        # Empty rows (middle)
        for row in range(2, 6):
            self.grid[row] = [None for _ in range(8)]
        
        # White pieces (bottom - rows 6 and 7)
        self.grid[6] = [Pawn('white') for _ in range(8)]
        self.grid[7] = [
            Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
            King('white'), Bishop('white'), Knight('white'), Rook('white')
        ]
    
    def get_piece(self, row, col):
        """Get piece at given position"""
        return self.grid[row][col]
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece and return captured piece if any"""
        piece = self.grid[from_row][from_col]
        captured = self.grid[to_row][to_col]
        
        # Perform the move
        self.grid[to_row][to_col] = piece
        self.grid[from_row][from_col] = None
        piece.has_moved = True
        
        # Pawn promotion - auto promote to Queen
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_row == 0) or \
               (piece.color == 'black' and to_row == 7):
                self.grid[to_row][to_col] = Queen(piece.color)
                print(f"\n🎉 Pawn promoted to Queen!")
        
        return captured
    
    def find_king(self, color):
        """Find the King's position for given color"""
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None
    
    def is_in_check(self, color):
        """Check if the given color's king is in check"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        opponent = 'black' if color == 'white' else 'white'
        king_row, king_col = king_pos
        
        # Check if any opponent piece can capture the king
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == opponent:
                    moves = piece.get_valid_moves(row, col, self.grid)
                    if (king_row, king_col) in moves:
                        return True
        return False
    
    def is_valid_move(self, from_row, from_col, to_row, to_col, color):
        """Check if a move is valid (doesn't leave king in check)"""
        piece = self.grid[from_row][from_col]
        
        # Must have a piece to move
        if piece is None:
            return False
        
        # Must be player's own piece
        if piece.color != color:
            return False
        
        # Check if destination is in piece's valid moves
        valid_moves = piece.get_valid_moves(from_row, from_col, self.grid)
        if (to_row, to_col) not in valid_moves:
            return False
        
        # Simulate the move and check if king is in check
        temp_board = copy.deepcopy(self)
        temp_board.grid[to_row][to_col] = temp_board.grid[from_row][from_col]
        temp_board.grid[from_row][from_col] = None
        
        if temp_board.is_in_check(color):
            return False
        
        return True
    
    def get_all_valid_moves(self, color):
        """Get all valid moves for a given color"""
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    for to_row, to_col in piece.get_valid_moves(row, col, self.grid):
                        if self.is_valid_move(row, col, to_row, to_col, color):
                            all_moves.append((row, col, to_row, to_col))
        return all_moves
    
    def is_checkmate(self, color):
        """Check if given color is in checkmate"""
        if not self.is_in_check(color):
            return False
        return len(self.get_all_valid_moves(color)) == 0
    
    def is_stalemate(self, color):
        """Check if given color is in stalemate"""
        if self.is_in_check(color):
            return False
        return len(self.get_all_valid_moves(color)) == 0
