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


convert_code2key = {
    82: "up",
    79: "right",
    81: "down",
    80: "left",
    44: "spacebar"
}


class Sprite(Image):
    pass


class Player(Sprite):
    speed = kp.NumericProperty(PLAYER.get("speed"))
    jump = kp.NumericProperty(PLAYER.get("jump"))
    vel = kp.ObjectProperty(Vector(0, 0))
    acc = kp.ObjectProperty(Vector(0, 0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        self.keys = set()

    def _on_keyboard_down(self, *args):
        print("_on_keyboard_down", args)
        code = args[2]
        key = convert_code2key.get(code)
        print(key)
        self.keys.add(key)
        print(self.keys)

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

        # move horizontally:
        if "right" in self.keys:
            sign = 1
        elif "left" in self.keys:
            sign = -1
        else:
            sign = 0
        self.x += sign * self.speed * dt

        # Jump:
        if "spacebar" in self.keys:
            self.vel.y = self.jump
        self.y += self.vel.y

        # Gravity:
        self.acc.y = -PLAYER.get("gravity")

        # Kinematic:
        self.vel += self.acc * dt
        self.pos = Vector(self.pos) + self.vel * dt + 0.5 * self.acc * dt ** 2

        # colissions:
        # collision - Ground:
        if self.y <= 0:
            self.y = 0



class Game(Screen):
    def update(self, dt):
        self.player.update(dt)


class GameApp(App):
    tilesize = kp.NumericProperty(Window.height / 12)
    def build(self):
        self.game = Game()
        Clock.schedule_interval(self.game.update, 1 / GAME.get("fps", 60))
        return self.game

if __name__ == "__main__":
    GameApp().run()