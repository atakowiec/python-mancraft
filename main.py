import math
import time
import pygame
from player import Player
from world import *
from dropped_item import DroppedItem
from inventory_view import InventoryView
from crafting_view import CraftingView


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1000, 640))
        pygame.display.set_caption("Minecraft 3.0")
        self.player = Player(self)
        self.world = World()
        self.clock = pygame.time.Clock()
        self.player.pos[0] = len(self.world.blocks)//2
        self.clicked_block = [0, 0]
        self.tick_time = 0
        self.breaking_time = 0
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.screen_state = "game"

        self.mouse_click = pygame.mouse.get_pressed(3)
        self.mouse_hold = False

        self.BACKGROUND_COLOR = (30, 144, 255)
        self.IGNORED_BLOCKS = (0, 6, 7)
        self.ITEM_HINT_FONT = pygame.font.Font("freesansbold.ttf", 18)
        self.TICK = 30
        self.DAY_DURATION = 600 * self.TICK  # in seconds multiplied by tick amount

        self.MOON_IMAGE = pygame.image.load("textures/environment/moon.png")
        self.SUN_IMAGE = pygame.image.load("textures/environment/sun.png")

        self.to_update = [self, self.player]
        self.items_on_ground = []
        self.entity_list = []

        for e, i in enumerate(self.world.blocks[len(self.world.blocks)//2]):
            if i == 2:
                self.player.pos[1] = e+1
                # break

        while self.running:
            timer = time.time()
            self.clock.tick(self.TICK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.player.current_slot += 1
                    if event.button == 5:
                        self.player.current_slot -= 1

                    self.player.current_slot += 9
                    self.player.current_slot %= 9

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player.current_slot = 0
                    elif event.key == pygame.K_2:
                        self.player.current_slot = 1
                    elif event.key == pygame.K_3:
                        self.player.current_slot = 2
                    elif event.key == pygame.K_4:
                        self.player.current_slot = 3
                    elif event.key == pygame.K_5:
                        self.player.current_slot = 4
                    elif event.key == pygame.K_6:
                        self.player.current_slot = 5
                    elif event.key == pygame.K_7:
                        self.player.current_slot = 6
                    elif event.key == pygame.K_8:
                        self.player.current_slot = 7
                    elif event.key == pygame.K_9:
                        self.player.current_slot = 8
                    if event.key == pygame.K_e:
                        if self.screen_state == "game":
                            self.to_update = [self, self.player, InventoryView(self)]
                            self.screen_state = "inventory"
                        elif self.screen_state == "inventory":
                            self.to_update = [self, self.player]
                            self.screen_state = "game"

                # mouse click
                self.mouse_click = pygame.mouse.get_pressed(3)

            self.screen.fill(self.BACKGROUND_COLOR)

            for i in self.to_update:
                i.update()

            self.tick_time = round(time.time()-timer, 4)
            self.screen.blit(self.font.render(f"FPS: {round((1000 / self.TICK) * 30 / ((time.time() - timer) * 1000), 1)}", False, (0, 0, 0)), (10, 10))
            pygame.display.flip()

    def update(self):
        self.world.time_in_game += 1
        mouse_pos = pygame.mouse.get_pos()
        last_block = self.clicked_block
        self.clicked_block = None
        line_length = math.sqrt(((mouse_pos[0]-500)**2)+((mouse_pos[1]-420)**2))
        line_color = (60,60,60)

        # mechanizm dnia i nocy
        day_lightness = pygame.Surface(self.screen.get_size(), 32).convert_alpha()
        time_of_day = self.world.time_in_game % self.DAY_DURATION
        day_percent = (time_of_day/self.DAY_DURATION)
        dark = 220

        if 0 < day_percent <= 0.05:
            # sunrise
            day_lightness.fill((0,0,0,dark - (dark*20*day_percent)))
            self.screen.blit(day_lightness, (0, 0))
        elif 0.05 < day_percent <= 0.45:
            # day
            day_lightness.fill((0,0,0,0))
            self.screen.blit(day_lightness, (0, 0))
        elif 0.45 < day_percent <= 0.5:
            # sunset
            day_lightness.fill((0,0,0,0 + (dark*20*(day_percent-0.45))))
            self.screen.blit(day_lightness, (0, 0))
        else:
            # night
            day_lightness.fill((0,0,0,dark))
            self.screen.blit(day_lightness, (0,0))

        moon_x = self.screen.get_width()*day_percent*2-self.screen.get_width()
        sun_x = (self.screen.get_width()+64)*day_percent*2-64
        self.screen.blit(self.MOON_IMAGE, (moon_x, 500-get_sun_height(moon_x)))
        self.screen.blit(self.SUN_IMAGE, (sun_x, 500-get_sun_height(sun_x)))

        self.screen.blit(self.font.render(f"TIME: {int((24*day_percent+6)%24)}:{int((((24*day_percent+6)%24)-(((24*day_percent+6)%24)//1))*60)}", False, (0, 0, 0)), (10, 30))

        # Głowna pętla przechądząca po wszystkich blokach i obslugująca render, klikniecia itp
        for col in range(int(self.player.pos[0]-26), int(self.player.pos[0]+27)):
            if 0 <= col <= len(self.world.blocks)+1:
                try:
                    for row in range(int(self.player.pos[1]-10), int(self.player.pos[1]+25)):
                        j = self.world.blocks[col][row]
                        rect = pygame.Rect(round((col - self.player.pos[0]+25)*20 + self.player.damage_earthquake[0], 2), round(640 - ((row-self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1], 2), 20, 20)

                        if (self.mouse_click[0] or self.mouse_click[2]) and rect.collidepoint(mouse_pos):
                            self.clicked_block = [col, row]

                        if j != 0:
                            if j in (6, 7, 2, 3) or self.world.blocks[col-1][row] == 0 or self.world.blocks[col+1][row] == 0 or self.world.blocks[col][row-1] == 0 or self.world.blocks[col][row+1] == 0:
                                self.screen.blit(self.world.block_types[j][2], (round((col - self.player.pos[0]+25)*20 + self.player.damage_earthquake[0], 2), round(640 - ((row-self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1], 2)))
                            else:
                                if rect.collidepoint(mouse_pos):
                                    line_color = (220,0,0)
                                pygame.draw.rect(self.screen, (10,10,10), rect)

                except IndexError:
                    pass

        pygame.draw.rect(self.screen, (0,0,0), (25*20+self.player.damage_earthquake[0], 640-(11*20)+self.player.damage_earthquake[1], 20, 40))
        if line_length > self.player.range_of_hand*20:
            line_color = (220,0,0)
        pygame.draw.line(self.screen, line_color, (25*20+10, 640-(11*20)+10), (mouse_pos[0], mouse_pos[1]))

        # obsługa przedmiotów na ziemii
        for i, item in enumerate(self.items_on_ground):
            item.update()

            if item.life_time > 5000 or (item.to_remove and item.life_time > self.TICK * 1):
                del self.items_on_ground[i]
                self.player.add_to_inventory(item)
            else:
                if not item.to_remove:
                    if abs(item.pos[0] - self.player.pos[0]) <= 2 and -1 < (item.pos[1] - self.player.pos[1]) <= 2 and self.player.has_enough_space(item):
                        item.has_been_picked()

        # stawianie blokow
        if self.mouse_click[2] and self.clicked_block is not None and line_length <= self.player.range_of_hand*20:
            if not self.world.blocks[self.clicked_block[0]][self.clicked_block[1]]:
                # jesli klikniety blok jest powietrzem
                if self.player.inventory[self.player.current_slot] is not None:
                    self.world.blocks[self.clicked_block[0]][self.clicked_block[1]] = self.player.inventory[self.player.current_slot].item_id
                    if self.player.inventory[self.player.current_slot].count == 1:
                        self.player.inventory[self.player.current_slot] = None
                    else:
                        self.player.inventory[self.player.current_slot].count -= 1
            else:
                # jesli nie jest powietrzem
                clicked_block_type = self.world.blocks[self.clicked_block[0]][self.clicked_block[1]]
                if clicked_block_type == 14:
                    self.to_update = [self, CraftingView(self)]
                    self.screen_state = "inventory"
        if self.mouse_click[0] and self.clicked_block is not None and line_length <= self.player.range_of_hand*20:
            if self.clicked_block == last_block:
                if self.world.blocks[self.clicked_block[0]][self.clicked_block[1]]:
                    self.breaking_time += self.tick_time
                    breaking_time = self.world.block_types[self.world.blocks[self.clicked_block[0]][self.clicked_block[1]]][1]

                    if self.breaking_time >= breaking_time:
                        # Zniszczenie bloku
                        self.breaking_time = 0
                        self.create_item_on_ground(self.world.blocks[last_block[0]][last_block[1]], last_block)
                        self.world.blocks[last_block[0]][last_block[1]] = 0
                    else:
                        # Block breaking animation
                        nr = (self.breaking_time/breaking_time)//0.1
                        self.screen.blit(destroy_stages[int(nr)], (
                            round((self.clicked_block[0] - self.player.pos[0] + 25) * 20 + self.player.damage_earthquake[0], 2),
                            round(640 - ((self.clicked_block[1] - self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1], 2)))
            else:
                self.breaking_time = 0

        # Update kazdego moba
        for entity in self.entity_list:
            entity.update()

    def create_item_on_ground(self, item_id, pos, immunite=0, velocity=None):
        self.items_on_ground.append(DroppedItem(self, item_id, pos, immunite=immunite, velocity=velocity))


def get_sun_height(x):
    return ((-x*x)/625) + (1.6*x)


if __name__ == '__main__':
    Game()
