import random

import pygame
import os
from game import Game
import shutil
from variables import color_modes

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_state = 0
        self.delete_world = False
        self.splash_text = get_random_splash()
        self.splash_scale = .9
        self.splash_scale_change = -0.009

        self.TEXT_COLOR = color_modes[self.game.settings["color_mode"]]["main_menu_text"]
        self.SHADOW_COLOR = color_modes[self.game.settings["color_mode"]]["main_menu_text_shadow"]
        self.BUTTON_BG = color_modes[self.game.settings["color_mode"]]["main_menu_button_bg"]
        self.BUTTON_BG_HOVER = color_modes[self.game.settings["color_mode"]]["main_menu_button_bg_hover"]
        self.BUTTON_BORDER = color_modes[self.game.settings["color_mode"]]["main_menu_button_border"]
        self.BACKGROUND = color_modes[self.game.settings["color_mode"]]["main_menu_background"]

        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 90)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 50)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.TINY_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 25)
        self.SMALL_NORMAL_FONT = pygame.font.Font("textures/fonts/Merriweather-Regular.ttf", 30)

        # components
        self.logo_light = self.FONT.render("Mankraft", False, self.TEXT_COLOR)
        self.logo_dark = self.FONT.render("Mankraft", False, self.SHADOW_COLOR)
        self.st_button_text = self.SMALL_FONT.render("Singleplayer", False, self.TEXT_COLOR)
        self.nd_button_text = self.SMALL_FONT.render("Options", False, self.TEXT_COLOR)
        self.rd_button_text = self.SMALL_FONT.render("Exit", False, self.TEXT_COLOR)

        # Loading world list
        self.scroll_offset = 0
        self.world_list = self.get_world_list()

        self.world_list_surface = pygame.Surface((420, 100*len(self.world_list)), pygame.SRCALPHA)
        self.world_list_surface.convert_alpha()

        self.entered_name = ""
        self.input_focus = False
        self.cursor_counter = 0

        self.options_buttons = [
            [50, 520, 250, 80, self.SMALL_FONT.render("Go back", False, self.TEXT_COLOR)],
            [700, 520, 250, 80, self.SMALL_FONT.render("Credits", False, self.TEXT_COLOR)],
            [50, 100, 400, 80, self.SMALL_FONT.render("Color mode: "+self.game.settings["color_mode"].replace("_", " "), False, self.TEXT_COLOR)]
        ]


    def update(self):
        # tło
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((0,0,0))
        self.screen.blit(self.BACKGROUND, (0, 0))
        if self.screen_state == 0:
            # Main menu
            # logo
            self.screen.blit(self.logo_dark, ((self.screen.get_width() - self.logo_light.get_width()) / 2 + 5, 55))
            self.screen.blit(self.logo_light, ((self.screen.get_width() - self.logo_light.get_width()) / 2, 50))

            if self.splash_scale > .95 or self.splash_scale < 0.8:
                self.splash_scale_change *= -1
            self.splash_scale -= self.splash_scale_change

            text = self.TINY_FONT.render(self.splash_text, False, (0,0,0))
            text = pygame.transform.rotate(text, 25)
            self.screen.blit(pygame.transform.scale(text, [int(i*self.splash_scale) for i in text.get_size()]), ((self.screen.get_width()+self.logo_light.get_width())/2 - text.get_width()/2, 50+self.logo_light.get_height()-text.get_height()/2))

            text = self.TINY_FONT.render(self.splash_text, False, (255,255,255))
            text = pygame.transform.rotate(text, 25)
            self.screen.blit(pygame.transform.scale(text, [int(i*self.splash_scale) for i in text.get_size()]), ((self.screen.get_width()+self.logo_light.get_width())/2 - text.get_width()/2, 48+self.logo_light.get_height()-text.get_height()/2))

            # przyciski
            hovered = [False, False, False]

            rect = pygame.Rect(300, 200, 400, 90)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered[0] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect, border_radius=10)
            pygame.draw.rect(self.screen, color, pygame.Rect(305, 205, 390, 80), border_radius=10)
            self.screen.blit(self.st_button_text,
                             (500 - (self.st_button_text.get_width() / 2), 245 - self.st_button_text.get_height() / 2))

            color = self.BUTTON_BG
            rect = pygame.Rect(300, 320, 400, 90)
            if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered[1] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect, border_radius=10)
            pygame.draw.rect(self.screen, color, pygame.Rect(305, 325, 390, 80), border_radius=10)
            self.screen.blit(self.nd_button_text,
                             (500 - (self.nd_button_text.get_width() / 2), 365 - self.nd_button_text.get_height() / 2))

            color = self.BUTTON_BG
            rect = pygame.Rect(300, 440, 400, 90)
            if rect.collidepoint(mouse_pos):
                hovered[2] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect, border_radius=10)
            pygame.draw.rect(self.screen, color, pygame.Rect(305, 445, 390, 80), border_radius=10)
            self.screen.blit(self.rd_button_text, (500 - (self.rd_button_text.get_width() / 2), 485 - self.rd_button_text.get_height() / 2))

            if 1 in self.game.mouse_press:
                if hovered[0]:
                    self.screen_state = 1
                elif hovered[1]:
                    self.screen_state = 3
                elif hovered[2]:
                    self.game.running = False

        elif self.screen_state == 1:
            # world selector
            hovered = [False, False, False, False, False]

            rect = pygame.Rect(50, 50, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[0] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (55, 55, 240, 70))
            text = self.SMALL_FONT.render("New World", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 90 - text.get_height() / 2))

            rect = pygame.Rect(50, 150, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[1] = True
                color = self.BUTTON_BG_HOVER
            if self.delete_world:
                color = (90, 90, 90)
                text = self.SMALL_FONT.render("Click world to delete", False, self.TEXT_COLOR)
                self.screen.blit(self.SMALL_FONT.render("Click world to delete", False, (0,0,0)), (177 - text.get_width() / 2, 252))
                self.screen.blit(text, (175 - text.get_width() / 2, 250))

            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (55, 155, 240, 70))
            text = self.SMALL_FONT.render("Delete World", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 190 - text.get_height() / 2))

            rect = pygame.Rect(50, 520, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[2] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (55, 525, 240, 70))
            text = self.SMALL_FONT.render("Go Back", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 560 - text.get_height() / 2))

            rect = pygame.Rect(900, 230, 80, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[3] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (905, 235, 70, 70))
            text = self.SMALL_NORMAL_FONT.render("↑", False, self.TEXT_COLOR)
            self.screen.blit(text, (940 - text.get_width() / 2, 270 - text.get_height() / 2))

            rect = pygame.Rect(900, 320, 80, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[4] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (905, 325, 70, 70))
            text = self.SMALL_NORMAL_FONT.render("↓", False, self.TEXT_COLOR)
            self.screen.blit(text, (940 - text.get_width() / 2, 360 - text.get_height() / 2))

            # World list
            hovered_world = None
            for i, world_data in enumerate(self.world_list):
                rect = pygame.Rect(450, 50+self.scroll_offset+(i*100), 400, 90)
                number = self.MEDIUM_FONT.render(str(i+1)+".", False, (255,255,255))
                name = self.SMALL_FONT.render(world_data[1], False, (255,255,255))
                # date = self.SMALL_FONT.render(world_data[2], False, (255,255,255))
                color = self.BUTTON_BG
                if rect.collidepoint(mouse_pos):
                    hovered_world = i
                    color = self.BUTTON_BG_HOVER
                pygame.draw.rect(self.world_list_surface, self.BUTTON_BORDER, pygame.Rect(0, i*100, 400, 90))
                pygame.draw.rect(self.world_list_surface, color, pygame.Rect(5, i*100+5, 390, 80))
                self.world_list_surface.blit(number, (20, (i*100)+50-(number.get_height()/2)))
                self.world_list_surface.blit(name, (80, (i*100)+50-(name.get_height()/2)))

            self.screen.blit(self.world_list_surface, (450, 50+self.scroll_offset))

            if self.game.mouse_hold[0]:
                if hovered[3]:
                    if not(self.scroll_offset < 0 and self.scroll_offset < -self.world_list_surface.get_height()+120):
                        self.scroll_offset -= 10
                elif hovered[4]:
                    if self.scroll_offset < 0:
                        self.scroll_offset += 10

            if 4 in self.game.mouse_press:
                if not(self.scroll_offset < 0 and self.scroll_offset < -self.world_list_surface.get_height()+120):
                    self.scroll_offset -= 20
            if 5 in self.game.mouse_press:
                if self.scroll_offset < 0:
                    self.scroll_offset += 20

            if 1 in self.game.mouse_press:
                if hovered[0]:
                    self.screen_state = 2
                elif hovered[1]:
                    self.delete_world = not self.delete_world
                elif hovered[2]:
                    self.screen_state = 0
                elif hovered_world is not None:
                    if not self.delete_world:
                        self.game.game = Game(self.game, self.world_list[hovered_world][3])
                        self.game.state = "game"
                        del self
                    else:
                        # deleting world
                        self.delete_world = False
                        shutil.rmtree(os.path.join(self.game.GAME_PATH, f"saves/{self.world_list[hovered_world][3]}"))
                        self.world_list = self.get_world_list()
                        self.world_list_surface = pygame.Surface((420, 100 * len(self.world_list)), pygame.SRCALPHA)


        elif self.screen_state == 2:
            hovered = [False, False, False]

            rect = pygame.Rect(250, 50, 500, 80)
            color = self.BUTTON_BG
            self.cursor_counter += 1
            temp = ""
            if rect.collidepoint(mouse_pos):
                hovered[0] = True
                color = self.BUTTON_BG_HOVER
            if self.input_focus:
                if self.cursor_counter % 40 < 20:
                    temp = "|"
                color = (90, 90, 90)

            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (255, 55, 490, 70))
            text = self.SMALL_FONT.render("Name:", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 90 - text.get_height() / 2))
            text = self.SMALL_FONT.render(self.entered_name + temp, False, self.TEXT_COLOR)
            self.screen.blit(text, (270, 90 - text.get_height() / 2))

            rect = pygame.Rect(375, 150, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[1] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (380, 155, 240, 70))
            text = self.SMALL_FONT.render("Create!", False, self.TEXT_COLOR)
            self.screen.blit(text, (500 - text.get_width() / 2, 190 - text.get_height() / 2))

            rect = pygame.Rect(50, 520, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                hovered[2] = True
                color = self.BUTTON_BG_HOVER
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (55, 525, 240, 70))
            text = self.SMALL_FONT.render("Go Back", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 560 - text.get_height() / 2))

            if pygame.mouse.get_pressed(3)[0]:
                if hovered[0]:
                    self.input_focus = True
                else:
                    self.input_focus = False
                    if hovered[1]:
                        if self.entered_name == "":
                            self.entered_name = "New World"
                        self.game.game = Game(self.game, -1, self.entered_name)
                        self.game.state = "game"
                        self.world_list = self.get_world_list()
                        self.world_list_surface = pygame.Surface((420, 100 * len(self.world_list)), pygame.SRCALPHA)
                        self.input_focus = False
                        self.entered_name = ""
                        del self
                    elif hovered[2]:
                        self.entered_name = ""
                        self.input_focus = False
                        self.screen_state = 1

        elif self.screen_state == 3:
            # options screen
            text = self.MEDIUM_FONT.render("Options", False, (0,0,0))
            self.screen.blit(text, (502 - text.get_width()/2, 22))
            text = self.MEDIUM_FONT.render("Options", False, (255,255,255))
            self.screen.blit(text, (500 - text.get_width()/2, 20))
            hovered = None
            for i, e in enumerate(self.options_buttons):
                rect = pygame.Rect(e[0], e[1], e[2], e[3])
                color = self.BUTTON_BG
                if rect.collidepoint(mouse_pos):
                    hovered = i
                    color = self.BUTTON_BG_HOVER
                pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
                pygame.draw.rect(self.screen, color, (e[0]+5, e[1]+5, e[2]-10, e[3]-10))
                self.screen.blit(e[4], (e[0]+e[2]/2 - e[4].get_width()/2, e[1]+e[3]/2 - e[4].get_height() / 2))

            if 1 in self.game.mouse_press and hovered is not None:
                if hovered == 0:
                    self.screen_state = 0
                elif hovered == 1:
                    self.screen_state = 4
                elif hovered == 2:
                    if self.game.settings["color_mode"] == "light_mode":
                        self.game.settings["color_mode"] = "dark_mode"
                        self.game.main_menu = MainMenu(self.game)
                    elif self.game.settings["color_mode"] == "dark_mode":
                        self.game.settings["color_mode"] = "light_mode"
                        self.game.main_menu = MainMenu(self.game)

        elif self.screen_state == 4:
            # creators screen
            text = self.MEDIUM_FONT.render("Credits", False, (0,0,0))
            self.screen.blit(text, (502 - text.get_width()/2, 22))
            text = self.MEDIUM_FONT.render("Credits", False, (255,255,255))
            self.screen.blit(text, (500 - text.get_width()/2, 20))

            text = self.MEDIUM_FONT.render("Wszystko (prawie): Mateusz Cieszczyk", False, (0,0,0))
            self.screen.blit(text, (505 - text.get_width()/2+3, 203))
            text = self.MEDIUM_FONT.render("Wszystko (prawie): Mateusz Cieszczyk", False, (255,255,255))
            self.screen.blit(text, (505 - text.get_width()/2, 200))

            temp = 505 - text.get_width()/2
            text = self.SMALL_FONT.render("Kwiaty i chmury: Karol Lukiewski", False, (0,0,0))
            self.screen.blit(text, (temp+3, 303))
            text = self.SMALL_FONT.render("Kwiaty i chmury: Karol Lukiewski", False, (255,255,255))
            self.screen.blit(text, (temp, 300))

            rect = pygame.Rect(50, 520, 250, 80)
            color = self.BUTTON_BG
            if rect.collidepoint(mouse_pos):
                color = self.BUTTON_BG_HOVER
                if 1 in self.game.mouse_press:
                    self.screen_state = 3
            pygame.draw.rect(self.screen, self.BUTTON_BORDER, rect)
            pygame.draw.rect(self.screen, color, (55, 525, 240, 70))
            text = self.SMALL_FONT.render("Go Back", False, self.TEXT_COLOR)
            self.screen.blit(text, (175 - text.get_width() / 2, 560 - text.get_height() / 2))

    def get_world_list(self):
        temp = []
        for i in os.listdir(os.path.join(self.game.GAME_PATH, "saves")):
            try:
                with open(os.path.join(self.game.GAME_PATH, f"saves/{i}/main_data.txt")) as file:
                    lines = file.readlines()
                    lines = [i.strip() for i in lines]
                    lines.append(i)
                    temp.append(lines)
            except FileNotFoundError:
                pass
        return temp


def get_random_splash():
    with open("textures/gui/splashes.txt", encoding="utf-8") as file:

        return random.choice(file.readlines()).strip()
