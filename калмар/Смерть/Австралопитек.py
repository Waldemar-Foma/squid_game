import pygame
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np

pygame.init()

# Установка полноэкранного режима
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Video Player")

video_path = "Death.mp4"
clip = VideoFileClip(video_path)

pygame.mixer.init(frequency=44100)
audio = clip.audio.to_soundarray(fps=44100)
audio = (audio * 32767).astype(np.int16)
sound = pygame.sndarray.make_sound(audio)
sound.play()

fps = clip.fps

clock = pygame.time.Clock()
running = True
current_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    frame = clip.get_frame(current_time)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (screen_width, screen_height))

    screen.blit(frame, (0, 0))
    pygame.display.flip()

    current_time += 1 / fps
    clock.tick(fps)

sound.stop()
pygame.quit()
clip.close()