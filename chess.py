import os
import string

os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console 

class ChessPiece:
    def __init__(self, symbol, is_white):
        self.symbol = symbol
        self.is_white = is_white
        self.has_moved = False
        
    def __str__(self):
        return self.symbol

class Board:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn_count = 1  # Starts at 1 for the first turn
        
    def initialize_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        white_pieces = ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
        black_pieces = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]

        for i in range(8):
            board[0][i] = ChessPiece(white_pieces[i], True)
            board[7][i] = ChessPiece(black_pieces[i], False)
            board[1][i] = ChessPiece("♙", True)
            board[6][i] = ChessPiece("♟", False)

        return board

    def __str__(self):
        board_str = "  a b c d e f g h\n"
        for i, row in enumerate(self.board):
            board_str += f"{8 - i} "
            for cell in row:
                if cell is None:
                    board_str += "+ "
                else:
                    board_str += str(cell) + " "
            board_str += f"{8 - i}\n"
        board_str += "  a b c d e f g h"

        return board_str

    def move_piece(self, start, end, promotion=None):
        if not self.is_valid_move(start, end):
            return
        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        if promotion is not None:
            if isinstance(self.board[end[0]][end[1]], Pawn) and (end[0] == 0 or end[0] == 7):
                self.board[end[0]][end[1]] = promotion

        return True

        if piece.symbol.lower() == '♔' and not piece.has_moved:
            if (start == "e1" and end == "g1") or (start == "e8" and end == "g8"):  # King-side castling
                rook_start = (start_x, start_y + 3)
                rook_end = (start_x, start_y + 1)
            elif (start == "e1" and end == "c1") or (start == "e8" and end == "c8"):  # Queen-side castling
                rook_start = (start_x, start_y - 4)
                rook_end = (start_x, start_y - 1)
            else:
                return False

            if self.is_valid_castling_move((start_x, start_y), (end_x, end_y), rook_start, rook_end):
                self.board[end_x][end_y] = piece
                self.board[start_x][start_y] = None
                piece.has_moved = True

                rook = self.board[rook_start[0]][rook_start[1]]
                self.board[rook_end[0]][rook_end[1]] = rook
                self.board[rook_start[0]][rook_start[1]] = None
                rook.has_moved = True

                return True

        return False

    def parse_notation(self, notation):
        col = string.ascii_lowercase.index(notation[0])
        row = 8 - int(notation[1])
        return row, col

        def is_valid_move(self, piece, start, end):
            piece_type = piece.symbol.lower()
            target_piece = self.board[end[0]][end[1]]
            if target_piece is not None and piece.is_white == target_piece.is_white:
                return False

            if piece_type == '♙' or piece_type == '♟':
                return self.is_valid_pawn_move(piece, start, end, target_piece)
            elif piece_type == '♖' or piece_type == '♜':
                return self.is_valid_rook_move(start, end)
            elif piece_type == '♘' or piece_type == '♞':
                return self.is_valid_knight_move(start, end)
            elif piece_type == '♗' or piece_type == '♝':
                return self.is_valid_bishop_move(start, end)
            elif piece_type == '♕' or piece_type == '♛':
                return self.is_valid_queen_move(start, end)
            elif piece_type == '♔' or piece_type == '♚':
                return self.is_valid_king_move(start, end)
            return False
        
    def is_valid_pawn_move(self, piece, start, end, target_piece):
        start_x, start_y = start
        end_x, end_y = end
        direction = 1 if piece.is_white else -1

        if start_y == end_y and end_x == start_x + direction and target_piece is None:
            return True
        if abs(start_y - end_y) == 1 and end_x == start_x + direction and target_piece is not None:
            return True
        return False

    def is_valid_rook_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        target_piece = self.board[end_x][end_y]

        if start_x != end_x and start_y != end_y:
            return False

        dx, dy = end_x - start_x, end_y - start_y
        steps = abs(dx) if dx != 0 else abs(dy)

        for i in range(1, steps):
            x = start_x + i * dx // steps
            y = start_y + i * dy // steps
            if self.board[x][y] is not None:
                return False

        return True
        
    def is_valid_knight_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        dx, dy = abs(start_x - end_x), abs(start_y - end_y)
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return True

        return False

    def is_valid_bishop_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        if abs(start_x - end_x) != abs(start_y - end_y):
            return False

        dx = 1 if end_x > start_x else -1
        dy = 1 if end_y > start_y else -1

        x, y = start_x + dx, start_y + dy
        while x != end_x and y != end_y:
            if self.board[x][y] is not None:
                return False
            x += dx
            y += dy

        return True

    def is_valid_queen_move(self, start, end):
        return self.is_valid_rook_move(start, end) or self.is_valid_bishop_move(start, end)

    def is_valid_king_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        dx, dy = abs(start_x - end_x), abs(start_y - end_y)
        if dx <= 1 and dy <= 1:
            return True

        # Check for castling move
        if not self.board[start_x][start_y].has_moved and dy == 2:
            if dx != 0:
                return False

            if end_y > start_y:  # King-side castling
                rook = self.board[start_x][7]
                if rook is None or rook.symbol != '♜' or rook.has_moved:
                    return False

                for y in range(start_y + 1, end_y):
                    if self.board[start_x][y] is not None:
                        return False

                return True

            else:  # Queen-side castling
                rook = self.board[start_x][0]
                if rook is None or rook.symbol != '♜' or rook.has_moved:
                    return False

                for y in range(start_y - 1, end_y, -1):
                    if self.board[start_x][y] is not None:
                        return False

                return True

    def is_valid_castling_move(self, king_start, king_end, rook_start, rook_end):
        king = self.board[king_start[0]][king_start[1]]
        rook = self.board[rook_start[0]][rook_start[1]]

        if king is None or rook is None:
            return False

        if king.symbol.lower() != '♔' or rook.symbol.lower() not in ('♖', '♜'):
            return False

        if king.has_moved or rook.has_moved:
            return False

        if not self.is_valid_king_move(king_start, king_end) or not self.is_valid_rook_move(rook_start, rook_end):
            return False

        # Ensure there are no pieces between the king and rook
        start_col, end_col = sorted((king_start[1], rook_start[1]))
        for col in range(start_col + 1, end_col):
            if self.board[king_start[0]][col] is not None:
                return False

    # Perform castling move
        if king_start == (7, 4) and king_end == (7, 6):
            self.castle((7, 4), (7, 6))
        elif king_start == (7, 4) and king_end == (7, 2):
            self.castle((7, 4), (7, 2))
        elif king_start == (0, 4) and king_end == (0, 6):
            self.castle((0, 4), (0, 6))
        elif king_start == (0, 4) and king_end == (0, 2):
            self.castle((0, 4), (0, 2))

        return True


    def castle(self, king_start, king_end):
        row = king_start[0]
        if king_start[1] < king_end[1]:  # Kingside castling
            rook_start = (row, 7)
            rook_end = (row, king_end[1] - 1)
        else:  # Queenside castling
            rook_start = (row, 0)
            rook_end = (row, king_end[1] + 1)

        king = self.board[king_start[0]][king_start[1]]
        rook = self.board[rook_start[0]][rook_start[1]]

        self.board[king_end[0]][king_end[1]] = king
        self.board[king_start[0]][king_start[1]] = None
        self.board[rook_end[0]][rook_end[1]] = rook
        self.board[rook_start[0]][rook_start[1]] = None

        king.move(king_end)
        rook.move(rook_end)

    def is_check(self, board, king_color):
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == king_color and isinstance(piece, King):
                    king_position = (row, col)
                    break
            if king_position:
                break

        opponent_color = 'white' if king_color == 'black' else 'black'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == opponent_color:
                    if king_position in piece.get_valid_moves(board, (row, col)):
                        return True
        return False

    def is_checkmate(self, board, king_color):
        if not self.is_check(board, king_color):
            return False

        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == king_color:
                    for move in piece.get_valid_moves(board, (row, col)):
                        board_copy = copy.deepcopy(board)
                        move_piece(board_copy, (row, col), move)
                        if not self.is_check(board_copy, king_color):
                            return False
        return True



# Main loop
if __name__ == "__main__":
    board = Board()
    print(board)

    while True:
        try:
            move = input("Enter your move: ")
            if board.move_piece(move):
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console
                print(board)
            else:
                print("Invalid move")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
