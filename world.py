import random

import pygame.image


blocks = {
        # id: (name, break_time, color)
        1: ("stone", .1, pygame.image.load("./textures/blocks/stone.png")),  # stone
        2: ("grass", .1, pygame.image.load("./textures/blocks/grass_block.png")),  # grass
        3: ("dirt", .1, pygame.image.load("./textures/blocks/dirt.png")),  # dirt
        4: ("bedrock", 1000000, pygame.image.load("./textures/blocks/bedrock.png")),  # bedrock
        5: ("cobblestone", 1.5, pygame.image.load("./textures/blocks/cobblestone.png")),
        6: ("wood log", 0, pygame.image.load("./textures/blocks/oak_log.png")),  # wood
        7: ("leaves", 0.01, pygame.image.load("./textures/blocks/oak_leaves.png")),  # leaves
        8: ("diamond ore", 2, pygame.image.load("./textures/blocks/diamond_ore.png")),  # diamond
        9: ("gold ore", 2, pygame.image.load("./textures/blocks/gold_ore.png")),  # gold
        10: ("iron ore", 1.8, pygame.image.load("./textures/blocks/iron_ore.png")),  # iron
        11: ("coal ore", 1.5, pygame.image.load("./textures/blocks/coal_ore.png")),  # coal
        12: ("lapis ore", 2, pygame.image.load("./textures/blocks/lapis_ore.png")),  # lapis
        13: ("wood plank", 2, pygame.image.load("./textures/blocks/oak_planks.png")),
        14: ("crafting table", 2, pygame.image.load("./textures/blocks/crafting_table.png")),
        15: ("furnace", 2, pygame.image.load("./textures/blocks/furnace.png")),

        30: ("blue flower", .5, pygame.image.load("./textures/blocks/kwiat1.png")),
        31: ("orange flower", .5, pygame.image.load("./textures/blocks/kwiat2.png")),
        32: ("purple flower", .5, pygame.image.load("./textures/blocks/kwiat3.png")),
        33: ("pink flower", .5, pygame.image.load("./textures/blocks/kwiat4.png")),
        34: ("light blue flower", .5, pygame.image.load("./textures/blocks/kwiat5.png")),
        35: ("green flower", .5, pygame.image.load("./textures/blocks/kwiat6.png")),
        36: ("red flower", .5, pygame.image.load("./textures/blocks/kwiat7.png")),
}

destroy_stages = [
    pygame.image.load(f"./textures/blocks/destroy_stage_{i}.png") for i in range(10)
]


class World:
    def __init__(self):
        # 1000x600
        self.blocks = []
        self.block_types = blocks
        self.time_in_game = 0

        # generator variables
        random_height = random.randint(55, 80)
        tree_pos = random.randint(6, 10)
        last = 0
        plains = 0
        flower_pos = random.randint(6, 10)

        for i in range(400):
            tmp = [4]
            for j in range(256):
                if j < random_height - 4:
                    tmp.append(1)
                elif j < random_height - 1:
                    tmp.append(3)
                elif j < random_height:
                    tmp.append(2)
                else:
                    tmp.append(0)

            # Tree Generator
            if i == tree_pos:
                tree_pos += random.randint(5, 15)
                # if tree_pos > len(self.blocks):
                #     tree_pos = i
                tree_height = random.randint(6, 8)
                for index, k in enumerate(self.blocks[i - 2]):
                    if tree_height == 0:
                        self.blocks[i - 2][index] = 7
                        tree_height = index
                        break
                    elif k == 0:
                        tree_height -= 1
                        self.blocks[i - 2][index] = 6
                self.blocks[i - 1][tree_height - 1], self.blocks[i - 3][tree_height - 1] = 7, 7
                self.blocks[i - 1][tree_height - 2], self.blocks[i - 3][tree_height - 2] = 7, 7
                tmp[tree_height - 2], self.blocks[i - 4][tree_height - 2] = 7, 7
                self.blocks[i - 1][tree_height - 3], self.blocks[i - 3][tree_height - 3] = 7, 7
                tmp[tree_height - 3], self.blocks[i - 4][tree_height - 3] = 7, 7

            if flower_pos == i:
                if tmp[random_height+1] != 0:
                    flower_pos += random.randint(1, 3)
                else:
                    flower_pos += random.randint(5, 15)
                    tmp[random_height+1] = random.randint(30, 36)

            if plains > 0:
                plains -= 1
                add = 0
            else:
                if random.randint(1, 10) == 1:
                    plains = random.randint(5,10)
                add = random.randint(0, 2)-1
                if last > 0:
                    add = 0
                # elif last < 0:
                #     add = random.randint(0, 2)-1
            last = add
            random_height += add
            self.blocks.append(tmp)

        # cave variables
        cave_pos = [random.randint(2,10), random.randint(2, 60)]
        cave_height = 1
        cave_length = random.randint(20,90)
        # ore generate
        ores_position = []
        for i in range(5):
            ores_position.append(random.randint(2, 10))
        # 0 - diamond
        # 1 - gold
        # 2 - iron
        # 3 - coal
        # 4 - lapis
        for col in range(len(self.blocks)):
            if col == ores_position[0]:
                ores_position[0] += random.randint(10, 30)
                pos = [col, random.randint(2, 10)]
                self.put_ore(pos, 8)
                for i in range(random.randint(0, 5)):
                    if random.choice((0, 1)):
                        pos[0] += (random.randint(0, 2) - 1)
                    else:
                        pos[1] += (random.randint(0, 2) - 1)
                    self.put_ore(pos, 8)

            if col == ores_position[1]:
                ores_position[1] += random.randint(10, 25)
                pos = [col, random.randint(2, 15)]
                self.put_ore(pos, 9)
                for i in range(random.randint(0, 6)):
                    if random.choice((0, 1)):
                        pos[0] += (random.randint(0, 2) - 1)
                    else:
                        pos[1] += (random.randint(0, 2) - 1)
                    self.put_ore(pos, 9)

            if col == ores_position[2]:
                ores_position[2] += random.randint(5, 10)
                pos = [col, random.randint(2, 60)]
                self.put_ore(pos, 10)
                for i in range(random.randint(4, 10)):
                    if random.choice((0, 1)):
                        pos[0] += (random.randint(0, 2) - 1)
                    else:
                        pos[1] += (random.randint(0, 2) - 1)
                    self.put_ore(pos, 10)

            if col == ores_position[3]:
                ores_position[3] += random.randint(5, 15)
                pos = [col, random.randint(2, 65)]
                self.put_ore(pos, 11)
                for i in range(random.randint(5, 15)):
                    if random.choice((0, 1)):
                        pos[0] += (random.randint(0, 2) - 1)
                    else:
                        pos[1] += (random.randint(0, 2) - 1)
                    self.put_ore(pos, 11)

            if col == ores_position[4]:
                ores_position[4] += random.randint(10, 30)
                pos = [col, random.randint(2, 15)]
                self.put_ore(pos, 12)
                for i in range(random.randint(0, 5)):
                    if random.choice((0, 1)):
                        pos[0] += (random.randint(0, 2) - 1)
                    else:
                        pos[1] += (random.randint(0, 2) - 1)
                    self.put_ore(pos, 12)
            # generating caves
            if cave_pos[0] == col:
                for j in range(cave_height):
                    if self.blocks[col][cave_pos[1]+j] not in (4,6,7):
                        self.blocks[col][cave_pos[1]+j] = 0
                cave_length -= 1
                cave_pos[0] = col+1
                cave_height += (random.randint(0, 2)-1)
                cave_pos[1] += (random.randint(0, 2)-1)
                if cave_height < 3:
                    cave_height = 3
                elif cave_height > 5:
                    cave_height = 5

            if cave_length == 0:
                try:
                    if self.blocks[col+1][cave_pos[1]] != 4:
                        self.blocks[col+1][cave_pos[1]] = 0
                except IndexError:
                    pass

                cave_pos[1] = random.randint(2, 60)
                cave_length = random.randint(20, 80)

            self.blocks[col][-1] = 4
        for i in range(len(self.blocks[0])):
            self.blocks[0][i] = 4
            self.blocks[len(self.blocks)-2][i] = 4

    def put_ore(self, pos, id):
        try:
            if self.blocks[pos[0]][pos[1]] == 1:
                self.blocks[pos[0]][pos[1]] = id
        except IndexError:
            pass
