import random

import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
PLAYER_SIZE = 40
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60  # Countdown timer (in seconds)

# Load images
player1_img = pygame.image.load('resources/player.png')
player2_img = pygame.image.load('resources/player.png')
background_img = pygame.image.load('resources/woods.png')


class GameK2:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Wandering in the Woods - K-2 Version')

        self.meet_sound = pygame.mixer.Sound('resources/meet_notification.wav')
        pygame.mixer.music.load('resources/bacground_music.wav')
        pygame.mixer.music.play(-1)  # Play background music in a loop

        self.player1_pos = [0, 0]
        self.player2_pos = [SCREEN_WIDTH - PLAYER_SIZE, SCREEN_HEIGHT - PLAYER_SIZE]

        self.start_ticks = pygame.time.get_ticks()  # Countdown timer

        self.running = True

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (SCREEN_WIDTH, y))

    def draw_players(self):
        self.screen.blit(player1_img, self.player1_pos)
        self.screen.blit(player2_img, self.player2_pos)

    def move_randomly(self, player_pos):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and player_pos[1] > 0:
            player_pos[1] -= GRID_SIZE
        elif direction == 'down' and player_pos[1] < SCREEN_HEIGHT - PLAYER_SIZE:
            player_pos[1] += GRID_SIZE
        elif direction == 'left' and player_pos[0] > 0:
            player_pos[0] -= GRID_SIZE
        elif direction == 'right' and player_pos[0] < SCREEN_WIDTH - PLAYER_SIZE:
            player_pos[0] += GRID_SIZE

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.move_randomly(self.player1_pos)
            self.move_randomly(self.player2_pos)

            if self.player1_pos == self.player2_pos:
                self.meet_sound.play()
                print("Players have met!")
                self.player1_pos = [0, 0]
                self.player2_pos = [SCREEN_WIDTH - PLAYER_SIZE, SCREEN_HEIGHT - PLAYER_SIZE]

            self.screen.blit(background_img, (0, 0))
            self.draw_grid()
            self.draw_players()

            seconds_passed = (pygame.time.get_ticks() - self.start_ticks) / 1000
            time_left = MAX_TIME - seconds_passed
            if time_left <= 0:
                print("Time's up!")
                break

            pygame.display.flip()
            pygame.time.wait(500)

        pygame.quit()


def start():
    game = GameK2()
    game.run()
