# This whole code was written by ChatGPT :V

class ChessEngine:
    def __init__(self):
        # Create an empty chess board
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def get_board(self):
        return self.board

    def move(self, from_x, from_y, to_x, to_y):
        # Make sure the move is valid
        if not self.is_valid_move(from_x, from_y, to_x, to_y):
            return False

        # Make the move
        self.board[to_y][to_x] = self.board[from_y][from_x]
        self.board[from_y][from_x] = None
        return True

    def is_valid_move(self, from_x, from_y, to_x, to_y):
        # Make sure the move is on the board
        if from_x < 0 or from_x > 7 or to_x < 0 or to_x > 7 or from_y < 0 or from_y > 7 or to_y < 0 or to_y > 7:
            return False

        # Make sure there is a piece to move
        if self.board[from_y][from_x] is None:
            return False

        # Make sure the destination is empty or has an enemy piece
        if self.board[to_y][to_x] is not None and self.board[from_y][from_x].color == self.board[to_y][to_x].color:
            return False

        # Check piece-specific rules
        return self.board[from_y][from_x].is_valid_move(from_x, from_y, to_x, to_y)

    def get_all_valid_moves(self, color):
        # Generate a list of all valid moves for the given color
        valid_moves = []
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None and piece.color == color:
                    for move in piece.get_valid_moves():
                        if self.is_valid_move(x, y, move[0], move[1]):
                            valid_moves.append((x, y, move[0], move[1]))
        return valid_moves

    def evaluate(self):
        # Simple evaluation function: just count the number of pieces of each color
        white_score = 0
        black_score = 0
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece is not None:
                    if piece.color == "white":
                        white_score += 1
                    else:
                        black_score += 1
        return white_score - black_score

engine = ChessEngine()

# Set up the board
engine.board[0][0] = Knight("white", (0, 0))
engine.board[7][7] = Knight("black", (7, 7))

# Make a move
engine.move(0, 0, 1, 2)

# Print the board
for row in engine.get_board():
    print(row)
    
#Define each piece class

class ChessPiece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def is_valid_move(self, from_x, from_y, to_x, to_y):
        # Make sure the move is on the board
        if to_x < 0 or to_x > 7 or to_y < 0 or to_y > 7:
            return False

        # Check piece-specific rules
        return self.is_valid_move_by_piece(from_x, from_y, to_x, to_y)

    def is_valid_move_by_piece(self, from_x, from_y, to_x, to_y):
        raise NotImplementedError

class Pawn(ChessPiece):
    def get_valid_moves(self):
        x, y = self.position
        moves = []
        if self.color == "white":
            if y == 6:
                moves.append((x, y-2))
            moves.append((x, y-1))
        else:
            if y == 1:
                moves.append((x, y+2))
            moves.append((x, y+1))
        return moves

    def is_valid_move_by_piece(self, from_x, from_y, to_x, to_y):
        # Pawns can only move forward
        if self.color == "white":
            if to_y > from_y:
                return False
        else:
            if to_y < from_y:
                return False

        # Pawns can move two squares forward on their first move
        if (self.color == "white" and from_y == 6) or (self.color == "black" and from_y == 1):
            if abs(to_y - from_y) > 2:
                return False

        # Pawns can only capture diagonally
        if to_x != from_x and to_y != from_y:
            return False

        return True

class Knight(ChessPiece):
    def get_valid_moves(self):
        x, y = self.position
        moves = []
        for dx in [-2, -1, 1, 2]:
            for dy in [-2, -1, 1, 2]:
                if abs(dx) + abs(dy) == 3:
                    moves.append((x+dx, y+dy))
        return moves

    def is_valid_move_by_piece(self, from_x, from_y, to_x, to_y):
        return True

class Bishop(ChessPiece):
    def get_valid_moves(self):
        x, y = self.position
        moves = []
        for i in range(1, 8):
            moves.append((x+i, y+i))
            moves.append((x-i, y-i))
            moves.append((x-i, y+i))
            moves.append((x+i, y-i))
        return moves

    def is_valid_move_by_piece(self, from_x, from_y, to_x, to_y):
        # Bishops can only move diagonally
        if abs(to_x - from_x) != abs(to_y - from_y):
            return False
        return True