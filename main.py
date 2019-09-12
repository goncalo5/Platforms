# kivy:
from kivy.app import App
from kivy.core.window import Window
from kivy import properties as kp
from kivy.clock import Clock
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


class Game(Screen):
    def __init__(self):
        super().__init__()
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
        if "right" in self.keys:
            sign = 1
        elif "left" in self.keys:
            sign = -1
        else:
            sign = 0

        self.player.x += sign * self.player.speed * dt


class GameApp(App):
    tilesize = kp.NumericProperty(Window.height / 12)
    def build(self):
        self.game = Game()
        Clock.schedule_interval(self.game.update, 1 / GAME.get("fps", 60))
        return self.game

if __name__ == "__main__":
    GameApp().run()