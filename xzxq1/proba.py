import pygame
import time
from module.games.glass.GlassGame import GlassGame
from module.games.roulette.RouletteGame import RussianRoulette

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Главное меню")

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Функция для отображения текста на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Функция для главного меню
def main_menu(games, game_names):
    font = pygame.font.Font(None, 48)
    menu_running = True
    selected_game = 0

    while menu_running:
        screen.fill(WHITE)

        # Отображение названия игры и списка доступных игр
        draw_text("Выберите игру", font, BLACK, screen, screen_width // 2, screen_height // 4)

        for i, game_name in enumerate(game_names):
            color = RED if i == selected_game else BLACK
            draw_text(game_name, font, color, screen, screen_width // 2, screen_height // 2 + i * 60)

        pygame.display.update()

        # Обработка событий для навигации по меню
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_game = (selected_game + 1) % len(games)
                elif event.key == pygame.K_UP:
                    selected_game = (selected_game - 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    run_games_in_order(games)

# Функция для последовательного запуска игр
def run_games_in_order(games):
    for game_func in games:
        game_func()

# Пример функций для игр
def load_game1():
    print("Запуск игры 1")
    game = GlassGame()
    game.main()  # Ждет завершения игры


def load_game2():
    print("Запуск игры 2")
    game = RussianRoulette()
    game.main()  # Ждет завершения игры

# Список доступных игр и их названия
games = [load_game1, load_game2]
game_names = ["Игра 1", "Игра 2"]

# Запуск меню
main_menu(games, game_names)
