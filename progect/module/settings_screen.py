import pygame
import os
import json

class SettingsScreen:
    def __init__(self, screen, screen_width, screen_height, font, small_font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font
        self.small_font = small_font

        # Загрузка фонового изображения
        self.background_path = os.path.join("data/background.png")
        self.load_background()

        # Затемненное поле под кнопки
        self.dark_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.dark_surface.fill((0, 0, 0, 128))  # Полупрозрачное затемнение

        # Настройки
        self.settings = self.load_settings()
        self.music_volume = self.settings.get("music_volume", 0.5)
        self.sound_volume = self.settings.get("sound_volume", 0.5)
        self.difficulty = self.settings.get("difficulty", "medium")

        # Ползунки громкости
        self.slider_width = 200
        self.slider_height = 10
        self.slider_x = (self.screen_width - self.slider_width) // 2
        self.slider_y_music = self.screen_height // 2 - 50  # Позиция ползунка музыки
        self.slider_y_sound = self.screen_height // 2 + 20  # Позиция ползунка звуков
        self.slider_rect_music = pygame.Rect(self.slider_x, self.slider_y_music, self.slider_width, self.slider_height)
        self.slider_rect_sound = pygame.Rect(self.slider_x, self.slider_y_sound, self.slider_width, self.slider_height)
        self.slider_handle_radius = 10
        self.slider_handle_x_music = self.slider_x + int(self.music_volume * self.slider_width)
        self.slider_handle_x_sound = self.slider_x + int(self.sound_volume * self.slider_width)

        # Текст для выбора сложности
        self.difficulty_text = f"Сложность: {self.difficulty.capitalize()}"
        self.difficulty_text_pos = (self.screen_width // 2, self.screen_height // 2 - 150)  # Позиция текста сложности
        self.difficulty_text_rect = None  # Для обработки кликов

        # Кнопка "Назад"
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 100, 200, 50
        )  # Позиция кнопки "Назад"

    def load_background(self):
        """Загрузка и масштабирование фонового изображения."""
        try:
            self.background = pygame.image.load(self.background_path)
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            print("ОШИБКА: Фоновое изображение не найдено по пути:", self.background_path)
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 0, 0))  # Черный фон, если изображение не найдено

    def load_settings(self):
        """Загрузка настроек из файла."""
        settings_path = os.path.join("data/settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_settings(self):
        """Сохранение настроек в файл."""
        settings_path = os.path.join("data/settings.json")
        with open(settings_path, "w", encoding="utf-8") as file:
            json.dump({
                "music_volume": self.music_volume,
                "sound_volume": self.sound_volume,
                "difficulty": self.difficulty
            }, file)

    def update_screen_size(self, new_width, new_height):
        """Обновление размеров экрана и перерисовка элементов."""
        self.screen_width = new_width
        self.screen_height = new_height
        self.load_background()
        self.slider_x = (self.screen_width - self.slider_width) // 2
        self.slider_rect_music = pygame.Rect(self.slider_x, self.slider_y_music, self.slider_width, self.slider_height)
        self.slider_rect_sound = pygame.Rect(self.slider_x, self.slider_y_sound, self.slider_width, self.slider_height)
        self.slider_handle_x_music = self.slider_x + int(self.music_volume * self.slider_width)
        self.slider_handle_x_sound = self.slider_x + int(self.sound_volume * self.slider_width)
        self.difficulty_text_pos = (self.screen_width // 2, self.screen_height // 2 - 150)  # Обновляем позицию текста
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 100, 200, 50
        )  # Обновляем позицию кнопки "Назад"

    def draw(self, darken_surface):
        """Отрисовка экрана настроек."""
        # Отрисовка фона
        self.screen.blit(self.background, (0, 0))

        # Затемнение фона
        self.screen.blit(darken_surface, (0, 0))

        # Отрисовка текста сложности
        self.draw_difficulty_text()

        # Отрисовка ползунков громкости
        self.draw_volume_slider()

        # Отрисовка кнопки "Назад"
        self.draw_button("Назад", self.back_button_rect)

        pygame.display.flip()

    def draw_button(self, text, rect):
        """Отрисовка кнопки."""
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos)
        button_color = (150, 150, 150) if not hovered else (200, 200, 200)  # Осветление при наведении
        pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
        text_surface = self.small_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_difficulty_text(self):
        """Отрисовка текста для выбора сложности."""
        text_surface = self.small_font.render(self.difficulty_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.difficulty_text_pos)
        self.screen.blit(text_surface, text_rect)
        self.difficulty_text_rect = text_rect  # Сохраняем rect для обработки кликов

    def draw_volume_slider(self):
        """Отрисовка стилизованных ползунков громкости."""
        # Ползунок для музыки
        self.draw_slider(self.slider_rect_music, self.slider_handle_x_music, self.slider_y_music, "Музыка")

        # Ползунок для звуков
        self.draw_slider(self.slider_rect_sound, self.slider_handle_x_sound, self.slider_y_sound, "Звуки")

    def draw_slider(self, slider_rect, handle_x, y, label):
        """Отрисовка одного ползунка."""
        # Фон ползунка
        pygame.draw.rect(self.screen, (100, 100, 100), slider_rect, border_radius=5)

        # Активная часть ползунка (градиент или цвет)
        active_width = handle_x - slider_rect.x
        active_rect = pygame.Rect(slider_rect.x, slider_rect.y, active_width, slider_rect.height)
        pygame.draw.rect(self.screen, (255, 0, 0), active_rect, border_radius=5)

        # Ручка ползунка
        pygame.draw.circle(self.screen, (255, 255, 255), (handle_x, y + self.slider_height // 2), self.slider_handle_radius)

        # Текст
        label_surface = self.small_font.render(label, True, (255, 255, 255))
        self.screen.blit(label_surface, (slider_rect.x - 100, y - 20))

    def handle_event(self, event):
        """Обработка событий на экране настроек."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            # Перемещение ручек ползунков
            if event.buttons[0]:  # Если зажата левая кнопка мыши
                if self.slider_rect_music.collidepoint(mouse_pos):
                    self.slider_handle_x_music = max(self.slider_x, min(mouse_pos[0], self.slider_x + self.slider_width))
                    self.music_volume = (self.slider_handle_x_music - self.slider_x) / self.slider_width
                    pygame.mixer.music.set_volume(self.music_volume)
                elif self.slider_rect_sound.collidepoint(mouse_pos):
                    self.slider_handle_x_sound = max(self.slider_x, min(mouse_pos[0], self.slider_x + self.slider_width))
                    self.sound_volume = (self.slider_handle_x_sound - self.slider_x) / self.slider_width
                    self.hover_sound.set_volume(self.sound_volume)
                    self.click_sound.set_volume(self.sound_volume)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Обработка клика по тексту сложности
            if self.difficulty_text_rect and self.difficulty_text_rect.collidepoint(mouse_pos):
                difficulties = ["easy", "medium", "hard"]
                current_index = difficulties.index(self.difficulty)
                next_index = (current_index + 1) % len(difficulties)
                self.difficulty = difficulties[next_index]
                self.difficulty_text = f"Сложность: {self.difficulty.capitalize()}"
                self.save_settings()

            # Обработка клика по кнопке "Назад"
            if self.back_button_rect.collidepoint(mouse_pos):
                self.save_settings()
                return "back"
        return None
