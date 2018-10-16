#!/usr/bin/env python
import random
import pygame as pg
from pygame.locals import Color as Col
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.s = game.settings.get('player').get
        self._layer = self.s('layer')
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        self.image = pg.Surface((self.s('width'), self.s('height')))
        self.image.fill(Col(self.s('color')))
        self.rect = self.image.get_rect()
        self.pos = vec(self.s('pos')['x'], game.height - self.s('pos')['y'])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        # self.rect.midbottom = self.pos
        self.dx = 0
        self.mass = self.s('mass')
        self.weight = self.mass * game.settings['gravity']
        # self.weight = self.s('weight')
        self.touch_the_ground = False

    def events(self):
        keys = pg.key.get_pressed()
        if self.touch_the_ground:
            if keys[pg.K_LEFT]:
                self.vel.x += -self.s('speed')['running']
                self.acc.x += -self.s('aceleration')
            if keys[pg.K_RIGHT]:
                self.vel.x += self.s('speed')['running']
                self.acc.x += self.s('aceleration')
            if keys[pg.K_SPACE]:
                self.vel.y = -self.s('jump')

    def update(self):
        # print 1
        # print 'pos: %s' % self.pos
        # print 'vel: %s' % self.vel
        # print 'acc: %s' % self.acc
        print 1, self.touch_the_ground
        self.acc.x = 0
        self.acc.y = 0 if self.touch_the_ground else self.weight
        print 15, self.weight
        print 2, self.pos, self.vel, self.acc
        # print 2
        # print 'pos: %s' % self.pos
        # print 'vel: %s' % self.vel
        # print 'acc: %s' % self.acc
        self.events()
        # print 3
        # print 'pos: %s' % self.pos
        # print 'vel: %s' % self.vel
        # print 'acc: %s' % self.acc
        # aplly the friction
        if self.touch_the_ground:
            self.acc.x += self.vel.x * self.game.settings['air_resistence']
        print 4, self.pos, self.vel, self.acc
        # print 'pos: %s' % self.pos
        # print 'vel: %s' % self.vel
        # print 'acc: %s' % self.acc
        # kinematic equations:
        self.vel += self.acc * self.game.dt
        print 5, self.pos, self.vel, self.acc
        self.pos += self.vel * self.game.dt + self.acc * self.game.dt ** 2 / 2.

        print 6, self.pos, self.vel, self.acc
        if self.pos.x > self.game.width - 100:
            self.pos.x = 0

        # stop faster
        if abs(self.vel.x) < .5:
            self.vel.x = 0

        # exit(0)
        self.rect.midbottom = self.pos
        # print 5
        # print 'pos: %s' % self.pos
        # print 'vel: %s' % self.vel
        # print 'acc: %s' % self.acc
