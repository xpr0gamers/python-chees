from figures import *


class ChessField():
    columns = "ABCDEFGH"

    def __init__(self):
        self.board = self._get_initial_board()

    def _get_initial_board(self):
        # board initialisieren
        board = [[None for rows in range(0, 8)] for columns in range(0, 8)]

        # Computer
        board[0][0] = Rook(True, self)
        board[0][1] = Knight(True, self)
        board[0][2] = Bishop(True, self)
        board[0][3] = Queen(True, self)
        board[0][4] = King(True, self)
        board[0][5] = Bishop(True, self)
        board[0][6] = Knight(True, self)
        board[0][7] = Rook(True, self)

        # Spieler
        board[7][0] = Rook(False, self)
        board[7][1] = Knight(False, self)
        board[7][2] = Bishop(False, self)
        board[7][3] = Queen(False, self)
        board[7][4] = King(False, self)
        board[7][5] = Bishop(False, self)
        board[7][6] = Knight(False, self)
        board[7][7] = Rook(False, self)

        # Bauern aufstellen
        for index in range(0, 8):
            board[1][index] = Pawn(True, self)
            board[6][index] = Pawn(False, self)
        return board

    def get_figure_at_position(self, position):
        try:
            return self.board[position[0]][position[1]]
        except:
            return None

    # gibt den gewinner zurück 0=Untentschieden, 1=Computer, -1=Spieler, None noch keiner
    def get_winner(self):
        score = self.get_current_board_score()
        if score == float("inf"):
            return 1
        elif score == float("-inf"):
            return -1
        elif score is None:
            return 0
        else:
            return None

    def get_current_board_score(self):
        score = 0
        all_figures = []
        queen_figures = []
        for row in self.board:
            for figure in row:
                if figure is None:
                    continue
                all_figures.append(figure)
                if figure.is_white is True:
                    score += figure.MATERIALSCORE
                else:
                    score -= figure.MATERIALSCORE

                if isinstance(figure, Queen):
                    queen_figures.append(figure)

        queen_white = list(filter(lambda figure: figure.is_white is True, queen_figures))
        queen_black = list(filter(lambda figure: figure.is_white is False, queen_figures))

        if len(queen_white) != 1:
            # computer hat verloren
            return float('-inf')
        elif len(queen_black) != 1:
            # computer hat gewonnen
            return float('inf')
        elif len(all_figures) == 2:
            return None
        else:
            return score

    def move_figure_to_position_without_check(self, position_current, position_target):
        figure_current = self.get_figure_at_position(position_current)
        self.board[position_current[0]][position_current[1]] = None
        self.board[position_target[0]][position_target[1]] = figure_current

    def move_figure_to_position(self, position_current, position_target, is_white):
        figure_current = self.get_figure_at_position(position_current)
        figure_target = self.get_figure_at_position(position_target)
        if figure_current is None:
            raise BaseException("Ungültige Position, an der ausgewählten Stelle befindet sich keine Figur")
        elif figure_current.is_white is not is_white:
            raise BaseException("Es dürfen nur eigene Figuren bewegt werden")
        elif figure_target is not None and figure_target.is_white == is_white:
            raise BaseException("Die ausgewählte Postion ist bereits mit einer eigenen Figur besetzt")
        if not figure_current.is_valid_move(position_current, position_target):
            raise BaseException("Ungültiger Schachzug")

        # alles ok, figur setzen
        self.board[position_current[0]][position_current[1]] = None
        self.board[position_target[0]][position_target[1]] = figure_current

        if figure_target is not None:
            print("Die Figur {} wurde geworfen".format(figure_target.get_zeichen()))

    def convert_coordinates_to_input(self, coordinates):
        column = self.columns[coordinates[1]]
        row = coordinates[0] + 1
        return column + "" + str(row)

    def convert_input_to_coordinates(self, input):
        positions = input.upper().split(" ")
        if len(positions) != 2:
            raise ValueError("Ungültige Eingabe. Beispiel: A2 A3")
        try:
            index_column_1 = self.columns.index(positions[0][0])
            index_column_2 = self.columns.index(positions[1][0])
        except:
            raise ValueError("Ungültige Spalteneingabe. Spalte außerhalb des gültigen Bereichs")

        try:
            index_row_1 = int(positions[0][1])
            index_row_2 = int(positions[1][1])
        except BaseException:
            raise BaseException("Ungültige Eingabe. Als Zeilenangabe darf nur eine Zahl eingegeben werden")
        index_row_1 = index_row_1 - 1
        index_row_2 = index_row_2 - 1

        if not index_row_1 in range(0, 8) or not index_row_2 in range(0, 8):
            raise BaseException("Ungültige Eingabe. Die Zeilenangabe ist falsch")
        return ((index_row_1, index_column_1), (index_row_2, index_column_2))

    def draw_field(self):
        for index_row, row in enumerate(self.board):
            # Bei der ersten Zeile die Zeilenbezeichnung mit ausgeben
            if index_row == 0:
                line_head = ' '
                for head in range(0, 8):
                    line_head += ' ' + self.columns[head]
                print(line_head)

            line = ''
            for index_column, value in enumerate(row):
                if index_column == 0:
                    line += str(index_row + 1)
                if value is not None:
                    line += ' ' + value.get_zeichen()
                else:
                    line += ' ' + '_'
            print(line)
        print("\n")

    def get_possible_moves(self, is_white):
        # alle möglichen züge zurückgeben
        possible_moves = []
        for index_row in range(0, len(self.board)):
            for index_column in range(0, len(self.board)):
                figure = self.board[index_row][index_column]
                if figure is not None and figure.is_white is is_white:
                    for move in figure.get_moves((index_row, index_column)):
                        possible_moves.append([(index_row, index_column), move])

        return possible_moves
