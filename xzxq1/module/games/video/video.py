import pygame
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np


class VideoPlayer:
    def __init__(self, video_path):
        pygame.init()

        # Установка полноэкранного режима
        screen_info = pygame.display.Info()
        self.screen_width = screen_info.current_w
        self.screen_height = screen_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Video Player")

        self.clip = VideoFileClip(video_path)

        pygame.mixer.init(frequency=44100)
        audio = self.clip.audio.to_soundarray(fps=44100)
        audio = (audio * 32767).astype(np.int16)
        self.sound = pygame.sndarray.make_sound(audio)
        self.sound.play()

        self.fps = self.clip.fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_time = 0

    def run(self):
        while self.running:
            self.handle_events()

            frame = self.clip.get_frame(self.current_time)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.scale(frame, (self.screen_width, self.screen_height))

            self.screen.blit(frame, (0, 0))
            pygame.display.flip()

            self.current_time += 1 / self.fps
            self.clock.tick(self.fps)

        self.cleanup()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def cleanup(self):
        self.sound.stop()
        pygame.quit()
        self.clip.close()


def main():
    video_path = "Death.mp4"
    player = VideoPlayer(video_path)
    player.run()


if __name__ == "__main__":
    main()
