# main.py - Entry Point for Python Chess Game

from game import Game


def main():
    """Start the chess game"""
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Goodbye! ♟\n")


if __name__ == "__main__":
    main()
