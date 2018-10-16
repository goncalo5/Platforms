#!/usr/bin/env python
import pygame as pg
from pygame.locals import Color as Col
from functions import col
vec = pg.math.Vector2


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, id=None, group=None, rect=None,
                 pos=None, image=None, layer=None):
        self.group = group
        if id:
            self.s = game.settings.get(self.group)[id].get
            layer = self.s('layer')
        self._layer = layer
        super(Obstacle, self).__init__(self.groups)
        self.game = game
        self.id = id

        if id:
            size = (self.s('width'), self.s('height'))
            pos = self.s('pos')['x'], game.height - self.s('pos')['y']
            try:
                color = col(game.settings[self.group]['color'])
            except ValueError:
                color = Col(game.settings[self.group]['color'])

            self.image = pg.Surface(size)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.pos = vec(pos)
            self.rect.midbottom = self.pos
        else:
            self.rect = rect
            self.image = image
            self.pos = pos

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.area = self.rect.width * self.rect.height
        self.density = game.settings[self.group]['density']
        self.mass = self.density * self.area
        self.weight = self.mass * game.settings['gravity']
        self.coef_static_friction =\
            float(game.settings[self.group]['coefficient of friction']['static'])
        self.coef_kinetic_friction =\
            float(game.settings[self.group]['coefficient of friction']['kinetic'])
        self.calc_friction()

        self.touch_left = None
        self.touch_right = None
        self.touch_top = None
        self.touch_bot = None

        self.hit_direction = None

    def calc_friction(self):
        self.static_friction = self.coef_static_friction * self.weight
        self.kinetic_friction = self.coef_kinetic_friction * self.weight

    def update(self):
        self.acc.x = 0
        self.acc.y = 0 if self.touch_bot else self.weight
        self.acc.y = min(self.acc.y, 1000)
        # aplly the friction
        # if self.touch_bot:
        #     self.acc.x += self.vel.x * self.game.settings['air_resistence']
        # kinematic equations:
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + self.acc * self.game.dt ** 2 / 2.

        if pg.sprite.collide_rect(self, self.game.ground):
            # self.rect.bottom = self.game.ground.rect.top
            self.pos.y = self.game.ground.rect.top + 1
            self.vel.y = 0
            self.touch_bot = self.game.ground
        else:
            self.touch_bot = None

        self.rect.midbottom = self.pos


class Rock(Obstacle):
    def __init__(self, game, id=None, rect=None,
                 pos=None, image=None, layer=None):
        self.groups = game.all_sprites, game.obstacles, game.rocks
        super(Rock, self).__init__(game, id=id, group='rocks')
        print 'self.groups', self.groups


class Box(Obstacle):
    def __init__(self, game, id=None, rect=None,
                 pos=None, image=None, layer=None):
        self.groups = game.all_sprites, game.obstacles, game.boxes
        super(Box, self).__init__(game, id=id, group='boxes')
        print 'self.groups', self.groups
