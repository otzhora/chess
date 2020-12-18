import chess

from engine.value_functions import ClassicValue


class BaseEngine:
    def __init__(self, value_function=None):
        self.value_function = value_function()

    def __call__(self, board):
        raise NotImplementedError


class MinMaxEngine(BaseEngine):
    def __init__(self, value_function, max_depth, beam_search=True):
        super(MinMaxEngine, self).__init__(value_function)
        self.max_depth = max_depth
        self.nodes_explored = 0
        self.beam_search = beam_search
        self.seen_positions = {}

    def __call__(self, board):
        self.nodes_explored = 0
        return self.explore_tree(board)

    def explore_tree(self, board, depth=0, alpha=None, beta=None):

        if alpha is None:
            alpha = self.value_function.MINVALUE
        if beta is None:
            beta = self.value_function.MAXVALUE

        self.nodes_explored += 1
        if depth >= self.max_depth or board.is_game_over():
            return self.value_function(board), None

        legal_moves = self.seen_positions.get(board.fen(), list(board.legal_moves))
        moves = []
        for move in legal_moves:
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

        # beam search
        if self.beam_search and depth >= 3:
            moves = moves[:10]

        for move_val, move in moves:
            board.push(move)
            tval, _ = self.explore_tree(board, depth + 1, alpha, beta)
            board.pop()

            if is_maximizing and tval >= val:
                val = tval
                computer_move = move
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            elif not is_maximizing and tval <= val:
                val = tval
                computer_move = move
                beta = min(beta, val)
                if beta <= alpha:
                    break

        return val, computer_move


if __name__ == "__main__":
    engine = MinMaxEngine(ClassicValue, 1)
    b = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    print(engine(b))
