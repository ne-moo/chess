import pygame
import os
from game import Game
from pieces import Rook,Knight,Bishop,Queen
game=Game()
pygame.init()
width=640
height=640
cell_width=80
cell_height=80
cream=(240, 217, 181)
brown=(181, 136, 99)
selected_color=(100, 150, 255, 120)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("CHESS GAME")

selected_surf = pygame.Surface((80,80), pygame.SRCALPHA)
selected_surf.fill((255, 255, 0, 120))

running = True
selected_pos=None
selected_piece=None
selected=False
legal_moves=[]

game_over = False
winner = None
pawn_promotion=False

images=["bB","bK","bN","bP","bQ","bR","wB","wK","wN","wP","wQ","wR"]
piece_images={}
base_path=os.path.dirname(__file__)
for name in images:
    image=pygame.image.load(os.path.join(base_path, "assets", name + ".png"))
    piece_images[name]=pygame.transform.scale(image, (70, 70))

rect=[]
def get_promotion_choice(color,dest_pos):
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((80, 80, 80))
    screen.blit(overlay, (0, 0))
    option=["bQ","bR","bN","bB"] if color=="black" else ["wQ","wR","wN","wB"]
    options=[]
    pieces=[Queen,Rook,Knight,Bishop]
    for i,opt in enumerate(pieces):
        options.append((option[i],opt(color,dest_pos)))
    col=2;row=2*cell_height
    for op in options:
        screen.blit(piece_images[op[0]],(col*cell_width, row))
        rect.append((op, pygame.Rect(col*cell_width, row, 80, 80)))
        col+=1
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for op, rectangle in rect:
                    if rectangle.collidepoint(pos):
                        return op[1]

    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            posx,posy=pygame.mouse.get_pos()
            x=posx//cell_width
            y=posy//cell_height
            piece=game.board.get_piece(y, x)
           
            if selected==False:
               if piece and piece.color==game.turn: 
                selected_piece=piece
                selected_pos=(y,x)
                legal_moves= piece.get_legal_moves(game.board)
                selected = True 
            
            else:
                dest_pos=(y,x)
                if str(selected_piece ) in ["bK","wK"]:
                    if game.is_castling_move(selected_pos,dest_pos) and game.can_castling(selected_piece.color):
                        game.Executecastling(selected_pos,dest_pos)
                        game.turn="white" if selected_piece.color=="black" else "black"
                        
            
                elif dest_pos in legal_moves :
                    game.make_move(selected_pos,dest_pos)
                    moved_piece = game.board.get_piece(dest_pos[0],dest_pos[1])
                    if moved_piece:
                        moved_piece.moved=True
                    if str(moved_piece) in ["wP","bP"]:
                      if dest_pos==game.board.en_passant_target:
                          row=game.board.en_passant_target[0]+1 if moved_piece.color=='white' else game.board.en_passant_target[0]-1
                          game.board.set_piece(row,dest_pos[1],None)
                          game.board.en_passant_target=None
                      if abs(dest_pos[0]-selected_pos[0])==2:
                          tar_pos=dest_pos[0]-1 if moved_piece.color=="black" else dest_pos[0]+1
                          game.board.en_passant_target=(tar_pos,dest_pos[1])
                      else:
                          game.board.en_passant_target=None
                          
                      if moved_piece.can_promote(dest_pos):
                          op=get_promotion_choice(moved_piece.color,dest_pos)
                          game.board.set_piece(dest_pos[0],dest_pos[1],op)
                          game.turn="white" if op.color=="black" else "black"
                    else:
                        game.board.en_passant_target=None
                   
                if game.is_checkmate(game.turn):
                         winner = "White" if game.turn == "black" else "Black"  
                         game_over = True
                if game.is_stalemate(game.turn):
                        game_over=True 
               
                selected_piece=None
                selected_pos=None
                selected=False
                      
           
            
    for row in range(8):
        for col in range(8):
            color=brown if (row+col)%2==0 else cream
            pygame.draw.rect(screen, color, (col*cell_width, row*cell_height, cell_width, cell_height))
            if selected:
                if (row,col)in legal_moves or selected_pos==(row,col):
                     screen.blit(selected_surf, (col * cell_width, row * cell_height))

            piece=str(game.board.get_piece(row,col))
            if piece in images:
                screen.blit(piece_images[piece],(col*cell_width, row*cell_height))

    if game_over:
         overlay = pygame.Surface((width, height))
         overlay.set_alpha(200)
         overlay.fill((0, 0, 0))
         screen.blit(overlay, (0, 0))
    
         font = pygame.font.Font(None, 74)
         if winner:
          text = font.render(f"{winner} Wins!", True, (255, 255, 255))
         else:
              text = font.render("Draw!!", True, (255, 255, 255))
         screen.blit(text, (width//2 - text.get_width()//2, height//2))

    pygame.display.flip()
    
pygame.quit()
