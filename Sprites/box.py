#!/usr/bin/env python
import pygame as pg
from pygame.locals import Color as Col
from functions import col
vec = pg.math.Vector2


class Box(pg.sprite.Sprite):
    def __init__(self, game, id):
        print game.settings.get('boxes')[id]
        self.s = game.settings.get('boxes')[id].get
        self._layer = self.s('layer')
        self.groups = game.all_sprites, game.boxes
        super(Box, self).__init__(self.groups)
        self.game = game
        self.id = id

        self.image = pg.Surface((self.s('width'), self.s('height')))
        self.image.fill(col(self.s('color')))
        self.rect = self.image.get_rect()
        self.pos = vec(self.s('pos')['x'], game.height - self.s('pos')['y'])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.midbottom = self.pos

        self.area = self.rect.width * self.rect.height
        self.density = game.settings['boxes']['density']
        self.mass = self.density * self.area
        self.weight = self.mass * game.settings['gravity']
        self.coef_static_friction =\
            float(game.settings['boxes']['coefficient of friction']['static'])
        self.coef_kinetic_friction =\
            float(game.settings['boxes']['coefficient of friction']['kinetic'])
        self.calc_friction()

        if self.rect.bottom >= game.ground.rect.top:
            self.touch_the_ground = True
        else:
            self.touch_the_ground = False

        self.hit_direction = None

    def calc_friction(self):
        print 'calc_friction'
        self.static_friction = self.coef_static_friction * self.weight
        self.kinetic_friction = self.coef_kinetic_friction * self.weight
        print 'self.weight', self.weight
        print 'self.coef_static_friction', self.coef_static_friction
        print 'self.static_friction', self.static_friction

    def update(self):
        self.acc.x = 0
        self.acc.y = 0 if self.touch_the_ground else self.weight
        # aplly the friction
        if self.touch_the_ground:
            self.acc.x += self.vel.x * self.game.settings['air_resistence']
        print 1, self.pos.y, self.vel, self.acc
        # kinematic equations:
        self.vel += self.acc * self.game.dt
        print 2, self.pos.y, self.vel, self.acc
        self.pos += self.vel * self.game.dt + self.acc * self.game.dt ** 2 / 2.
        print 3, self.pos.y, self.vel, self.acc

        if pg.sprite.collide_rect(self, self.game.ground):
            # self.rect.bottom = self.game.ground.rect.top
            self.pos.y = self.game.ground.rect.top + 1
            self.vel.y = 0
            self.touch_the_ground = True
        else:
            self.touch_the_ground = False

        self.rect.midbottom = self.pos
