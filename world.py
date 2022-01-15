import random
from variables import block_type
import pygame.image
from block import Block

destroy_stages = [
    pygame.image.load(f"./textures/blocks/destroy_stage_{i}.png") for i in range(10)
]


class World:
    def __init__(self):
        # 1000x600
        self.blocks = []
        self.time_in_game = 0

        # generator variables
        random_height = random.randint(55, 80)
        tree_pos = random.randint(6, 10)
        last = 0
        plains = 0
        flower_pos = random.randint(6, 10)

        for i in range(1200):
            tmp = [Block(4)]
            for j in range(256):
                if j < random_height - 4:
                    tmp.append(Block(1))
                elif j < random_height - 1:
                    tmp.append(Block(3, True))
                elif j < random_height:
                    tmp.append(Block(2, True))
                else:
                    tmp.append(Block(0, True, True))

            # Tree Generator
            if i == tree_pos:
                tree_pos += random.randint(5, 15)
                tree_height = random.randint(6, 8)
                for index, k in enumerate(self.blocks[i - 2]):
                    if k.block_id == 0:
                        for j in range(tree_height+1):
                            self.blocks[i - 2][index+j] = Block(6, True, True)
                            if j == tree_height:
                                self.blocks[i - 2][index+j] = Block(7, True, True)
                        tree_height += index
                        break

                self.blocks[i - 1][tree_height - 1], self.blocks[i - 3][tree_height - 1] = Block(7, True, True), Block(7, True, True)
                self.blocks[i - 1][tree_height - 2], self.blocks[i - 3][tree_height - 2] = Block(7, True, True), Block(7, True, True)
                tmp[tree_height - 2], self.blocks[i - 4][tree_height - 2] = Block(7, True, True), Block(7, True, True)
                self.blocks[i - 1][tree_height - 3], self.blocks[i - 3][tree_height - 3] = Block(7, True, True), Block(7, True, True)
                tmp[tree_height - 3], self.blocks[i - 4][tree_height - 3] = Block(7, True, True), Block(7, True, True)

            if flower_pos == i:
                if tmp[random_height+1].block_id != 0:
                    flower_pos += random.randint(1, 3)
                else:
                    flower_pos += random.randint(5, 15)
                    tmp[random_height+1] = Block(random.randint(30, 36), True, True)

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
                    if self.blocks[col][cave_pos[1]+j].block_id not in (4,6,7):
                        self.blocks[col][cave_pos[1]+j] = Block(0, True, True)
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
                    if self.blocks[col+1][cave_pos[1]].block_id != 4:
                        self.blocks[col+1][cave_pos[1]] = Block(0, True, True)
                except IndexError:
                    pass

                cave_pos[1] = random.randint(2, 60)
                cave_length = random.randint(20, 80)

            self.blocks[col][-1] = Block(4)
        for i in range(len(self.blocks[0])):
            self.blocks[0][i] = Block(4)
            self.blocks[len(self.blocks)-2][i] = Block(4)

    def put_ore(self, pos, id):
        try:
            if self.blocks[pos[0]][pos[1]].block_id == 1:
                self.blocks[pos[0]][pos[1]] = Block(id)
        except IndexError:
            pass
