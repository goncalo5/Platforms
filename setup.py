#!/usr/bin/env python
from os import path
import random
import yaml
import pygame as pg
from pygame.locals import Color as Col
from Sprites.player import Player


class Game(object):
    def __init__(self):
        with open('settings.yml') as file:
            self.settings = yaml.load(file)
        self.s = self.settings.get
        print self.settings
        pg.init()
        self.width = int(self.s('screen').get('width'))
        self.height = int(self.s('screen').get('height'))
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.s('name'))
        self.clock = pg.time.Clock()
        self.fps = self.s('screen').get('fps')

        # variables
        self.cmd_key_down = False

        self.load_data()
        self.new()
        self.run()

        pg.quit()

    def load_data(self):
        self.dir = path.dirname(__file__)
        pg.mixer.init()  # for sound

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = Player(self, 100, 100)

    def run(self):
        # game loop - set  self.playing = False to end the game
        self.running = True
        while self.running:
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

    def draw(self):
        self.screen.fill(Col(self.s('background').get('color')))
        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def quit(self):
        self.running = False


Game()
