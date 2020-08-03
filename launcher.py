from go import game_manager
from go import rulebooks

def main():
    game = game_manager.Game(number_of_players=2, size=13, rulebook=rulebooks.Standard())
    game.start()


if __name__ == "__main__":
    main()
