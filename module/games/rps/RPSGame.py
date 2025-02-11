import pygame
import random


class RockPaperScissorsGame:
    def __init__(self):
        pygame.init()

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_GRAY = (50, 50, 50)
        self.LIGHT_GRAY = (100, 100, 100)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Размеры окна
        self.WIDTH, self.HEIGHT = 1000, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Камень, ножницы, бумага")

        # Шрифты
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Загрузка изображений
        self.rock_img = pygame.image.load('rock.png')
        self.paper_img = pygame.image.load('paper.png')
        self.scissors_img = pygame.image.load('scissor.png')

        # Масштабирование изображений
        self.rock_img = pygame.transform.scale(self.rock_img, (150, 150))
        self.paper_img = pygame.transform.scale(self.paper_img, (150, 150))
        self.scissors_img = pygame.transform.scale(self.scissors_img, (150, 150))

        # Фоновое изображение
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        self.player_choice = None
        self.computer_choice = None
        self.result = ""

    def main(self):
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.player_choice = "rock"
                    elif event.key == pygame.K_x:
                        self.player_choice = "paper"
                    elif event.key == pygame.K_c:
                        self.player_choice = "scissors"

                    if self.player_choice:
                        self.computer_choice = random.choice(["rock", "paper", "scissors"])
                        self.result = self.determine_winner(self.player_choice, self.computer_choice)
                        if "Вы выиграли" in self.result or "Вы проиграли" in self.result:
                            running = False  # Заканчиваем игру

            # Отображение выборов
            if self.player_choice:
                self.screen.blit(
                    self.rock_img if self.player_choice == "rock" else self.paper_img if self.player_choice == "paper" else self.scissors_img,
                    (150, 300))

            if self.computer_choice:
                self.screen.blit(
                    self.rock_img if self.computer_choice == "rock" else self.paper_img if self.computer_choice == "paper" else self.scissors_img,
                    (500, 300))

            # Отображение результата
            result_color = self.GREEN if "Вы выиграли" in self.result else self.RED if "Вы проиграли" in self.result else self.WHITE
            result_text = self.font.render(self.result, True, result_color)
            self.screen.blit(result_text, (self.WIDTH // 2 - result_text.get_width() // 2, 100))

            # Инструкции
            instruction_text = self.small_font.render("Нажмите Z для камня, X для бумаги, C для ножниц", True, self.WHITE)
            self.screen.blit(instruction_text, (self.WIDTH // 2 - instruction_text.get_width() // 2, 500))

            pygame.display.flip()


    def determine_winner(self, player, computer):
        if player == computer:
            return "Ничья!"
        elif (player == "rock" and computer == "scissors") or \
                (player == "scissors" and computer == "paper") or \
                (player == "paper" and computer == "rock"):
            return "Вы выиграли!"
        else:
            return "Вы проиграли!"


if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.main()
