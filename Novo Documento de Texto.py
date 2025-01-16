import pygame
import sys
import os

# Cores
WHITE = (228, 228, 222)
BLACK = (22, 21, 18)
LIGHT = (227, 189, 139)
DARK = (127, 104, 73)
GREEN = (50, 250, 50)
BLUE = (0, 0, 100)
CIAN = (0, 0, 250)

# Configurações do tabuleiro
BOARD_WIDTH, BOARD_HEIGHT = 10, 10
TILE_SIZE = 23
BOARD_SIZE = TILE_SIZE * BOARD_WIDTH, TILE_SIZE * BOARD_HEIGHT
BORDER_SIZE = 1
PIECE_SIZE = 20

# Diretório das imagens
IMG_DIR = os.path.join(os.path.dirname(__file__), "IMG")

# Inicializa o PyGame
pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE[0], 3 * BOARD_SIZE[1] + 2 * BORDER_SIZE))
pygame.display.set_caption('3D Chess Game - Three Boards 10x10')

# Função para carregar e redimensionar imagens
def load_piece_image(file_name):
    img = pygame.image.load(os.path.join(IMG_DIR, file_name)).convert_alpha()
    return pygame.transform.scale(img, (PIECE_SIZE, PIECE_SIZE))

# Carregamento das imagens
B_peao_img = load_piece_image("B-peao.png")
P_peao_img = load_piece_image("P-peao.png")
B_torre_img = load_piece_image("B-torre.png")
P_torre_img = load_piece_image("P-torre.png")
B_cavalo_img = load_piece_image("B-cavalo.png")
P_cavalo_img = load_piece_image("P-cavalo.png")
B_bispo_img = load_piece_image("B-bispo.png")
P_bispo_img = load_piece_image("P-bispo.png")
B_dragao_img = load_piece_image("B-dragao.png")
P_dragao_img = load_piece_image("P-dragao.png")
B_rainha_img = load_piece_image("B-rainha.png")
P_rainha_img = load_piece_image("P-rainha.png")
B_rei_img = load_piece_image("B-rei.png")
P_rei_img = load_piece_image("P-rei.png")


class Piece(pygame.sprite.Sprite):
    def __init__(self, color, pos, shape):
        super().__init__()
        self.image = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)
        self.color = color
        self.shape = shape
        self.draw_shape()
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))  # Apenas x e y
        self.pos = pos  # (x, y, z): Coordenadas no tabuleiro 3D


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

    def valid_moves(self, board):
        """
       Retorna uma lista de movimentos válidos para a peça.
        :param board: Representação do tabuleiro 3D (lista de listas de listas).
        :return: Lista de tuplas com coordenadas válidas (x, y, z).
        """
        x, y, z = self.pos[0] // TILE_SIZE, self.pos[1] // TILE_SIZE, self.pos[2]  # Coordenadas no tabuleiro 3D
        moves = []
    
        if self.shape in ["B-peao", "P-peao"]:  # Movimento do Peão
            moves = self.pawn_moves(board, x, y, z)
        elif self.shape in ["B-torre", "P-torre"]:  # Movimento da Torre
            moves = self.rook_moves(board, x, y, z)
        elif self.shape in ["B-cavalo", "P-cavalo"]:  # Movimento do Cavalo
            moves = self.knight_moves(board, x, y, z)
        elif self.shape in ["B-bispo", "P-bispo"]:  # Movimento do Bispo
            moves = self.bishop_moves(board, x, y, z)
        elif self.shape in ["B-dragao", "P-dragao"]:  # Movimento do Dragão
            moves = self.dragon_moves(board, x, y, z)
        elif self.shape in ["B-rainha", "P-rainha"]:  # Movimento da Rainha
            moves = self.queen_moves(board, x, y, z)
        elif self.shape in ["B-rei", "P-rei"]:  # Movimento do Rei
            moves = self.king_moves(board, x, y, z)
    
        return moves
    
    def pawn_moves(self, board, x, y, z):
        moves = []
        direction = -1 if self.color == BLACK else 1  # Preto desce (-y), branco sobe (+y)
    
        # Movimento simples para frente
        if 0 <= y + direction < BOARD_HEIGHT and board[z][y + direction][x] == "":
            moves.append((x, y + direction, z))
    
        # Captura na diagonal
        if x > 0 and 0 <= y + direction < BOARD_HEIGHT and board[z][y + direction][x - 1] != "" and board[z][y + direction][x - 1].color != self.color:
            moves.append((x - 1, y + direction, z))
        if x < BOARD_WIDTH - 1 and 0 <= y + direction < BOARD_HEIGHT and board[z][y + direction][x + 1] != "" and board[z][y + direction][x + 1].color != self.color:
            moves.append((x + 1, y + direction, z))
    
        # Movimento vertical entre planos
        if z > 0 and board[z - 1][y][x] == "":  # Subir
            moves.append((x, y, z - 1))
        if z < 2 and board[z + 1][y][x] == "":  # Descer
            moves.append((x, y, z + 1))
    
        return moves
    
    def rook_moves(self, board, x, y, z):
        moves = []
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            while 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 0 <= nz < 3:
                if board[nz][ny][nx] == "":
                    moves.append((nx, ny, nz))
                elif board[nz][ny][nx].color != self.color:  # Captura
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
                nx, ny, nz = nx + dx, ny + dy, nz + dz
    
        return moves
    
    def knight_moves(self, board, x, y, z):
        moves = []
        directions = [(-2, -1, 0), (-2, 1, 0), (2, -1, 0), (2, 1, 0),
                      (-1, -2, 0), (-1, 2, 0), (1, -2, 0), (1, 2, 0),
                      (-2, 0, -1), (-2, 0, 1), (2, 0, -1), (2, 0, 1),
                      (-1, 0, -2), (-1, 0, 2), (1, 0, -2), (1, 0, 2),
                      (0, -2, -1), (0, -2, 1), (0, 2, -1), (0, 2, 1),
                      (0, -1, -2), (0, -1, 2), (0, 1, -2), (0, 1, 2)]
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 0 <= nz < 3:
                if board[nz][ny][nx] == "" or board[nz][ny][nx].color != self.color:
                    moves.append((nx, ny, nz))
    
        return moves
    
    def bishop_moves(self, board, x, y, z):
        moves = []
        directions = [(1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                      (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),
                      (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1)]
    
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            while 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 0 <= nz < 3:
                if board[nz][ny][nx] == "":
                    moves.append((nx, ny, nz))
                elif board[nz][ny][nx].color != self.color:  # Captura
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
                nx, ny, nz = nx + dx, ny + dy, nz + dz
    
        return moves
    
    def dragon_moves(self, board, x, y, z):
        moves = []
        directions = [(1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1),
                      (1, 1, -1), (1, -1, -1), (-1, 1, -1), (-1, -1, -1)]
    
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            while 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 0 <= nz < 3:
                if board[nz][ny][nx] == "":
                    moves.append((nx, ny, nz))
                elif board[nz][ny][nx].color != self.color:  # Captura
                    moves.append((nx, ny, nz))
                    break
                else:
                    break
                nx, ny, nz = nx + dx, ny + dy, nz + dz
    
        return moves
    
    def queen_moves(self, board, x, y, z):
        return self.rook_moves(board, x, y, z) + self.bishop_moves(board, x, y, z) + self.dragon_moves(board, x, y, z)
    
    def king_moves(self, board, x, y, z):
        moves = []
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
                      (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                      (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
                      (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
                      (1, 1, 1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1),
                      (1, 1, -1), (1, -1, -1), (-1, 1, -1), (-1, -1, -1)]
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 0 <= nz < 3:
                if board[nz][ny][nx] == "" or board[nz][ny][nx].color != self.color:
                    moves.append((nx, ny, nz))
    
        return moves

def draw_board1(screen, z):
    offset_y = z * (BOARD_SIZE[1] + BORDER_SIZE)
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(
                screen,
                color,
                (col * TILE_SIZE, offset_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            )

def draw_board2(screen, z):
    offset_y = z * (BOARD_SIZE[1] + BORDER_SIZE)
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = DARK if (row + col) % 2 == 0 else LIGHT
            pygame.draw.rect(
                screen,
                color,
                (col * TILE_SIZE, offset_y + row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            )

def draw_dividers(screen):
    for i in range(1, 3):
        pygame.draw.rect(
            screen,
            GREEN,
            (0, i * BOARD_SIZE[1] + (i - 1) * BORDER_SIZE, BOARD_SIZE[0], BORDER_SIZE),
        )
        
def draw_board_and_pieces(screen, board):
    """
    Desenha o tabuleiro e as peças na tela.
    """
    for z in range(3):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                # Desenhar o tabuleiro
                color = LIGHT if (x + y) % 2 == 0 else DARK
                pygame.draw.rect(
                    screen,
                    color,
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

                # Desenhar peças
                piece = board[z][y][x]
                if piece:
                    screen.blit(piece.image, piece.rect)
                    
def move_piece(board, selected_piece, target_pos):
    """
    Move uma peça para uma nova posição no tabuleiro.
    """
    x, y, z = selected_piece.pos
    tx, ty, tz = target_pos

    # Atualiza o estado do tabuleiro
    board[z][y][x] = None
    board[tz][ty][tx] = selected_piece

    # Atualiza a posição da peça
    selected_piece.pos = (tx, ty, tz)
    selected_piece.rect.topleft = (tx * TILE_SIZE, ty * TILE_SIZE)

def initialize_board():
    """
    Inicializa o tabuleiro 3D e posiciona as peças.
    """
    board = [[[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)] for _ in range(3)]  # 3 planos (z)

    # Configuração inicial no plano 0 (z=0) e plano 2 (z=2)
    # Peças pretas
    board[0][0] = [Piece(BLACK, (i * TILE_SIZE, 0), "B-torre") if i == 0 or i == 7 else
                   Piece(BLACK, (i * TILE_SIZE, 0), "B-cavalo") if i == 1 or i == 6 else
                   Piece(BLACK, (i * TILE_SIZE, 0), "B-bispo") if i == 2 or i == 5 else
                   Piece(BLACK, (i * TILE_SIZE, 0), "B-rainha") if i == 3 else
                   Piece(BLACK, (i * TILE_SIZE, 0), "B-rei") for i in range(BOARD_WIDTH)]

    board[0][1] = [Piece(BLACK, (i * TILE_SIZE, TILE_SIZE), "B-peao") for i in range(BOARD_WIDTH)]

    # Peças brancas
    board[2][6] = [Piece(WHITE, (i * TILE_SIZE, 6 * TILE_SIZE), "P-peao") for i in range(BOARD_WIDTH)]
    board[2][7] = [Piece(WHITE, (i * TILE_SIZE, 7 * TILE_SIZE), "P-torre") if i == 0 or i == 7 else
                   Piece(WHITE, (i * TILE_SIZE, 7 * TILE_SIZE), "P-cavalo") if i == 1 or i == 6 else
                   Piece(WHITE, (i * TILE_SIZE, 7 * TILE_SIZE), "P-bispo") if i == 2 or i == 5 else
                   Piece(WHITE, (i * TILE_SIZE, 7 * TILE_SIZE), "P-rainha") if i == 3 else
                   Piece(WHITE, (i * TILE_SIZE, 7 * TILE_SIZE), "P-rei") for i in range(BOARD_WIDTH)]

    return board


def initialize_pieces(board):
    """
    Inicializa as peças do jogo nos três tabuleiros (z = 0, 1, 2).
    Adiciona as peças ao tabuleiro tridimensional e aos grupos de sprites.
    """
    pieces_group1 = pygame.sprite.Group()  # Grupo para peças no tabuleiro z = 0
    pieces_group2 = pygame.sprite.Group()  # Grupo para peças no tabuleiro z = 1
    pieces_group3 = pygame.sprite.Group()  # Grupo para peças no tabuleiro z = 2

    # Tabuleiro 1 (z = 0)
    shapes_board1 = [
        ["P-torre", "P-cavalo", "P-bispo", "P-dragao", "P-rei", "P-rainha", "P-dragao", "P-bispo", "P-cavalo", "P-torre"],
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
    ]

    # Tabuleiro 2 (z = 1)
    shapes_board2 = [
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
        ["P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao", "P-peao"],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
    ]

    # Tabuleiro 3 (z = 2)
    shapes_board3 = [        
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", ""],
        ["B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao", "B-peao"],
        ["B-torre", "B-cavalo", "B-bispo", "B-dragao", "B-rei", "B-rainha", "B-dragao", "B-bispo", "B-cavalo", "B-torre"],
    ]

    # Inicializando peças no tabuleiro z = 0
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            shape1 = shapes_board1[row][col]
            if shape1:
                piece = Piece(BLACK, (col * TILE_SIZE, row * TILE_SIZE, 0), shape1)
                pieces_group1.add(piece)
                board[0][row][col] = piece  # Adiciona a peça ao tabuleiro 3D (z = 0)

    # Inicializando peças no tabuleiro z = 1
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            shape2 = shapes_board2[row][col]
            if shape2:
                piece = Piece(WHITE, (col * TILE_SIZE, row * TILE_SIZE, 1), shape2)
                pieces_group2.add(piece)
                board[1][row][col] = piece  # Adiciona a peça ao tabuleiro 3D (z = 1)

    # Inicializando peças no tabuleiro z = 2
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            shape3 = shapes_board3[row][col]
            if shape3:
                piece = Piece(WHITE, (col * TILE_SIZE, row * TILE_SIZE, 2), shape3)
                pieces_group3.add(piece)
                board[2][row][col] = piece  # Adiciona a peça ao tabuleiro 3D (z = 2)

    return pieces_group1, pieces_group2, pieces_group3


def main():
    # Inicializa o tabuleiro 3D
    board = [[[ "" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)] for _ in range(3)]
    pieces_group1, pieces_group2, pieces_group3 = initialize_pieces(board)
    selected_piece = None  # Peça atualmente selecionada
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = x // TILE_SIZE, y // TILE_SIZE
            
                if selected_piece:
                    # Verificar se o clique é um movimento válido
                    target = (x, y, selected_piece.pos[2])  # Assume que o movimento ocorre no mesmo plano
                    if target in selected_piece.valid_moves(board):
                        move_piece(board, selected_piece, target)
                        selected_piece = None  # Deseleciona a peça
                    else:
                        selected_piece = None  # Clique inválido, deseleciona
                else:
                    # Selecionar uma peça
                    z = 2  # Exemplo: selecionar no plano mais alto
                    piece = board[z][y][x]
                    if piece and piece.color == current_player_color:  # Selecionar apenas peças do jogador atual
                        selected_piece = piece


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_piece:
                    pos = pygame.mouse.get_pos()
                    z = selected_piece.pos[2]  # Tabuleiro atual da peça selecionada

                    # Converte a posição do clique em índices do tabuleiro
                    x = pos[0] // TILE_SIZE
                    y = (pos[1] - z * (BOARD_SIZE[1] + BORDER_SIZE)) // TILE_SIZE

                    # Verifica se o movimento é válido
                    if (x, y, z) in selected_piece.valid_moves(board):
                        # Atualiza o tabuleiro 3D
                        board[z][selected_piece.pos[1] // TILE_SIZE][selected_piece.pos[0] // TILE_SIZE] = ""
                        selected_piece.rect.center = (
                            x * TILE_SIZE + TILE_SIZE // 2,
                            y * TILE_SIZE + TILE_SIZE // 2 + z * (BOARD_SIZE[1] + BORDER_SIZE),
                        )
                        selected_piece.pos = (x, y, z)
                        board[z][y][x] = selected_piece
                    selected_piece = None

        # Desenha o tabuleiro e as peças
        screen.fill(WHITE)
        for z in range(3):
            if z == 0:
                draw_board1(screen, z)
            elif z == 1:
                draw_board2(screen, z)
            else:
                draw_board1(screen, z)
        draw_dividers(screen)
        pieces_group1.draw(screen)
        pieces_group2.draw(screen)
        pieces_group3.draw(screen)

        # Destaca peça selecionada e movimentos válidos
        if selected_piece:
            pygame.draw.rect(screen, BLUE, selected_piece.rect.inflate(5, 5), 3)
            for move in selected_piece.valid_moves(board):
                pygame.draw.rect(screen, CIAN, (
                    move[0] * TILE_SIZE, 
                    move[1] * TILE_SIZE + move[2] * (BOARD_SIZE[1] + BORDER_SIZE), 
                    TILE_SIZE, TILE_SIZE), 2)

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()