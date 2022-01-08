import random
import pygame.draw


class DroppedItem:
    def __init__(self, game, item_id, pos, immunite=0, velocity=None, life_time = 0):
        self.game = game
        self.world = self.game.world

        self.type = item_id
        self.pos = [pos[0] + 0.25 + (random.randint(1, 10)-5)/10, pos[1] + 0.25]
        self.size = (10, 10)
        self.life_time = life_time
        self.to_remove = False
        self.immunite = immunite

        # Moving variables
        self.gravity = -0.2
        self.vector = [0, self.gravity]
        if velocity is None:
            velocity = [0, 0]
        self.velocity = velocity

    def update(self):
        self.immunite -= 1
        self.life_time += 1
        self.vector = [self.velocity[0], self.gravity+self.velocity[1]]
        if not (-0.05 < self.velocity[0] < 0.05):
            self.velocity[0] *= 0.9
        else:
            self.velocity[0] = 0

        self.velocity[1] *= (-self.gravity/10)

        # Mechanika Kolizji z podłożem oraz podskakiwanie itemow
        if self.world.blocks[int(self.pos[0])][int(self.pos[1]-0.1)] not in self.game.IGNORED_BLOCKS or self.world.blocks[int(self.pos[0]+0.2)][int(self.pos[1]-0.1)] not in self.game.IGNORED_BLOCKS:
            self.vector = [0, 0]
            self.pos[1] = int(self.pos[1]+0.1)
            self.velocity[1] = 0.005

        # Kolizje z blokami obok
        if self.world.blocks[int(self.pos[0] + 0.5)][int(self.pos[1])] not in self.game.IGNORED_BLOCKS:
            self.pos[0] = int(self.pos[0])+0.5
            self.vector[0] = 0
            self.velocity[0] = 0
        elif self.world.blocks[int(self.pos[0] - 0.1)][int(self.pos[1])] not in self.game.IGNORED_BLOCKS:
            self.pos[0] = int(self.pos[0]+0.8)
            self.vector[0] = 0
            self.velocity[0] = 0

        # Mechanika przylatywania itemow do gracza
        if self.to_remove:
            self.vector[0] += (self.game.player.pos[0]-self.pos[0]+0.25)/(30/self.life_time)
            self.vector[1] += (self.game.player.pos[1]-self.pos[1]+1.25)/(30/self.life_time)

        self.pos[0] += (self.vector[0]+self.velocity[0])
        self.pos[1] += (self.vector[1]+self.velocity[1])

        self.game.screen.blit(pygame.transform.scale(self.world.block_types[self.type][2], (10,10)), (round((self.pos[0] - self.game.player.pos[0]+25)*20, 2), round(650 - ((self.pos[1]-self.game.player.pos[1] + 10) * 20), 2)))
        # pygame.draw.rect(self.game.screen, self.world.block_types[self.type][2], pygame.Rect(round((self.pos[0] - self.game.player.pos[0]+25)*20, 2), round(650 - ((self.pos[1]-self.game.player.pos[1] + 10) * 20), 2), 10, 10))

    def has_been_picked(self):
        if self.immunite <= 0:
            self.life_time = 0
            self.to_remove = True
