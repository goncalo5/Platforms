#!/usr/bin/env python
import pygame as pg
from pygame.locals import Color as Col
vec = pg.math.Vector2


class Rock(pg.sprite.Sprite):
    def __init__(self, game, id=None, rect=None,
                 pos=None, image=None, layer=None):
        if id:
            self.s = game.settings.get('rocks')[id].get
            layer = self.s('layer')
        self._layer = layer
        self.groups = game.all_sprites, game.rocks
        super(Rock, self).__init__(self.groups)
        self.game = game
        self.id = id

        if id:
            size = (self.s('width'), self.s('height'))
            pos = (self.s('pos')['x'], game.height - self.s('pos')['y'])
            color = Col(game.settings['rocks']['color'])
            self.image = pg.Surface(size)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.pos = vec(pos)
            self.rect.midbottom = self.pos
        else:
            self.rect = rect
            self.image = image
            self.pos = pos

        if self.rect.bottom >= game.ground.rect.top:
            self.touch_the_ground = True
        else:
            self.touch_the_ground = False

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.area = self.rect.width * self.rect.height
        self.density = game.settings['rocks']['density']
        self.mass = self.density * self.area
        self.weight = self.mass * game.settings['gravity']
        self.coef_static_friction =\
            float(game.settings['rocks']['coefficient of friction']['static'])
        self.coef_kinetic_friction =\
            float(game.settings['rocks']['coefficient of friction']['kinetic'])
        self.static_friction = self.coef_static_friction * self.weight
        self.kinetic_friction = self.coef_kinetic_friction * self.weight

    def update(self):
        self.rect.midbottom = self.pos
