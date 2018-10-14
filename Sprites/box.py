#!/usr/bin/env python
import pygame as pg
from pygame.locals import Color as Col
from functions import col
vec = pg.math.Vector2


class Box(pg.sprite.Sprite):
    def __init__(self, game, box_id):
        print game.settings.get('boxes')[box_id]
        self.s = game.settings.get('boxes')[box_id].get
        self._layer = self.s('layer')
        self.groups = game.all_sprites, game.boxes
        super(Box, self).__init__(self.groups)
        self.game = game

        self.image = pg.Surface((self.s('width'), self.s('height')))
        self.image.fill(col(self.s('color')))
        self.rect = self.image.get_rect()
        self.pos = vec(self.s('pos')['x'], game.height - self.s('pos')['y'])
        self.rect.midbottom = self.pos

    def update(self):
        self.rect.midbottom = self.pos
