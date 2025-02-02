import pygame
import os
import time
import math


class LoadingScreen:
    def __init__(self, screen, screen_width, screen_height, font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

        # Текст
        self.title_text = "BY PARADOX_TEAM"
        self.loading_text = "Загрузка..."

        # Уменьшенный шрифт для текста
        self.small_font = pygame.font.Font("data/play_font.otf", 36)  # Шрифт с размером 36

        # Статус-бар
        self.status_bar_width = 600  # Ширина статус-бара
        self.status_bar_height = 30  # Высота статус-бара
        self.status_bar_color = (255, 0, 0)  # Цвет заполнения статус-бара
        self.status_bar_bg_color = (50, 50, 50)  # Цвет фона статус-бара
        self.status_bar_rect = pygame.Rect(
            (self.screen_width - self.status_bar_width) // 2,  # Позиция по X
            self.screen_height // 2 + 50,  # Позиция по Y
            self.status_bar_width,
            self.status_bar_height
        )

        # Прогресс загрузки
        self.progress = 0
        self.progress_speed = 0.5  # Скорость увеличения прогресса

    def draw(self):
        """Отрисовка экрана загрузки."""
        self.screen.fill((0, 0, 0))  # Черный фон

        # Отрисовка текста "BY PARADOX COMAND"
        title_surface = self.small_font.render(self.title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_surface, title_rect)

        # Отрисовка текста "Загрузка..."
        loading_surface = self.small_font.render(self.loading_text, True, (255, 255, 255))
        loading_rect = loading_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(loading_surface, loading_rect)

        # Отрисовка статус-бара
        pygame.draw.rect(self.screen, self.status_bar_bg_color, self.status_bar_rect)  # Фон статус-бара
        filled_width = int(self.status_bar_width * (self.progress / 100))  # Ширина заполненной части
        filled_rect = pygame.Rect(self.status_bar_rect.x, self.status_bar_rect.y, filled_width, self.status_bar_height)
        pygame.draw.rect(self.screen, self.status_bar_color, filled_rect)  # Заполненная часть

        # Отрисовка прогресса загрузки в процентах (округление до двух знаков)
        progress_surface = self.small_font.render(f"{round(self.progress, 2)}%", True, (255, 255, 255))
        progress_rect = progress_surface.get_rect(center=(self.screen_width // 2, self.status_bar_rect.y + 50))
        self.screen.blit(progress_surface, progress_rect)

        pygame.display.flip()

    def update(self, delta_time):
        """Обновление состояния экрана загрузки."""
        self.progress = min(self.progress + self.progress_speed * delta_time * 60, 100)
