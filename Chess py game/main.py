import pygame
import chess
import chess.engine
import sys
import os


pygame.init()


WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
DELAY = 500 


selected_square = None
player_clicks = []
player_color = chess.WHITE  


def load_images():
    pieces = ['wP', 'bP', 'wN', 'bN', 'wB', 'bB', 'wR', 'bR', 'wQ', 'bQ', 'wK', 'bK']
    for piece in pieces:
        try:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        except FileNotFoundError:
            print(f"Error: File images/{piece}.png not found.")
            sys.exit()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')


STOCKFISH_PATH = r"path/to/stockfish-windows-x86-64-avx2.exe"


def main():
    global selected_square, player_clicks, player_color
    
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()
    board = chess.Board()
    load_images()
    
  
    if not os.path.isfile(STOCKFISH_PATH):
        print(f"Error: Stockfish binary not found at {STOCKFISH_PATH}")
        sys.exit()
    else:
        print(f"Stockfish binary found at {STOCKFISH_PATH}")

    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except FileNotFoundError:
        print(f"Error: Stockfish binary not found at {STOCKFISH_PATH}")
        sys.exit()
    
    running = True
    player_turn = True  

 
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                engine.quit()
                pygame.quit()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and player_turn:
                location = pygame.mouse.get_pos() 
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                square = chess.square(col, 7 - row)
                if selected_square is None:
                    selected_square = square
                    player_clicks.append(square)
                else:
                    player_clicks.append(square)
                    move = chess.Move(player_clicks[0], player_clicks[1])
                    if move in board.legal_moves:
                        board.push(move)
                        player_turn = False
                        pygame.time.wait(DELAY) 
                    selected_square = None
                    player_clicks = []

        if not player_turn:
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
            player_turn = True
            pygame.time.wait(DELAY) 

        draw_game_state(screen, board, selected_square)
        clock.tick(MAX_FPS)
        pygame.display.flip()

    engine.quit()


def draw_game_state(screen, board, selected_square):
    draw_board(screen)
    draw_pieces(screen, board)
    if selected_square is not None:
        highlight_square(screen, selected_square)


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.piece_at(chess.square(c, 7 - r))
            if piece:
                piece_image_key = ('w' if piece.color == chess.WHITE else 'b') + piece.symbol().upper()
                screen.blit(IMAGES[piece_image_key], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, square):
    col = chess.square_file(square)
    row = 7 - chess.square_rank(square)
    s = pygame.Surface((SQ_SIZE, SQ_SIZE))
    s.set_alpha(128) 
    s.fill(pygame.Color("red"))
    screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

if __name__ == "__main__":
    main()
