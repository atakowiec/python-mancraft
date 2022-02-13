import math

transformations = {
    7: 67,
    4: 4,
    2: 72,
    26: 27,
    6: 71,
    74: 74,
    75: 75,
    73: 73,
    72: 72,
    71: 71,
    70: 70,
    67: 67,
    66: 66
}


class NetherReactorCore:
    def __init__(self, game):
        self.game = game
        self.running = False
        self.reactor_pos = []
        self.transformed = []
        self.to_transform = []
        self.SPEED = 1

    def update(self):
        if not self.game.tick_counter%self.SPEED and self.running:
            new_to_transform = []
            for block in self.to_transform:
                if block not in self.transformed:
                    block_id = self.game.world.blocks[block[0]][block[1]].block_id
                    if block_id == 4:
                        continue
                    if block_id in transformations.keys():
                        self.game.world.blocks[block[0]][block[1]].block_id = transformations[block_id]
                    else:
                        self.game.world.blocks[block[0]][block[1]].block_id = 66
                    self.transformed.append(block)

                    for i in (-1,1):
                        temp = [block[0], block[1]+i]
                        if temp not in self.transformed and temp not in new_to_transform:
                            if math.hypot(self.reactor_pos[0]-temp[0], self.reactor_pos[1]-temp[1]) < 25:
                                new_to_transform.append(temp)
                            else:
                                self.game.world.blocks[temp[0]][temp[1]].block_id = 76

                        temp = [block[0]+i, block[1]]

                        if temp not in self.transformed and temp not in new_to_transform:
                            if math.hypot(self.reactor_pos[0]-temp[0], self.reactor_pos[1]-temp[1]) < 25:
                                new_to_transform.append(temp)
                            else:
                                self.game.world.blocks[temp[0]][temp[1]].block_id = 76

            self.to_transform = new_to_transform
            if not self.to_transform:
                self.running = False

    def create_reactor(self, pos):
        if not self.running:
            self.running = True
            self.reactor_pos = pos
            self.to_transform = [pos]
            self.transformed = []
            for i in (-1,0,1):
                for j in (-1,0,1):
                    block_id = self.game.world.blocks[pos[0]+i][pos[1]+j].block_id
                    if block_id == 5:
                        self.game.world.blocks[pos[0] + i][pos[1] + j].block_id = 74
                    if block_id == 63:
                        self.game.world.blocks[pos[0] + i][pos[1] + j].block_id = 75
