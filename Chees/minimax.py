class MiniMax:
    MAX_DEPTH = 3

    def __init__(self, cheesfield, max_depth=MAX_DEPTH):
        self.cheesfield = cheesfield
        self.max_depth = max_depth

    def compute(self):
        #hätte man auch mit der negamax variante machen können
        #hätte doppeltes conding erspart, aber übersichtlicher und verständlicher ist diese variante
        best_result = self.max(float("-inf"), float("inf"), self.max_depth)

        output_from = self.cheesfield.convert_coordinates_to_input(best_result[0])
        output_to = self.cheesfield.convert_coordinates_to_input(best_result[1])
        print("Computer fährt von {} nach {}".format(output_from, output_to))
        self.cheesfield.move_figure_to_position(best_result[0], best_result[1], True)

    def max(self, alpha, beta, depth):
        winner = self.cheesfield.get_current_board_score()
        if depth == 0 or winner is None or winner == float('-inf') or winner == float('inf'):
            return winner

        best_move = None
        max_score = alpha
        for move in self.cheesfield.get_possible_moves(True):
            figure_target = self.cheesfield.get_figure_at_position(move[1])
            self.cheesfield.move_figure_to_position_without_check(move[0], move[1])
            score = self.min(max_score, beta, depth - 1)
            # undo
            self.cheesfield.board[move[0][0]][move[0][1]] = self.cheesfield.board[move[1][0]][move[1][1]]
            self.cheesfield.board[move[1][0]][move[1][1]] = figure_target

            if score > max_score:
                if depth == self.MAX_DEPTH:
                    best_move = move
                max_score = score
                if max_score >= beta:
                    break

        #wenn max für den root knoten durchgeführt wurde, des besten zug zurückgeben
        if depth == self.MAX_DEPTH:
            return best_move
        else:
            return max_score

    def min(self, alpha, beta, depth):
        winner = self.cheesfield.get_current_board_score()
        if depth == 0 or winner is None or winner == float('-inf') or winner == float('inf'):
            return winner

        min_score = beta
        for move in self.cheesfield.get_possible_moves(True):
            figure_target = self.cheesfield.get_figure_at_position(move[1])
            self.cheesfield.move_figure_to_position_without_check(move[0], move[1])
            score = self.max(alpha, min_score, depth - 1)
            # undo
            self.cheesfield.board[move[0][0]][move[0][1]] = self.cheesfield.board[move[1][0]][move[1][1]]
            self.cheesfield.board[move[1][0]][move[1][1]] = figure_target

            if score < min_score:
                min_score = score
                if min_score <= alpha:
                    break

        return min_score
