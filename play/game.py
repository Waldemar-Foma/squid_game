import pygame
import random
import cv2
import numpy as np
import time
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox


def check_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
    cap.release()
    return True


def show_camera_prompt():
    def on_yes():
        root.destroy()
        if not check_camera():
            messagebox.showerror("Ошибка", "Камера не найдена. Игра не может быть запущена.")
            webbrowser.open("https://www.dns-shop.ru/product/a16647327518ed20/veb-kamera-dexp-df2m3fm1/")
            exit()
        else:
            return

    def on_no():
        root.destroy()
        webbrowser.open("https://www.dns-shop.ru/product/a16647327518ed20/veb-kamera-dexp-df2m3fm1/")
        exit()

    root = tk.Tk()
    root.title("Проверка камеры")
    root.geometry("300x100")

    label = tk.Label(root, text="У вас есть камера?")
    label.pack(pady=10)

    yes_button = tk.Button(root, text="Да", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=20)

    no_button = tk.Button(root, text="Нет", command=on_no)
    no_button.pack(side=tk.RIGHT, padx=20)

    root.mainloop()

show_camera_prompt()

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Squid Game")

folderPath = 'frames'
mylist = os.listdir(folderPath)
graphic = [pygame.image.load(f'{folderPath}/{imPath}') for imPath in mylist]
green = graphic[0]
red = graphic[1]
kill = graphic[2]
winner = graphic[3]
intro = graphic[4]


def scale_image(image, scale):
    return pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))


green = scale_image(green, 0.69)
red = scale_image(red, 0.69)
kill = scale_image(kill, 0.69)
winner = scale_image(winner, 0.69)
intro = scale_image(intro, 0.69)

TIMER_MAX = 80
TIMER = TIMER_MAX
maxMove = 6500000
win = False
isgreen = True

font = pygame.font.SysFont("Arial", 50)

cap = cv2.VideoCapture(0)

prev = time.time()
prevDoll = time.time()

showFrame = green

hold_time_required = 30
hold_start_time = None
hold_progress = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if isgreen and event.key == pygame.K_w:
                if hold_start_time is None:
                    hold_start_time = time.time()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if hold_start_time is not None:
                    hold_progress += (time.time() - hold_start_time) / hold_time_required
                    hold_start_time = None

    cur = time.time()
    if cur - prev >= 1:
        prev = cur
        TIMER -= 1

    no = random.randint(3, 5)
    if cur - prevDoll >= no:
        prevDoll = cur
        if isgreen:
            showFrame = red
            isgreen = False
            ret, frame = cap.read()
            if ret:
                ref = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            showFrame = green
            isgreen = True

    if not isgreen:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frameDelta = cv2.absdiff(ref, gray)
            thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
            change = np.sum(thresh)
            if change > maxMove:
                running = False

    if isgreen and hold_start_time is not None:
        current_progress = (cur - hold_start_time) / hold_time_required
        total_progress = hold_progress + current_progress
        if total_progress >= 1.0:
            win = True
            running = False

    window.blit(showFrame, (0, 0))

    timer_text = font.render(f"Time: {TIMER}", True, (255, 255, 255))
    window.blit(timer_text, (50, 50))

    if isgreen:
        total_progress = hold_progress
        if hold_start_time is not None:
            total_progress += (cur - hold_start_time) / hold_time_required
        pygame.draw.rect(window, (255, 255, 255), (50, 100, 300, 20), 2)  # Рамка статус-бара
        pygame.draw.rect(window, (0, 255, 0), (50, 100, 300 * total_progress, 20))  # Заливка статус-бара

    pygame.display.flip()

cap.release()
if not win:
    for i in range(10):
        window.blit(kill, (0, 0))
        pygame.display.flip()
        time.sleep(0.1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                exit()
        window.blit(kill, (0, 0))
        pygame.display.flip()
else:
    window.blit(winner, (0, 0))
    pygame.display.flip()
    time.sleep(2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                exit()
        window.blit(winner, (0, 0))
        pygame.display.flip()

pygame.quit()