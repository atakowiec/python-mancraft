import pygame
import os
from game import Game

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_state = 0

        self.BACKGROUND = pygame.image.load("textures/backgrounds/main_menu.png")
        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 90)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 50)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.SMALL_NORMAL_FONT = pygame.font.Font("textures/fonts/Merriweather-Regular.ttf", 30)

        # components
        self.logo_light = self.FONT.render("Mankraft", False, (255, 255, 255))
        self.logo_dark = self.FONT.render("Mankraft", False, (0, 0, 0))
        self.st_button_text = self.SMALL_FONT.render("Singleplayer", False, (255, 255, 255))
        self.nd_button_text = self.SMALL_FONT.render("Exit", False, (255, 255, 255))

        # Loading world list
        self.scroll_offset = 0
        self.world_list = []
        for i in os.listdir(os.path.join(self.game.GAME_PATH, "saves")):
            with open(os.path.join(self.game.GAME_PATH, f"saves/{i}/main_data.txt")) as file:
                lines = file.readlines()
                lines = [i.strip() for i in lines]
                self.world_list.append(lines)

        self.world_list_surface = pygame.Surface((420, 100*len(self.world_list)), pygame.SRCALPHA)
        self.world_list_surface.convert_alpha()

    def update(self):
        # tło

        self.screen.blit(self.BACKGROUND, (0, 0))
        if self.screen_state == 0:
            # Main menu
            # logo
            self.screen.blit(self.logo_dark, ((self.screen.get_width() - self.logo_light.get_width()) / 2 + 5, 55))
            self.screen.blit(self.logo_light, ((self.screen.get_width() - self.logo_light.get_width()) / 2, 50))

            # przyciski
            mouse_pos = pygame.mouse.get_pos()
            hovered = [False, False]

            rect = pygame.Rect(300, 200, 400, 90)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered[0] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=10)
            pygame.draw.rect(self.screen, color, pygame.Rect(305, 205, 390, 80), border_radius=10)
            self.screen.blit(self.st_button_text,
                             (500 - (self.st_button_text.get_width() / 2), 245 - self.st_button_text.get_height() / 2))

            color = (140, 140, 140)
            rect = pygame.Rect(300, 320, 400, 90)
            if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                hovered[1] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect, border_radius=10)
            pygame.draw.rect(self.screen, color, pygame.Rect(305, 325, 390, 80), border_radius=10)
            self.screen.blit(self.nd_button_text,
                             (500 - (self.nd_button_text.get_width() / 2), 365 - self.nd_button_text.get_height() / 2))

            if pygame.mouse.get_pressed(3)[0]:
                if hovered[1]:
                    self.game.running = False
                if hovered[0]:
                    self.screen_state = 1

        elif self.screen_state == 1:
            # world selector
            hovered = [False, False, False, False, False]
            mouse_pos = pygame.mouse.get_pos()

            rect = pygame.Rect(50, 50, 250, 80)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos):
                hovered[0] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect)
            pygame.draw.rect(self.screen, color, (55, 55, 240, 70))
            text = self.SMALL_FONT.render("New World", False, (255, 255, 255))
            self.screen.blit(text, (175 - text.get_width() / 2, 90 - text.get_height() / 2))

            rect = pygame.Rect(50, 150, 250, 80)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos):
                hovered[1] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect)
            pygame.draw.rect(self.screen, color, (55, 155, 240, 70))
            text = self.SMALL_FONT.render("Delete World", False, (255, 255, 255))
            self.screen.blit(text, (175 - text.get_width() / 2, 190 - text.get_height() / 2))

            rect = pygame.Rect(50, 520, 250, 80)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos):
                hovered[2] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect)
            pygame.draw.rect(self.screen, color, (55, 525, 240, 70))
            text = self.SMALL_FONT.render("Go Back", False, (255, 255, 255))
            self.screen.blit(text, (175 - text.get_width() / 2, 560 - text.get_height() / 2))

            rect = pygame.Rect(900, 230, 80, 80)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos):
                hovered[3] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect)
            pygame.draw.rect(self.screen, color, (905, 235, 70, 70))
            text = self.SMALL_NORMAL_FONT.render("↑", False, (255, 255, 255))
            self.screen.blit(text, (940 - text.get_width() / 2, 270 - text.get_height() / 2))

            rect = pygame.Rect(900, 320, 80, 80)
            color = (140, 140, 140)
            if rect.collidepoint(mouse_pos):
                hovered[4] = True
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, (40, 40, 40), rect)
            pygame.draw.rect(self.screen, color, (905, 325, 70, 70))
            text = self.SMALL_NORMAL_FONT.render("↓", False, (255, 255, 255))
            self.screen.blit(text, (940 - text.get_width() / 2, 360 - text.get_height() / 2))

            # World list
            hovered_world = None
            for i, world_data in enumerate(self.world_list):
                rect = pygame.Rect(450, 50+self.scroll_offset+(i*100), 400, 90)
                number = self.MEDIUM_FONT.render(str(i+1)+".", False, (255,255,255))
                name = self.SMALL_FONT.render(world_data[1], False, (255,255,255))
                date = self.SMALL_FONT.render(world_data[2], False, (255,255,255))
                color = (140, 140, 140)
                if rect.collidepoint(mouse_pos):
                    hovered_world = i+1
                    color = (100, 100, 100)
                pygame.draw.rect(self.world_list_surface, (40, 40, 40), pygame.Rect(0, i*100, 400, 90))
                pygame.draw.rect(self.world_list_surface, color, pygame.Rect(5, i*100+5, 390, 80))
                self.world_list_surface.blit(number, (20, (i*100)+50-(number.get_height()/2)))
                self.world_list_surface.blit(name, (80, (i*100)+50-(name.get_height()/2)))

            self.screen.blit(self.world_list_surface, (450, 50+self.scroll_offset))

            if pygame.mouse.get_pressed(3)[0]:
                if hovered[1]:
                    pass
                elif hovered[2]:
                    self.screen_state = 0
                elif hovered[3]:
                    if not(self.scroll_offset < 0 and self.scroll_offset < -self.world_list_surface.get_height()+120):
                        self.scroll_offset -= 10
                elif hovered[4]:
                    if self.scroll_offset < 0:
                        self.scroll_offset += 10
                elif hovered_world is not None:
                    self.game.game = Game(self.game, hovered_world)
                    self.game.state = "game"
                    del self
