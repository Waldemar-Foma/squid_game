import pygame
import os
import time
import tkinter as tk
from tkinter import messagebox

from module.error_window import show_error_message
from module.play_screen import PlayScreen
from module.settings_screen import SettingsScreen
from module.loading_screen import LoadingScreen
from module.about_screen import AboutScreen


class Game:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()

        # Статистика
        self.stats = {
            "play_clicks": 0,
            "settings_clicks": 0,
            "continue_clicks": 0,
            "new_game_clicks": 0,
            "stats_clicks": 0,
            "about_clicks": 0  # Добавляем статистику для кнопки "О проекте"
        }

        # Настройки экрана
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Игра в кальмара")

        # Флаг полноэкранного режима
        self.fullscreen = False

        # Шрифт для экрана загрузки
        self.font_path = os.path.join("data/play_font.otf")
        try:
            self.pixel_font = pygame.font.Font(self.font_path, 72)
            self.pixel_font_small = pygame.font.Font(self.font_path, 36)
        except FileNotFoundError:
            show_error_message(f"ОШИБКА: Файл шрифта не найден по пути: {self.font_path}")

        # Надпись в левом нижнем углу
        self.version_text = "Alpha_test v.0.1"
        self.version_font = pygame.font.Font("data/play_font.otf", 15)  # Шрифт для версии

        # Экран загрузки
        self.loading_screen = LoadingScreen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.pixel_font)

        # Остальные ресурсы и настройки
        self.load_resources()

        # Создание затемнения
        self.darken = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.darken.fill((0, 0, 0))
        self.darken.set_alpha(190)

        # Создание дополнительного затемнения для экрана игры
        self.darken_play = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.darken_play.fill((0, 0, 0))
        self.darken_play.set_alpha(200)

        # Текст и кнопки
        self.title_text = self.pixel_font.render("Игра в кальмара", True, (255, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))

        self.play_text = self.pixel_font_small.render("Играть", True, (255, 255, 255))
        self.play_rect = self.play_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        self.settings_text = self.pixel_font_small.render("Настройки", True, (255, 255, 255))
        self.settings_rect = self.settings_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 80))

        self.about_text = self.pixel_font_small.render("О проекте", True, (255, 255, 255))  # Кнопка "О проекте"
        self.about_rect = self.about_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 160))

        self.exit_text = self.pixel_font_small.render("Выход", True, (255, 255, 255))
        self.exit_rect = self.exit_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 240))

        # Состояния кнопок
        self.play_hovered = False
        self.settings_hovered = False
        self.about_hovered = False  # Состояние кнопки "О проекте"
        self.exit_hovered = False

        # Экран игры
        self.play_screen = PlayScreen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.pixel_font,
                                      self.pixel_font_small)

        # Экран настроек
        self.settings_screen = SettingsScreen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.pixel_font,
                                              self.pixel_font_small)
        self.settings_screen.hover_sound = self.hover_sound
        self.settings_screen.click_sound = self.click_sound

        # Экран "О проекте"
        self.about_screen = AboutScreen(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.pixel_font,
                                        self.pixel_font_small)

    def load_resources(self):
        """Загрузка ресурсов с отображением экрана загрузки."""
        clock = pygame.time.Clock()
        start_time = time.time()

        while self.loading_screen.progress < 100:
            delta_time = clock.tick(60) / 1000  # Время в секундах

            # Обновление экрана загрузки
            self.loading_screen.update(delta_time)
            self.loading_screen.draw()

            # Имитация загрузки
            if time.time() - start_time > 0.1:  # Увеличиваем прогресс каждые 0.1 секунды
                self.loading_screen.progress += 1
                start_time = time.time()

        # Загрузка остальных ресурсов
        try:
            self.background = pygame.image.load(os.path.join("data", "background.png"))
            self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        except FileNotFoundError:
            show_error_message(
                f"ОШИБКА: Фоновое изображение не найдено по пути: {os.path.join('data', 'background.png')}")

        try:
            self.hover_sound = pygame.mixer.Sound(os.path.join("data", "sounds", "hover.mp3"))
            self.click_sound = pygame.mixer.Sound(os.path.join("data", "sounds", "click.mp3"))
        except FileNotFoundError:
            show_error_message(f"ОШИБКА: Звуковые файлы не найдены по пути: {os.path.join('data', 'sounds')}")

        # Загрузка и воспроизведение музыки
        try:
            self.music_path = os.path.join("data", "sounds", "background_music.mp3")
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)  # Зацикливание музыки
        except FileNotFoundError:
            print(f"ОШИБКА: Музыкальный файл не найден по пути: {self.music_path}")
        except pygame.error as e:
            print(f"ОШИБКА: Не удалось загрузить музыку. {e}")

    def show_stats(self):
        """Отображение статистики в окне Tkinter."""
        root = tk.Tk()
        root.withdraw()  # Скрываем основное окно Tkinter

        stats_message = (
            f"Нажатий на 'Играть': {self.stats['play_clicks']}\n"
            f"Нажатий на 'Настройки': {self.stats['settings_clicks']}\n"
            f"Нажатий на 'Продолжить': {self.stats['continue_clicks']}\n"
            f"Нажатий на 'Новая игра': {self.stats['new_game_clicks']}\n"
            f"Нажатий на 'Статистика': {self.stats['stats_clicks']}\n"
            f"Нажатий на 'О проекте': {self.stats['about_clicks']}"
        )
        messagebox.showinfo("Статистика", stats_message)

    def toggle_fullscreen(self):
        """Переключение между полноэкранным и оконным режимом."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.update_screen_elements()  # Обновляем элементы интерфейса после изменения режима

    def update_screen_elements(self):
        """Обновление элементов экрана при изменении размера окна."""
        # Обновление позиций текста и кнопок
        self.title_rect = self.title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))
        self.play_rect = self.play_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        self.settings_rect = self.settings_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 80))
        self.about_rect = self.about_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 160))
        self.exit_rect = self.exit_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 240))

        # Обновление фонового изображения
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.darken = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.darken.fill((0, 0, 0))
        self.darken.set_alpha(190)
        self.darken_play = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.darken_play.fill((0, 0, 0))
        self.darken_play.set_alpha(200)

        # Обновление позиций элементов в PlayScreen, SettingsScreen и AboutScreen
        self.play_screen.update_screen_size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.settings_screen.update_screen_size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.about_screen.update_screen_size(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def draw_version_text(self):
        """Отрисовка надписи 'PARADOX STUDIO v1.0' в левом нижнем углу."""
        version_surface = self.version_font.render(self.version_text, True, (255, 255, 255))
        version_rect = version_surface.get_rect(bottomleft=(20, self.SCREEN_HEIGHT - 20))
        self.screen.blit(version_surface, version_rect)

    def run(self):
        """Основной цикл игры."""
        running = True
        in_play_screen = False
        in_settings_screen = False
        in_about_screen = False  # Флаг для экрана "О проекте"

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                # Обработка изменения размера окна
                if event.type == pygame.VIDEORESIZE:
                    self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.size
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
                    self.update_screen_elements()

                if in_play_screen:
                    result = self.play_screen.handle_event(event)
                    if result == "back":
                        in_play_screen = False
                    elif result == "continue":
                        self.stats["continue_clicks"] += 1
                        print("Продолжить игру")
                    elif result == "new_game":
                        self.stats["new_game_clicks"] += 1
                        print("Начать новую игру")
                    elif result == "stats":
                        self.stats["stats_clicks"] += 1
                        self.show_stats()
                elif in_settings_screen:
                    result = self.settings_screen.handle_event(event)
                    if result == "back":
                        in_settings_screen = False
                elif in_about_screen:  # Обработка событий на экране "О проекте"
                    result = self.about_screen.handle_event(event)
                    if result == "back":
                        in_about_screen = False
                else:
                    if event.type == pygame.MOUSEMOTION:
                        mouse_pos = pygame.mouse.get_pos()

                        # Проверка наведения на кнопку "Играть"
                        if self.play_rect.collidepoint(mouse_pos):
                            if not self.play_hovered:  # Звук воспроизводится только при первом наведении
                                self.hover_sound.play()
                            self.play_hovered = True
                        else:
                            self.play_hovered = False

                        # Проверка наведения на кнопку "Настройки"
                        if self.settings_rect.collidepoint(mouse_pos):
                            if not self.settings_hovered:  # Звук воспроизводится только при первом наведении
                                self.hover_sound.play()
                            self.settings_hovered = True
                        else:
                            self.settings_hovered = False

                        # Проверка наведения на кнопку "О проекте"
                        if self.about_rect.collidepoint(mouse_pos):
                            if not self.about_hovered:  # Звук воспроизводится только при первом наведении
                                self.hover_sound.play()
                            self.about_hovered = True
                        else:
                            self.about_hovered = False

                        # Проверка наведения на кнопку "Выход"
                        if self.exit_rect.collidepoint(mouse_pos):
                            if not self.exit_hovered:  # Звук воспроизводится только при первом наведении
                                self.hover_sound.play()
                            self.exit_hovered = True
                        else:
                            self.exit_hovered = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.play_rect.collidepoint(mouse_pos):
                            self.stats["play_clicks"] += 1
                            self.click_sound.play()
                            in_play_screen = True
                        if self.settings_rect.collidepoint(mouse_pos):
                            self.stats["settings_clicks"] += 1
                            self.click_sound.play()
                            in_settings_screen = True
                        if self.about_rect.collidepoint(mouse_pos):  # Обработка нажатия на кнопку "О проекте"
                            self.stats["about_clicks"] += 1
                            self.click_sound.play()
                            in_about_screen = True
                        if self.exit_rect.collidepoint(mouse_pos):
                            running = False  # Завершение игры

            # Отрисовка
            if in_play_screen:
                self.play_screen.draw(self.darken_play)
            elif in_settings_screen:
                self.settings_screen.draw(self.darken)
            elif in_about_screen:  # Отрисовка экрана "О проекте"
                self.about_screen.draw(self.darken)
            else:
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.darken, (0, 0))
                self.screen.blit(self.title_text, self.title_rect)

                if self.play_hovered:
                    play_text = self.pixel_font_small.render("Играть", True, (200, 0, 0))
                else:
                    play_text = self.pixel_font_small.render("Играть", True, (255, 255, 255))
                self.screen.blit(play_text, self.play_rect)

                if self.settings_hovered:
                    settings_text = self.pixel_font_small.render("Настройки", True, (200, 0, 0))
                else:
                    settings_text = self.pixel_font_small.render("Настройки", True, (255, 255, 255))
                self.screen.blit(settings_text, self.settings_rect)

                if self.about_hovered:  # Отрисовка кнопки "О проекте"
                    about_text = self.pixel_font_small.render("О проекте", True, (200, 0, 0))
                else:
                    about_text = self.pixel_font_small.render("О проекте", True, (255, 255, 255))
                self.screen.blit(about_text, self.about_rect)

                if self.exit_hovered:
                    exit_text = self.pixel_font_small.render("Выход", True, (200, 0, 0))
                else:
                    exit_text = self.pixel_font_small.render("Выход", True, (255, 255, 255))
                self.screen.blit(exit_text, self.exit_rect)

            self.draw_version_text()

            pygame.display.flip()

        pygame.quit()
