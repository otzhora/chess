import chess

from engine.value_functions import ClassicValue


class BaseEngine:
    def __init__(self, value_function=None):
        self.value_function = value_function()

    def __call__(self, board):
        raise NotImplementedError


class MinMaxEngine(BaseEngine):
    def __init__(self, value_function, max_depth):
        super(MinMaxEngine, self).__init__(value_function)
        self.max_depth = max_depth

    def __call__(self, board):
        return self.explore_tree(board)

    def explore_tree(self, board, depth=0):
        if depth >= self.max_depth or board.is_game_over():
            return self.value_function(board), None

        moves = []
        for move in board.legal_moves:
            board.push(move)
            moves.append((self.value_function(board), move))
            board.pop()

        is_maximizing = board.turn  # white is maximizing player
        if is_maximizing:
            val = self.value_function.MINVALUE
        else:
            val = self.value_function.MAXVALUE

        moves = sorted(moves, key=lambda x: x[0], reverse=is_maximizing)
        computer_move = moves[0]

        for move_val, move in moves:
            board.push(move)
            tval, _ = self.explore_tree(board, depth + 1)
            board.pop()

            if is_maximizing and tval >= val:
                val = tval
                computer_move = move
            elif not is_maximizing and tval <= val:
                val = tval
                computer_move = move

        return val, computer_move


if __name__ == "__main__":
    engine = MinMaxEngine(ClassicValue, 1)
    b = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    print(engine(b))
