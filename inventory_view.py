import pygame
from itemstack import ItemStack
from dropped_item import DroppedItem


# noinspection PyTypeChecker
class InventoryView:
    def __init__(self, game):
        self.game = game
        self.item_on_mouse = None
        self.crafting_slots = [None, None, None, None, None]
        self.font = pygame.font.Font("freesansbold.ttf", 20)

    def display_inventory(self):
        surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
        surface.convert_alpha()
        surface_pos = (0,0)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = [mouse_pos[0]-surface_pos[0], mouse_pos[1]-surface_pos[1]]
        hovered_item = None
        
        for i, itemstack in enumerate(self.game.player.inventory):
            rect = pygame.Rect(235 + (60*(i % 9)), 335 + (60*(i//9)), 50, 50)
            pygame.draw.rect(surface, self.game.BUTTON_BORDER, rect, border_radius=5)
            pygame.draw.rect(surface, self.game.INV_SLOT_BG, (238+(60*(i % 9)), 338+(60*(i//9)), 44, 44), border_radius=5)
            if (1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press) and rect.collidepoint(mouse_pos):
                self.item_on_mouse, self.game.player.inventory[i] = self.handle_inv_click(self.item_on_mouse, itemstack)

            if itemstack is not None:
                surface.blit(itemstack.txt, (250 + (60*(i % 9)), 350+(60*(i//9))))
                if itemstack.count > 1:
                    text = self.game.font.render(str(itemstack.count), False, (255, 255, 255))
                    width = text.get_size()[0]
                    surface.blit(text, (288 + (60*(i % 9)) - width, 371+(60*(i//9))))

                if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    hovered_item = itemstack

        if hovered_item is not None:
            behind_message = ""
            if hovered_item.behind:
                behind_message = "(behind)"

            render = self.game.ITEM_HINT_FONT.render(f"{hovered_item.name} {behind_message}", False, (0, 0, 0))
            pygame.draw.rect(surface, (70, 70, 70), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(surface, (140, 140, 140), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            surface.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        # wyswietlanie itemu trzymanego na myszce
        if self.item_on_mouse is not None:
            surface.blit(self.item_on_mouse.txt, mouse_pos)
            text = self.game.font.render(str(self.item_on_mouse.count), False, (255, 255, 255))
            surface.blit(text, (mouse_pos[0]+20, mouse_pos[1]+20))

        self.game.screen.blit(surface, surface_pos)

        # return clicked, hovered_item

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game.screen_state = "game"
            self.game.to_update = [self.game, self.game.player]
            for i, itemstack in enumerate(self.crafting_slots[:-1]):
                self.game.player.drop_item(itemstack)

                self.crafting_slots = [None, None, None, None, None]
            self.game.player.drop_item(self.item_on_mouse)
            self.item_on_mouse = None

        elif pygame.key.get_pressed()[pygame.K_e]:
            for i, itemstack in enumerate(self.crafting_slots[:-1]):
                self.game.player.drop_item(itemstack)

            self.crafting_slots = [None, None, None, None, None]
            self.game.player.drop_item(self.item_on_mouse)
            self.item_on_mouse = None

        inv_background = pygame.Surface(self.game.screen.get_size(), 32).convert_alpha()
        inv_background.fill((0,0,0,150))
        self.game.screen.blit(inv_background, (0,0))

        # Tło
        bg_rect = pygame.Rect(215, 50, 570, 535)
        pygame.draw.rect(self.game.screen, self.game.INV_BORDER, bg_rect, border_radius=10)
        pygame.draw.rect(self.game.screen, self.game.INV_BG, (220, 55, 560, 525), border_radius=10)

        self.display_crafting_2x2(550, 150)
        self.display_inventory()

        # Wyrzucanie blokow
        if not bg_rect.collidepoint(mouse_pos) and self.item_on_mouse is not None and (1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press):
            v = 0.2
            if (25*20)-mouse_pos[0] > 0:
                v = -v
                position = [self.game.player.pos[0],self.game.player.pos[1]+1.5]
            else:
                position = [self.game.player.pos[0],self.game.player.pos[1]+1.5]
            for i in range(self.item_on_mouse.count):
                self.game.create_item_on_ground(self.item_on_mouse.item_id, position, immunite=30, velocity=[v,0], behind=self.item_on_mouse.behind)
            self.item_on_mouse = None


    def display_crafting_2x2(self, x, y):
        clicked = None
        hovered = None
        for i in range(4):
            rect = pygame.Rect(x + (60*(i % 2)), y+(60*(i//2)), 50, 50)

            pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
            pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG, (x + 3 + (60*(i % 2)), y+3+(60*(i//2)), 44, 44), border_radius=5)

            if self.crafting_slots[i] is not None:
                self.game.screen.blit(self.crafting_slots[i].txt, (x + 15 + (60*(i % 2)), y+15+(60*(i//2))))
                if self.crafting_slots[i].count > 1:
                    text = self.font.render(str(self.crafting_slots[i].count), False, (255, 255, 255))
                    width = text.get_size()[0]
                    self.game.screen.blit(text, (-width+x+47+(60*(i % 2)), y+25+(60*(i//2))))

            if rect.collidepoint(pygame.mouse.get_pos()):
                if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                    clicked = i
                hovered = i

        rect = pygame.Rect(x + 140, y + 30, 50, 50)
        pygame.draw.rect(self.game.screen, self.game.BUTTON_BORDER, rect, border_radius=5)
        pygame.draw.rect(self.game.screen, self.game.INV_SLOT_BG, (x + 143, y + 33, 44, 44), border_radius=5)

        if self.crafting_slots[4] is not None:
            self.game.screen.blit(self.crafting_slots[4].txt, (x + 155, y + 45))
            if self.crafting_slots[4].count:
                text = self.font.render(str(self.crafting_slots[4].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (x+187-width, y + 55))

        if rect.collidepoint(pygame.mouse.get_pos()):
            if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                clicked = 4
            hovered = 4

        # Wyswietlanie nazwy przedmiotu po najechaniu (w craftingu)
        if hovered is not None and self.crafting_slots[hovered] is not None:
            behind_message = ""
            if self.crafting_slots[hovered].behind:
                behind_message = " (behind)"
            mouse_pos = pygame.mouse.get_pos()
            render = self.game.ITEM_HINT_FONT.render(self.crafting_slots[hovered].name + behind_message, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (70, 70, 70), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (140, 140, 140), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            self.game.screen.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        crafting_shape = [[0,0],[0,0]]
        if clicked is not None:
            if clicked == 4:
                if self.crafting_slots[4] is not None:
                    if self.item_on_mouse is None:
                        self.item_on_mouse = self.crafting_slots[4]
                        self.crafting_slots[4] = None
                        self.get_crafted_item()
                    elif self.item_on_mouse is not None and self.item_on_mouse.item_id == self.crafting_slots[4].item_id and self.item_on_mouse.behind == self.crafting_slots[4].behind:
                        self.item_on_mouse.count += self.crafting_slots[4].count
                        self.crafting_slots[4] = None
                        self.get_crafted_item()
            else:
                if 1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press:
                    self.item_on_mouse, self.crafting_slots[clicked] = self.handle_inv_click(self.item_on_mouse, self.crafting_slots[clicked])

            for i in range(4):
                if self.crafting_slots[i] is None:
                    crafting_shape[i//2][i % 2] = 0
                else:
                    crafting_shape[i//2][i % 2] = self.crafting_slots[i].item_id

            self.crafting_slots[4] = self.get_crafting_recipe(crafting_shape)

    def handle_inv_click(self, item_on_mouse, item_in_slot, blocked=False):
        if blocked:
            if item_in_slot is not None:
                if item_on_mouse is None:
                    return item_in_slot, None
                elif item_in_slot.item_id == item_on_mouse.item_id and item_in_slot.behind == item_on_mouse.behind:
                    item_on_mouse.count += item_in_slot.count
                    return item_on_mouse, None
            return item_on_mouse, item_in_slot
        else:
            if 1 in self.game.game.mouse_press:
                if item_in_slot is None or item_on_mouse is None or item_in_slot.item_id != item_on_mouse.item_id or item_in_slot.behind != item_on_mouse.behind:
                    item_in_slot, item_on_mouse = item_on_mouse, item_in_slot
                else:
                    item_in_slot.count += item_on_mouse.count
                    item_on_mouse = None

            elif 3 in self.game.game.mouse_press:
                if item_in_slot is None and item_on_mouse is not None:
                    item_in_slot = ItemStack(item_on_mouse.item_id, 1, behind=item_on_mouse.behind)
                    item_on_mouse.count -= 1
                    if item_on_mouse.count == 0:
                        item_on_mouse = None
                elif item_in_slot is not None and item_on_mouse is not None and item_in_slot.item_id == item_on_mouse.item_id and item_in_slot.behind == item_on_mouse.behind:
                    item_in_slot.count += 1
                    item_on_mouse.count -= 1
                    if item_on_mouse.count == 0:
                        item_on_mouse = None
                elif item_in_slot is not None and item_on_mouse is not None and (item_in_slot.item_id != item_on_mouse.item_id or item_in_slot.behind != item_on_mouse.behind):
                    item_in_slot, item_on_mouse = item_on_mouse, item_in_slot
                elif item_in_slot is not None and item_on_mouse is None:
                    count = item_in_slot.count // 2
                    if count != 0:
                        item_on_mouse = ItemStack(item_in_slot.item_id, count, behind=item_in_slot.behind)
                        item_in_slot.count -= count
                    else:
                        item_on_mouse = ItemStack(item_in_slot.item_id, item_in_slot.count, behind=item_in_slot.behind)
                        item_in_slot = None

            return item_on_mouse, item_in_slot

    def get_crafted_item(self):
        for i in range(4):
            if self.crafting_slots[i] is not None:
                self.crafting_slots[i].count -= 1
                if self.crafting_slots[i].count == 0:
                    self.crafting_slots[i] = None
        self.crafting_slots[4] = None

    def get_crafting_recipe(self, shape):
        shape = get_default_combination(shape)
        for id, item in self.game.block_type.items():
            try:
                for recipe in item["crafting_recipe"]:
                    if recipe == shape:
                        behind = False
                        if "default_behind" in item.keys():
                            behind = item["default_behind"]
                        return ItemStack(id, item["crafting_amount"], behind=behind)
            except KeyError:
                pass
        return None


def get_default_combination(shape):
    w = 0
    for i in shape:
        w = max(w, len(i))

    for i in range(w-1, -1, -1):
        remove = True
        for j in shape:
            if j[i] != 0:
                remove = False
        if remove:
            for j in range(len(shape)):
                shape[j].pop(i)

    for _ in range(len(shape[0])):
        for i in range(len(shape)):
            if shape[i][-1] == 0:
                shape[i].pop(-1)
    for i in range(len(shape)-1, -1, -1):
        if not shape[i]:
            shape.pop(i)

    return shape
