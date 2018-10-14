#!/usr/bin/env python
import pygame as pg
from pygame.locals import Color as Col
vec = pg.math.Vector2


class Rock(pg.sprite.Sprite):
    def __init__(self, game, rock_id=None, rect=None,
                 pos=None, image=None, layer=None):
        if rock_id:
            self.s = game.settings.get('rocks')[rock_id].get
            size = (self.s('width'), self.s('height'))
            pos = (self.s('pos')['x'], game.height - self.s('pos')['y'])
            color = Col(self.s('color'))
            layer = self.s('layer')
        self._layer = layer
        self.groups = game.all_sprites, game.rocks
        super(Rock, self).__init__(self.groups)
        self.game = game

        if rock_id:
            self.image = pg.Surface(size)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.pos = vec(pos)
            self.rect.midbottom = self.pos
        else:
            self.rect = rect
            self.image = image
            self.pos = pos

    def update(self):
        self.rect.midbottom = self.pos
