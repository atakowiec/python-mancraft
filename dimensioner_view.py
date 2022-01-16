import pygame
from itemstack import ItemStack


# noinspection PyUnresolvedReferences,PyTypeChecker
class DimensionerView:
    def __init__(self, game):
        self.game = game
        self.slots = [None, None]
        self.font = pygame.font.Font("freesansbold.ttf", 20)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game.screen_state = "game"
            self.game.to_update = [self.game, self.game.player]

            self.game.player.drop_item(self.slots[0])
            self.slots = [None, None]
            self.game.player.drop_item(self.game.inventory_view.item_on_mouse)
            self.game.inventory_view.item_on_mouse = None

        elif pygame.key.get_pressed()[pygame.K_e]:
            for i, itemstack in enumerate(self.slots[:-1]):
                self.game.player.drop_item(itemstack)

            self.game.player.drop_item(self.slots[0])
            self.slots = [None, None]
            self.game.player.drop_item(self.game.inventory_view.item_on_mouse)
            self.game.inventory_view.item_on_mouse = None

        inv_background = pygame.Surface(self.game.screen.get_size(), 32).convert_alpha()
        inv_background.fill((0, 0, 0, 150))
        self.game.screen.blit(inv_background, (0, 0))

        # Tło
        bg_rect = pygame.Rect(215, 50, 570, 535)
        pygame.draw.rect(self.game.screen, self.game.INV_BORDER, bg_rect, border_radius=10)
        pygame.draw.rect(self.game.screen, self.game.INV_BG, (220, 55, 560, 525), border_radius=10)

        self.display_dimensioner(415, 100)
        self.game.inventory_view.display_inventory()

        # Wyrzucanie blokow
        if not bg_rect.collidepoint(mouse_pos) and self.game.inventory_view.item_on_mouse is not None and (1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press):
            v = 0.2
            if (25 * 20) - mouse_pos[0] > 0:
                v = -v
                position = [self.game.player.pos[0], self.game.player.pos[1] + 1.5]
            else:
                position = [self.game.player.pos[0], self.game.player.pos[1] + 1.5]
            for i in range(self.game.inventory_view.item_on_mouse.count):
                self.game.create_item_on_ground(self.game.inventory_view.item_on_mouse.item_id, position, immunite=30, velocity=[v, 0])

            self.game.inventory_view.item_on_mouse = None



    def display_dimensioner(self, x, y):
        hovered = None
        rect = pygame.Rect(x+0, y+0, 50, 50)
        pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
        pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG,
                         (x+3, y+3, 44, 44), border_radius=5)

        if self.slots[0] is not None:
            self.game.screen.blit(self.slots[0].txt, (x + 15, y + 15))
            if self.slots[0].count > 1:
                text = self.font.render(str(self.slots[0].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (-width + x + 47, y + 25))

        if rect.collidepoint(pygame.mouse.get_pos()):
            hovered = 0
            if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                self.game.inventory_view.item_on_mouse, self.slots[0] = self.game.inventory_view.handle_inv_click(self.game.inventory_view.item_on_mouse, self.slots[0])

        rect = pygame.Rect(x + 120, y + 0, 50, 50)
        pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
        pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG, (x + 123, y + 3, 44, 44), border_radius=5)
        if self.slots[1] is not None:
            self.game.screen.blit(self.slots[1].txt, (x + 135, y + 15))
            if self.slots[1].count > 1:
                text = self.font.render(str(self.slots[1].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (-width + x + 167, y + 25))

        if rect.collidepoint(pygame.mouse.get_pos()):
            hovered = 1
            if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                if self.slots[1] is not None:
                    if self.game.inventory_view.item_on_mouse is None:
                        self.game.inventory_view.item_on_mouse = self.slots[1]
                        self.slots = [None, None]
                    elif self.game.inventory_view.item_on_mouse is not None and self.game.inventory_view.item_on_mouse.item_id == self.slots[1].item_id and self.game.inventory_view.item_on_mouse.behind == self.slots[1].behind:
                        self.game.inventory_view.item_on_mouse.count += self.slots[1].count
                        self.slots = [None, None]

        # Wyswietlanie nazwy przedmiotu po najechaniu (w craftingu)
        if hovered is not None and self.slots[hovered] is not None:
            mouse_pos = pygame.mouse.get_pos()
            behind_message = ""
            if self.slots[hovered].behind:
                behind_message = " (behind)"
            render = self.game.ITEM_HINT_FONT.render(self.slots[hovered].name+behind_message, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (70, 70, 70), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (140, 140, 140), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            self.game.screen.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        self.slots[1] = None
        if self.slots[0] is not None and self.slots[0].data['type'] == "block":
            self.slots[1] = ItemStack(self.slots[0].item_id, self.slots[0].count, not self.slots[0].behind)
