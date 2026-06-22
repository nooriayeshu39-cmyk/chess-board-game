# pieces.py - All Chess Pieces and their Movement Rules

class Piece:
    """Base class for all chess pieces"""
    
    def __init__(self, color, symbol, name):
        self.color = color        # 'white' or 'black'
        self.symbol = symbol      # Unicode chess symbol
        self.name = name          # Piece name
        self.has_moved = False    # For castling and pawn double move
    
    def __str__(self):
        return self.symbol
    
    def get_valid_moves(self, row, col, board):
        """Override in each subclass"""
        raise NotImplementedError
    
    def is_within_bounds(self, row, col):
        """Check if position is on the board"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_moves_in_direction(self, row, col, board, directions):
        """Get all valid moves in given directions (for sliding pieces)"""
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.is_within_bounds(r, c):
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))  # Can capture
                    break
                else:
                    break  # Blocked by own piece
                r += dr
                c += dc
        return moves


class Pawn(Piece):
    """Pawn - moves forward, captures diagonally"""
    
    def __init__(self, color):
        symbol = '♙' if color == 'white' else '♟'
        super().__init__(color, symbol, 'Pawn')
    
    def get_valid_moves(self, row, col, board):
        moves = []
        # White moves up (decreasing row), Black moves down (increasing row)
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        
        # Move forward one square
        new_row = row + direction
        if self.is_within_bounds(new_row, col) and board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Move forward two squares from starting position
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))
        
        # Diagonal captures
        for dc in [-1, 1]:
            new_col = col + dc
            if self.is_within_bounds(new_row, new_col):
                target = board[new_row][new_col]
                if target is not None and target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves


class Rook(Piece):
    """Rook - moves horizontally and vertically"""
    
    def __init__(self, color):
        symbol = '♖' if color == 'white' else '♜'
        super().__init__(color, symbol, 'Rook')
    
    def get_valid_moves(self, row, col, board):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return self.get_moves_in_direction(row, col, board, directions)


class Knight(Piece):
    """Knight - moves in L-shape, can jump over pieces"""
    
    def __init__(self, color):
        symbol = '♘' if color == 'white' else '♞'
        super().__init__(color, symbol, 'Knight')
    
    def get_valid_moves(self, row, col, board):
        moves = []
        # All 8 possible L-shape moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2),  (1, 2),  (2, -1),  (2, 1)
        ]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_within_bounds(new_row, new_col):
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        return moves


class Bishop(Piece):
    """Bishop - moves diagonally"""
    
    def __init__(self, color):
        symbol = '♗' if color == 'white' else '♝'
        super().__init__(color, symbol, 'Bishop')
    
    def get_valid_moves(self, row, col, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.get_moves_in_direction(row, col, board, directions)


class Queen(Piece):
    """Queen - moves horizontally, vertically, and diagonally"""
    
    def __init__(self, color):
        symbol = '♕' if color == 'white' else '♛'
        super().__init__(color, symbol, 'Queen')
    
    def get_valid_moves(self, row, col, board):
        # Combines Rook and Bishop movements
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),   # Rook directions
            (-1, -1), (-1, 1), (1, -1), (1, 1)    # Bishop directions
        ]
        return self.get_moves_in_direction(row, col, board, directions)


class King(Piece):
    """King - moves one square in any direction"""
    
    def __init__(self, color):
        symbol = '♔' if color == 'white' else '♚'
        super().__init__(color, symbol, 'King')
    
    def get_valid_moves(self, row, col, board):
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0,  -1),           (0,  1),
            (1,  -1), (1,  0), (1,  1)
        ]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_within_bounds(new_row, new_col):
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        return moves
