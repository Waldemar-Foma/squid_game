import pygame
import os


class AboutScreen:
    def __init__(self, screen, screen_width, screen_height, font, small_font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.small_font = small_font

        # Загрузка фонового изображения
        self.background_path = os.path.join("data/background.png")
        self.load_background()

        # Затемненное поле под текст
        self.dark_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.dark_surface.fill((0, 0, 0, 128))  # Полупрозрачное затемнение

        # Текст "О проекте"
        self.about_text = [
            "1) Что это за игра",
            "Это игра в кальмара, где игроки соревнуются в различных мини-играх.",
            "2) Правила",
            "Правила просты: выживай и побеждай!",
            "3) Авторы",
            "Разработано: Фоменко Владислав, Айрапетян Эрик"
        ]

        # Разбиваем текст на строки с учетом ширины экрана
        self.wrapped_text = self.wrap_text(self.about_text, self.screen_width - 100)

        # Кнопка "Назад"
        self.back_button = {"text": "Назад", "action": "back", "pos": (self.screen_width // 2, self.screen_height - 50),
                            "hovered": False}

    def wrap_text(self, text_lines, max_width):
        """Разбивает текст на строки с учетом ширины экрана."""
        wrapped_lines = []
        for line in text_lines:
            words = line.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_width, _ = self.small_font.size(test_line)
                if test_width <= max_width:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            if current_line:
                wrapped_lines.append(current_line)
        return wrapped_lines

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
        self.back_button["pos"] = (self.screen_width // 2, self.screen_height - 50)  # Обновление позиции кнопки "Назад"
        self.wrapped_text = self.wrap_text(self.about_text, self.screen_width - 100)  # Пересчет переноса текста

    def draw(self, darken_surface):
        """Отрисовка экрана 'О проекте'."""
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Затемнение фона
        self.screen.blit(darken_surface, (0, 0))

        # Отрисовка текста
        y_offset = 100
        for line in self.wrapped_text:
            text_surface = self.small_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 30  # Увеличиваем отступ между строками

        # Отрисовка кнопки "Назад"
        self.draw_button(self.back_button["text"], self.back_button["pos"], self.back_button["hovered"])

        pygame.display.flip()

    def draw_button(self, text, pos, hovered):
        """Отрисовка кнопки."""
        button_color = (255, 255, 255) if not hovered else (200, 200, 200)
        button_surface = self.small_font.render(text, True, button_color)
        button_rect = button_surface.get_rect(center=pos)
        self.screen.blit(button_surface, button_rect)

    def handle_event(self, event):
        """Обработка событий на экране 'О проекте'."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            button_surface = self.small_font.render(self.back_button["text"], True, (255, 255, 255))
            button_rect = button_surface.get_rect(center=self.back_button["pos"])
            self.back_button["hovered"] = button_rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_surface = self.small_font.render(self.back_button["text"], True, (255, 255, 255))
            button_rect = button_surface.get_rect(center=self.back_button["pos"])
            if button_rect.collidepoint(mouse_pos):
                return "back"
        return None
