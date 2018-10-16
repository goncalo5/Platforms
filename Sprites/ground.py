#!/usr/bin/env python
import random
import pygame as pg
from pygame.locals import Color as Col
vec = pg.math.Vector2


class Ground(pg.sprite.Sprite):
    def __init__(self, game):
        self.s = game.settings.get('ground').get
        self._layer = self.s('layer')
        self.groups = game.all_sprites
        super(Ground, self).__init__(self.groups)
        self.game = game
        n_of_ground = 10
        self.image = pg.Surface((self.s('width'),
                                 self.s('height') + game.height * n_of_ground))
        self.image.fill(Col(self.s('color')))
        self.rect = self.image.get_rect()
        self.rect.bottom = game.height * (n_of_ground + 1)
        self.friction = self.s('friction')

        self.pos = vec(self.rect.topleft)

        print 12, self.rect

    def update(self):
        self.rect.topleft = self.pos
