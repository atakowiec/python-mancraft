import copy
import random
import pygame.draw
import time
from world import destroy_stages
from itemstack import ItemStack
from entity import Entity
from crafting_view import CraftingView
from block import Block
from dimensioner_view import DimensionerView


class Player:
    def __init__(self, game):
        self.game = game
        self.pos = [0, 0]
        self.velocity = 0
        self.range_of_hand = 8  # in blocks
        self.inventory = [None for _ in range(36)]
        self.current_slot = 0
        self.hp = 20
        self.max_hp = 20
        self.fall_distance = 0
        pygame.font.get_init()
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.heart_images = (pygame.image.load("textures/gui/left_heart.png"), pygame.image.load("textures/gui/right_heart.png"), pygame.image.load("textures/gui/left_heart_empty.png"), pygame.image.load("textures/gui/right_heart_empty.png"))
        self.damage_earthquake_duration = 0
        self.damage_earthquake = [0, 0]
        self.item_name_timer = 0

    def update(self):
        # Wyswietlanie nazwy trzymanego itemu
        if self.item_name_timer > 0:
            self.item_name_timer -= 1
            if self.inventory[self.current_slot] is not None:
                item = self.inventory[self.current_slot]
                msg = item.name
                if item.behind and item.data['type'] == "block":
                    msg += " (behind)"
                text = self.game.game.TINY_FONT.render(msg, False, (0,0,0))
                self.game.screen.blit(text, (self.game.screen.get_width()/2 - text.get_width()/2 + 2, 102))
                text = self.game.game.TINY_FONT.render(msg, False, (220,220,220))
                self.game.screen.blit(text, (self.game.screen.get_width()/2 - text.get_width()/2, 100))

        # scrollowanie slotow
        if self.game.game.mouse_press is not []:
            if 4 in self.game.game.mouse_press:
                self.current_slot += 1
                self.game.breaking_time = 0
                self.item_name_timer = 45
            elif 5 in self.game.game.mouse_press:
                self.current_slot -= 1
                self.game.breaking_time = 0
                self.item_name_timer = 45

            self.current_slot += 9
            self.current_slot %= 9

        for event in self.game.game.clicked_once:
            if event.key == pygame.K_1:
                self.game.breaking_time = 0
                self.current_slot = 0
                self.item_name_timer = 45
            elif event.key == pygame.K_2:
                self.game.breaking_time = 0
                self.current_slot = 1
                self.item_name_timer = 45
            elif event.key == pygame.K_3:
                self.game.breaking_time = 0
                self.current_slot = 2
                self.item_name_timer = 45
            elif event.key == pygame.K_4:
                self.game.breaking_time = 0
                self.current_slot = 3
                self.item_name_timer = 45
            elif event.key == pygame.K_5:
                self.game.breaking_time = 0
                self.current_slot = 4
                self.item_name_timer = 45
            elif event.key == pygame.K_6:
                self.game.breaking_time = 0
                self.current_slot = 5
                self.item_name_timer = 45
            elif event.key == pygame.K_7:
                self.game.breaking_time = 0
                self.current_slot = 6
                self.item_name_timer = 45
            elif event.key == pygame.K_8:
                self.game.breaking_time = 0
                self.current_slot = 7
                self.item_name_timer = 45
            elif event.key == pygame.K_9:
                self.game.breaking_time = 0
                self.current_slot = 8
                self.item_name_timer = 45

        #  wyświetlanie ekwipunku
        for i in range(9):
            if self.current_slot == i:
                pygame.draw.rect(self.game.screen, (0,0,0), (228 + (60*i), 8, 54, 54), border_radius=5)
                pygame.draw.rect(self.game.screen, (100,100,100), (232 + (60*i), 12, 46, 46), border_radius=5)
            else:
                pygame.draw.rect(self.game.screen, (50,50,50), (230 + (60*i), 10, 50, 50), border_radius=5)
                pygame.draw.rect(self.game.screen, (140,140,140), (233 + (60*i), 13, 44, 44), border_radius=5)

            if self.inventory[i] is not None:
                # pygame.draw.rect(self.game.screen, self.inventory[i].txt, (245 + (60*i), 25, 20, 20))
                self.game.screen.blit(self.inventory[i].txt, (245 + (60*i), 25))
                if self.inventory[i].count > 1:
                    text = self.font.render(str(self.inventory[i].count), False, (255, 255, 255))
                    width = text.get_size()[0]
                    self.game.screen.blit(text, (273 + (60 * i) - width, 36))

        # Wyświetlanie hp
        for i in range(self.max_hp):
            if i < self.hp:
                self.game.screen.blit(self.heart_images[i % 2], (335+(i*16), 60))
            else:
                self.game.screen.blit(self.heart_images[(i % 2)+2], (335+(i*16), 60))

        # obsługa damage_earthquakes
        if self.damage_earthquake_duration != 0:
            self.damage_earthquake_duration -= 1
            self.damage_earthquake = [j*0.9*((-1)**(self.damage_earthquake_duration % 2)) for j in self.damage_earthquake]
        else:
            self.damage_earthquake = [0, 0]

        # moving
        pressed = pygame.key.get_pressed()
        self.velocity = round(self.velocity, 2)
        vector = [0, self.velocity-0.1]
        if self.velocity >= 0:
            self.velocity -= 0.3

        if pressed[pygame.K_w]:
            if self.pos[1] == int(self.pos[1]) and (not self.game.world.blocks[int(self.pos[0])][int(self.pos[1]-0.1)].background or not self.game.world.blocks[int(self.pos[0]+0.99)][int(self.pos[1]-0.1)].background):
                self.velocity = 1.2
        if pressed[pygame.K_d]:
            vector[0] += 0.25
        if pressed[pygame.K_a]:
            vector[0] -= 0.25

        # Magiczna siła zapobiegająca blokowaniu w klockach
        if not self.game.world.blocks[int(self.pos[0])][int(self.pos[1])].background or not self.game.world.blocks[int(self.pos[0]+0.9)][int(self.pos[1])].background:
            self.pos[1] = int(self.pos[1]+1)

        # Kolizje gracza
        if vector[0] > 0:
            if not self.game.world.blocks[int(self.pos[0]+1)][int(self.pos[1])].background or not self.game.world.blocks[int(self.pos[0]+1)][int(self.pos[1]+1)].background:
                vector[0] = 0
                self.pos[0] = int(self.pos[0])
        elif vector[0] < 0:
            # Sprawdzenie bloku po lewej
            if not self.game.world.blocks[int(self.pos[0]-0.1)][int(self.pos[1])].background or not self.game.world.blocks[int(self.pos[0]-0.1)][int(self.pos[1]+1)].background:
                vector[0] = 0
                self.pos[0] = int(self.pos[0]+0.4)
        if vector[1] > 0:
            # Sprawdzenie bloku nad głowa
            if not self.game.world.blocks[int(self.pos[0])][int(self.pos[1]+2)].background or not self.game.world.blocks[int(self.pos[0]+0.90)][int(self.pos[1]+2)].background:
                vector[1] = 0
                self.pos[1] = int(self.pos[1])
                self.velocity = 0
        elif vector[1] < 0:
            # Sprawdzenie bloku pod nogami
            if not self.game.world.blocks[int(self.pos[0])][int(self.pos[1]+vector[1])].background or not self.game.world.blocks[int(self.pos[0]+0.90)][int(self.pos[1]+vector[1])].background:
                vector[1] = 0
                self.pos[1] = int(self.pos[1]+vector[1])

        self.compute_fall_damage(vector[1])

        self.pos[0] += vector[0]
        self.pos[1] += vector[1]
        self.pos[0] = round(self.pos[0], 3)
        self.pos[1] = round(self.pos[1], 3)

        if self.pos[1] > len(self.game.world.blocks[0]) - 3:
            self.pos[1] = len(self.game.world.blocks[0]) - 3
        elif self.pos[1] < 0:
            self.pos[1] = 0
        elif self.pos[0] > len(self.game.world.blocks)-2:
            self.pos[0] = len(self.game.world.blocks)-2
        elif self.pos[0] < 1:
            self.pos[0] = 1
            
        # iterakcje z blokami
        if 3 in self.game.game.mouse_press and self.game.clicked_block is not None and self.game.line_length <= self.game.player.range_of_hand * 20 and not self.game.paused:
            if not self.game.world.blocks[self.game.clicked_block[0]][self.game.clicked_block[1]].block_id:
                # jesli klikniety blok jest powietrzem
                if self.game.player.inventory[self.game.player.current_slot] is not None and self.game.player.inventory[self.game.player.current_slot].type == "block":
                    self.game.world.blocks[self.game.clicked_block[0]][self.game.clicked_block[1]] = Block(self.game.player.inventory[self.game.player.current_slot].item_id, True, self.game.player.inventory[self.game.player.current_slot].behind)
                    if self.game.player.inventory[self.game.player.current_slot].count == 1:
                        self.game.player.inventory[self.game.player.current_slot] = None
                    else:
                        self.game.player.inventory[self.game.player.current_slot].count -= 1
            else:
                # jesli nie jest powietrzem
                clicked_block_type = self.game.world.blocks[self.game.clicked_block[0]][self.game.clicked_block[1]].block_id
                if clicked_block_type == 14:
                    self.game.to_update = [self.game, CraftingView(self.game)]
                    self.game.screen_state = "inventory"
                elif clicked_block_type == 15:
                    self.game.to_update = [self.game]
                    self.game.furnace_view.open_furnace(self.game.clicked_block)
                    self.game.screen_state = "inventory"
                elif clicked_block_type == 25:
                    self.game.to_update = [self.game, DimensionerView(self.game)]
                    self.game.screen_state = "inventory"
                elif clicked_block_type == 26:
                    pattern = [
                        63,5,63,
                        5,26,5,
                        0,5,0
                    ]
                    block = [i-1 for i in self.game.clicked_block]
                    correct = True
                    for i in range(9):
                        if self.game.world.blocks[block[0]+(i%3)][block[1]+(i//3)].block_id != pattern[i]:
                            correct = False
                            break

                    if correct and not self.game.nether_reactor_core.running:
                        self.game.nether_reactor_core.create_reactor(self.game.clicked_block)

        if self.game.mouse_click[0] and self.game.clicked_block is not None and self.game.line_length <= self.game.player.range_of_hand * 20 and not self.game.paused:
            if self.game.clicked_block == self.game.last_block:
                if self.game.world.blocks[self.game.clicked_block[0]][self.game.clicked_block[1]].block_id:
                    self.game.breaking_time += time.time()-self.game.tick_time

                    # w trakcie niszczenia
                    block_id = self.game.world.blocks[self.game.last_block[0]][self.game.last_block[1]].block_id
                    discount = 1
                    tool_level = 0
                    tool_type = 0
                    intended_tool = []
                    required_tool_level = 0
                    if self.inventory[self.current_slot] is not None:
                        if "tool_level" in self.inventory[self.current_slot].data.keys():
                            tool_level = self.inventory[self.current_slot].data["tool_level"]
                            tool_type = self.inventory[self.current_slot].data["tool_type"]
                    if "intended_tool" in self.game.block_type[block_id].keys():
                        intended_tool = self.game.block_type[block_id]["intended_tool"]
                        required_tool_level = self.game.block_type[block_id]["required_tool_level"]

                    if tool_type in intended_tool:
                        # TODO tutaj mozna dodac efficiency
                        discount -= (0.15*(tool_level+1))

                    breaking_time = self.game.block_type[block_id]["breaking_time"]*discount

                    if self.game.breaking_time >= breaking_time:
                        # Zniszczenie bloku
                        self.game.breaking_time = 0

                        if required_tool_level <= tool_level:
                            # obliczanie dropu
                            drop_list = self.game.block_type[block_id]["drop"]
                            drop_amount = self.game.block_type[block_id]["amount"]
                            drop_probability = self.game.block_type[block_id]["drop_probability"]*1000
                            if random.randint(1, 1000) <= drop_probability % 1000:
                                drop_amount = [i+1 for i in drop_amount]

                            for drop in drop_list:
                                for i in range(random.choice(drop_amount)):
                                    self.game.create_item_on_ground(drop, self.game.last_block, behind=self.game.world.blocks[self.game.clicked_block[0]][self.game.clicked_block[1]].background)

                        self.game.world.blocks[self.game.last_block[0]][self.game.last_block[1]] = Block(0, True, True)

                    else:
                        # Block breaking animation
                        nr = (self.game.breaking_time / breaking_time) // 0.1
                        self.game.screen.blit(destroy_stages[int(nr)], (
                            round(
                                (self.game.clicked_block[0] - self.game.player.pos[0] + 25) * 20 + self.game.player.damage_earthquake[
                                    0], 2),
                            round(640 - ((self.game.clicked_block[1] - self.game.player.pos[1] + 10) * 20) +
                                  self.game.player.damage_earthquake[1], 2)))
            else:
                self.game.breaking_time = 0

        if pressed[pygame.K_DOWN]:
            self.pos[1] -= 2
        if pressed[pygame.K_UP]:
            self.pos[1] += 2
        if pressed[pygame.K_LEFT]:
            self.pos[0] -= 2
        if pressed[pygame.K_RIGHT]:
            self.pos[0] += 2
        if pressed[pygame.K_F1]:
            self.game.world.time_in_game += 100
            self.game.game.TICK = 200
        else:
            if self.game.game.TICK != 30:
                self.game.game.TICK = 30
        if pressed[pygame.K_F2]:
            self.game.world.blocks[int(self.pos[0])][int(self.pos[1])-1].block_id = random.randint(1, 15)
        if pressed[pygame.K_F3]:
            self.game.entity_list.append(Entity(self.game, 1, [self.pos[0], self.pos[1]]))
            
        

    def has_enough_space(self, item):
        for k, v in enumerate(self.inventory):
            if v is None or (v.item_id == item.type and v.behind == item.behind):
                return True
        return False

    # noinspection PyTypeChecker
    def add_to_inventory(self, item):
        for k, v in enumerate(self.inventory):
            if v is not None and v.item_id == item.type and v.behind == item.behind:
                self.inventory[k].count += 1
                return True

        for k, v in enumerate(self.inventory):
            if v is None:
                self.inventory[k] = ItemStack(item.type, behind=item.behind)
                return True

        raise Exception("Unfortunately not enough space in inventory :(")

    def compute_fall_damage(self, vector):
        if vector < 0:
            self.fall_distance -= vector
        else:
            # print(self.fall_distance)
            if self.fall_distance > 7:
                damage = round(self.fall_distance-7, 1)
                self.hp -= damage
                self.damage_earthquake_duration = 10
                if damage > 8:
                    damage = 8
                self.damage_earthquake = [[damage, damage],[damage, -damage]][random.randint(0, 1)]
            self.fall_distance = 0

    def drop_item(self, itemstack):
        if itemstack is None:
            return False
        v = 0.2
        if self.game.screen.get_width()/2 - pygame.mouse.get_pos()[0] > 0:
            v = -v
        position = [self.pos[0],self.pos[1]+1.5]
        for i in range(itemstack.count):
            self.game.create_item_on_ground(itemstack.item_id, position, immunite=30, velocity=[v,0], behind=itemstack.behind)
        return True
