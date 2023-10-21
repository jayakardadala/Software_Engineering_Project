import random
import sys

import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 128)
GREEN = (0, 128, 0)
ORANGE = (255, 140, 0)

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRID_SIZE = 40
PLAYER_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60
MAX_MOVES = 10000
MIN_GRID_SIZE = 10
MAX_GRID_SIZE = 20

PADDING = 20
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50
BUTTON_SPACING = 75
TEXT_OFFSET = 25

player_colors = [ORANGE, GREEN, DARK_BLUE, (255, 255, 0)]

background_img = pygame.image.load('resources/woods.png')
player_imgs = [
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png')
]

# Wandering Protocols
WANDERING_PROTOCOLS = ['Random Walk', 'Edges First', 'Center Outwards']

# Initialize pygame
pygame.init()

# Display setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering in the Woods Game: Grades 6-8')

clicked = False


# Class to manage game setup and execution
class GameK68:
    def __init__(self):
        self.grid_width = MIN_GRID_SIZE
        self.grid_height = MIN_GRID_SIZE
        self.number_of_players = 2
        self.player_positions = []
        self.wandering_protocol = 'Random Walk'
        self.experimental_runs = 1
        self.current_run = 1
        self.initial_player_positions = []
        self.setup_done = False
        self.placing_players = False
        self.placed_players = 0
        self.all_players = []
        self.met_groups = []
        self.move_count = 0
        self.game_over = False

    # Function to draw a button on the screen
    def draw_button(self, text, x, y, width, height, inactive_color, active_color):
        global clicked
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, width, height))
            if click[0] == 1 and not clicked:
                clicked = True
                return True
            if click[0] == 0:
                clicked = False
        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height))

        font = pygame.font.SysFont(None, 35)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.center = (x + (width / 2), y + (height / 2))
        screen.blit(text_surf, text_rect)
        return False

    # Function to display text on the screen
    def draw_text(self, text, x, y):
        font = pygame.font.SysFont(None, 35)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surf, text_rect)

    # Function to move players based on the selected protocol
    def move_players_based_on_protocol(self, positions, protocol):
        new_positions = positions.copy()

        RANDOM_FACTOR = 0.1  # 10% chance of random movement

        for idx, pos in enumerate(positions):
            directions = ['up', 'down', 'left', 'right']

            if random.random() < RANDOM_FACTOR:
                random.shuffle(directions)

            elif protocol == 'Random Walk':
                random.shuffle(directions)

            elif protocol == 'Edges First':
                x, y = pos
                if x == 0:
                    directions = ['right', 'up', 'down']
                elif x == self.grid_width - 1:
                    directions = ['left', 'up', 'down']
                elif y == 0:
                    directions = ['down', 'left', 'right']
                elif y == self.grid_height - 1:
                    directions = ['up', 'left', 'right']

            elif protocol == 'Center Outwards':
                x, y = pos
                center_x, center_y = self.grid_width // 2, self.grid_height // 2
                if x < center_x and y < center_y:
                    directions = ['right', 'down'] + directions
                elif x > center_x and y < center_y:
                    directions = ['left', 'down'] + directions
                elif x < center_x and y > center_y:
                    directions = ['right', 'up'] + directions
                elif x > center_x and y > center_y:
                    directions = ['left', 'up'] + directions

            new_pos = list(pos)
            for direction in directions:
                if direction == 'up' and new_pos[1] > 0:
                    new_pos[1] -= 1
                elif direction == 'down' and new_pos[1] < self.grid_height - 1:
                    new_pos[1] += 1
                elif direction == 'left' and new_pos[0] > 0:
                    new_pos[0] -= 1
                elif direction == 'right' and new_pos[0] < self.grid_width - 1:
                    new_pos[0] += 1

                if tuple(new_pos) not in new_positions and tuple(new_pos) not in positions:
                    break
                else:
                    new_pos = list(pos)

            new_positions[idx] = tuple(new_pos)
        return new_positions

    # Function to check if any players have met and group them together
    def check_meetings(self, positions):
        met_groups = []
        single_players = []

        # Check for any meetings
        meetings = {}
        for pos in positions:
            if pos in meetings:
                meetings[pos].append(pos)
            else:
                meetings[pos] = [pos]

        # Separate out groups and single players
        for pos, met_players in meetings.items():
            if len(met_players) > 1:
                met_group = sorted(met_players)
                if met_group not in met_groups:
                    met_groups.append(met_group)
            else:
                single_players.append(pos)

        return met_groups, single_players

    # Function to handle game setup

    def setup_screen(self):
        self.setup_done = False
        self.placing_players = False
        self.placed_players = 0
        self.player_positions = []

        screen.fill(WHITE)

        while not self.setup_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.placing_players and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    cell_x = x // GRID_SIZE
                    cell_y = y // GRID_SIZE

                    if (cell_x, cell_y) not in self.player_positions:
                        self.player_positions.append((cell_x, cell_y))
                        self.placed_players += 1
                        if self.placed_players == self.number_of_players:
                            self.placing_players = False
                            self.setup_done = True

            screen.fill(WHITE)

            # Draw the current grid
            for x in range(self.grid_width):
                for y in range(self.grid_height):
                    pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                    if (x, y) in self.player_positions:
                        pygame.draw.circle(screen, player_colors[self.player_positions.index((x, y))],
                                           (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                           PLAYER_SIZE // 2)

            # Dynamic starting position for buttons and text based on screen size
            startY = (screen.get_height() - (5 * BUTTON_HEIGHT + 4 * BUTTON_SPACING)) // 2

            # Draw the setup options
            if not self.placing_players:
                # Set grid width
                if self.draw_button("<", PADDING, startY, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE,
                                    RED) and self.grid_width > MIN_GRID_SIZE:
                    self.grid_width -= 1
                if self.draw_button(">", PADDING + BUTTON_WIDTH + TEXT_OFFSET, startY, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    BLUE, RED) and self.grid_width < MAX_GRID_SIZE:
                    self.grid_width += 1
                self.draw_text(f"Grid Width: {self.grid_width}", PADDING + 2 * BUTTON_WIDTH + 2 * TEXT_OFFSET,
                               startY + BUTTON_HEIGHT // 2)
                startY += BUTTON_SPACING

                # Set grid height
                if self.draw_button("<", PADDING, startY, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE,
                                    RED) and self.grid_height > MIN_GRID_SIZE:
                    self.grid_height -= 1
                if self.draw_button(">", PADDING + BUTTON_WIDTH + TEXT_OFFSET, startY, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    BLUE, RED) and self.grid_height < MAX_GRID_SIZE:
                    self.grid_height += 1
                self.draw_text(f"Grid Height: {self.grid_height}", PADDING + 2 * BUTTON_WIDTH + 2 * TEXT_OFFSET,
                               startY + BUTTON_HEIGHT // 2)
                startY += BUTTON_SPACING

                # Set number of players
                if self.draw_button("<", PADDING, startY, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE,
                                    RED) and self.number_of_players > 2:
                    self.number_of_players -= 1
                if self.draw_button(">", PADDING + BUTTON_WIDTH + TEXT_OFFSET, startY, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    BLUE, RED) and self.number_of_players < 4:
                    self.number_of_players += 1
                self.draw_text(f"Players: {self.number_of_players}", PADDING + 2 * BUTTON_WIDTH + 2 * TEXT_OFFSET,
                               startY + BUTTON_HEIGHT // 2)
                startY += BUTTON_SPACING

                # Choose wandering protocol
                if self.draw_button("<", PADDING, startY, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE, RED):
                    curr_idx = WANDERING_PROTOCOLS.index(self.wandering_protocol)
                    self.wandering_protocol = WANDERING_PROTOCOLS[(curr_idx - 1) % len(WANDERING_PROTOCOLS)]
                if self.draw_button(">", PADDING + BUTTON_WIDTH + TEXT_OFFSET, startY, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    BLUE, RED):
                    curr_idx = WANDERING_PROTOCOLS.index(self.wandering_protocol)
                    self.wandering_protocol = WANDERING_PROTOCOLS[(curr_idx + 1) % len(WANDERING_PROTOCOLS)]
                self.draw_text(f"Wandering Protocol: {self.wandering_protocol}",
                               PADDING + 2 * BUTTON_WIDTH + 2 * TEXT_OFFSET, startY + BUTTON_HEIGHT // 2)
                startY += BUTTON_SPACING

                # Choose number of experimental runs
                if self.draw_button("<", PADDING, startY, BUTTON_WIDTH, BUTTON_HEIGHT, BLUE,
                                    RED) and self.experimental_runs > 1:
                    self.experimental_runs -= 1
                if self.draw_button(">", PADDING + BUTTON_WIDTH + TEXT_OFFSET, startY, BUTTON_WIDTH, BUTTON_HEIGHT,
                                    BLUE, RED):
                    self.experimental_runs += 1
                self.draw_text(f"Experimental Runs: {self.experimental_runs}",
                               PADDING + 2 * BUTTON_WIDTH + 2 * TEXT_OFFSET, startY + BUTTON_HEIGHT // 2)
                startY += BUTTON_SPACING

                # Start player placement
                if self.draw_button("Place Players", PADDING, startY, 250, BUTTON_HEIGHT, BLUE, RED):
                    self.placing_players = True
                    self.player_positions = []
                    self.placed_players = 0

            pygame.display.update()

        self.initial_player_positions = self.player_positions.copy()

    # Main game loop
    def game_loop(self):
        pygame.display.set_caption('Wandering in the Woods - Grades 6-8 Version')

        pygame.mixer.music.load('resources/bacground_music.wav')
        pygame.mixer.music.play(-1)

        meet_sound = pygame.mixer.Sound('resources/meet_notification.wav')

        for run in range(self.experimental_runs):
            self.all_players = self.initial_player_positions.copy()
            self.met_groups = []
            self.move_count = 0
            self.game_over = False

            while not self.game_over and self.move_count < MAX_MOVES:
                self.move_count += 1

                # Move players based on the selected protocol
                self.all_players = self.move_players_based_on_protocol(self.all_players, self.wandering_protocol)

                # Check for meetings
                new_met_groups, self.all_players = self.check_meetings(self.all_players)
                self.met_groups.extend(new_met_groups)

                for group in new_met_groups:
                    meet_sound.play()

                # Display
                screen.blit(background_img, (0, 0))
                for x in range(self.grid_width):
                    for y in range(self.grid_height):
                        pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                        pos = (x, y)
                        if pos in self.all_players:
                            idx = self.all_players.index(pos)
                            screen.blit(player_imgs[idx], (x * GRID_SIZE, y * GRID_SIZE))
                        for group in self.met_groups:
                            if pos in group:
                                idx = group.index(pos)
                                screen.blit(player_imgs[idx], (x * GRID_SIZE, y * GRID_SIZE))

                # Check if all players have met
                if len(self.met_groups) == 1 and len(self.met_groups[0]) == self.number_of_players:
                    self.game_over = True

                pygame.display.flip()
                pygame.time.wait(500)

            print(f"Run {run + 1}: All players met in {self.move_count} moves or reached max moves!")

        self.setup_screen()


# Start the game
def start():
    game = GameK68()
    game.setup_screen()
    game.game_loop()
