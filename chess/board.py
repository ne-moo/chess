from pieces import Rook,Knight,Bishop,Queen,King,Pawn
class Board:
    def __init__(self):
        self.board=[[None for _ in range(8)] for _ in range(8)]
        self.setup_initial_position()
        self.en_passant_target=None
    def display(self):
        for row in self.board:
            for piece in row:
                if piece:
                    print (str(piece),end=" ")
                else:
                    print("...",end=" ")
            print("\n")

    def setup_initial_position(self):
           piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    
           for col, PieceClass in enumerate(piece_order):
             self.set_piece(0, col, PieceClass("black", (0, col)))
           for col, PieceClass in enumerate(piece_order):
              self.set_piece(7, col, PieceClass("white", (7, col)))
           for col in range(8):
               self.set_piece(1, col, Pawn("black", (1, col)))
               self.set_piece(6, col, Pawn("white", (6, col)))
               
       
    def get_piece(self,row,col):
        return self.board[row][col]
    def set_piece(self,row,col,piece):
        self.board[row][col]=piece
        if piece:
         piece.position=(row,col)
    def move_piece(self,from_pos,to_pos):
        piece=self.get_piece(from_pos[0],from_pos[1])
        captured=self.get_piece(to_pos[0],to_pos[1])
        self.set_piece(to_pos[0],to_pos[1],piece)
        self.set_piece(from_pos[0],from_pos[1],None)
        return captured
    
    def undo_move(self, from_pos, to_pos, captured):
        self.move_piece(to_pos, from_pos)
        self.set_piece(to_pos[0], to_pos[1], captured)
