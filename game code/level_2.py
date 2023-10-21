import random
import sys

import pygame

# Re-initializing pygame and other constants
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 128)
GREEN = (0, 128, 0)
ORANGE = (255, 140, 0)

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GRID_SIZE = 40
PLAYER_SIZE = 40
NUM_CELLS = SCREEN_WIDTH // GRID_SIZE
MAX_TIME = 60  # Countdown timer (in seconds)

# Setting up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wandering in the Woods Game')

# Grades 3-5 Game Version: Setup Screen
MIN_GRID_SIZE = 10
MAX_GRID_SIZE = 20
grid_width = MIN_GRID_SIZE
grid_height = MIN_GRID_SIZE
number_of_players = 2
player_positions = []
player_colors = [ORANGE, GREEN, DARK_BLUE, (255, 255, 0)]
background_img = pygame.image.load('resources/woods.png')
player_imgs = [
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png'),
    pygame.image.load('resources/player.png')
]

clicked = False  # Global variable to keep track of button clicks

# New variables to store game statistics
longest_run = 0
shortest_run = float('inf')
total_runs = 0
total_time_taken = 0


class GameK35:
    def __init__(self):
        self.setup_done = False
        self.placing_players = False
        self.placed_players = 0
        self.timer = 0
        self.start_time = 0
        self.all_players = []
        self.met_groups = []
        self.game_over = False

    def update_statistics(self, run_time):
        global longest_run, shortest_run, total_runs, total_time_taken

        longest_run = max(longest_run, run_time)
        shortest_run = min(shortest_run, run_time)
        total_runs += 1
        total_time_taken += run_time

    def display_statistics(self):
        avg_run = total_time_taken / total_runs if total_runs > 0 else 0

        font = pygame.font.SysFont(None, 50)

        longest_str = f"Longest Run: {longest_run:.2f} seconds"
        text_surf = font.render(longest_str, True, ORANGE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        screen.blit(text_surf, text_rect)

        shortest_str = f"Shortest Run: {shortest_run:.2f} seconds"
        text_surf = font.render(shortest_str, True, ORANGE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surf, text_rect)

        avg_str = f"Average Run: {avg_run:.2f} seconds"
        text_surf = font.render(avg_str, True, ORANGE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(text_surf, text_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Show for 3 seconds

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

    def setup_screen(self):
        global grid_width, grid_height, number_of_players, player_positions

        self.setup_done = False
        self.placing_players = False
        self.placed_players = 0
        player_positions = []

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

                    if (cell_x, cell_y) not in player_positions:
                        player_positions.append((cell_x, cell_y))
                        self.placed_players += 1
                        if self.placed_players == number_of_players:
                            self.placing_players = False
                            self.setup_done = True

            screen.fill(WHITE)

            # Draw the current grid
            for x in range(grid_width):
                for y in range(grid_height):
                    pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                    if (x, y) in player_positions:
                        pygame.draw.circle(screen, player_colors[player_positions.index((x, y))],
                                           (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2),
                                           PLAYER_SIZE // 2)

            # If not placing players, draw the setup options
            if not self.placing_players:
                # Allow user to choose grid width
                if self.draw_button("<", 50, 50, 50, 50, ORANGE, DARK_BLUE) and grid_width > MIN_GRID_SIZE:
                    grid_width -= 1
                if self.draw_button(">", 150, 50, 50, 50, ORANGE, DARK_BLUE) and grid_width < MAX_GRID_SIZE:
                    grid_width += 1
                self.draw_text(f"Grid Width: {grid_width}", 300, 75)

                # Allow user to choose grid height
                if self.draw_button("<", 50, 150, 50, 50, ORANGE, DARK_BLUE) and grid_height > MIN_GRID_SIZE:
                    grid_height -= 1
                if self.draw_button(">", 150, 150, 50, 50, ORANGE, DARK_BLUE) and grid_height < MAX_GRID_SIZE:
                    grid_height += 1
                self.draw_text(f"Grid Height: {grid_height}", 300, 175)

                # Allow user to choose the number of players
                if self.draw_button("<", 50, 250, 50, 50, ORANGE, DARK_BLUE) and number_of_players > 2:
                    number_of_players -= 1
                if self.draw_button(">", 150, 250, 50, 50, ORANGE, DARK_BLUE) and number_of_players < 4:
                    number_of_players += 1
                self.draw_text(f"Players: {number_of_players}", 300, 275)

                # Start player placement
                if self.draw_button("Place Players", 50, 350, 250, 50, ORANGE, DARK_BLUE):
                    self.placing_players = True
                    player_positions = []
                    self.placed_players = 0

            pygame.display.update()

    def draw_text(self, text, x, y):
        font = pygame.font.SysFont(None, 35)
        text_surf = font.render(text, True, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_surf, text_rect)

    def move_players_randomly(self):
        """Function to move multiple players and groups randomly."""
        new_positions = self.all_players.copy()
        occupied_positions = set(self.all_players + [group[0] for group in self.met_groups])
        new_occupied_positions = set()  # To track positions players have moved to in this iteration

        for idx, pos in enumerate(self.all_players):
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_pos = list(pos)
            if direction == 'up' and new_pos[1] > 0:
                new_pos[1] -= 1
            elif direction == 'down' and new_pos[1] < grid_height - 1:
                new_pos[1] += 1
            elif direction == 'left' and new_pos[0] > 0:
                new_pos[0] -= 1
            elif direction == 'right' and new_pos[0] < grid_width - 1:
                new_pos[0] += 1

            # If the new position isn't occupied, update the position
            if tuple(new_pos) not in occupied_positions and tuple(new_pos) not in new_occupied_positions:
                new_positions[idx] = tuple(new_pos)
                new_occupied_positions.add(tuple(new_pos))

        # Move groups
        for group in self.met_groups:
            direction = random.choice(['up', 'down', 'left', 'right'])
            new_group_pos = list(group[0])
            if direction == 'up' and new_group_pos[1] > 0:
                new_group_pos[1] -= 1
            elif direction == 'down' and new_group_pos[1] < grid_height - 1:
                new_group_pos[1] += 1
            elif direction == 'left' and new_group_pos[0] > 0:
                new_group_pos[0] -= 1
            elif direction == 'right' and new_group_pos[0] < grid_width - 1:
                new_group_pos[0] += 1

            # If the new group position isn't occupied, update the group's position
            if tuple(new_group_pos) not in new_positions and tuple(new_group_pos) not in occupied_positions and tuple(
                    new_group_pos) not in new_occupied_positions:
                for idx in range(len(group)):
                    group[idx] = tuple(new_group_pos)
                new_occupied_positions.add(tuple(new_group_pos))

        self.all_players = new_positions

    def check_meetings(self):
        """Check if any players have met and group them together."""
        met_groups = []
        single_players = []

        # Check for any meetings
        meetings = {}
        for pos in self.all_players:
            if pos in meetings:
                meetings[pos].append(pos)
            else:
                meetings[pos] = [pos]

        # Separate out groups and single players
        for pos, met_players in meetings.items():
            if len(met_players) > 1:
                met_groups.append(met_players)
            else:
                single_players.append(pos)

        self.met_groups = met_groups
        return met_groups, single_players

    def display_timer(self, time_left):
        font = pygame.font.SysFont(None, 50)
        mins = int(time_left) // 60
        secs = int(time_left) % 60
        time_str = f"{mins:02}:{secs:02}"
        text_surf = font.render(time_str, True, ORANGE)
        text_rect = text_surf.get_rect()
        text_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
        screen.blit(text_surf, text_rect)

    def handle_time_out(self):
        font = pygame.font.SysFont(None, 100)
        text_surf = font.render("TIME OUT", True, ORANGE)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surf, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # Show for 3 seconds
        pygame.mixer.music.stop()

    def game_loop(self):
        self.timer = MAX_TIME
        self.start_time = self.timer

        pygame.display.set_caption('Wandering in the Woods - Grades 3-5 Version')

        pygame.mixer.music.load('resources/bacground_music.wav')
        pygame.mixer.music.play(-1)

        meet_sound = pygame.mixer.Sound('resources/meet_notification.wav')

        self.all_players = player_positions.copy()
        self.met_groups = []

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_timer(self.timer)
            self.timer -= 0.5
            if self.timer <= 0:
                self.handle_time_out()
                return

            self.move_players_randomly()

            new_met_groups, self.all_players = self.check_meetings()
            self.met_groups.extend(new_met_groups)

            for group in new_met_groups:
                meet_sound.play()

            screen.blit(background_img, (0, 0))

            for x in range(grid_width):
                for y in range(grid_height):
                    pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                    pos = (x, y)
                    if pos in self.all_players:
                        idx = self.all_players.index(pos)
                        screen.blit(player_imgs[idx], (x * GRID_SIZE, y * GRID_SIZE))
                    for group in self.met_groups:
                        if pos in group:
                            idx = group.index(pos)
                            screen.blit(player_imgs[idx], (x * GRID_SIZE, y * GRID_SIZE))

            if len(self.met_groups) == 1 and len(self.met_groups[0]) == number_of_players:
                game_time_taken = self.start_time - self.timer
                self.update_statistics(game_time_taken)
                self.display_statistics()
                self.setup_screen()

            pygame.display.flip()
            pygame.time.wait(500)


class StartScreen:
    def __init__(self):
        self.game = GameK35()

    def start(self):
        while True:
            self.game.setup_screen()
            self.game.game_loop()


def start():
    start_screen = StartScreen()
    start_screen.start()
