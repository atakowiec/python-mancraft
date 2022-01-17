import json

import pygame
from main_menu import MainMenu
from game import Game
import os
import copy


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
        self.loading_screen_state = 0

        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 90)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 50)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.TINY_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 25)
        self.SMALL_NORMAL_FONT = pygame.font.Font("textures/fonts/Merriweather-Regular.ttf", 30)

        # constants
        self.TICK = 30
        self.GAME_PATH = os.path.join(os.environ["appdata"], "mankraft")

        self.create_default_tree()

        # Ladowanie ustawien
        self.settings = {}
        with open(os.path.join(self.GAME_PATH, "options.txt")) as file:
            self.settings = json.loads(file.read())


        self.game = None
        self.main_menu = MainMenu(self)

        while self.running:
            self.clicked_once = []
            self.clicked_hold = []
            self.mouse_hold = []
            self.mouse_press = []
            self.clock.tick(self.TICK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.game is not None:
                        self.game.save_world()
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.clicked_once.append(event)
                    if self.state == "main_menu" and self.main_menu.input_focus != -1 and self.main_menu.screen_state == 2:
                        if event.key == pygame.K_BACKSPACE:
                            self.main_menu.entered_values[self.main_menu.input_focus] = self.main_menu.entered_values[self.main_menu.input_focus][:-1]
                        else:
                            if self.main_menu.input_focus == 1 and event.unicode.isnumeric():
                                self.main_menu.entered_values[self.main_menu.input_focus] += event.unicode
                                if self.main_menu.entered_values[self.main_menu.input_focus] != "":
                                    if int(self.main_menu.entered_values[self.main_menu.input_focus]) > 20000:
                                        self.main_menu.entered_values[self.main_menu.input_focus] = "20000"
                            elif self.main_menu.input_focus == 0:
                                self.main_menu.entered_values[self.main_menu.input_focus] += event.unicode

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_press.append(event.button)
            self.clicked_hold = pygame.key.get_pressed()
            self.mouse_hold = pygame.mouse.get_pressed(5)

            if self.state == "main_menu":
                self.main_menu.update()

            elif self.state == "game":
                self.game.general_update()

            pygame.display.flip()
            self.screen.fill((0, 0, 0))

        # Zapisywanie ustawien
        with open(os.path.join(self.GAME_PATH, "options.txt"), "w") as file:
            file.write(json.dumps(self.settings, indent=1))

    def create_default_tree(self):
        if not os.path.exists(self.GAME_PATH):
            os.makedirs(self.GAME_PATH)
        if not os.path.exists(os.path.join(self.GAME_PATH, "saves")):
            os.makedirs(os.path.join(self.GAME_PATH, "saves"))
        if not os.path.exists(os.path.join(self.GAME_PATH, "options.txt")):
            with open(os.path.join(self.GAME_PATH, "options.txt"), "x") as file:
                file.write(json.dumps({"color_mode": "dark_mode"}, indent=1))


if __name__ == '__main__':
    Main()
    # print("1776 linii")
