import random
import pygame.draw
from world import blocks as block_types
from itemstack import ItemStack
from entity import Entity

class Player:
    def __init__(self, game):
        self.game = game
        self.pos = [0, 0]
        self.velocity = 0
        self.range_of_hand = 8  # in blocks
        self.inventory = [None for _ in range(36)]
        self.inventory[0] = ItemStack(14)
        self.inventory[1] = ItemStack(5, 10)
        # self.inventory = [ItemStack((i % 13) + 1, random.randint(1, 10000)) for i in range(36)]
        self.current_slot = 0
        self.hp = 20
        self.max_hp = 20
        self.fall_distance = 0
        pygame.font.get_init()
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.heart_images = (pygame.image.load("./images/left_heart.png"), pygame.image.load("./images/right_heart.png"), pygame.image.load("./images/left_heart_empty.png"), pygame.image.load("./images/right_heart_empty.png"))
        self.damage_earthquake_duration = 0
        self.damage_earthquake = [0, 0]

    def update(self):
        #  wyświetlanie ekwipunku
        for i in range(9):
            if self.current_slot == i:
                pygame.draw.rect(self.game.screen, (0,0,0), (228 + (60*i), 8, 54, 54), border_radius=5)
                pygame.draw.rect(self.game.screen, (100,100,100), (232 + (60*i), 12, 46, 46), border_radius=5)
            else:
                pygame.draw.rect(self.game.screen, (50,50,50), (230 + (60*i), 10, 50, 50), border_radius=5)
                pygame.draw.rect(self.game.screen, (120,120,120), (233 + (60*i), 13, 44, 44), border_radius=5)

            if self.inventory[i] is not None:
                # pygame.draw.rect(self.game.screen, self.inventory[i].txt, (245 + (60*i), 25, 20, 20))
                self.game.screen.blit(self.inventory[i].txt, (245 + (60*i), 25))
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
            if self.pos[1] == int(self.pos[1]) and (self.game.world.blocks[int(self.pos[0])][int(self.pos[1]-0.99)] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]+0.99)][int(self.pos[1]-0.99)] not in self.game.IGNORED_BLOCKS):
                self.velocity = 1.2
        if pressed[pygame.K_d]:
            vector[0] += 0.25
        if pressed[pygame.K_a]:
            vector[0] -= 0.25

        # Magiczna siła zapobiegająca blokowaniu w klockach
        if self.game.world.blocks[int(self.pos[0])][int(self.pos[1])] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]+0.9)][int(self.pos[1])] not in self.game.IGNORED_BLOCKS:
            self.pos[1] = int(self.pos[1]+1)

        # Kolizje gracza
        if vector[0] > 0:
            if self.game.world.blocks[int(self.pos[0]+1)][int(self.pos[1])] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]+1)][int(self.pos[1]+1)] not in self.game.IGNORED_BLOCKS:
                vector[0] = 0
                self.pos[0] = int(self.pos[0])
        elif vector[0] < 0:
            pass  # Sprawdzenie bloku po lewej
            if self.game.world.blocks[int(self.pos[0]-0.1)][int(self.pos[1])] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]-0.1)][int(self.pos[1]+1)] not in self.game.IGNORED_BLOCKS:
                vector[0] = 0
                self.pos[0] = int(self.pos[0]+0.4)
        if vector[1] > 0:
            # Sprawdzenie bloku nad głowa
            if self.game.world.blocks[int(self.pos[0])][int(self.pos[1]+2)] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]+0.90)][int(self.pos[1]+2)] not in self.game.IGNORED_BLOCKS:
                vector[1] = 0
                self.pos[1] = int(self.pos[1])
                self.velocity = 0
        elif vector[1] < 0:
            # Sprawdzenie bloku pod nogami
            if self.game.world.blocks[int(self.pos[0])][int(self.pos[1]+vector[1])] not in self.game.IGNORED_BLOCKS or self.game.world.blocks[int(self.pos[0]+0.90)][int(self.pos[1]+vector[1])] not in self.game.IGNORED_BLOCKS:
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
        elif self.pos[0] > len(self.game.world.blocks)-3:
            self.pos[0] = len(self.game.world.blocks)-3
        elif self.pos[0] < 1:
            self.pos[0] = 1

        if pressed[pygame.K_DOWN]:
            self.pos[1] -= 2
        if pressed[pygame.K_UP]:
            self.pos[1] += 1
        if pressed[pygame.K_LEFT]:
            self.pos[0] -= 1
        if pressed[pygame.K_RIGHT]:
            self.pos[0] += 1
        if pressed[pygame.K_F1]:
            self.game.world.time_in_game += (self.game.DAY_DURATION*0.01)
        if pressed[pygame.K_F2]:
            self.game.entity_list.append(Entity(self.game, 1, [self.pos[0], self.pos[1]]))
        if pressed[pygame.K_F3]:
            self.game.entity_list.append(Entity(self.game, 0, [self.pos[0], self.pos[1]]))

    def has_enough_space(self, item):
        for k, v in enumerate(self.inventory):
            if v is None or v.item_id == item.type:
                return True
        return False

    def add_to_inventory(self, item):
        for k, v in enumerate(self.inventory):
            if v is not None and v.item_id == item.type:
                self.inventory[k].count += 1
                return True

        for k, v in enumerate(self.inventory):
            if v is None:
                self.inventory[k] = ItemStack(item.type)
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
