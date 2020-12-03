import minimax as mima
from chessfield import ChessField


def get_player_input():
    # Die weißen figuren gehören zum Computer

    print("Eingabe in Form von SpalteZeile SpalteZeile. Beispiel A7 A6")
    cheesfield = ChessField()
    cheesfield.draw_field()
    minimax = mima.MiniMax(cheesfield)
    need_input = True

    while need_input:
        raw_input = input('Please make your move ')

        try:
            coordinates = cheesfield.convert_input_to_coordinates(raw_input)
            cheesfield.move_figure_to_position(coordinates[0], coordinates[1], False)
        except BaseException as e:
            print(str(e))
            continue

        winner = cheesfield.get_winner()
        if winner is None:
            minimax.compute()
            winner = cheesfield.get_winner()

        cheesfield.draw_field()
        if winner is not None:
            output_winner(winner)


def output_winner(winner):
    if winner == -1:
        print("Spieler hat gewonnen!")
    elif winner == 0:
        print("Unentschieden!")
    elif winner == 1:
        print("Computer hat gewonnen, Schach!")


def main():
    get_player_input()


if __name__ == "__main__":
    main()
