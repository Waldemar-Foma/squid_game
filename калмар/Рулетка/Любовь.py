import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Русская рулетка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Шрифты
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Переменные игры
bullets = [0, 0, 0, 0, 0, 1]  # 1 - пуля, 0 - пустой патрон
random.shuffle(bullets)
current_turn = "player"  # Игрок или бот
player_shot_used = False  # Использовал ли игрок выстрел в соперника
bot_shot_used = False  # Использовал ли бот выстрел в соперника
game_over = False
message = ""  # Сообщение о результате выстрела


def draw_text(text, x, y, color=BLACK, font_type=font):
    text_surface = font_type.render(text, True, color)
    screen.blit(text_surface, (x, y))


def reset_game():
    global bullets, current_turn, player_shot_used, bot_shot_used, game_over, message
    bullets = [0, 0, 0, 0, 0, 1]
    random.shuffle(bullets)
    current_turn = "player"
    player_shot_used = False
    bot_shot_used = False
    game_over = False
    message = ""


def bot_turn():
    global current_turn, bot_shot_used, game_over, message
    if not game_over:
        # Бот решает, стрелять в себя или в игрока (если еще не использовал выстрел в соперника)
        if not bot_shot_used and random.random() < 0.2:  # 50% шанс выстрелить в игрока
            bot_shot_used = True
            if bullets.pop(0) == 1:
                message = "Вы умерли!"
                game_over = True
            else:
                message = "Вы выжили!"
        else:
            if bullets.pop(0) == 1:
                message = "Противник умер!"
                game_over = True
            else:
                message = "Противник выжил!"
        current_turn = "player"


# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_s:  # Игрок стреляет в себя
                if bullets.pop(0) == 1:
                    message = "Вы умерли!"
                    game_over = True
                else:
                    message = "Вы выжили!"
                    current_turn = "bot"
            elif event.key == pygame.K_a and not player_shot_used:  # Игрок стреляет в бота
                player_shot_used = True
                if bullets.pop(0) == 1:
                    message = "Противник умер!"
                    game_over = True
                else:
                    message = "Противник выжил!"
                    current_turn = "bot"

        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Перезапуск игры
                reset_game()


    # Отображение текущего состояния игры
    if not game_over:
        if current_turn == "player":
            pass
        else:
            draw_text("Ход бота...", 300, 100)
            pygame.display.flip()
            pygame.time.wait(1000)  # Задержка для имитации "думания" бота
            bot_turn()

    # Отображение результата выстрела
    if message:
        draw_text(message, 200, 200, BLACK if "проиграл" in message else BLACK)

    # Отображение правил внизу экрана
    draw_text("Правила:", 10, HEIGHT - 125, BLACK, small_font)
    draw_text("1. Нажмите S, чтобы выстрелить в себя.", 10, HEIGHT - 100, BLACK, small_font)
    draw_text("2. Нажмите A, чтобы выстрелить в бота (одна попытка).", 10, HEIGHT - 75, BLACK, small_font)
    draw_text("3. Бот также может выстрелить в вас один раз.", 10, HEIGHT - 50, BLACK, small_font)
    draw_text("4. Рестарт на R.", 10, HEIGHT - 25, BLACK, small_font)

    pygame.display.flip()

pygame.quit()