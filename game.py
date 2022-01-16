import datetime
import json
import math
import os
import time
import pygame
from player import Player
from world import *
from dropped_item import DroppedItem
from inventory_view import InventoryView
from crafting_view import CraftingView
from pause_menu import PauseMenu
from itemstack import ItemStack
from entity import Entity
from furnace_view import FurnaceView
from variables import block_type, color_modes


class Game:
    def __init__(self, game, world_id, world_name="New world"):
        self.screen = game.screen

        self.game = game
        self.player = Player(self)
        self.world = World()
        self.pause_menu = PauseMenu(self)
        self.furnace_view = FurnaceView(self)
        self.inventory_view = InventoryView(self)
        self.block_type = block_type

        self.world_id = world_id

        self.clock = pygame.time.Clock()
        self.player.pos[0] = len(self.world.blocks) // 2
        self.clicked_block = [0, 0]
        self.tick_time = 0
        self.breaking_time = 0
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.screen_state = "game"
        self.paused = False
        self.line_length = 0
        self.last_block = None
        self.tick_counter = 0

        # tworzenie chmur
        self.cloud_images = (pygame.image.load("textures/environment/cloud_1.png"), pygame.image.load("textures/environment/cloud_2.png"))
        self.clouds = []
        a = random.randint(-200,-100)
        while a < 1000:
            self.clouds.append([[a, random.randint(50,100)], random.choice((0, 1))])
            a += random.randint(200,300)


        self.mouse_click = pygame.mouse.get_pressed(3)

        self.TICK = self.game.TICK
        self.BACKGROUND_COLOR = (30, 144, 255)

        self.ITEM_HINT_FONT = pygame.font.Font("freesansbold.ttf", 18)
        self.DAY_DURATION = 600 * self.TICK  # in seconds multiplied by tick amount

        self.MOON_IMAGE = pygame.image.load("textures/environment/moon.png")
        self.SUN_IMAGE = pygame.image.load("textures/environment/sun.png")

        # colors
        self.TEXT_COLOR = color_modes[self.game.settings["color_mode"]]["main_menu_text"]
        self.SHADOW_COLOR = color_modes[self.game.settings["color_mode"]]["main_menu_text_shadow"]
        self.BUTTON_BG = color_modes[self.game.settings["color_mode"]]["main_menu_button_bg"]
        self.BUTTON_BG_HOVER = color_modes[self.game.settings["color_mode"]]["main_menu_button_bg_hover"]
        self.BUTTON_BORDER = color_modes[self.game.settings["color_mode"]]["main_menu_button_border"]
        self.INV_SLOT_BG = color_modes[self.game.settings["color_mode"]]["inv_slot_bg"]
        self.INV_BG = color_modes[self.game.settings["color_mode"]]["inv_bg"]
        self.INV_BORDER = color_modes[self.game.settings["color_mode"]]["inv_border"]

        self.to_update = [self, self.player]
        self.items_on_ground = []
        self.entity_list = []

        for e, i in enumerate(self.world.blocks[len(self.world.blocks) // 2]):
            if i.block_id == 2:
                self.player.pos[1] = e + 1
                # break

        # ladowanie swiata
        if self.world_id != -1 and self.world_id is not None and os.path.exists(os.path.join(self.game.GAME_PATH, f"saves/{self.world_id}")):
            self.load_world()
        else:
            wid = len(os.listdir(os.path.join(self.game.GAME_PATH, "saves")))
            while os.path.exists(os.path.join(self.game.GAME_PATH, f"saves/{wid}")):
                wid += 1
            self.world_id = wid
            os.makedirs(os.path.join(self.game.GAME_PATH, "saves/"+str(wid)))
            with open(os.path.join(self.game.GAME_PATH, "saves/"+str(wid)+"/main_data.txt"), "w") as file:
                file.write(str(wid)+"\n")
                file.write(world_name+"\n")
                date = datetime.datetime.now()
                file.write(f"{date.day}.{date.month}.{date.year}\n")

    def general_update(self):
        # mouse click
        self.mouse_click = pygame.mouse.get_pressed(3)
        self.tick_counter += 1

        for i in self.to_update:
            i.update()

        self.tick_time = time.time()

    def update(self):
        # pressed
        for event in self.game.clicked_once:
            if event.key == pygame.K_e:
                if self.screen_state == "game":
                    self.to_update = [self, self.inventory_view]
                    self.screen_state = "inventory"
                elif self.screen_state == "inventory":
                    self.to_update = [self, self.player]
                    self.screen_state = "game"

                    if self.furnace_view.opened_furnace is not None:
                        self.furnace_view.opened_furnace = None

            if event.key == pygame.K_ESCAPE:
                if self.screen_state == "game":
                    self.to_update = [self, self.pause_menu]
                    self.screen_state = "pause_menu"
                    self.paused = True

                elif self.screen_state == "pause_menu":
                    self.to_update = [self, self.player]
                    self.screen_state = "game"
                    self.paused = False


        self.screen.fill(self.BACKGROUND_COLOR)

        if not self.paused:
            self.world.time_in_game += 1

        mouse_pos = pygame.mouse.get_pos()
        self.last_block = self.clicked_block
        self.clicked_block = None
        self.line_length = math.sqrt(((mouse_pos[0] - 500) ** 2) + ((mouse_pos[1] - 420) ** 2))
        line_color = (60, 60, 60)

        # mechanizm dnia i nocy
        day_lightness = pygame.Surface(self.screen.get_size(), 32).convert_alpha()
        block_darkness = pygame.Surface(self.screen.get_size(), 32).convert_alpha()
        time_of_day = self.world.time_in_game % self.DAY_DURATION
        day_percent = (time_of_day / self.DAY_DURATION)
        dark = 235
        block_dark = 180

        if 0 < day_percent <= 0.05:
            # sunrise
            day_lightness.fill((0, 0, 0, dark - (dark * 20 * day_percent)))
            block_darkness.fill((0, 0, 0, block_dark - (block_dark * 20 * day_percent)))
        elif 0.05 < day_percent <= 0.45:
            # day
            day_lightness.fill((0, 0, 0, 0))
            block_darkness.fill((0, 0, 0, 0))
        elif 0.45 < day_percent <= 0.5:
            # sunset
            day_lightness.fill((0, 0, 0, 0 + (dark * 20 * (day_percent - 0.45))))
            block_darkness.fill((0, 0, 0, 0 + (block_dark * 20 * (day_percent - 0.45))))
        else:
            # night
            day_lightness.fill((0, 0, 10, dark))
            block_darkness.fill((0, 0, 0, block_dark))
        self.screen.blit(day_lightness, (0, 0))

        moon_x = self.screen.get_width() * day_percent * 2 - self.screen.get_width()
        sun_x = (self.screen.get_width() + 64) * day_percent * 2 - 64
        self.screen.blit(self.MOON_IMAGE, (moon_x - 32, 500 - get_sun_height(moon_x)))
        self.screen.blit(self.SUN_IMAGE, (sun_x - 32, 500 - get_sun_height(sun_x)))

        for i, cloud in enumerate(self.clouds):
            self.screen.blit(self.cloud_images[cloud[1]], cloud[0])
            cloud_speed = .4
            self.clouds[i][0][0] += cloud_speed
            if self.clouds[i][0][0] > 1000:
                self.clouds.pop(i)
            if self.tick_counter % int(250/cloud_speed) == 0:
                self.clouds.append([[random.randint(-200,-150), random.randint(50,100)], random.choice((0, 1))])
                self.tick_counter += 1


        self.screen.blit(self.font.render(
            f"TIME: {int((24 * day_percent + 6) % 24)}:{int((((24 * day_percent + 6) % 24) - (((24 * day_percent + 6) % 24) // 1)) * 60)}",
            False, (0, 0, 0)), (10, 30))

        # Głowna pętla przechądząca po wszystkich blokach i obslugująca render, klikniecia itp
        for col in range(int(self.player.pos[0] - 26), int(self.player.pos[0] + 27)):
            if 0 <= col <= len(self.world.blocks) + 1:
                try:
                    for row in range(int(self.player.pos[1] - 10), int(self.player.pos[1] + 25)):
                        j = self.world.blocks[col][row]
                        rect = pygame.Rect(
                            round((col - self.player.pos[0] + 25) * 20 + self.player.damage_earthquake[0], 2),
                            round(640 - ((row - self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1], 2),
                            20, 20)

                        if (self.mouse_click[0] or self.mouse_click[2]) and rect.collidepoint(mouse_pos):
                            self.clicked_block = [col, row]

                        if j.block_id != 0:
                            if j.visible or self.world.blocks[col - 1][row].block_id == 0 or self.world.blocks[col + 1][row].block_id == 0 or self.world.blocks[col][row - 1].block_id == 0 or self.world.blocks[col][row + 1].block_id == 0:
                                self.screen.blit(self.block_type[j.block_id]["txt"], (
                                    round((col - self.player.pos[0] + 25) * 20 + self.player.damage_earthquake[0], 2),
                                    round(640 - ((row - self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1],2)))
                                # if j.background:
                                #     sur = pygame.Surface((20,20), 32).convert_alpha()
                                #     sur.fill((0,0,0,120))
                                #     self.screen.blit(sur, (
                                #         round((col - self.player.pos[0] + 25) * 20 + self.player.damage_earthquake[0], 2),
                                #         round(640 - ((row - self.player.pos[1] + 10) * 20) + self.player.damage_earthquake[1], 2)))
                            else:
                                if rect.collidepoint(mouse_pos):
                                    line_color = (220, 0, 0)
                                pygame.draw.rect(self.screen, (10, 10, 10), rect)

                except IndexError:
                    pass

        pygame.draw.rect(self.screen, (0, 0, 0), (
            25 * 20 + self.player.damage_earthquake[0], 640 - (11 * 20) + self.player.damage_earthquake[1], 20, 40))
        if self.line_length > self.player.range_of_hand * 20:
            line_color = (220, 0, 0)
        pygame.draw.line(self.screen, line_color, (25 * 20 + 10, 640 - (11 * 20) + 10), (mouse_pos[0], mouse_pos[1]))

        # obsługa przedmiotów na ziemii
        for i, item in enumerate(self.items_on_ground):
            item.update()

            if item.life_time > 5000:
                del self.items_on_ground[i]
            elif item.to_remove and item.life_time > self.TICK:
                del self.items_on_ground[i]
                self.player.add_to_inventory(item)
            else:
                if not item.to_remove:
                    if abs(item.pos[0] - self.player.pos[0]) <= 2 and -1 < (
                            item.pos[1] - self.player.pos[1]) <= 2 and self.player.has_enough_space(item):
                        item.has_been_picked()

        self.screen.blit(self.font.render(f"FPS: {round((1000 / self.TICK) * 30 / ((time.time() - self.tick_time) * 1000), 1)}", False, (0, 0, 0)), (10, 10))
        self.screen.blit(self.font.render(f"X: {round(self.player.pos[0], 1)}", False, (0, 0, 0)), (10, 50))
        self.screen.blit(self.font.render(f"Y: {round(self.player.pos[1], 1)}", False, (0, 0, 0)), (10, 70))

        # Update kazdego moba
        for entity in self.entity_list:
            entity.update()

        self.screen.blit(block_darkness, (0,0))
        self.furnace_view.update()

    def create_item_on_ground(self, item_id, pos, immunite=0, velocity=None, life_time=0, behind=False):
        self.items_on_ground.append(DroppedItem(self, item_id, pos, immunite=immunite, velocity=velocity, life_time=life_time, behind=behind))

    def load_world(self):
        try:
            save_dir = os.path.join(self.game.GAME_PATH, f"saves/{self.world_id}")
            # Ladowanie blokow swiata
            with open(save_dir+"/world.txt") as file:
                self.world.blocks = []
                data = json.loads(file.read())
                for col in data:
                    temp = []
                    for block in col:
                        if block == {}:
                            temp.append(Block(0, True, True))
                        else:
                            block_id = block["block_id"]
                            visible = False
                            background = False
                            if "visible" in block.keys():
                                visible = block["visible"]
                            if "background" in block.keys():
                                background = block["background"]
                            temp.append(Block(block_id, visible, background))
                    self.world.blocks.append(temp)

            # Ladowanie ekwipunku i pozycji
            with open(save_dir+"/player.txt") as file:
                data = json.loads(file.read())
                self.player.pos = data["pos"]
                self.player.fall_distance = data["fall_distance"]
                self.player.hp = data["hp"]
                for index, itemstack in enumerate(data["inventory"]):
                    if itemstack is None:
                        self.player.inventory[index] = None
                    else:
                        behind = False
                        count = 1
                        if "behind" in itemstack.keys():
                            behind = itemstack["behind"]
                        if "count" in itemstack.keys():
                            count = itemstack["count"]
                        self.player.inventory[index] = ItemStack(itemstack["item_id"], count, behind=behind)

            # Ladowanie entities
            with open(save_dir+"/entity.txt") as file:
                data = json.loads(file.read())
                for entity in data:
                    self.entity_list.append(Entity(self, entity["type"], entity["pos"], entity["task"], entity["task_duration"]))

            # Ladowanie dropped items
            with open(save_dir+"/dropped_items.txt") as file:
                self.items_on_ground = []
                data = json.loads(file.read())
                for item in data:
                    self.create_item_on_ground(item_id=item["id"], pos=item["pos"], life_time=item["life_time"])

            # Ladowanie ustawien swiata
            with open(save_dir+"/world_data.txt") as file:
                data = json.loads(file.read())
                self.world.time_in_game = float(data['time_in_game'])

            # Ladowanie piecykow
            with open(save_dir+"/furnaces.txt") as file:
                data = json.loads(file.read())
                for furnace in data:
                    pos = furnace["pos"]
                    fuel_left = furnace['fuel_left']
                    smelting_ticks = furnace['smelting_ticks']
                    fuel_full = furnace['fuel_full']
                    subject = None
                    fuel = None
                    result = None
                    if furnace["subject"] is not None:
                        subject = ItemStack(furnace["subject"]["id"], furnace["subject"]["count"])
                    if furnace["fuel"] is not None:
                        fuel = ItemStack(furnace["fuel"]["id"], furnace["fuel"]["count"])
                    if furnace["result"] is not None:
                        result = ItemStack(furnace["result"]["id"], furnace["result"]["count"])
                    self.furnace_view.create_furnace(pos, subject, fuel, result, fuel_left, smelting_ticks, fuel_full)

        except FileNotFoundError:
            print("Save file not found, creating..")

    def save_world(self):
        default = os.path.join(self.game.GAME_PATH, "saves/"+str(self.world_id))
        with open(default+"/world.txt", "w") as file:
            data = []
            for col in self.world.blocks:
                line = []
                for element in col:
                    temp = {}
                    if element.block_id != 0:
                        temp["block_id"] = element.block_id
                        if element.visible:
                            temp["visible"] = True
                        if element.background:
                            temp["background"] = True
                    line.append(temp)
                data.append(line)
            file.write(json.dumps(data))
        print("Saved: world")

        with open(default+"/player.txt", "w") as file:
            data = {
                "pos": self.player.pos,
                "fall_distance": self.player.fall_distance,
                "hp": self.player.hp
            }
            inv = []
            for itemstack in self.player.inventory:
                if itemstack is not None:
                    inv.append({
                                "item_id": itemstack.item_id,
                                "count": itemstack.count,
                                "behind": itemstack.behind
                                })
                else:
                    inv.append(None)
            data["inventory"] = inv
            file.write(json.dumps(data, indent=1))
        print("Saved: player")

        with open(default+"/entity.txt", "w") as file:
            data = []
            for entity in self.entity_list:
                data.append({
                    "type": entity.type,
                    "task": entity.task,
                    "task_duration": round(entity.task_duration, 1),
                    "pos": entity.pos
                })
            file.write(json.dumps(data, indent=1))
        print("Saved: entity")

        with open(default+"/dropped_items.txt", "w") as file:
            data = []
            for item in self.items_on_ground:
                data.append({"id": item.type,
                             "pos": item.pos,
                             "life_time": item.life_time
                             })
            file.write(json.dumps(data, indent=1))
        print("Saved: dropped_items")

        with open(default+"/world_data.txt", "w") as file:
            data = {
                "time_in_game": self.world.time_in_game
            }
            file.write(json.dumps(data, indent=1))
        print("Saved: world_data")

        with open(default+"/furnaces.txt", "w") as file:
            data = []
            for furnace in self.furnace_view.furnaces_data:
                temp = {
                    "pos": furnace[0],
                    "subject": None,
                    "fuel": None,
                    "result": None,
                    "fuel_left": furnace[4],
                    "smelting_ticks": furnace[5],
                    "fuel_full": furnace[6]
                }
                if furnace[1] is not None:
                    temp["subject"] = {
                        "id": furnace[1].item_id,
                        "count": furnace[1].count
                    }
                if furnace[2] is not None:
                    temp["fuel"] = {
                        "id": furnace[2].item_id,
                        "count": furnace[2].count
                    }
                if furnace[3] is not None:
                    temp["result"] = {
                        "id": furnace[3].item_id,
                        "count": furnace[3].count
                    }

                data.append(temp)
            file.write(json.dumps(data, indent=1))

        print("Saved: furnaces")


def get_sun_height(x):
    return ((-x * x) / 625) + (1.6 * x) + 70
