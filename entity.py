import random
from variables import entity_types


class Entity:
    def __init__(self, game, entity_type, pos, task=0, task_duration=5):
        self.game = game
        self.type = entity_type
        self.pos = pos
        self.stats = entity_types[entity_type]
        self.task = task
        self.task_duration = task_duration
        self.velocity = 0
        self.direction = 2

    def update(self):
        # wyswietlanie moba
        self.game.screen.blit(self.stats[self.direction], (round((self.pos[0] - self.game.player.pos[0] + 25) * 20 + self.game.player.damage_earthquake[0], 2), round(660 - self.stats[4][1] - ((self.pos[1] - self.game.player.pos[1] + 10) * 20) + self.game.player.damage_earthquake[1], 2)))

        if self.game.paused:
            return 0
        vector = [0, round(self.velocity, 2)-0.1]

        if self.velocity >= 0:
            self.velocity *= 0.9

        if self.task == -1:
            vector[0] -= 0.1
            self.task_duration -= 0.1
            self.direction = 2
        elif self.task == 1:
            vector[0] += 0.1
            self.task_duration -= 0.1
            self.direction = 3
        else:
            self.task_duration -= 0.07

        if -0.1 < self.task_duration < 0.1:
            if self.task != 0:
                self.task = 0
            else:
                self.task = random.choice((-1,1))

            self.task_duration = random.randint(5, 10)

        # Kolizje
        if vector[1] < 0:
            # sprawdzanie blokow pod nogami
            for i in range(self.stats[4][0]//20+1):
                if self.game.world.blocks[int(self.pos[0]+i)][int(self.pos[1] + vector[1])] not in self.game.IGNORED_BLOCKS:
                    vector[1] = 0
                    self.pos[1] = int(self.pos[1])

            if self.game.world.blocks[int(self.pos[0]+(self.stats[4][0]/20))][int(self.pos[1] + vector[1])] not in self.game.IGNORED_BLOCKS:
                vector[1] = 0
                self.pos[1] = int(self.pos[1])

        if vector[0] < 0:
            # sprawdzanie bloku po lewej
            for i in range(self.stats[4][1]//20+1):
                if self.game.world.blocks[int(self.pos[0] + vector[0])][int(self.pos[1])+i] not in self.game.IGNORED_BLOCKS:
                    vector[0] = 0
                    self.jump()

            if self.game.world.blocks[int(self.pos[0] + vector[0])][int(self.pos[1] + (self.stats[4][1]/20))] not in self.game.IGNORED_BLOCKS:
                vector[0] = 0
                self.jump()

        elif vector[0] > 0:
            # sprawdzanie bloku po prawej
            for i in range(self.stats[4][1]//20+1):
                if self.game.world.blocks[int(self.pos[0] + vector[0] + self.stats[4][0]/20)][int(self.pos[1])+i] not in self.game.IGNORED_BLOCKS:
                    vector[0] = 0
                    self.jump()

            if self.game.world.blocks[int(self.pos[0] + vector[0] + self.stats[4][0]/20)][int(self.pos[1] + (self.stats[4][1]/20))] not in self.game.IGNORED_BLOCKS:
                vector[0] = 0
                self.jump()

        self.pos = [self.pos[i]+vector[i] for i in range(2)]

    def jump(self):
        for i in range(self.stats[4][0]//20+1):
            if self.game.world.blocks[int(self.pos[0]+i)][int(self.pos[1]-0.1)] not in self.game.IGNORED_BLOCKS:
                self.velocity = .3
                # TODO dodac sprawdzanie bloku nad glowa
                break
