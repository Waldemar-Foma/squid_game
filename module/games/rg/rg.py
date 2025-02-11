import pygame
import random
import cv2
import numpy as np
import time
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox


class SquidGame:
    def __init__(self):
        pygame.init()
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Squid Game")

        self.folderPath = 'frames'
        self.mylist = os.listdir(self.folderPath)
        self.graphic = [pygame.image.load(f'{self.folderPath}/{imPath}') for imPath in self.mylist]

        self.green = pygame.transform.scale(self.graphic[0], (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.red = pygame.transform.scale(self.graphic[1], (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.kill = pygame.transform.scale(self.graphic[2], (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.winner = pygame.transform.scale(self.graphic[3], (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.intro = pygame.transform.scale(self.graphic[4], (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.TIMER_MAX = 80
        self.TIMER = self.TIMER_MAX
        self.maxMove = 6500000
        self.win = False
        self.isgreen = True

        self.font = pygame.font.SysFont("Arial", 50)

        self.cap = cv2.VideoCapture(0)

        self.prev = time.time()
        self.prevDoll = time.time()

        self.showFrame = self.green

        self.hold_time_required = 30
        self.hold_start_time = None
        self.hold_progress = 0

        self.running = True

        self.check_camera_prompt()

    def check_camera_prompt(self):
        root = tk.Tk()
        root.title("Проверка камеры")
        root.geometry("300x100")

        label = tk.Label(root, text="У вас есть камера?")
        label.pack(pady=10)

        yes_button = tk.Button(root, text="Да", command=root.destroy)
        yes_button.pack(side=tk.LEFT, padx=20)

        no_button = tk.Button(root, text="Нет", command=self.on_no)
        no_button.pack(side=tk.RIGHT, padx=20)

        root.mainloop()

        if not self.check_camera():
            messagebox.showerror("Ошибка", "Камера не найдена. Игра не может быть запущена.")
            webbrowser.open("https://www.dns-shop.ru/product/a16647327518ed20/veb-kamera-dexp-df2m3fm1/")
            exit()

    def on_no(self):
        webbrowser.open("https://www.dns-shop.ru/product/a16647327518ed20/veb-kamera-dexp-df2m3fm1/")
        exit()

    def check_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False
        cap.release()
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                if self.isgreen and event.key == pygame.K_w:
                    if self.hold_start_time is None:
                        self.hold_start_time = time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    if self.hold_start_time is not None:
                        self.hold_progress += (time.time() - self.hold_start_time) / self.hold_time_required
                        self.hold_start_time = None

    def update_timer(self):
        cur = time.time()
        if cur - self.prev >= 1:
            self.prev = cur
            self.TIMER -= 1

    def update_doll(self):
        cur = time.time()
        no = random.randint(3, 5)
        if cur - self.prevDoll >= no:
            self.prevDoll = cur
            if self.isgreen:
                self.showFrame = self.red
                self.isgreen = False
                ret, frame = self.cap.read()
                if ret:
                    self.ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                self.showFrame = self.green
                self.isgreen = True

    def check_movement(self):
        if not self.isgreen:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frameDelta = cv2.absdiff(self.ref, gray)
                thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
                change = np.sum(thresh)
                if change > self.maxMove:
                    self.running = False

    def check_win(self):
        cur = time.time()
        if self.isgreen and self.hold_start_time is not None:
            current_progress = (cur - self.hold_start_time) / self.hold_time_required
            total_progress = self.hold_progress + current_progress
            if total_progress >= 1.0:
                self.win = True
                self.running = False

    def draw(self):
        self.window.blit(self.showFrame, (0, 0))

        timer_text = self.font.render(f"Time: {self.TIMER}", True, (255, 255, 255))
        self.window.blit(timer_text, (50, 50))

        if self.isgreen:
            total_progress = self.hold_progress
            if self.hold_start_time is not None:
                total_progress += (time.time() - self.hold_start_time) / self.hold_time_required
            pygame.draw.rect(self.window, (255, 255, 255), (50, 100, 300, 20), 2)  # Рамка статус-бара
            pygame.draw.rect(self.window, (0, 255, 0), (50, 100, 300 * total_progress, 20))  # Заливка статус-бара

        pygame.display.flip()

    def game_over(self):
        for i in range(10):
            self.window.blit(self.kill, (0, 0))
            pygame.display.flip()
            time.sleep(0.1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    exit()
            self.window.blit(self.kill, (0, 0))
            pygame.display.flip()

    def game_win(self):
        self.window.blit(self.winner, (0, 0))
        pygame.display.flip()
        time.sleep(2)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    exit()
            self.window.blit(self.winner, (0, 0))
            pygame.display.flip()

    def main(self):
        while self.running:
            self.handle_events()
            self.update_timer()
            self.update_doll()
            self.check_movement()
            self.check_win()
            self.draw()

        self.cap.release()
        if not self.win:
            self.game_over()
        else:
            self.game_win()


if __name__ == "__main__":
    game = SquidGame()
    game.main()
