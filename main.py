import pygame
from main_menu import MainMenu
from game import Game
import os


class Main:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1000, 640))
        pygame.display.set_caption("Minecraft 3.0")
        self.state = "main_menu"
        self.clock = pygame.time.Clock()
        self.clicked_once = []
        self.clicked_hold = []
        self.mouse_press = []
        self.mouse_hold = []

        # constants
        self.TICK = 30
        self.GAME_PATH = os.path.join(os.environ["appdata"], "mankraft")

        self.create_default_tree()

        self.game = None
        self.main_menu = MainMenu(self)

        while self.running:
            self.clicked_once = []
            self.clicked_hold = []
            self.mouse_hold = []
            self.mouse_press = []
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.game is not None:
                        self.game.save_world()
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.clicked_once.append(event)
                    if self.state == "main_menu" and self.main_menu.input_focus and self.main_menu.screen_state == 2:
                        if event.key == pygame.K_BACKSPACE:
                            self.main_menu.entered_name = self.main_menu.entered_name[:-1]
                        else:
                            self.main_menu.entered_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press.append(event.button)
            self.clicked_hold = pygame.key.get_pressed()
            self.mouse_hold = pygame.mouse.get_pressed(3)

            if self.state == "main_menu":
                self.main_menu.update()

            elif self.state == "game":
                self.game.general_update()

            pygame.display.flip()
            self.screen.fill((0, 0, 0))

    def create_default_tree(self):
        if not os.path.exists(self.GAME_PATH):
            os.makedirs(self.GAME_PATH)
        if not os.path.exists(os.path.join(self.GAME_PATH, "saves")):
            os.makedirs(os.path.join(self.GAME_PATH, "saves"))


if __name__ == '__main__':
    Main()
