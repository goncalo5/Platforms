
from kivy.config import Config
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')
# Config.set('graphics', 'height', '200')

# kivy:
from kivy.app import App
from kivy.core.window import Window
from kivy import properties as kp
from kivy.clock import Clock
from kivy.vector import Vector
# uix:
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
# self:
from settings import GAME, PLAYER

# Window.fullscreen = 'auto'


convert_code2key = {
    82: "up",
    79: "right",
    81: "down",
    80: "left",
    44: "spacebar"
}


class Sprite(Image):
    pass


class Platform(Sprite):
    pass


class Rock(Sprite):
    pass


class Player(Sprite):
    # constants:
    # speed = kp.NumericProperty(PLAYER.get("speed"))
    jump = kp.NumericProperty(PLAYER.get("jump"))
    gravity = kp.NumericProperty(PLAYER.get("gravity"))

    # vars:
    vel = kp.ObjectProperty(Vector(0, 0))
    acc = kp.ObjectProperty(Vector(0, 0))
    is_touching = kp.BooleanProperty(True)

    def __init__(self, **kwargs):
        # print("__init__ player", self.width)
        super().__init__(**kwargs)
        # print(self.width)
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        self.keys = set()
        Clock.schedule_once(self.after_init, 0)

    def after_init(self, dt):
        # print(self.width)
        self.app = App.get_running_app()
        self.tilesize = self.app.tilesize
        self.speed = PLAYER.get("speed") * self.tilesize

    def _on_keyboard_down(self, *args):
        # print("_on_keyboard_down", args)
        code = args[2]
        key = convert_code2key.get(code)
        # print(key)
        self.keys.add(key)
        # print(self.keys)

    def _on_keyboard_up(self, *args):
        print("_on_keyboard_up", args)
        code = args[2]
        key = convert_code2key.get(code)
        print(key)
        self.keys.remove(key)
        print(self.keys)

    def on_touch_down(self, touch):
        pass


    def update(self, dt):
        # print("update player", self.pos)

        if self.is_touching:
            # print("is_touching")
            self.acc = Vector(0, 0)
            self.vel = Vector(0, 0)
            # move horizontally:
            if "right" in self.keys:
                sign = 1
            elif "left" in self.keys:
                sign = -1
            else:
                sign = 0
            self.vel.x = sign * self.speed
            print(55, self.vel.x, self.keys, dt)


            # Jump:
            if "spacebar" in self.keys:
                y = self.jump * self.width
                self.vel.y = (2 * self.gravity * y) ** 0.5
                self.is_touching = False
        else:
            # Gravity:
            # print("apply grav")
            self.acc.y = -self.gravity

        # Kinematic:
        self.vel += self.acc * dt
        self.pos = Vector(self.pos) + self.vel * dt + 0.5 * self.acc * dt ** 2
        print(57, self.vel.x, self.keys)


class Game(Screen):
    def update(self, dt):
        self.player.update(dt)

        # collision - platforms:
        is_touching_in_any_platform = False
        for sprite in self.children:
            if isinstance(sprite, Platform):
                # print(sprite, self.player, sprite == self.player)
                if self.player.collide_widget(sprite):
                    # print("collide")
                    if self.player.center_y < sprite.top:
                        continue
                    if self.player.vel.y <= 0:
                        self.player.y = sprite.top
                        self.player.is_touching = True
                        is_touching_in_any_platform = True

        self.player.is_touching = is_touching_in_any_platform


class GameApp(App):
    tilesize = kp.NumericProperty(Window.height * GAME.get("tilesize", 1 / 12))
    def build(self):
        self.game = Game()
        Clock.schedule_interval(self.game.update, 1 / GAME.get("fps", 60))
        return self.game

if __name__ == "__main__":
    GameApp().run()