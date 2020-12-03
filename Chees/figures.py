class Figur():
    ZEICHEN = None
    MATERIALSCORE = None

    def __init__(self, is_white, cheesfield):
        self.is_white = is_white  # Computer ist hier der weisse Spieler
        self.cheesfield = cheesfield

    # liefert alle möglichen züge einer figur
    def get_moves(self, position):
        pass

    # liefert alle möglichen horizontalen züge ausgehender der position einer figur
    def get_horizontal_moves(self, position):
        result = []
        # horizontal fahren lassen nach rechts
        for column in range(position[1] + 1, len(self.cheesfield.board), 1):
            figure_target = self.cheesfield.get_figure_at_position((position[0], column))
            if figure_target is None:
                result.append((position[0], column))
            elif figure_target.is_white is not self.is_white:
                result.append((position[0], column))
                break
            else:
                # eigene Figur steht im weg
                break

        # horizontal fahren lassen nach links
        for column in range(position[1] - 1, 0, -1):
            figure_target = self.cheesfield.get_figure_at_position((position[0], column))
            if figure_target is None:
                result.append((position[0], column))
            elif figure_target.is_white is not self.is_white:
                result.append((position[0], column))
                break
            else:
                # eigene Figur steht im weg
                break
        return result

    # liefert alle möglichen vertikalen züge ausgehender der position einer figur
    def get_vertical_moves(self, position):
        result = []
        # vertikal fahren lassen nach unten
        for row in range(position[0] + 1, len(self.cheesfield.board), 1):
            figure_target = self.cheesfield.get_figure_at_position((row, position[1]))
            if figure_target is None:
                result.append((row, position[1]))
            elif figure_target.is_white is not self.is_white:
                result.append((row, position[1]))
                break
            else:
                # eigene Figur steht im weg
                break

        # vertikal fahren lassen nach oben
        for row in range(position[0] - 1, 0, -1):
            figure_target = self.cheesfield.get_figure_at_position((row, position[1]))
            if figure_target is None:
                result.append((row, position[1]))
            elif figure_target.is_white is not self.is_white:
                result.append((row, position[1]))
                break
            else:
                # eigene Figur steht im weg
                break
        return result

    def get_diagonal_moves(self, position):
        def get_diagonal_moves_inner(row_offset, column_offset):
            result = []
            position_target = [position[0] + row_offset, position[1] + column_offset]
            while True:
                if not position_target[0] in range(0, len(self.cheesfield.board)):
                    break
                elif not position_target[1] in range(0, len(self.cheesfield.board)):
                    break

                figure_target = self.cheesfield.get_figure_at_position((position_target[0], position_target[1]))
                if figure_target is None:
                    result.append((position_target[0], position_target[1]))
                    position_target[0] = position_target[0] + row_offset
                    position_target[1] = position_target[1] + column_offset
                elif figure_target.is_white is not self.is_white:
                    result.append((position_target[0], position_target[1]))
                    break
                else:
                    # eigene Figur steht im weg
                    break
            return result

        result = get_diagonal_moves_inner(1, 1)
        result += get_diagonal_moves_inner(1, -1)
        result += get_diagonal_moves_inner(-1, 1)
        result += get_diagonal_moves_inner(-1, -1)
        return result

    def get_zeichen(self):
        if self.is_white:
            return self.ZEICHEN
        else:
            return self.ZEICHEN.lower()

    def is_valid_move(self, position_current, position_target):
        moves = self.get_moves(position_current)
        # check if position target is in possible moves
        return position_target in moves


# Königin
class Queen(Figur):
    ZEICHEN = "D"
    MATERIALSCORE = 1000

    def __init__(self, is_white, cheesfield):
        super(Queen, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        horizontal_moves = self.get_horizontal_moves(position)
        vertical_moves = self.get_vertical_moves(position)
        diagonal_moves = self.get_diagonal_moves(position)
        result = []
        for move in horizontal_moves:
            result.append(move)
        for move in vertical_moves:
            result.append(move)
        for move in diagonal_moves:
            result.append(move)
        return result


# König
class King(Figur):
    ZEICHEN = "K"
    MATERIALSCORE = 500

    def __init__(self, is_white, cheesfield):
        super(King, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        result = []
        possible_vectors = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for possible_vector in possible_vectors:
            position_to_check = (position[0] + possible_vector[0], position[1] + possible_vector[1])
            if not position_to_check[0] in range(0, len(self.cheesfield.board)):
                continue
            elif not position_to_check[1] in range(0, len(self.cheesfield.board)):
                continue
            figur = self.cheesfield.get_figure_at_position(position_to_check)
            if figur is None or figur.is_white is not self.is_white:
                result.append(position_to_check)
        return result


# Turm
class Rook(Figur):
    ZEICHEN = "T"
    MATERIALSCORE = 500

    def __init__(self, is_white, cheesfield):
        super(Rook, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        horizontal_moves = self.get_horizontal_moves(position)
        vertical_moves = self.get_vertical_moves(position)
        return horizontal_moves + vertical_moves


# Läufer
class Bishop(Figur):
    ZEICHEN = "L"
    MATERIALSCORE = 300

    def __init__(self, is_white, cheesfield):
        super(Bishop, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        return self.get_diagonal_moves(position)


# Springer
class Knight(Figur):
    ZEICHEN = "S"
    MATERIALSCORE = 300

    def __init__(self, is_white, cheesfield):
        super(Knight, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        # der springer darf von seinen aktuellen standort immer:
        # zwei nach unten, eins nach rechts/links
        # eins nach unten, zwei nach rechts/links
        result = []
        possible_vectors = [(2, -1), (2, 1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, -2), (-1, 2)]

        for possible_vector in possible_vectors:
            position_to_check = (position[0] + possible_vector[0], position[1] + possible_vector[1])
            if not position_to_check[0] in range(0, len(self.cheesfield.board)):
                continue
            elif not position_to_check[1] in range(0, len(self.cheesfield.board)):
                continue
            figur = self.cheesfield.get_figure_at_position(position_to_check)
            if figur is None or figur.is_white is not self.is_white:
                result.append(position_to_check)
        return result


# Bauer
class Pawn(Figur):
    ZEICHEN = "B"
    MATERIALSCORE = 100

    def __init__(self, is_white, cheesfield):
        super(Pawn, self).__init__(is_white, cheesfield)

    def get_moves(self, position):
        result = []
        negieren = 1 if self.is_white else -1

        # grundstellung der bauern
        figure_current_position = self.cheesfield.get_figure_at_position(position)
        if figure_current_position.is_white is True and position[0] == 1:
            # beim ersten zug darf bauer zwei nach vorne, wenn nichts im weg steht
            if self.cheesfield.get_figure_at_position((position[0] + 2, position[1])) is None \
                    and self.cheesfield.get_figure_at_position((position[0] + 1, position[1])) is None:
                result.append((position[0] + 2, position[1]))
        elif figure_current_position.is_white is False and position[0] == 6:
            # beim ersten zug darf bauer zwei nach vorne, wenn nichts im weg steht
            if self.cheesfield.get_figure_at_position((position[0] - 2, position[1])) is None \
                    and self.cheesfield.get_figure_at_position((position[0] - 1, position[1])) is None:
                result.append((position[0] - 2, position[1]))

        # keine Grundstellung der bauern
        if position[1] in range(1, len(self.cheesfield.board)):
            # Bauer darf auch seitlich nach links fahren, wenn eine Figur geschmissen wird
            figur_diagonal = self.cheesfield.get_figure_at_position((position[0] + 1 * negieren, position[1] - 1))
            if figur_diagonal is not None and figur_diagonal.is_white is not self.is_white:
                result.append((position[0] + 1 * negieren, position[1] - 1))
        if position[1] in range(0, 6):
            # Bauer darf auch seitlich nach rechts fahren, wenn eine Figur geschmissen wird
            figur_diagonal = self.cheesfield.get_figure_at_position((position[0] + 1 * negieren, position[1] + 1))
            if figur_diagonal is not None and figur_diagonal.is_white is not self.is_white:
                result.append((position[0] + 1 * negieren, position[1] + 1))

        # bauer darf immer nach vorne, wenn keiner geschmissen wird
        if self.cheesfield.get_figure_at_position((position[0] + 1 * negieren, position[1])) is None:
            result.append((position[0] + 1 * negieren, position[1]))

        return result
