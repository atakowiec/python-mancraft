import pygame
from itemstack import ItemStack
from variables import furnace_recipes, fuel_list


class FurnaceView:
    def __init__(self, game):
        self.opened_furnace = None
        self.game = game
        # [(x, y), subject, fuel, result, fuel_left (tick), smelting_ticks, fuel_full]
        self.furnaces_data = []
        self.ITEM_SMELTING_TIME = 0.1 * self.game.game.TICK

        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 40)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)

        self.furnace_components = [
            [100, 50, 50, 50],
            [100, 180, 50, 50],
            [280, 115, 50, 50],
            [113, 112, 24, 56],
            [170, 125, 90, 30],
        ]

    def update(self):
        # Obsluga kazdego piecyka / wyswietlanie aktualnego
        for index, furnace in enumerate(self.furnaces_data):
            if furnace[1] is not None and furnace[1].item_id in furnace_recipes.keys() and (furnace[3] is None or furnace[3].item_id == furnace_recipes[furnace[1].item_id]):
                # warunki kiedy MA SIE PRZEPALAC

                if furnace[4] == 0:
                    self.furnaces_data[index][5] += 1
                    if furnace[2] is not None and furnace[2].item_id in fuel_list.keys():
                        self.furnaces_data[index][4] = int(fuel_list[furnace[2].item_id]*self.ITEM_SMELTING_TIME)
                        self.furnaces_data[index][6] = int(fuel_list[furnace[2].item_id]*self.ITEM_SMELTING_TIME)
                        self.furnaces_data[index][2].count -= 1
                        if self.furnaces_data[index][2].count == 0:
                            self.furnaces_data[index][2] = None
                    else:
                        if furnace[5] > 0:
                            if self.furnaces_data[index][5] >= 2:
                                self.furnaces_data[index][5] -= 2
                            elif self.furnaces_data[index][5] != 0:
                                self.furnaces_data[index][5] = 0


                if self.furnaces_data[index][5] >= self.ITEM_SMELTING_TIME:
                    # item przepalony!
                    self.furnaces_data[index][5] = 0
                    if furnace[3] is None:
                        self.furnaces_data[index][3] = ItemStack(furnace_recipes[furnace[1].item_id])
                        furnace[1].count -= 1
                    else:
                        furnace[3].count += 1
                        furnace[1].count -= 1

                    if furnace[1].count == 0:
                        self.furnaces_data[index][1] = None
            else:
                self.furnaces_data[index][5] = 0

            if furnace[4] > 0:
                self.furnaces_data[index][4] -= 1

            if self.opened_furnace == furnace[0]:
                surface = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
                surface.convert_alpha()
                surface.fill((0, 0, 0, 150))

                mouse_pos = pygame.mouse.get_pos()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.game.screen_state = "game"
                    self.game.to_update = [self.game, self.game.player]

                self.game.screen.blit(surface, (0, 0))

                # tło
                bg_rect = pygame.Rect(215, 50, 570, 535)
                pygame.draw.rect(self.game.screen, (0,0,0), bg_rect, border_radius=10)
                pygame.draw.rect(self.game.screen, (180,180,180), (220, 55, 560, 525), border_radius=10)

                self.display_furnace(index)
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


    def display_furnace(self, furnace_id):
        if pygame.K_ESCAPE in (i.key for i in self.game.game.clicked_once):
            self.opened_furnace = None
        x_pos = 285
        y_pos = 50

        clicked = None
        furnace = self.furnaces_data[furnace_id]
        hovered_item = None

        for i, e in enumerate(self.furnace_components):
            x = e[0] + x_pos
            y = e[1] + y_pos
            rect = pygame.Rect(x, y, e[2], e[3])
            pygame.draw.rect(self.game.screen, (50, 50, 50), rect, border_radius=5)
            pygame.draw.rect(self.game.screen, (120, 120, 120), (x+3, y+3, e[2]-6, e[3]-6), border_radius=5)

            if i == 3:
                pygame.draw.rect(self.game.screen, (255, 255, 0), (x+3, y+3+(e[3]-6)*(1-furnace[4]/furnace[6]), e[2]-6, (e[3]-6)*(furnace[4]/furnace[6])), border_radius=5)

            if i == 4:
                pygame.draw.rect(self.game.screen, (0, 255, 0), (x+3, y+3, (e[2]-6)*(furnace[5]/self.ITEM_SMELTING_TIME), e[3]-6), border_radius=5)

            if i in (0, 1, 2) and furnace[i+1] is not None:
                self.game.screen.blit(furnace[i+1].txt, (x+15, y+15))
                text = self.game.font.render(str(furnace[i+1].count), False, (255, 255, 255))
                width = text.get_size()[0]
                self.game.screen.blit(text, (x+53 - width, y+36))

                if rect.collidepoint(pygame.mouse.get_pos()):
                    hovered_item = furnace[i+1]

            if (1 in self.game.game.mouse_press or 3 in self.game.game.mouse_press) and rect.collidepoint(pygame.mouse.get_pos()):
                clicked = i+1

        # Wyswietlanie nazwy przedmiotu po najechaniu (w furnace)
        if hovered_item is not None:
            mouse_pos = pygame.mouse.get_pos()
            render = self.game.ITEM_HINT_FONT.render(hovered_item.name, False, (0, 0, 0))
            pygame.draw.rect(self.game.screen, (50, 50, 50), (mouse_pos[0] - 10, mouse_pos[1] - render.get_height() - 15, render.get_width() + 20, render.get_height() + 20), border_radius=5)
            pygame.draw.rect(self.game.screen, (120, 120, 120), (mouse_pos[0] - 5, mouse_pos[1] - render.get_height() - 10, render.get_width() + 10, render.get_height() + 10), border_radius=5)
            self.game.screen.blit(render, (mouse_pos[0], mouse_pos[1] - render.get_height() - 5))

        if clicked == 3:
            # Kliknieto w rezultat
            self.game.inventory_view.item_on_mouse, self.furnaces_data[furnace_id][3] = self.game.inventory_view.handle_inv_click(self.game.inventory_view.item_on_mouse, self.furnaces_data[furnace_id][3], blocked=True)
        elif clicked == 2 or clicked == 1:
            self.game.inventory_view.item_on_mouse, self.furnaces_data[furnace_id][clicked] = self.game.inventory_view.handle_inv_click(self.game.inventory_view.item_on_mouse, self.furnaces_data[furnace_id][clicked], blocked=False)

    def open_furnace(self, furnace_pos):
        for i, e in enumerate(self.furnaces_data):
            if furnace_pos in e:
                self.opened_furnace = furnace_pos
                return
        self.opened_furnace = furnace_pos
        self.create_furnace(furnace_pos)

    def create_furnace(self, furnace_pos):
        self.furnaces_data.append([furnace_pos, None, None, None, 0, 0, 1])
