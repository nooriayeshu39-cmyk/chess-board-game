# player.py - Player Class

class Player:
    """Represents a chess player"""
    
    def __init__(self, name, color):
        self.name = name          # Player's name
        self.color = color        # 'white' or 'black'
        self.captured_pieces = [] # List of captured pieces
    
    def add_captured_piece(self, piece):
        """Add a captured piece to player's collection"""
        self.captured_pieces.append(piece)
    
    def get_captured_display(self):
        """Return string of captured pieces"""
        if not self.captured_pieces:
            return "None"
        return ' '.join(str(p) for p in self.captured_pieces)
    
    def __str__(self):
        return f"{self.name} ({self.color.capitalize()})"
