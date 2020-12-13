import chess


class BaseValue:
    def __init__(self):
        self.MAXVALUE = 10000000
        self.MINVALUE = -10000000

    def __call__(self, board):
        """
        Calculate value of given engine position
        :param board: engine position
        :return: value of a position
        """
        raise NotImplementedError


class ClassicValue(BaseValue):
    def __init__(self):
        super(ClassicValue, self).__init__()

        self.piece_values = {
            'p': 1,
            'n': 3,
            'b': 3,
            'r': 5,
            'q': 9,
            'k': 500,
        }
        self.square_mul = 0.05
        self.square_values = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def __call__(self, board):
        """
        Calculate value of given engine position
        :param board: engine position
        :return: value of a position
        """
        val = 0.0

        # if the game is over
        if board.is_game_over():
            if board.result() == "1-0":
                return self.MAXVALUE
            elif board.result() == "0-1":
                return self.MINVALUE
            return 0

        # piece values
        for square, piece in board.piece_map().items():
            if piece.color == chess.WHITE:
                val += self.piece_values[piece.symbol().lower()]
            else:
                val -= self.piece_values[piece.symbol().lower()]

        # center control
        for attack_from in range(64):
            piece = board.piece_at(attack_from)

            if piece is None:
                continue

            attack_squares = board.attacks(attack_from)

            for attack_to in attack_squares:
                coord_i = attack_to // 8
                coord_j = attack_to % 8
                if piece.color:
                    val += self.square_mul * self.square_values[coord_i][coord_j]
                else:
                    val -= self.square_mul * self.square_values[coord_i][coord_j]

        # mobility
        turn = board.turn
        board.turn = chess.WHITE
        val += 0.1 * board.legal_moves.count()
        board.turn = chess.BLACK
        val -= 0.1 * board.legal_moves.count()
        board.turn = turn

        # TODO: king safety
        # TODO: piece-square table

        return val

# black checkmates: rrnb1k1nr/pppp1ppp/4p3/2b5/4P3/PP6/2PP1qPP/RNBQKBNR w KQkq - 0 5
# white cheskmates: r1bqkbnr/ppp2Qpp/2np4/4p3/2B5/4P3/PPPP1PPP/RNB1K1NR b KQkq - 0 4


if __name__ == "__main__":
    b = chess.Board("rnbqkbnr/ppp1pppp/3p4/8/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 2")
    val_function = ClassicValue()
    print(val_function(b))
