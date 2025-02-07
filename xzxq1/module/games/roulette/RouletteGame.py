import pygame
import random


class RussianRoulette:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1000, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Русская рулетка")

        self.RED = (255, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)

        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)

        self.shot_sound = pygame.mixer.Sound("shot.wav")
        self.empty_sound = pygame.mixer.Sound("empty.wav")
        self.click_sound = pygame.mixer.Sound("click.wav")

        self.background = pygame.image.load("background.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.bullets = [0, 0, 0, 0, 0, 1]
        random.shuffle(self.bullets)
        self.current_turn = "player"
        self.player_shot_used = False
        self.bot_shot_used = False
        self.game_over = False
        self.message = ""

    def draw_text(self, text, x, y, color=None, font_type=None):
        color = color or self.GRAY
        font_type = font_type or self.font
        text_surface = font_type.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def fade_effect(self, final_message):
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill(self.BLACK)
        for alpha in range(0, 100, 5):
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            self.draw_text(final_message, self.WIDTH // 2 - 150, self.HEIGHT // 2, self.RED)
            pygame.display.flip()
            pygame.time.delay(30)
        pygame.quit()
        exit()

    def bot_turn(self):
        if not self.game_over:
            pygame.time.wait(1000)
            self.click_sound.play()
            if not self.bot_shot_used and random.random() < 0.2:
                self.bot_shot_used = True
                if self.bullets.pop(0) == 1:
                    self.message = "Вы умерли!"
                    self.shot_sound.play()
                    self.fade_effect("Вы умерли!")
                    self.game_over = True
                else:
                    self.message = "Вы выжили!"
                    self.empty_sound.play()
            else:
                if self.bullets.pop(0) == 1:
                    self.message = "Противник умер!"
                    self.shot_sound.play()
                    self.fade_effect("Противник умер!")
                    self.game_over = True
                else:
                    self.message = "Противник выжил!"
                    self.empty_sound.play()
            self.current_turn = "player"

    def main(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_s:
                        self.click_sound.play()
                        pygame.time.wait(500)
                        if self.bullets.pop(0) == 1:
                            self.message = "Вы умерли!"
                            self.shot_sound.play()
                            self.fade_effect("Вы умерли!")
                            self.game_over = True
                        else:
                            self.message = "Вы выжили!"
                            self.empty_sound.play()
                            self.current_turn = "bot"
                    elif event.key == pygame.K_a and not self.player_shot_used:
                        self.player_shot_used = True
                        self.click_sound.play()
                        pygame.time.wait(500)
                        if self.bullets.pop(0) == 1:
                            self.message = "Противник умер!"
                            self.shot_sound.play()
                            self.fade_effect("Противник умер!")
                            self.game_over = True
                        else:
                            self.message = "Противник выжил!"
                            self.empty_sound.play()
                            self.current_turn = "bot"

            self.draw_text("Русская рулетка", self.WIDTH // 2 - 170, 20, self.RED)
            if self.message:
                self.draw_text(self.message, self.WIDTH // 2 - 150, self.HEIGHT // 2, self.GRAY)

            self.draw_text("S - выстрелить в себя", 20, self.HEIGHT - 120, self.GRAY, self.small_font)
            self.draw_text("A - выстрелить в бота (1 раз)", 20, self.HEIGHT - 80, self.GRAY, self.small_font)

            pygame.display.flip()

            if not self.game_over and self.current_turn == "bot":
                self.bot_turn()



if __name__ == "__main__":
    game = RussianRoulette()
    game.main()
