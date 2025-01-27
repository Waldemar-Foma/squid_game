import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Камень, ножницы, бумага")

font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

rock_img = pygame.image.load('rock.png')
paper_img = pygame.image.load('paper.png')
scissors_img = pygame.image.load('scissor.jpg')

rock_img = pygame.transform.scale(rock_img, (100, 100))
paper_img = pygame.transform.scale(paper_img, (100, 100))
scissors_img = pygame.transform.scale(scissors_img, (100, 100))


def main():
    running = True
    player_choice = None
    computer_choice = None
    result = ""

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    player_choice = "rock"
                    computer_choice = random.choice(["rock", "paper", "scissors"])
                    result = determine_winner(player_choice, computer_choice)
                elif event.key == pygame.K_x:
                    player_choice = "paper"
                    computer_choice = random.choice(["rock", "paper", "scissors"])
                    result = determine_winner(player_choice, computer_choice)
                elif event.key == pygame.K_c:
                    player_choice = "scissors"
                    computer_choice = random.choice(["rock", "paper", "scissors"])
                    result = determine_winner(player_choice, computer_choice)

        if player_choice:
            if player_choice == "rock":
                screen.blit(rock_img, (150, 300))
            elif player_choice == "paper":
                screen.blit(paper_img, (150, 300))
            elif player_choice == "scissors":
                screen.blit(scissors_img, (150, 300))

        if computer_choice:
            if computer_choice == "rock":
                screen.blit(rock_img, (550, 300))
            elif computer_choice == "paper":
                screen.blit(paper_img, (550, 300))
            elif computer_choice == "scissors":
                screen.blit(scissors_img, (550, 300))

        result_text = font.render(result, True, BLACK)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))

        instruction_text = small_font.render("Нажмите Я для камня, Ч для бумаги, С для ножниц", True, BLACK)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 500))

        pygame.display.flip()

    pygame.quit()


def determine_winner(player, computer):
    if player == computer:
        return "Ничья!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        return "Вы выиграли!"
    else:
        return "Вы проиграли!"


if __name__ == "__main__":
    main()