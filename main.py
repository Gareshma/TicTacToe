import pygame
import sys
from pygame import mixer
from tkinter import Tk, messagebox

# Initialize pygame and mixer
pygame.init()
mixer.init()

# --- Constants ---
WIDTH, HEIGHT = 400, 540
CELL_SIZE = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)

# --- Fonts ---
FONT_LARGE = pygame.font.SysFont(None, 80)
FONT_MEDIUM = pygame.font.SysFont(None, 36)
FONT_SMALL = pygame.font.SysFont(None, 24)

# --- Load Sounds ---
sound_x = mixer.Sound("success.mp3")
sound_o = mixer.Sound("success_O.mp3")
sound_win = mixer.Sound("win.mp3")
sound_draw = mixer.Sound("game_draw.mp3")

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# --- Game State Variables ---
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None
game_over = False
winning_line = []
x_score, o_score = 0, 0
start_time = pygame.time.get_ticks()
end_time = 0

# --- Utility Functions ---

def draw_grid():
    screen.fill(WHITE)
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 80), (i * CELL_SIZE, 440), 5)
        pygame.draw.line(screen, BLACK, (0, 80 + i * CELL_SIZE), (WIDTH, 80 + i * CELL_SIZE), 5)

def draw_marks():
    for row in range(3):
        for col in range(3):
            mark = board[row][col]
            if mark:
                color = RED if mark == "X" else BLUE
                text = FONT_LARGE.render(mark, True, color)
                rect = text.get_rect(center=(col * CELL_SIZE + 60, row * CELL_SIZE + 140))
                screen.blit(text, rect)

def draw_ui():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 if not game_over else end_time
    screen.blit(FONT_SMALL.render(f"X: {x_score}  O: {o_score}", True, BLACK), (20, 20))
    screen.blit(FONT_SMALL.render(f"Time: {elapsed_time}s", True, BLACK), (WIDTH - 110, 20))

    if winner:
        win_text = FONT_MEDIUM.render(f"{winner} Wins!", True, RED)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        screen.blit(win_text, win_rect)

    # Restart Button
    button_rect = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 35)
    pygame.draw.rect(screen, BRIGHT_GREEN if game_over else GREEN, button_rect, border_radius=10)
    button_text = FONT_SMALL.render("Restart", True, BLACK)
    screen.blit(button_text, (button_rect.x + 25, button_rect.y + 7))

def draw_winning_line():
    if winning_line:
        start = winning_line[0][1] * CELL_SIZE + 60, winning_line[0][0] * CELL_SIZE + 140
        end = winning_line[2][1] * CELL_SIZE + 60, winning_line[2][0] * CELL_SIZE + 140
        pygame.draw.line(screen, RED, start, end, 6)

def show_popup_message(message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Game Over !!!", message)
    root.destroy()

def check_winner():
    global winning_line
    lines = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
    ]
    for line in lines:
        a, b, c = line
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] != "":
            winning_line = line
            return board[a[0]][a[1]]
    return None

def check_draw():
    return all(board[row][col] != "" for row in range(3) for col in range(3)) and not winner

def reset_game():
    global board, current_player, winner, game_over, winning_line, start_time, end_time
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    game_over = False
    winning_line = []
    start_time = pygame.time.get_ticks()
    end_time = 0

def get_cell_clicked(position):
    x, y = position
    if 80 <= y <= 440 and 0 <= x <= WIDTH:
        return (y - 80) // CELL_SIZE, x // CELL_SIZE
    return None

# --- Main Game Loop ---
running = True
while running:
    draw_grid()
    draw_marks()
    draw_ui()
    if winner:
        draw_winning_line()

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 40, 120, 35)

            if restart_button.collidepoint(mouse_pos):
                reset_game()

            elif not game_over:
                cell = get_cell_clicked(mouse_pos)
                if cell:
                    row, col = cell
                    if board[row][col] == "":
                        board[row][col] = current_player
                        (sound_x if current_player == "X" else sound_o).play()

                        winner = check_winner()
                        if winner:
                            game_over = True
                            if winner == "X":
                                x_score += 1
                            else:
                                o_score += 1
                            end_time = (pygame.time.get_ticks() - start_time) // 1000
                            sound_win.play()
                            show_popup_message(f"{winner} Wins!")
                        elif check_draw():
                            game_over = True
                            end_time = (pygame.time.get_ticks() - start_time) // 1000
                            sound_draw.play()
                            show_popup_message("It's a Draw!")
                        else:
                            current_player = "O" if current_player == "X" else "X"

pygame.quit()
sys.exit()