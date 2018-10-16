#!/usr/bin/env python
from os import path
import random
import yaml
import json
import pygame as pg
from pygame.locals import Color as Col
from functions import sign, backoff, backoff3
from Sprites.player import Player
from Sprites.ground import Ground
# from Sprites.rock import Rock
from Sprites.obstacle import Box, Rock


vec = pg.math.Vector2


class Game(object):
    def __init__(self):
        with open('settings.yml') as file:
            self.settings = yaml.load(file)
        self.s = self.settings.get
        print(json.dumps(self.settings, sort_keys=True, indent=4))
        pg.init()
        self.width = int(self.s('screen')['width'])
        self.height = int(self.s('screen')['height'])
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.fps = self.s('screen')['fps']

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.new()
        self.run()

        pg.quit()

    def m2pixels(self, meters):
        pixels = meters * int(self.s('meter'))
        return pixels

    def load_data(self):
        self.dir = path.dirname(__file__)
        pg.mixer.init()  # for sound

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        # create Groups:
        self.rocks = pg.sprite.Group()
        self.boxes = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        # create sprites:
        self.player = Player(self)
        self.ground = Ground(self)
        self.rock1 = Rock(self, 'rock1')
        self.rock2 = Rock(self, 'rock2')
        self.rock3 = Rock(self, 'rock3')
        self.box1 = Box(self, 'box1')
        self.box2 = Box(self, 'box2')
        self.box3 = Box(self, 'box3')

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
            self.dt = self.clock.tick(self.fps) / 1000.
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            self.handle_common_events(event)

    def handle_common_events(self, event):
        # check for closing window
        if event.type == pg.QUIT:
            # force quit
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == 310:
                self.cmd_key_down = True
            if self.cmd_key_down and event.key == pg.K_q:
                # force quit
                quit()

        if event.type == pg.KEYUP:
            if event.key == 310:
                self.cmd_key_down = False

    def update(self):
        # update portion of the game loop

        # print 1, 'self.player.touch_left', self.player.touch_left
        # print 1, 'self.player.touch_right', self.player.touch_right
        # print 1, 'self.player.touch_top', self.player.touch_top
        # print 1, 'self.player.touch_bot', self.player.touch_bot
        self.all_sprites.update()

        # reset touch:
        self.player.reset_touch()

        force = self.player.mass * self.player.acc.x
        # player hit ground
        if pg.sprite.collide_rect(self.player, self.ground):
            # self.player.rect.bottom = self.ground.rect.top
            self.player.pos.y = self.ground.rect.top + 1
            self.player.vel.y = 0
            self.player.touch_bot = self.ground
        # player hit obstacles:
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        # print 'touch' if self.player.touch_the_ground else ''
        for sprite in hits:
            if sprite.hit_direction and sign(force) != sprite.hit_direction:
                sprite.calc_friction()
            if abs(force) <= abs(sprite.static_friction * -1):
                backoff3(self.player, sprite)
            else:
                if self.player.vel.x > 0:
                    sprite.pos.x = self.player.pos.x + self.player.rect.width / 2 + \
                        sprite.rect.width / 2
                if self.player.vel.x < 0:
                    sprite.pos.x = self.player.pos.x - self.player.rect.width / 2 - \
                        sprite.rect.width / 2
                self.player.acc.x -= sign(self.player.acc.x) * (sprite.static_friction)
                sprite.rect.midbottom = sprite.pos

        # # boxes hits rocks
        # hits = pg.sprite.groupcollide(self.boxes, self.rocks, False, False)
        # for box, rocks in hits.items():
        #     for rock in rocks:
        #         box.hit_direction = sign(self.player.vel.x)
        #         backoff3(box, rock)
        #         box.static_friction = rock.static_friction
        #     box.rect.midbottom = box.pos

        # obstacles hits other obstacles:
        hits = pg.sprite.groupcollide(self.obstacles, self.obstacles, False, False)
        for obstacle1, obstacles2 in hits.items():
            for obstacle2 in obstacles2:
                if obstacle1 is obstacle2:
                    continue
                print
                print 3, 'self.box1.pos', self.box1.pos
                print 4, 'self.box2.pos', self.box2.pos

                obstacle1.hit_direction = sign(self.player.vel.x)
                backoff(obstacle1, obstacle2)
                obstacle1.static_friction = obstacle2.static_friction
                # print 1, 'obstacle1.touch_left', obstacle1.touch_left
                # print 1, 'obstacle1.touch_right', obstacle1.touch_right
                # print 1, 'obstacle1.touch_top', obstacle1.touch_top
                # print 1, 'obstacle1.touch_bot', obstacle1.touch_bot
                # print 2, 'obstacle2.touch_left', obstacle2.touch_left
                # print 2, 'obstacle2.touch_right', obstacle2.touch_right
                # print 2, 'obstacle2.touch_top', obstacle2.touch_top
                # print 2, 'obstacle2.touch_bot', obstacle2.touch_bot

                print 5, 'self.box1.pos', self.box1.pos
                print 6, 'self.box2.pos', self.box2.pos
            obstacle1.rect.midbottom = obstacle1.pos

        # if player reaches 1/4 of screen:
        def handle_scroll():
            direction = sign(self.player.vel.x)
            scroll = -max(abs(self.player.vel.x), 2) * self.dt * direction
            self.ground.pos.x += scroll
            for rock in self.rocks:
                rock.pos.x += scroll
            for box in self.boxes:
                box.pos.x += scroll
            self.player.pos.x += scroll
        if self.player.pos.x > self.width * 3 / 4 and self.player.vel.x > 0:
            handle_scroll()
        if self.player.pos.x < self.width / 4 and self.player.vel.x < 0:
            handle_scroll()

        # update positions to draw:
        self.player.rect.midbottom = self.player.pos
        for obstacle in self.obstacles:
            obstacle.rect.midbottom = obstacle.pos

    def draw(self):
        caption = '%s - fps: %.4s' % (self.s('name'), self.clock.get_fps())
        pg.display.set_caption(caption)
        self.screen.fill(Col(self.s('background')['color']))
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
