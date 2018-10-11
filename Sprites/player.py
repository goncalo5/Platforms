#!/usr/bin/env python
import random
import pygame as pg
from pygame.locals import Color as Col


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        sets = game.settings.get('player').get
        self._layer = sets('layer')
        self.groups = game.all_sprites
        super(Player, self).__init__(self.groups)
        self.game = game
        tilesize = game.settings.get('tilesize')
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(Col('yellow'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0

    def events(self):
        self.dx = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.dx = -5
        if keys[pg.K_RIGHT]:
            self.dx = 5

    def update(self):
        self.events()
        self.rect.x += self.dx
        if self.rect.left > self.game.width:
            self.rect.right = 0
