import pygame
from itemstack import ItemStack
from variables import furnace_recipes, fuel_list


class FurnaceView:
    def __init__(self, game):
        self.opened_furnace = None
        self.game = game
        # [(x, y), subject, fuel, result, fuel_left (tick), smelting_ticks]
        self.furnaces_data = []

        self.FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 40)
        self.MEDIUM_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)
        self.SMALL_FONT = pygame.font.Font("textures/fonts/Minecraft.ttf", 30)

    def update(self):
        if pygame.K_ESCAPE in (i.key for i in self.game.game.clicked_once):
            self.opened_furnace = None
        # Obsluga kazdego piecyka / wyswietlanie aktualnego
        for index, furnace in enumerate(self.furnaces_data):
            if furnace[1] is not None and furnace[1].item_id in furnace_recipes.keys() and (furnace[3] is None or furnace[3].item_id == furnace[1].item_id):
                # warunki kiedy MA SIE PRZEPALAC

                if furnace[4] == 0:
                    if furnace[2] is not None and furnace[2].item_id in fuel_list.keys():
                        self.furnaces_data[4] = 450
                        # dodac paliwa!
                    else:
                        self.furnaces_data[index][5] -= 2

                self.furnaces_data[index][5] += 1
                if self.furnaces_data[index][5] >= 300:
                    # item przepalony!
                    self.furnaces_data[index][5] = 0
                    if furnace[3] is None:
                        self.furnaces_data[index][3] = ItemStack(furnace_recipes(furnace[1].item_id))
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

                # clicked_on_furnace = self.display_furnace(furnace)
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
                        print("dropped in fur")

                    self.game.inventory_view.item_on_mouse = None


    def display_furnace(self, furnace):
        return None
        pass

    def open_furnace(self, furnace_pos):
        for i, e in enumerate(self.furnaces_data):
            if furnace_pos in e:
                self.opened_furnace = furnace_pos
                return
        self.opened_furnace = furnace_pos
        self.create_furnace(furnace_pos)

    def create_furnace(self, furnace_pos):
        self.furnaces_data.append([furnace_pos, None, None, None, 0, 0])
