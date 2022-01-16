import pygame
from itemstack import ItemStack


# noinspection PyUnresolvedReferences,PyTypeChecker
class CraftingView:
    def __init__(self, game):
        self.game = game
        self.crafting_slots = [None for _ in range(10)]
        self.font = pygame.font.Font("freesansbold.ttf", 20)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game.screen_state = "game"
            self.game.to_update = [self.game, self.game.player]

        inv_background = pygame.Surface(self.game.screen.get_size(), 32).convert_alpha()
        inv_background.fill((0, 0, 0, 150))
        self.game.screen.blit(inv_background, (0, 0))

        # Tło
        bg_rect = pygame.Rect(215, 50, 570, 535)
        pygame.draw.rect(self.game.screen, self.game.INV_BORDER, bg_rect, border_radius=10)
        pygame.draw.rect(self.game.screen, self.game.INV_BG, (220, 55, 560, 525), border_radius=10)

        self.display_crafting_3x3(475, 100)
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
                print("dropped in cra")

            self.game.inventory_view.item_on_mouse = None



    def display_crafting_3x3(self, x, y):
        clicked = None
        hovered = None
        for i in range(9):
            rect = pygame.Rect(x + (60 * (i % 3)), y + (60 * (i // 3)), 50, 50)

            pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
            pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG,
                             (x + 3 + (60 * (i % 3)), y + 3 + (60 * (i // 3)), 44, 44), border_radius=5)

            if self.crafting_slots[i] is not None:
                self.game.screen.blit(self.crafting_slots[i].txt, (x + 15 + (60 * (i % 3)), y + 15 + (60 * (i // 3))))
                if self.crafting_slots[i].count > 1:
                    text = self.font.render(str(self.crafting_slots[i].count), False, (255, 255, 255))
                    width = text.get_size()[0]
                    self.game.screen.blit(text, (-width + x + 47 + (60 * (i % 3)), y + 25 + (60 * (i // 3))))

            if rect.collidepoint(pygame.mouse.get_pos()):
                if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                    clicked = i
                hovered = i

        rect = pygame.Rect(x + 200, y + 60, 50, 50)
        pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
        pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG, (x + 203, y + 63, 44, 44), border_radius=5)

        if self.crafting_slots[9] is not None:
            self.game.screen.blit(self.crafting_slots[9].txt, (x + 215, y + 75))
            if self.crafting_slots[9].count > 1:
                text = self.font.render(str(self.crafting_slots[9].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (x + 247 - width, y + 85))

        if rect.collidepoint(pygame.mouse.get_pos()):
            if 3 in self.game.game.mouse_press or 1 in self.game.game.mouse_press:
                clicked = 9
            hovered = 9

        # Wyswietlanie nazwy przedmiotu po najechaniu (w craftingu)
        if hovered is not None and self.crafting_slots[hovered] is not None:
            mouse_pos = pygame.mouse.get_pos()
            render = self.game.ITEM_HINT_FONT.render(self.crafting_slots[hovered].name, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (50, 50, 50), (
                mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20,
                render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (120, 120, 120), (
                mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10,
                render.get_height() + 10), border_radius=5)
            self.game.screen.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        crafting_shape = [[0,0,0],[0,0,0],[0,0,0]]
        if clicked is not None:
            if clicked == 9:
                if self.crafting_slots[9] is not None:
                    if self.game.inventory_view.item_on_mouse is None:
                        self.game.inventory_view.item_on_mouse = self.crafting_slots[9]
                        self.crafting_slots[9] = None
                        self.get_crafted_item()
                    elif self.game.inventory_view.item_on_mouse is not None and self.game.inventory_view.item_on_mouse.item_id == self.crafting_slots[9].item_id:
                        self.game.inventory_view.item_on_mouse.count += self.crafting_slots[9].count
                        self.crafting_slots[9] = None
                        self.get_crafted_item()

            else:
                if 1 in self.game.game.mouse_press:
                    if self.crafting_slots[clicked] is None or self.game.inventory_view.item_on_mouse is None or self.crafting_slots[clicked].item_id != self.game.inventory_view.item_on_mouse.item_id:
                        self.crafting_slots[clicked], self.game.inventory_view.item_on_mouse = self.game.inventory_view.item_on_mouse, self.crafting_slots[
                            clicked]
                    else:
                        self.crafting_slots[clicked].count += self.game.inventory_view.item_on_mouse.count
                        self.game.inventory_view.item_on_mouse = None

                elif 3 in self.game.game.mouse_press:
                    if self.crafting_slots[clicked] is None and self.game.inventory_view.item_on_mouse is not None:
                        self.crafting_slots[clicked] = ItemStack(self.game.inventory_view.item_on_mouse.item_id, 1)
                        self.game.inventory_view.item_on_mouse.count -= 1
                        if self.game.inventory_view.item_on_mouse.count == 0:
                            self.game.inventory_view.item_on_mouse = None
                    elif self.crafting_slots[clicked] is not None and self.game.inventory_view.item_on_mouse is not None and \
                            self.crafting_slots[clicked].item_id == self.game.inventory_view.item_on_mouse.item_id:
                        self.crafting_slots[clicked].count += 1
                        self.game.inventory_view.item_on_mouse.count -= 1
                        if self.game.inventory_view.item_on_mouse.count == 0:
                            self.game.inventory_view.item_on_mouse = None
                    elif self.crafting_slots[clicked] is not None and self.game.inventory_view.item_on_mouse is not None and \
                            self.crafting_slots[clicked].item_id != self.game.inventory_view.item_on_mouse.item_id:
                        self.crafting_slots[clicked], self.game.inventory_view.item_on_mouse = self.game.inventory_view.item_on_mouse, self.crafting_slots[
                            clicked]
                    elif self.crafting_slots[clicked] is not None and self.game.inventory_view.item_on_mouse is None:
                        count = self.crafting_slots[clicked].count // 2
                        self.game.inventory_view.item_on_mouse = ItemStack(self.crafting_slots[clicked].item_id, count)
                        self.crafting_slots[clicked].count -= count
            for i in range(9):
                if self.crafting_slots[i] is None:
                    crafting_shape[i//3][i % 3] = 0
                else:
                    crafting_shape[i//3][i % 3] = self.crafting_slots[i].item_id

            self.crafting_slots[9] = self.game.inventory_view.get_crafting_recipe(crafting_shape)
        # return clicked

    def get_crafted_item(self):
        for i in range(9):
            if self.crafting_slots[i] is not None:
                self.crafting_slots[i].count -= 1
                if self.crafting_slots[i].count == 0:
                    self.crafting_slots[i] = None
        self.crafting_slots[9] = None


def get_combination(r, crafting_type=2):
    # if crafting_type != 2 and crafting_type != 3:
    #     return []
    width = 0
    height = len(r)
    for i in r:
        width = max(len(i), width)

    possibilities = []

    for i in range(abs(height - (crafting_type+1))):
        for j in range(abs(width - (crafting_type+1))):
            temp = copy.deepcopy(r)
            for m in range(len(temp)):
                for _ in range(j):
                    temp[m].insert(0, 0)

            for k in range(i):
                temp.insert(0, [0, 0, 0])

            for m in temp:
                for _ in range(abs(len(m) - crafting_type)):
                    m.append(0)

            for _ in range(abs(len(temp) - crafting_type)):
                t = []
                for _ in range(crafting_type):
                    t.append(0)
                temp.append(t)

            possibilities.append(temp)
    return possibilities
