"""Main script to launch LeCopain"""


import argparse

from guesswho import GuessWho

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Main", description="Main script to launch the different games"
    )
    parser.add_argument("-g", "--game")
    args = parser.parse_args()

    if args["game"] == "guesswho":
        game = GuessWho(ai_player=True)
        game.launch()

    else:
        print("Game is not recognized")
