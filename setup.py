#!/usr/bin/env python
from os import path
import random
import yaml
import json
import pygame as pg
from pygame.locals import Color as Col
from functions import sign, backoff, backoff2, backoff3
from Sprites.player import Player
from Sprites.ground import Ground
from Sprites.rock import Rock
from Sprites.box import Box


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
        # create sprites:
        self.player = Player(self)
        self.ground = Ground(self)
        self.rock1 = Rock(self, 'rock1')
        self.rock2 = Rock(self, 'rock2')
        self.rock3 = Rock(self, 'rock3')
        self.box1 = Box(self, 'box1')

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
        self.all_sprites.update()
        # player hit ground
        if pg.sprite.collide_rect(self.player, self.ground):
            # self.player.rect.bottom = self.ground.rect.top
            self.player.pos.y = self.ground.rect.top + 1
            self.player.vel.y = 0
            self.player.touch_the_ground = True
        else:
            self.player.touch_the_ground = False
        # player hit rocks:
        hits = pg.sprite.spritecollide(self.player, self.rocks, False)
        print 'touch' if self.player.touch_the_ground else ''
        for rock in hits:
            backoff3(self.player, rock)
        # player hits boxes
        hits = pg.sprite.spritecollide(self.player, self.boxes, False)
        if hits:
            box = hits[0]
            # if self.player.vel.x > 0:
            #     box.pos.x = self.player.pos.x + self.player.rect.width / 2 + \
            #         box.rect.width / 2
            # if self.player.vel.x < 0:
            #     box.pos.x = self.player.pos.x - self.player.rect.width / 2 - \
            #         box.rect.width / 2
            # box.rect.midbottom = box.pos
            force = self.player.mass * self.player.acc.x
            if box.hit_direction and sign(force) != box.hit_direction:
                box.calc_friction()
            print 3, 'force: %s' % force
            print 4, 'box.static_friction: %s' % box.static_friction
            if abs(force) <= abs(box.static_friction * -1):
                print 1, 'rock'
                backoff3(self.player, box)
            else:
                print 2, 'box'
                if self.player.vel.x > 0:
                    box.pos.x = self.player.pos.x + self.player.rect.width / 2 + \
                        box.rect.width / 2
                if self.player.vel.x < 0:
                    box.pos.x = self.player.pos.x - self.player.rect.width / 2 - \
                        box.rect.width / 2
                self.player.acc.x -= sign(self.player.acc.x) * (box.static_friction)
                box.rect.midbottom = box.pos

        # boxes hits rocks
        hits = pg.sprite.groupcollide(self.boxes, self.rocks, False, False)
        for box, rocks in hits.items():
            print box, rocks
            for rock in rocks:
                print rock
                box.hit_direction = sign(self.player.vel.x)
                backoff3(box, rock)
                box.static_friction = rock.static_friction
            # rock = rock[0]
            # if box.pos.x + box.rect.width / 2 >\
            #         rock.pos.x - rock.rect.width / 2:
            #     # box.pos.x = \
            #     #     rock.pos.x - rock.rect.width / 2 - box.rect.width / 2
            #     # the box became a rock:
            #     Rock(self, rect=box.rect, pos=box.pos, image=box.image)
            #     box.kill()
            box.rect.midbottom = box.pos

        # if player reaches 1/4 of screen:
        def handle_scroll():
            direction = sign(self.player.vel.x)
            scroll = -max(abs(self.player.vel.x), 2) * self.dt * direction
            for rock in self.rocks:
                rock.pos.x += scroll
            for box in self.boxes:
                box.pos.x += scroll
            self.player.pos.x += scroll

        if self.player.pos.x > self.width * 3 / 4 and self.player.vel.x > 0:
            handle_scroll()
        if self.player.pos.x < self.width / 4 and self.player.vel.x < 0:
            handle_scroll()

        self.player.rect.midbottom = self.player.pos

    def draw(self):
        caption = '%s - fps: %.4s' % (self.s('name'), self.clock.get_fps())
        pg.display.set_caption(caption)
        self.screen.fill(Col(self.s('background')['color']))
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
