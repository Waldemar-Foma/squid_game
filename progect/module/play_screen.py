import pygame
import os


class PlayScreen:
    def __init__(self, screen, screen_width, screen_height, font, small_font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.small_font = small_font

        # Загрузка фонового изображения
        self.background_path = os.path.join("data/background.png")
        self.load_background()

        # Кнопки
        self.buttons = [
            {"text": "Продолжить игру", "action": "continue", "pos":
                (self.screen_width // 2, self.screen_height // 2 - 80), "hovered": False},
            {"text": "Начать новую игру", "action": "new_game", "pos":
                (self.screen_width // 2, self.screen_height // 2), "hovered": False},
            {"text": "Статистика", "action": "stats", "pos":
                (self.screen_width // 2, self.screen_height // 2 + 80), "hovered": False},
            {"text": "Назад", "action": "back", "pos":
                (self.screen_width // 2, self.screen_height // 2 + 160), "hovered": False}
        ]

        # Звук при наведении на кнопки
        self.hover_sound = pygame.mixer.Sound(os.path.join("data", "sounds", "hover.mp3"))

        # Надпись в левом нижнем углу
        self.version_text = "Alpha_test v.0.1"
        self.version_font = pygame.font.Font("data/play_font.otf", 15)  # Шрифт для версии

    def load_background(self):
        """Загрузка и масштабирование фонового изображения."""
        try:
            self.background = pygame.image.load(self.background_path)
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            print("ОШИБКА: Фоновое изображение не найдено по пути:", self.background_path)
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 0, 0))  # Черный фон, если изображение не найдено

    def update_screen_size(self, new_width, new_height):
        """Обновление размеров экрана и перерисовка элементов."""
        self.screen_width = new_width
        self.screen_height = new_height
        self.load_background()  # Перезагрузка фона с новыми размерами
        for button in self.buttons:
            button["pos"] = (self.screen_width // 2, button["pos"][1])  # Обновление позиций кнопок

    def draw(self, darken_surface):
        """Отрисовка экрана игры."""
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Затемнение фона
        self.screen.blit(darken_surface, (0, 0))

        # Отрисовка кнопок
        for button in self.buttons:
            self.draw_button(button["text"], button["pos"], button["hovered"])

        # Отрисовка надписи
        version_surface = self.version_font.render(self.version_text, True, (255, 255, 255))
        version_rect = version_surface.get_rect(bottomleft=(20, self.screen_height - 20))
        self.screen.blit(version_surface, version_rect)

        pygame.display.flip()

    def draw_button(self, text, pos, hovered):
        """Отрисовка кнопки."""
        button_color = (255, 255, 255) if not hovered else (200, 200, 200)
        button_surface = self.small_font.render(text, True, button_color)
        button_rect = button_surface.get_rect(center=pos)
        self.screen.blit(button_surface, button_rect)

    def handle_event(self, event):
        """Обработка событий на экране игры."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button_surface = self.small_font.render(button["text"], True, (255, 255, 255))
                button_rect = button_surface.get_rect(center=button["pos"])
                if button_rect.collidepoint(mouse_pos):
                    if not button["hovered"]:  # Звук воспроизводится только при первом наведении
                        self.hover_sound.play()
                    button["hovered"] = True
                else:
                    button["hovered"] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button_surface = self.small_font.render(button["text"], True, (255, 255, 255))
                button_rect = button_surface.get_rect(center=button["pos"])
                if button_rect.collidepoint(mouse_pos):
                    return button["action"]  # Возвращаем действие кнопки
        return None
