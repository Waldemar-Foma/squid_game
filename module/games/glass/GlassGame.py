import pygame
import random
import sys
import time
import math


class Glass:
    def __init__(self, x, y, width, height, is_safe):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_safe = is_safe
        self.revealed = False
        self.selected = False

    def draw(self, screen, glass_color, green, red, yellow):
        if self.revealed:
            color = green if self.is_safe else red
        else:
            color = glass_color if not self.selected else yellow  # Подсветка выбранного стекла
        pygame.draw.rect(screen, color, self.rect, border_radius=10)  # Закругленные углы
        if self.selected:
            pygame.draw.rect(screen, yellow, self.rect, width=3, border_radius=10)  # Обводка выбранного стекла


class GlassGame:
    def __init__(self):
        # Инициализация Pygame
        pygame.init()

        # Настройки экрана
        self.WIDTH, self.HEIGHT = 1000, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Игра в Стеклянные Мосты")

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (200, 200, 200)
        self.GLASS_COLOR = (173, 216, 230)  # Светло-голубой для стекол

        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        # Загрузка фона
        try:
            self.background = pygame.image.load("backgroundglass.png")  # Замените на ваш файл фона
        except FileNotFoundError:
            print("Файл фона не найден. Убедитесь, что 'background.png' находится в той же папке.")
            sys.exit()

        # Масштабирование фона под размеры окна
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.glasses = []
        self.selected_glass = None
        self.result_text = ""
        self.result_color = self.WHITE
        self.show_result = False  # Показывать ли результат выбора
        self.result_start_time = 0  # Время появления результата
        self.last_selected_glass = None  # Сохраняем последнее выбранное стекло для отображения текста
        self.shake_offset = 0  # Смещение для анимации покачивания камеры
        self.shake_duration = 0  # Длительность анимации покачивания

        # Настройки уровня сложности (по умолчанию легкий)
        self.lives = 3  # Количество жизней в легком режиме
        self.num_pairs = 5  # Количество пар стекол
        self.current_pair = 0  # Текущая пара стекол

        self.running = True
        self.game_over = False

    def draw_text(self, text, x, y, color=None, font_type=None):
        if color is None:
            color = self.WHITE
        if font_type is None:
            font_type = self.font
        text_surface = font_type.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def shake_screen(self, offset):
        self.screen.blit(self.background, (offset, 0))  # Сдвигаем фон по горизонтали

    def draw_cross(self, rect, color):
        # Рисуем две диагональные линии
        pygame.draw.line(self.screen, color, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), 5)
        pygame.draw.line(self.screen, color, (rect.x + rect.width, rect.y), (rect.x, rect.y + rect.height), 5)

    def main(self):
        # Основной игровой цикл
        while self.running:
            self.screen.fill(self.BLACK)  # Очистка экрана

            # Анимация покачивания камеры
            if self.shake_duration > 0:
                self.shake_offset = 5 * math.sin(time.time() * 20)  # Синусоидальное смещение
                self.shake_duration -= 1
            else:
                self.shake_offset = 0

            # Отрисовка фона с учетом смещения
            self.screen.blit(self.background, (self.shake_offset, 0))

            if self.game_over:
                # Экран проигрыша
                self.draw_text("Вы проиграли!", self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50, self.RED, self.large_font)
                self.draw_text("Нажмите ESC для выхода", self.WIDTH // 2 - 200, self.HEIGHT // 2 + 50, self.WHITE)
            else:
                # Создание стекол только при начале новой пары
                if self.current_pair < self.num_pairs and not self.glasses:
                    # Позиции стекол
                    glass1 = Glass(200, 200, 250, 200, random.choice([True, False]))  # Левое стекло
                    glass2 = Glass(550, 200, 250, 200, not glass1.is_safe)  # Правое стекло
                    self.glasses = [glass1, glass2]

                # Отрисовка стекол
                for glass in self.glasses:
                    glass.draw(self.screen, self.GLASS_COLOR, self.GREEN, self.RED, self.YELLOW)

                # Отрисовка результата выбора под стеклом
                if self.show_result and time.time() - self.result_start_time < 1:  # Показывать результат 1 секунду
                    if self.last_selected_glass:
                        text_x = self.last_selected_glass.rect.centerx - 50  # Центрируем текст под стеклом
                        text_y = self.last_selected_glass.rect.bottom + 10  # Позиция под стеклом
                        self.draw_text(self.result_text, text_x, text_y, self.result_color, self.font)
                else:
                    self.show_result = False  # Скрыть результат после 1 секунды

                # Отрисовка текста
                self.draw_text(f"Жизни: {self.lives}", 10, 10)
                self.draw_text(f"Пара: {self.current_pair + 1}/{self.num_pairs}", 10, 50)

                # Подсказка для игрока
                if self.selected_glass is None:
                    self.draw_text("Выберите стекло", self.WIDTH // 2 - 100, 100, self.WHITE, self.font)
                else:
                    self.draw_text("Нажмите ПРОБЕЛ чтобы прыгнуть", self.WIDTH // 2 - 200, 100, self.WHITE, self.font)

                # Если все пары пройдены
                if self.current_pair >= self.num_pairs:
                    self.draw_text("Вы прошли все пары!", self.WIDTH // 2 - 150, self.HEIGHT // 2, self.GREEN, self.large_font)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    self.running = False

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.game_over:
                        if self.current_pair < self.num_pairs:
                            # Выбор стекла
                            if self.selected_glass is None:
                                for glass in self.glasses:
                                    if glass.rect.collidepoint(pos):
                                        self.selected_glass = glass
                                        glass.selected = True
                                        self.result_text = ""
                                        self.result_color = self.WHITE
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.selected_glass is not None:
                        if self.selected_glass.is_safe:
                            self.result_text = "Правильно!"
                            self.result_color = self.GREEN
                            self.current_pair += 1
                        else:
                            self.lives -= 1
                            if self.lives == 0:
                                self.game_over = True
                            else:
                                self.result_text = "Ошибка!"
                                self.result_color = self.RED
                        self.show_result = True  # Показать результат
                        self.result_start_time = time.time()  # Засечь время появления результата
                        self.last_selected_glass = self.selected_glass  # Сохраняем выбранное стекло для отображения текста
                        self.selected_glass.revealed = True
                        self.selected_glass.selected = False
                        self.selected_glass = None
                        self.glasses = []  # Сбрасываем стекла для следующей пары
                        self.shake_duration = 30  # Запуск анимации покачивания камеры
                    if event.key == pygame.K_ESCAPE and self.game_over:
                        self.running = False

            pygame.display.flip()

        sys.exit()


if __name__ == "__main__":
    game = GlassGame()
    game.main()
