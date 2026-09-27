
import pygame
import heapq
import math

pygame.init()

# ==========================================
# HELLO KITTY: DUNGEON ESCAPE
# ==========================================

TILE = 48
COLS, ROWS = 15, 11
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 75

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hello Kitty: Dungeon Escape")
clock = pygame.time.Clock()

# Warna
PINK = (255, 160, 190)
LIGHT_PINK = (255, 220, 232)
DARK_PINK = (220, 80, 130)
WHITE = (255, 255, 255)
BLACK = (45, 35, 45)
PURPLE = (120, 90, 150)
WALL = (85, 65, 105)
FLOOR = (245, 230, 245)
RED = (240, 75, 100)
GOLD = (255, 210, 80)

font = pygame.font.SysFont("arial", 22, bold=True)
small_font = pygame.font.SysFont("arial", 16)

# 0 = jalan, 1 = tembok
dungeon = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Posisi awal
START_PLAYER = (1, 1)
START_ENEMY = (13, 9)

player = START_PLAYER
enemy = START_ENEMY
EXIT = (13, 1)

# AI monster
DETECTION_RANGE = 20
enemy_path = []
enemy_timer = 0

# Semakin kecil angka, semakin cepat monster
NORMAL_SPEED = 220
CHASE_SPEED = 160
ANGRY_SPEED = 100

game_over = False
win = False


# ==========================================
# ALGORITMA JARAK DAN TETANGGA
# ==========================================

def distance(a, b):
    """Menghitung jarak Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(pos):
    """Mencari kotak jalan di sekitar posisi."""
    x, y = pos
    result = []

    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy

        if 0 <= nx < COLS and 0 <= ny < ROWS:
            if dungeon[ny][nx] == 0:
                result.append((nx, ny))

    return result


# ==========================================
# ALGORITMA A* PATHFINDING
# ==========================================

def a_star(start, goal):
    """Mencari jalur dari start ke goal menggunakan A*."""
    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance(start, goal)}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.reverse()
            return path

        for next_pos in neighbors(current):
            tentative = g_score[current] + 1

            if tentative < g_score.get(next_pos, float("inf")):
                came_from[next_pos] = current
                g_score[next_pos] = tentative

                f_score[next_pos] = (
                    tentative + distance(next_pos, goal)
                )

                heapq.heappush(
                    open_list,
                    (f_score[next_pos], next_pos)
                )

    return []


# ==========================================
# GAMBAR HELLO KITTY
# ==========================================

def draw_kitty(pos):
    x = pos[0] * TILE + TILE // 2
    y = pos[1] * TILE + TILE // 2

    # Telinga
    pygame.draw.polygon(
        screen, WHITE,
        [(x-16,y-10), (x-20,y-27), (x-5,y-19)]
    )
    pygame.draw.polygon(
        screen, WHITE,
        [(x+16,y-10), (x+20,y-27), (x+5,y-19)]
    )

    # Kepala
    pygame.draw.ellipse(
        screen, WHITE,
        (x-20,y-19,40,36)
    )

    # Pita pink
    pygame.draw.circle(screen, DARK_PINK, (x+13,y-16), 7)
    pygame.draw.circle(screen, PINK, (x+4,y-20), 6)
    pygame.draw.circle(screen, PINK, (x+21,y-21), 6)
    pygame.draw.circle(screen, DARK_PINK, (x+13,y-16), 3)

    # Mata
    pygame.draw.ellipse(
        screen, BLACK, (x-11,y-3,4,7)
    )
    pygame.draw.ellipse(
        screen, BLACK, (x+7,y-3,4,7)
    )

    # Hidung
    pygame.draw.ellipse(
        screen, (255,190,40), (x-2,y+3,6,4)
    )

    # Pipi
    pygame.draw.ellipse(
        screen, LIGHT_PINK, (x-18,y+4,8,5)
    )
    pygame.draw.ellipse(
        screen, LIGHT_PINK, (x+10,y+4,8,5)
    )

    # Kumis
    pygame.draw.line(
        screen, BLACK, (x-15,y+5), (x-24,y+2), 1
    )
    pygame.draw.line(
        screen, BLACK, (x-15,y+9), (x-24,y+10), 1
    )
    pygame.draw.line(
        screen, BLACK, (x+15,y+5), (x+24,y+2), 1
    )
    pygame.draw.line(
        screen, BLACK, (x+15,y+9), (x+24,y+10), 1
    )


# ==========================================
# GAMBAR MONSTER
# ==========================================

def draw_monster(pos, chasing=False):
    x = pos[0] * TILE + TILE // 2
    y = pos[1] * TILE + TILE // 2

    body_color = RED if chasing else PURPLE

    # Telinga
    pygame.draw.polygon(
        screen, body_color,
        [(x-13,y-10), (x-17,y-25), (x-3,y-15)]
    )
    pygame.draw.polygon(
        screen, body_color,
        [(x+13,y-10), (x+17,y-25), (x+3,y-15)]
    )

    # Badan monster
    pygame.draw.ellipse(
        screen, body_color,
        (x-18,y-17,36,34)
    )

    # Mata
    pygame.draw.ellipse(
        screen, WHITE, (x-11,y-4,8,10)
    )
    pygame.draw.ellipse(
        screen, WHITE, (x+3,y-4,8,10)
    )
    pygame.draw.circle(screen, BLACK, (x-7,y), 2)
    pygame.draw.circle(screen, BLACK, (x+7,y), 2)

    # Mulut
    pygame.draw.arc(
        screen, BLACK,
        (x-6,y+3,12,9), 0, math.pi, 2
    )


# ==========================================
# GAMBAR DUNGEON
# ==========================================

def draw_game(chasing):
    screen.fill(LIGHT_PINK)

    for y in range(ROWS):
        for x in range(COLS):
            rect = (x*TILE, y*TILE, TILE, TILE)

            if dungeon[y][x] == 1:
                pygame.draw.rect(screen, WALL, rect)
                pygame.draw.rect(screen, PURPLE, rect, 2)
            else:
                pygame.draw.rect(screen, FLOOR, rect)
                pygame.draw.rect(
                    screen, (230,210,230), rect, 1
                )

    # Jalur yang sedang diikuti monster
    for p in enemy_path:
        pygame.draw.circle(
            screen, PINK,
            (p[0]*TILE + TILE//2,
             p[1]*TILE + TILE//2),
            5
        )

    # Pintu keluar
    ex, ey = EXIT
    pygame.draw.rect(
        screen, GOLD,
        (ex*TILE+10, ey*TILE+7, TILE-20, TILE-14)
    )
    pygame.draw.circle(
        screen, (150,90,40),
        (ex*TILE+TILE-17, ey*TILE+TILE//2),
        2
    )

    draw_kitty(player)
    draw_monster(enemy, chasing)

    # Panel informasi
    pygame.draw.rect(
        screen, WHITE,
        (0, ROWS*TILE, WIDTH, 75)
    )

    title = font.render(
        "HELLO KITTY: DUNGEON ESCAPE",
        True, DARK_PINK
    )
    screen.blit(title, (12, ROWS*TILE+4))

    if chasing:
        status = "MONSTER MENGEJAR KITTY!! LARIIII!"
        color = RED
    else:
        status = "Cari pintu kuning dan hindari monster!"
        color = PURPLE

    txt = small_font.render(status, True, color)
    screen.blit(txt, (12, ROWS*TILE+34))

    controls = small_font.render(
        "Gerak: WASD / ARROW KEYS | Restart: R",
        True, BLACK
    )
    screen.blit(controls, (12, ROWS*TILE+54))

    pygame.display.flip()


# ==========================================
# RESET GAME
# ==========================================

def reset_game():
    """Mengembalikan game ke kondisi awal."""
    global player, enemy, enemy_path
    global enemy_timer, game_over, win

    player = START_PLAYER
    enemy = START_ENEMY
    enemy_path = []
    enemy_timer = 0
    game_over = False
    win = False


# ==========================================
# GAME LOOP
# ==========================================

running = True

while running:
    dt = clock.tick(60)
    enemy_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Restart setelah menang atau kalah
            if event.key == pygame.K_r and (game_over or win):
                reset_game()
                continue

            # Input pergerakan player
            if not game_over and not win:
                dx, dy = 0, 0

                if event.key in (pygame.K_UP, pygame.K_w):
                    dy = -1
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    dy = 1
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    dx = -1
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    dx = 1

                new_pos = (
                    player[0] + dx,
                    player[1] + dy
                )

                if dx != 0 or dy != 0:
                    if (
                        0 <= new_pos[0] < COLS
                        and 0 <= new_pos[1] < ROWS
                        and dungeon[new_pos[1]][new_pos[0]] == 0
                    ):
                        player = new_pos

    # ======================================
    # AI MONSTER: DETECT, PATHFIND, CHASE
    # ======================================

    chasing = False

    if not game_over and not win:
        dist = distance(player, enemy)

        # Deteksi player
        if dist <= DETECTION_RANGE:
            chasing = True

            # Monster semakin dekat = semakin cepat
            if dist <= 3:
                move_delay = ANGRY_SPEED
            elif dist <= 8:
                move_delay = CHASE_SPEED
            else:
                move_delay = NORMAL_SPEED

            # Perbarui jalur menuju posisi Kitty terbaru
            enemy_path = a_star(enemy, player)

            # Gerakkan monster secara berkala
            if enemy_timer >= move_delay:
                enemy_timer = 0

                if enemy_path:
                    enemy = enemy_path[0]
                    enemy_path = []

        else:
            enemy_path = []
            enemy_timer = 0

        # Tertangkap
        if enemy == player:
            game_over = True

        # Berhasil kabur
        if player == EXIT:
            win = True

    draw_game(chasing)

    # ======================================
    # LAYAR AKHIR
    # ======================================

    if game_over or win:
        overlay = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((255, 230, 240, 210))
        screen.blit(overlay, (0, 0))

        if win:
            message = "YEAY! KITTY BERHASIL KABUR!"
        else:
            message = "OH NO! KITTY TERTANGKAP!"

        result = font.render(
            message, True, DARK_PINK
        )
        screen.blit(
            result,
            result.get_rect(
                center=(WIDTH//2, HEIGHT//2 - 12)
            )
        )

        restart_text = small_font.render(
            "Tekan R untuk bermain lagi",
            True, BLACK
        )
        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH//2, HEIGHT//2 + 22)
            )
        )

        pygame.display.flip()

pygame.quit()