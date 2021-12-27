import pygame
from itemstack import ItemStack
from dropped_item import DroppedItem


class InventoryView:
    def __init__(self, game):
        self.game = game
        self.item_on_mouse = None
        self.shown = False
        self.crafting_slots = [None, None, None, None, None]
        self.font = pygame.font.Font("freesansbold.ttf", 20)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game.screen_state = "game"

        inv_background = pygame.Surface(self.game.screen.get_size(), 32).convert_alpha()
        inv_background.fill((0,0,0,150))
        self.game.screen.blit(inv_background, (0,0))
        mouse_pos = pygame.mouse.get_pos()
        hovered_item = None
        clicked = None
        for i, itemstack in enumerate(self.game.player.inventory):
            rect = pygame.Rect(10 + (60*(i % 9)), 10+(60*(i//9)), 50, 50)
            pygame.draw.rect(self.game.screen, (50,50,50), rect, border_radius=5)
            pygame.draw.rect(self.game.screen, (120,120,120), (13 + (60*(i % 9)), 13+(60*(i//9)), 44, 44), border_radius=5)

            if self.game.mouse_click == 1 and rect.collidepoint(mouse_pos):
                clicked = -1
                if itemstack is None or self.item_on_mouse is None or itemstack.item_id != self.item_on_mouse.item_id:
                    self.game.player.inventory[i], self.item_on_mouse = self.item_on_mouse, self.game.player.inventory[i]
                else:
                    self.game.player.inventory[i].count += self.item_on_mouse.count
                    self.item_on_mouse = None

            elif self.game.mouse_click == 3 and rect.collidepoint(mouse_pos):
                clicked = -1
                if itemstack is None and self.item_on_mouse is not None:
                    self.game.player.inventory[i] = ItemStack(self.item_on_mouse.item_id, 1)
                    self.item_on_mouse.count -= 1
                    if self.item_on_mouse.count == 0:
                        self.item_on_mouse = None
                elif itemstack is not None and self.item_on_mouse is not None and itemstack.item_id == self.item_on_mouse.item_id:
                    self.game.player.inventory[i].count += 1
                    self.item_on_mouse.count -= 1
                    if self.item_on_mouse.count == 0:
                        self.item_on_mouse = None
                elif itemstack is not None and self.item_on_mouse is not None and itemstack.item_id != self.item_on_mouse.item_id:
                    self.game.player.inventory[i], self.item_on_mouse = self.item_on_mouse, self.game.player.inventory[i]
                elif itemstack is not None and self.item_on_mouse is None:
                    count = self.game.player.inventory[i].count//2
                    self.item_on_mouse = ItemStack(itemstack.item_id, count)
                    self.game.player.inventory[i].count -= count

            if itemstack is not None:
                # pygame.draw.rect(self.game.screen, itemstack.txt, (25 + (60*(i % 9)), 25+(60*(i//9)), 20, 20))
                self.game.screen.blit(itemstack.txt, (25 + (60*(i % 9)), 25+(60*(i//9))))
                text = self.game.font.render(str(itemstack.count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (53 + (60*(i % 9)) - width, 36+(60*(i//9))))

                if rect.collidepoint(mouse_pos):
                    hovered_item = itemstack

        # wyswietlanie craftingu
        clicked_on_crafting = self.display_crafting_2x2(590, 70)

        if clicked_on_crafting is None and clicked is None and self.game.mouse_click == 1 and self.item_on_mouse is not None:
            v = 0.2
            if (25*20)-mouse_pos[0] > 0:
                v = -v
                position = [self.game.player.pos[0],self.game.player.pos[1]+1.5]
            else:
                position = [self.game.player.pos[0],self.game.player.pos[1]+1.5]
            for i in range(self.item_on_mouse.count):
                self.game.create_item_on_ground(self.item_on_mouse.item_id, position, immunite=30, velocity=[v,0])
            self.item_on_mouse = None

        # wyswietlanie itemu trzymanego na myszce
        if self.item_on_mouse is not None:
            self.game.screen.blit(self.item_on_mouse.txt, pygame.mouse.get_pos())
            text = self.game.font.render(str(self.item_on_mouse.count), False, (255, 255, 255))
            self.game.screen.blit(text, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]+20))

        if hovered_item is not None:
            render = self.game.ITEM_HINT_FONT.render(hovered_item.name, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (50, 50, 50), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (120, 120, 120), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            self.game.screen.blit(self.game.ITEM_HINT_FONT.render(hovered_item.name, False, (0, 0, 0)), (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

    def display_crafting_2x2(self, x, y):
        clicked = None
        hovered = None
        for i in range(4):
            rect = pygame.Rect(x + (60*(i % 2)), y+(60*(i//2)), 50, 50)

            pygame.draw.rect(self.game.screen, (50,50,50), rect, border_radius=5)
            pygame.draw.rect(self.game.screen, (120,120,120), (x + 3 + (60*(i % 2)), y+3+(60*(i//2)), 44, 44), border_radius=5)

            if self.crafting_slots[i] is not None:
                self.game.screen.blit(self.crafting_slots[i].txt, (x + 15 + (60*(i % 2)), y+15+(60*(i//2))))
                text = self.font.render(str(self.crafting_slots[i].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (-width+x+47+(60*(i % 2)), y+25+(60*(i//2))))

            if rect.collidepoint(pygame.mouse.get_pos()):
                if self.game.mouse_click is not None:
                    clicked = i
                hovered = i

        rect = pygame.Rect(x + 140, y + 30, 50, 50)
        pygame.draw.rect(self.game.screen, (50,50,50), rect, border_radius=5)
        pygame.draw.rect(self.game.screen, (120,120,120), (x + 143, y + 33, 44, 44), border_radius=5)

        if self.crafting_slots[4] is not None:
            self.game.screen.blit(self.crafting_slots[4].txt, (x + 155, y + 45))
            text = self.font.render(str(self.crafting_slots[4].count), False, (255, 255, 255))
            width = text.get_size()[0]
            self.game.screen.blit(text, (x+187-width, y + 55))

        if rect.collidepoint(pygame.mouse.get_pos()):
            if self.game.mouse_click is not None:
                clicked = 4
            hovered = 4

        # Wyswietlanie nazwy przedmiotu po najechaniu (w craftingu)
        if hovered is not None and self.crafting_slots[hovered] is not None:
            mouse_pos = pygame.mouse.get_pos()
            render = self.game.ITEM_HINT_FONT.render(self.crafting_slots[hovered].name, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (50, 50, 50), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (120, 120, 120), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            self.game.screen.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        crafting_shape = [0,0,0,0]
        if clicked is not None:
            if clicked == 4:
                if self.crafting_slots[4] is not None:
                    if self.item_on_mouse is None:
                        self.item_on_mouse = self.crafting_slots[4]
                        self.crafting_slots[4] = None
                        self.get_crafted_item()
                    elif self.item_on_mouse is not None and self.item_on_mouse.item_id == self.crafting_slots[4].item_id:
                        self.item_on_mouse.count += self.crafting_slots[4].count
                        self.crafting_slots[4] = None
                        self.get_crafted_item()

            else:
                if self.game.mouse_click == 1:
                    if self.crafting_slots[clicked] is None or self.item_on_mouse is None or self.crafting_slots[clicked].item_id != self.item_on_mouse.item_id:
                        self.crafting_slots[clicked], self.item_on_mouse = self.item_on_mouse, self.crafting_slots[clicked]
                    else:
                        self.crafting_slots[clicked].count += self.item_on_mouse.count
                        self.item_on_mouse = None

                elif self.game.mouse_click == 3:
                    if self.crafting_slots[clicked] is None and self.item_on_mouse is not None:
                        self.crafting_slots[clicked] = ItemStack(self.item_on_mouse.item_id, 1)
                        self.item_on_mouse.count -= 1
                        if self.item_on_mouse.count == 0:
                            self.item_on_mouse = None
                    elif self.crafting_slots[clicked] is not None and self.item_on_mouse is not None and self.crafting_slots[clicked].item_id == self.item_on_mouse.item_id:
                        self.crafting_slots[clicked].count += 1
                        self.item_on_mouse.count -= 1
                        if self.item_on_mouse.count == 0:
                            self.item_on_mouse = None
                    elif self.crafting_slots[clicked] is not None and self.item_on_mouse is not None and self.crafting_slots[clicked].item_id != self.item_on_mouse.item_id:
                        self.crafting_slots[clicked], self.item_on_mouse = self.item_on_mouse, self.crafting_slots[clicked]
                    elif self.crafting_slots[clicked] is not None and self.item_on_mouse is None:
                        count = self.crafting_slots[clicked].count//2
                        self.item_on_mouse = ItemStack(self.crafting_slots[clicked].item_id, count)
                        self.crafting_slots[clicked].count -= count
            for i in range(4):
                if self.crafting_slots[i] is None:
                    crafting_shape[i] = 0
                else:
                    crafting_shape[i] = self.crafting_slots[i].item_id

            self.crafting_slots[4] = get_crafting_recipe(crafting_shape)
            return clicked

    def get_crafted_item(self):
        for i in range(4):
            if self.crafting_slots[i] is not None:
                self.crafting_slots[i].count -= 1
                if self.crafting_slots[i].count == 0:
                    self.crafting_slots[i] = None
        self.crafting_slots[4] = None


def get_crafting_recipe(shape):
    recipes = (
        ([0,0,0,6], ItemStack(13, 4)),
        ([0,0,6,0], ItemStack(13, 4)),
        ([0,6,0,0], ItemStack(13, 4)),
        ([6,0,0,0], ItemStack(13, 4)),
        ([13,13,13,13], ItemStack(14, 1)),
    )
    for i in recipes:
        if i[0] == shape:
            return i[1]
    return None
