
class Piece:
    def __init__(self,color,position):
        self.color=color
        self.position=position
        self.moved=False
        
        
    def moves(self,board,directions):
        legal_moves=[]
        cur_row,cur_col=self.position
        for dr in directions:
         x,y=cur_row+dr[0],cur_col+dr[1]
         while 0<=x<8 and 0<=y<8:
            cur_piece=board.get_piece(x,y)
            if cur_piece is None:
                    legal_moves.append((x, y))
            else:
                    if cur_piece.color != self.color:
                        legal_moves.append((x, y))
                        
                    break
            x+=dr[0];y+=dr[1]
        return legal_moves
    def kk_moves(self,board,directions):
        legal_moves=[]
        cur_row,cur_col=self.position
        for move in directions:
            x=cur_row+move[0]
            y=cur_col+move[1]
            if 0 <= x < 8 and 0 <= y < 8:
             cur_piece=board.get_piece(x,y)
             if cur_piece==None or cur_piece.color!=self.color:
              legal_moves.append((x,y))
        return legal_moves
class Rook(Piece):
    def __str__(self):
        if self.color=="white":
            return "wR"
        elif self.color=="black":
            return "bR"
    def get_legal_moves(self,board):
        directions=[(1,0), (-1,0), (0,1), (0,-1)]
        return self.moves(board,directions)
       
class Knight(Piece):     
    def __str__(self):
        if self.color=="white":
            return "wN"
        elif self.color=="black":
            return "bN"
    def get_legal_moves(self,board):
        knight_moves=[(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]
        return self.kk_moves(board,knight_moves)
class Bishop(Piece):
  def __str__(self):
        if self.color=="white":
            return "wB"
        elif self.color=="black":
            return "bB"
  def get_legal_moves(self,board):
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        return self.moves(board,directions)
class Queen(Piece):
    def __str__(self):
        if self.color=="white":
            return "wQ"
        elif self.color=="black":
            return "bQ"
    def get_legal_moves(self,board):
        directions = [(1,0), (-1,0), (0,1), (0,-1),(1,1), (1,-1), (-1,1), (-1,-1)]
        return self.moves(board,directions)
class King(Piece):
    def __str__(self):
        if self.color=="white":
            return "wK"
        elif self.color=="black":
            return "bK"
    def get_legal_moves(self,board):
        king_moves=[(1,0), (-1,0), (0,1), (0,-1),(1,1), (1,-1), (-1,1), (-1,-1)]
        return self.kk_moves(board,king_moves)
   

class Pawn(Piece):
    def __str__(self):
        if self.color=="white":
            return "wP"
        elif self.color=="black":
            return "bP"
    def get_legal_moves(self,board):
       legal_moves=[]
       cur_row,cur_col=self.position
       if self.color=="white": 
           direction=-1;start=6
       else : 
           direction=1;start=1
       cur_piece=board.get_piece(cur_row+direction,cur_col)
       if cur_piece is None:
           legal_moves.append((cur_row+direction,cur_col))
           if cur_row==start and board.get_piece(cur_row+direction*2,cur_col) is None:
            legal_moves.append((cur_row+direction*2,cur_col))
       for col_offset in [-1,1]:
        x,y=cur_row+direction,cur_col+col_offset
        if 0<=x<8 and 0<=y<8:
         cur_piece=board.get_piece(x,y)
         if cur_piece and self.color!=cur_piece.color:
           legal_moves.append((x,y))
       if board.en_passant_target:
           row,col=self.position
           if (self.color=="white" and row==3) or (self.color=="black" and row==4): 
               if abs(board.en_passant_target[1]-col)==1 and row==board.en_passant_target[0]-direction:
                   legal_moves.append(board.en_passant_target)  
       return legal_moves
    def can_promote(self,dest_pos):
        if (0==dest_pos[0] and self.color=="white") or (7==dest_pos[0] and self.color=="black"):
            return True
        return False
   