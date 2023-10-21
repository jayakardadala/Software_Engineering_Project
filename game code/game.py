import sys

import pygame

import level_2 as GameK35
import level_3 as GameK68
from level_1 import GameK2

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
PLAYER_SIZE = GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()


class Button:
    def __init__(self, x, y, text, font_size=36, color=(255, 140, 0), bg_color=WHITE):
        self.font = pygame.font.SysFont(None, font_size)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.text_surf = self.font.render(text, True, color)
        self.text_rect = self.text_surf.get_rect(center=(x, y))

    def draw(self, screen):
        screen.fill(self.bg_color, self.text_rect)
        screen.blit(self.text_surf, self.text_rect.topleft)

    def is_clicked(self, pos):
        return self.text_rect.collidepoint(pos)


class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont(None, 48)
        spacing = 60
        self.buttons = [
            Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4, "Grades K-2 (Level 1)"),
            Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + spacing, "Grades 3-5 (Level 2)"),
            Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 2 * spacing, "Grades 6-8 (Level 3)")
        ]

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_title()
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def draw_title(self):
        title_text = "Wandering in the Woods Game"
        title_surf = self.title_font.render(title_text, True, BLACK)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        self.screen.blit(title_surf, title_rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    if index == 0:
                        game = GameK2()
                        game.run()
                    elif index == 1:
                        GameK35.start()
                    elif index == 2:
                        GameK68.start()


def main():
    pygame.display.set_caption('Wandering in the Woods Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = GameMenu(screen)

    running = True
    while running:
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            menu.handle_event(event)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
