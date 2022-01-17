import pygame


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 40)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)

    def update(self):
        surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        surface.convert_alpha()
        surface.fill((0,0,0,150))

        text = self.FONT.render("PAUSE MENU", False, self.game.SHADOW_COLOR)
        surface.blit(text, (self.screen.get_width()/2 - text.get_width()/2+3, 83))
        text = self.FONT.render("PAUSE MENU", False, self.game.TEXT_COLOR)
        surface.blit(text, (self.screen.get_width()/2 - text.get_width()/2, 80))

        mouse_pos = pygame.mouse.get_pos()
        hovered = [False, False]

        text = self.MEDIUM_FONT.render("Back to game", False, self.game.TEXT_COLOR)
        rect = pygame.Rect(300, 200, 400, 90)
        color = self.game.BUTTON_BG 
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            hovered[0] = True
            color = self.game.BUTTON_BG_HOVER
        pygame.draw.rect(surface, self.game.BUTTON_BORDER, rect, border_radius=10)
        pygame.draw.rect(surface, color, pygame.Rect(305, 205, 390, 80), border_radius=10)
        surface.blit(text, (500 - (text.get_width() / 2), 245 - text.get_height() / 2))


        text = self.MEDIUM_FONT.render("Return to main menu", False, self.game.TEXT_COLOR)
        color = self.game.BUTTON_BG
        rect = pygame.Rect(300, 320, 400, 90)
        if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            hovered[1] = True
            color = self.game.BUTTON_BG_HOVER
        pygame.draw.rect(surface, self.game.BUTTON_BORDER, rect, border_radius=10)
        pygame.draw.rect(surface, color, pygame.Rect(305, 325, 390, 80), border_radius=10)
        surface.blit(text, (500 - (text.get_width() / 2), 365 - text.get_height() / 2))

        if pygame.mouse.get_pressed(3)[0]:
            if hovered[0]:
                self.game.screen_state = "game"
                self.game.paused = False
                self.game.to_update = [self.game, self.game.player]
            elif hovered[1]:
                self.game.save_world()
                self.game.game.game = None
                self.game.game.state = "main_menu"
                self.game.game.main_menu.screen_state = 1
                del self.game

        self.screen.blit(surface, (0,0))
