#!/usr/bin/env python
from os import path
import random
import yaml
import json
import pygame as pg
from pygame.locals import Color as Col
from functions import sign
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
        for rock in hits:
            # print self.player.vel
            # rock = hits[0]
            print rock.rect.top, self.player.pos.y, self.player.rect.bottom
            if rock.rect.left < self.player.pos.x < rock.rect.right:
                self.player.pos.y = rock.rect.y
            else:
                if self.player.pos.x < rock.rect.left:
                    self.player.pos.x =\
                        rock.rect.left - self.player.rect.width / 2
                if self.player.pos.x > rock.rect.right:
                    self.player.pos.x =\
                        rock.rect.right + self.player.rect.width / 2
            if self.player.pos.y == rock.rect.top:
                self.player.touch_the_ground = True
        # player hits boxes
        hits = pg.sprite.spritecollide(self.player, self.boxes, False)
        if hits:
            box = hits[0]
            if self.player.vel.x > 0:
                box.pos.x = self.player.pos.x + self.player.rect.width / 2 + \
                    box.rect.width / 2
            if self.player.vel.x < 0:
                box.pos.x = self.player.pos.x - self.player.rect.width / 2 - \
                    box.rect.width / 2
            box.rect.midbottom = box.pos
        # boxes hits rocks
        hits = pg.sprite.groupcollide(self.boxes, self.rocks, False, False)
        for box, rock in hits.items():
            print box, rock
            rock = rock[0]
            if box.pos.x + box.rect.width / 2 >\
                    rock.pos.x - rock.rect.width / 2:
                # box.pos.x = \
                #     rock.pos.x - rock.rect.width / 2 - box.rect.width / 2
                # the box became a rock:
                Rock(self, rect=box.rect,
                     pos=box.pos, image=box.image)
                box.kill()
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
