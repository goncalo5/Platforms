#!/usr/bin/env python
import random
import pygame as pg
from pygame.locals import Color as Col


class Ground(pg.sprite.Sprite):
    def __init__(self, game):
        self.s = game.settings.get('ground').get
        self._layer = self.s('layer')
        self.groups = game.all_sprites
        super(Ground, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((self.s('width'), self.s('height')))
        self.image.fill(Col(self.s('color')))
        self.rect = self.image.get_rect()
        self.rect.bottom = game.height
        self.friction = self.s('friction')
