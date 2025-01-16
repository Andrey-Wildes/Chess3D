import pygame
import sys
import os

WHITE = (228, 228, 222)
BLACK = (22, 21, 18)
LIGHT = (227, 189, 139)
DARK = (127, 104, 73)
GREEN = (50, 250, 50)

BOARD_WIDTH, BOARD_HEIGHT = 10, 10
TILE_SIZE = 40
BOARD_SIZE = TILE_SIZE * BOARD_WIDTH, TILE_SIZE * BOARD_HEIGHT
BORDER_SIZE = 1
PIECE_SIZE = 30

IMG_DIR = os.path.join(os.path.dirname(__file__), "IMG")

pygame.init()
screen = pygame.display.set_mode((3 * BOARD_SIZE[0] + 2 * BORDER_SIZE, BOARD_SIZE[1]))
pygame.display.set_caption('3D Chess Game - Three Boards 10x10')

B_peao_img = pygame.image.load(os.path.join(IMG_DIR, "B-peao.png")).convert_alpha()
P_peao_img = pygame.image.load(os.path.join(IMG_DIR, "P-peao.png")).convert_alpha()
B_torre_img = pygame.image.load(os.path.join(IMG_DIR, "B-torre.png")).convert_alpha()
P_torre_img = pygame.image.load(os.path.join(IMG_DIR, "P-torre.png")).convert_alpha()
B_cavalo_img = pygame.image.load(os.path.join(IMG_DIR, "B-cavalo.png")).convert_alpha()
P_cavalo_img = pygame.image.load(os.path.join(IMG_DIR, "P-cavalo.png")).convert_alpha()
B_bispo_img = pygame.image.load(os.path.join(IMG_DIR, "B-bispo.png")).convert_alpha()
P_bispo_img = pygame.image.load(os.path.join(IMG_DIR, "P-bispo.png")).convert_alpha()
B_dragao_img = pygame.image.load(os.path.join(IMG_DIR, "B-dragao.png")).convert_alpha()
P_dragao_img = pygame.image.load(os.path.join(IMG_DIR, "P-dragao.png")).convert_alpha()
B_rainha_img = pygame.image.load(os.path.join(IMG_DIR, "B-rainha.png")).convert_alpha()
P_rainha_img = pygame.image.load(os.path.join(IMG_DIR, "P-rainha.png")).convert_alpha()
B_rei_img = pygame.image.load(os.path.join(IMG_DIR, "B-rei.png")).convert_alpha()
P_rei_img = pygame.image.load(os.path.join(IMG_DIR, "P-rei.png")).convert_alpha()

B_peao_img = pygame.transform.scale(B_peao_img, (PIECE_SIZE, PIECE_SIZE))
P_peao_img = pygame.transform.scale(P_peao_img, (PIECE_SIZE, PIECE_SIZE))
B_torre_img = pygame.transform.scale(B_torre_img, (PIECE_SIZE, PIECE_SIZE))
P_torre_img = pygame.transform.scale(P_torre_img, (PIECE_SIZE, PIECE_SIZE))
B_cavalo_img = pygame.transform.scale(B_cavalo_img, (PIECE_SIZE, PIECE_SIZE))
P_cavalo_img = pygame.transform.scale(P_cavalo_img, (PIECE_SIZE, PIECE_SIZE))
B_bispo_img = pygame.transform.scale(B_bispo_img, (PIECE_SIZE, PIECE_SIZE))
P_bispo_img = pygame.transform.scale(P_bispo_img, (PIECE_SIZE, PIECE_SIZE))
B_dragao_img = pygame.transform.scale(B_dragao_img, (PIECE_SIZE, PIECE_SIZE))
P_dragao_img = pygame.transform.scale(P_dragao_img, (PIECE_SIZE, PIECE_SIZE))
B_rainha_img = pygame.transform.scale(B_rainha_img, (PIECE_SIZE, PIECE_SIZE))
P_rainha_img = pygame.transform.scale(P_rainha_img, (PIECE_SIZE, PIECE_SIZE))
B_rei_img = pygame.transform.scale(B_rei_img, (PIECE_SIZE, PIECE_SIZE))
P_rei_img = pygame.transform.scale(P_rei_img, (PIECE_SIZE, PIECE_SIZE))

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, pos, shape):
        super().__init__()
        self.image = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
        self.color = color
        self.shape = shape
        self.draw_shape()
        self.rect = self.image.get_rect(center=pos)
        self.id = shape
        self.pos = pos

    def draw_shape(self):
        if self.shape == "B-peao":
            self.image = B_peao_img
        elif self.shape == "P-peao":
            self.image = P_peao_img
        elif self.shape == "B-torre":
            self.image = B_torre_img
        elif self.shape == "P-torre":
            self.image = P_torre_img
        elif self.shape == "B-cavalo":
            self.image = B_cavalo_img
        elif self.shape == "P-cavalo":
            self.image = P_cavalo_img
        elif self.shape == "B-bispo":
            self.image = B_bispo_img
        elif self.shape == "P-bispo":
            self.image = P_bispo_img
        elif self.shape == "B-dragao":
            self.image = B_dragao_img
        elif self.shape == "P-dragao":
            self.image = P_dragao_img
        elif self.shape == "B-rainha":
            self.image = B_rainha_img
        elif self.shape == "P-rainha":
            self.image = P_rainha_img
        elif self.shape == "B-rei":
            self.image = B_rei_img
        elif self.shape == "P-rei":
            self.image = P_rei_img

def draw_board(screen, offset):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (offset + col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_board2(screen, offset):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = DARK if (row + col) % 2 == 0 else LIGHT
            pygame.draw.rect(screen, color, (offset + col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_dividers(screen):
    for i in range(1, 3):
        pygame.draw.rect(screen, GREEN, (i * BOARD_SIZE[0] + (i - 1) * BORDER_SIZE, 0, BORDER_SIZE, BOARD_SIZE[1]))

def initialize_pieces():
    pieces_group1 = pygame.sprite.Group()
    pieces_group2 = pygame.sprite.Group()
    pieces_group3 = pygame.sprite.Group()
    shapes_board1 = [
        ["B-torre", "B-cavalo", "B-bispo", "B-dragao", "B-rei", "B-rainha", "B-dragao", "B-bispo", "B-cavalo", "B-torre"],
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
    ]
    shapes_board2 = [
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
    ]
    shapes_board3 = [        
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
        ["P-torre", "P-cavalo", "P-bispo", "P-dragao", "P-rei", "P-rainha", "P-dragao", "P-bispo", "P-cavalo", "P-torre"],
    ]
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            pos = (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2)
            shape1 = shapes_board1[row][col]
            if shape1:
                piece = Piece(BLACK, pos, shape1)
                pieces_group1.add(piece)
            shape2 = shapes_board2[row][col]
            if shape2:
                piece = Piece(WHITE, (pos[0] + BOARD_SIZE[0] + BORDER_SIZE, pos[1]), shape2)
                pieces_group2.add(piece)
            shape3 = shapes_board3[row][col]
            if shape3:
                piece = Piece(WHITE, (pos[0] + 2 * BOARD_SIZE[0] + 2 * BORDER_SIZE, pos[1]), shape3)
                pieces_group3.add(piece)
    return pieces_group1, pieces_group2, pieces_group3

def main():
    pieces_group1, pieces_group2, pieces_group3 = initialize_pieces()
    selected_piece = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    for piece in pieces_group1.sprites() + pieces_group2.sprites() + pieces_group3.sprites():
                        if piece.rect.collidepoint(pos):
                            selected_piece = piece
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if selected_piece:
                        # Moving the piece to the center of the clicked tile
                        selected_piece.rect.center = (pos[0] // TILE_SIZE * TILE_SIZE + TILE_SIZE // 2,
                                                       pos[1] // TILE_SIZE * TILE_SIZE + TILE_SIZE // 2)
                        selected_piece = None

        screen.fill(WHITE)
        draw_board(screen, 0)
        draw_board2(screen, BOARD_SIZE[0] + BORDER_SIZE)
        draw_board(screen, 2 * BOARD_SIZE[0] + 2 * BORDER_SIZE)
        draw_dividers(screen)
        pieces_group1.draw(screen)
        pieces_group2.draw(screen)
        pieces_group3.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 