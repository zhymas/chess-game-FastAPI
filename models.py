from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db import save_match_result, close_db_connection
from datetime import datetime

class Piece(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def move(self, position_from, position_to):
        pass


class King(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        if abs(x2 - x1) <= 1 and abs(y2 - y1) <= 1:
            return True
        return False


class Rook(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        if x1 == x2 or y1 == y2:
            return True
        return False


class Knight(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)


class Pawn(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        if (x2 == x1 + 1 or (x2 == x1 + 2 and x1 == 1)) and y2 == y1:
            return True
        elif x2 == x1 + 1 and abs(y2 - y1) == 1:
            return True
        return False


class Bishop(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        return abs(x2 - x1) == abs(y2 - y1)


class Queen(Piece):
    def move(self, position_from, position_to):
        x1, y1 = position_from
        x2, y2 = position_to
        return (x1 == x2 or y1 == y2 or abs(x2 - x1) == abs(y2 - y1))


class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self.init_starting_position()

    def place_piece(self, piece, position):
        x, y = position
        if 0 <= x < 8 and 0 <= y < 8:
            self.board[x][y] = piece
        else:
            print("Недійсні координати для розміщення фігури на дошці")

    def remove_piece(self, position):
        x, y = position
        if 0 <= x < 8 and 0 <= y < 8:
            self.board[x][y] = None
        else:
            print("Недійсні координати для видалення фігури з дошки")

    def init_starting_position(self):
        self.place_piece(Rook("Rook"), (0, 0))
        self.place_piece(Knight("Knight"), (0, 1))
        self.place_piece(Bishop("Bishop"), (0, 2))
        self.place_piece(Queen("Queen"), (0, 3))
        self.place_piece(King("King"), (0, 4))
        self.place_piece(Bishop("Bishop"), (0, 5))
        self.place_piece(Knight("Knight"), (0, 6))
        self.place_piece(Rook("Rook"), (0, 7))
        for i in range(8):
            self.place_piece(Pawn("Pawn"), (1, i))

        self.place_piece(Rook("Rook"), (7, 0))
        self.place_piece(Knight("Knight"), (7, 1))
        self.place_piece(Bishop("Bishop"), (7, 2))
        self.place_piece(Queen("Queen"), (7, 3))
        self.place_piece(King("King"), (7, 4))
        self.place_piece(Bishop("Bishop"), (7, 5))
        self.place_piece(Knight("Knight"), (7, 6))
        self.place_piece(Rook("Rook"), (7, 7))
        for i in range(8):
            self.place_piece(Pawn("Pawn"), (6, i))


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = Board()

    def start_game(self):
        self.board.init_starting_position()

    def move(self, player, position_from, position_to):
        piece = self.board.board[position_from[0]][position_from[1]]

        if not piece:
            print("Invalid move: You cannot move your opponent's piece or an empty square.")
            return False

        if not piece.move(position_from, position_to):
            print("Invalid move:", piece.__class__.__name__, "cannot move to that position.")
            return False
        captured_piece = self.board.board[position_to[0]][position_to[1]]
        if captured_piece and captured_piece.color != player:
            self.board.remove_piece(position_to)

        self.board.remove_piece(position_from)
        self.board.place_piece(piece, position_to)
        return True


    def end_game(self, winner):
        save_match_result(self.player1, self.player2, winner, datetime.today().replace(microsecond=0))
        self
        print("Гра завершена.")

    def get_board(self):
        return self.board.board


Base = declarative_base()


class GameHistory(Base):
    __tablename__ = 'game_history'

    id = Column(Integer, primary_key=True, index=True)
    player = Column(String)
    position_from = Column(String)
    position_to = Column(String)