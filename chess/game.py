from board import Board
class Game:
    def __init__(self):
        self.turn="white"
        self.board=Board()
        
    
    def is_valid_move(self, from_pos, to_pos):
        cur_piece=self.board.get_piece(from_pos[0],from_pos[1])
        king_pos=self.find_king(self.turn)
        if cur_piece and cur_piece.color==self.turn:
            moves=cur_piece.get_legal_moves(self.board)
            if to_pos in moves: 
             captured=self.board.move_piece(from_pos,to_pos)
             if not self.is_in_check(self.turn):
                self.board.undo_move(from_pos,to_pos,captured)
                return True
             self.board.undo_move(from_pos,to_pos,captured)
                    
        else:
            return False
    def make_move(self, from_pos, to_pos):
        if self.is_valid_move(from_pos, to_pos):
             self.board.move_piece(from_pos,to_pos)
             self.turn="black" if self.turn=="white" else "white"
             return True
        else:
             return False
    def is_squareattacked(self,pos,color):
         for row in range(8):
            for col in range (8):
                piece=self.board.get_piece(row,col)
                if piece and piece.color!=color:
                    moves=piece.get_legal_moves(self.board)
                    if pos in moves:
                        return True
         return False

    def find_king(self,color):
        for row in range(8):
            for col in range (8):
                piece=self.board.get_piece(row,col)
                if piece and str(piece) in ["wK","bK"]:
                    if color==piece.color:
                        return (row,col)
    def is_in_check(self,color):
        king_pos=self.find_king(color)
        return self.is_squareattacked(king_pos,color)
    
    def is_checkmate(self,color):
        if self.is_in_check(color):
            for row in range(8):
                for col in range(8):
                    piece=self.board.get_piece(row,col)
                    if piece and piece.color==color:
                        pos=piece.position
                        moves=piece.get_legal_moves(self.board)
                        for move in moves:
                            captured=self.board.move_piece(pos,move)
                            if not self.is_in_check(color):
                                self.board.undo_move(pos,move,captured)
                                return False
                            self.board.undo_move(pos,move,captured)
            return True
        return False
    
    def is_stalemate(self,color):
        if not self.is_in_check(color):
            for row in range(8):
                for col in range(8):
                    piece=self.board.get_piece(row,col)
                    if piece and piece.color==color:
                        pos=piece.position
                        moves=piece.get_legal_moves(self.board)
                        for move in moves:
                            captured=self.board.move_piece(pos,move)
                            if not self.is_in_check(color):
                                self.board.undo_move(pos,move,captured)
                                return False
                            self.board.undo_move(pos,move,captured)
            return True
        return False
                            
    def can_castling(self,color):
        
        if not self.is_in_check(color) :
         row=7 if color=="white" else 0
         king=self.board.get_piece(row,4)
         if not king.moved:
            rook=[self.board.get_piece(row,0),self.board.get_piece(row,7)]
            for m in [0,1]:
             if  str(rook[m]) in ["bR","wR"] and rook[m].color==color :
                if rook[m].moved==False:
                    pos=(1,2,3) if m==0 else (5,6)
                    pos_=(2,3) if m==0 else (5,6)
                    empty=all(self.board.get_piece(row,col) is None for col in pos)
                    safe=all(self.is_squareattacked((row,col),color)is False for col in pos_)
                    if empty and safe:
                        return True
        return False   

    def is_castling_move(self,from_pos,to_pos):
        if from_pos[0]==to_pos[0]:
            for i in [-2,2]:
                if from_pos[1]+i==to_pos[1]:
                    return True
        return False


    def Executecastling(self,from_pos,to_pos):
        row = from_pos[0]   
        color = self.board.get_piece(row,from_pos[1]).color
        if to_pos[1] == 6:   
         rook_from = (row, 7)
         rook_to   = (row, 5)
        else:                 
         rook_from = (row, 0)
         rook_to   = (row, 3)
        king = self.board.get_piece(row,from_pos[1])
        self.board.set_piece(row,from_pos[1], None)
        self.board.set_piece(to_pos[0],to_pos[1] ,king)
        king.position = to_pos
        king.moved = True   
        rook = self.board.get_piece(rook_from[0],rook_from[1])
        self.board.set_piece(rook_from[0],rook_from[1], None)
        self.board.set_piece(rook_to[0],rook_to[1], rook)
        rook.position = rook_to
        rook.moved = True
        
    
      
   


    


             
             
     