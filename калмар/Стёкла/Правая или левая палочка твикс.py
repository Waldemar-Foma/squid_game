import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Стеклянная Игра")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
TURQUOISE = (64, 224, 208)  # Бирюзовый цвет
LIGHT_TURQUOISE = (144, 255, 240)  # Светло-бирюзовый для эффектов

# Шрифты
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Класс для стекол
class Glass:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.broken = False
        self.hovered = False

    def draw(self, screen):
        # Рисуем стекло с тенью
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 50))
        screen.blit(shadow, (self.rect.x + 5, self.rect.y + 5))

        # Рисуем стекло
        pygame.draw.rect(screen, self.color, self.rect)

        # Эффект при наведении
        if self.hovered:
            highlight = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, self.rect.topleft)

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hovered = False

    def draw(self, screen):
        # Рисуем кнопку с тенью
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 50))
        screen.blit(shadow, (self.rect.x + 5, self.rect.y + 5))

        # Рисуем кнопку
        pygame.draw.rect(screen, self.color, self.rect)

        # Эффект при наведении
        if self.hovered:
            highlight = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, self.rect.topleft)

        # Текст кнопки
        draw_text(self.text, self.rect.x + 10, self.rect.y + 10, BLACK)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Функция для отображения текста
def draw_text(text, x, y, color=WHITE, font_type=font):
    text_surface = font_type.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Основная функция игры
def main():
    # Настройки уровня сложности
    difficulty = None
    lives = 0
    checks = 0
    num_pairs = 5
    current_pair = 0

    # Кнопки для выбора сложности
    easy_button = Button(100, 200, 200, 50, "Лёгкий", GRAY)
    medium_button = Button(100, 300, 200, 50, "Средний", GRAY)
    hard_button = Button(100, 400, 200, 50, "Сложный", GRAY)

    # Кнопки для выбора действия
    check_button = Button(500, 500, 120, 50, "Проверить", GRAY)
    jump_button = Button(650, 500, 120, 50, "Прыгнуть", GRAY)

    # Кнопка "Закрыть" на экране проигрыша
    close_button = Button(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50, "Закрыть", GRAY)

    # Основной игровой цикл
    running = True
    game_started = False
    game_over = False
    selected_glass = None
    result_text = ""
    result_color = WHITE
    glasses = []
    broken_glass = None

    while running:
        screen.fill(BLACK)

        # Фоновый градиент
        for y in range(HEIGHT):
            # Ограничиваем значения цветов в диапазоне 0–255
            r = min(y // 3, 255)
            g = min(y // 2, 255)
            b = min(y, 255)
            color = (r, g, b)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))

        if not game_started:
            # Отрисовка кнопок выбора сложности
            easy_button.draw(screen)
            medium_button.draw(screen)
            hard_button.draw(screen)
            draw_text("Выберите уровень сложности:", 100, 100, WHITE, title_font)
        elif game_over:
            # Экран проигрыша
            draw_text("Вы проиграли!", WIDTH // 2 - 100, HEIGHT // 2 - 50, RED, title_font)
            close_button.draw(screen)
        else:
            # Создание стекол только при начале новой пары
            if current_pair < num_pairs and not glasses:
                glass1 = Glass(200, 300, 100, 200, TURQUOISE)  # Бирюзовый цвет
                glass2 = Glass(500, 300, 100, 200, TURQUOISE)  # Бирюзовый цвет
                glasses = [glass1, glass2]

                # Выбор случайного стекла, которое будет сломано
                broken_glass = random.choice(glasses)
                broken_glass.broken = True

            # Отрисовка стекол
            for glass in glasses:
                glass.hovered = glass.rect.collidepoint(pygame.mouse.get_pos())
                glass.draw(screen)

            # Отрисовка текста
            draw_text(f"Жизни: {lives}", 10, 10)
            draw_text(f"Проверки: {checks}", 10, 50)
            draw_text(f"Пара: {current_pair + 1}/{num_pairs}", 10, 90)
            draw_text(result_text, WIDTH // 2 - 100, HEIGHT // 2 - 50, result_color, title_font)

            # Подсказка для игрока
            if selected_glass is None:
                draw_text("Выберите стекло", WIDTH // 2 - 100, HEIGHT - 500, WHITE)
            else:
                draw_text("Выберите действие: Проверить или Прыгнуть", WIDTH // 2 - 200, HEIGHT - 500, WHITE)

            # Отрисовка кнопок действий
            check_button.draw(screen)
            jump_button.draw(screen)

            # Если все пары пройдены
            if current_pair >= num_pairs:
                draw_text("Вы прошли все пары!", WIDTH // 2 - 150, HEIGHT // 2, GREEN, title_font)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not game_started:
                    if easy_button.is_clicked(pos):
                        difficulty = "лёгкий"
                        lives = 3
                        checks = 2
                        game_started = True
                    elif medium_button.is_clicked(pos):
                        difficulty = "средний"
                        lives = 2
                        checks = 1
                        game_started = True
                    elif hard_button.is_clicked(pos):
                        difficulty = "сложный"
                        lives = 1
                        checks = 1
                        game_started = True
                elif game_over:
                    if close_button.is_clicked(pos):
                        running = False
                else:
                    if current_pair < num_pairs:
                        # Выбор стекла
                        if selected_glass is None:
                            for glass in glasses:
                                if glass.rect.collidepoint(pos):
                                    selected_glass = glass
                                    result_text = ""
                                    result_color = WHITE
                        # Выбор действия
                        elif check_button.is_clicked(pos):
                            if checks > 0:
                                if selected_glass.broken:
                                    result_text = "Стекло сломано!"
                                    result_color = RED
                                else:
                                    result_text = "Стекло целое!"
                                    result_color = GREEN
                                checks -= 1
                            else:
                                result_text = "Нет проверок!"
                                result_color = YELLOW
                            selected_glass = None  # Сброс выбора стекла после проверки
                        elif jump_button.is_clicked(pos):
                            if selected_glass.broken:
                                lives -= 1
                                if lives == 0:
                                    game_over = True
                                else:
                                    result_text = "Вы ошиблись!"
                                    result_color = RED
                            else:
                                result_text = "Вы выбрали правильное стекло!"
                                result_color = GREEN
                                current_pair += 1
                            selected_glass = None
                            glasses = []  # Сбрасываем стекла для следующей пары

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()