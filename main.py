
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
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
# self:
from settings import GAME, PLAYER
from map import Map, Camera

# Window.fullscreen = 'auto'


convert_code2key = {
    82: "up",
    79: "right",
    81: "down",
    80: "left",
    44: "spacebar"
}


class Sprite(Image):
    tilesize = kp.NumericProperty(Window.height * GAME.get("tilesize", 1 / 12))
    tile = kp.ListProperty([0, 0])
    mapx = kp.NumericProperty()
    def __init__(self, **kwargs):
        super().__init__()
        self.tile = kwargs.get("tile")

    def on_tile(self, *args):
        self.mapx = self.tile[0] * self.tilesize
        self.y = self.tilesize * self.tile[1]


class Platform(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Rock(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Coin(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Flag(Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Player(RelativeLayout):
    tilesize = kp.NumericProperty(Window.height * GAME.get("tilesize", 1 / 12))
    tile = kp.ListProperty([0, 0])
    mapx = kp.NumericProperty()
    # constants:
    # speed = kp.NumericProperty(PLAYER.get("speed"))
    jump = kp.NumericProperty(PLAYER.get("jump"))
    gravity = kp.NumericProperty(PLAYER.get("gravity"))

    # vars:
    vel = kp.ObjectProperty(Vector(0, 0))
    acc = kp.ObjectProperty(Vector(0, 0))
    is_touching = kp.DictProperty({
        "platform": True,
        "rock": False
    })
    is_grabbing = kp.BooleanProperty(False)

    # animation:
    img_i = kp.NumericProperty(1)
    is_walking = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        print("__init__ player", self)
        super().__init__()
        self.source = "atlas://Imgs/Player/player/p1_front"
        self.allow_stretch = True
        print(self.pos, self.size)
        Window.bind(on_key_down=self._on_keyboard_down)
        Window.bind(on_key_up=self._on_keyboard_up)
        self.keys = set()
        Clock.schedule_once(self.after_init, 0)
        Clock.schedule_interval(self.update_source, 0.1)

    def after_init(self, dt):
        print("after_init")
        self.app = App.get_running_app()
        self.speed = PLAYER.get("speed") * self.tilesize

    def update_source(self, dt):
        # print("update_source", self.img_i)
        if not self.is_walking:
            # print("stop")
            self.source = "atlas://Imgs/Player/player/p1_stand"
            return
        if self.img_i < 10:
            s = "0%s" % self.img_i
        else:
            s = "%s" % self.img_i

        self.source = "atlas://Imgs/Player/player/p1_walk%s" % s

        self.img_i += 1
        if self.img_i > 11:
            self.img_i = 1

    def new(self):
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.on_tile()

    def on_tile(self, *args):
        self.mapx = self.tile[0] * self.tilesize
        self.y = self.tilesize * self.tile[1]

    def _on_keyboard_down(self, *args):
        # print("_on_keyboard_down", args)
        if self.parent.manager.current == "main_menu":
            self.parent.manager.start_a_game()

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
        # print("\nupdate player mapx:%s, pos:%s, size:%s, acc:%s" % (self.mapx, self.pos, self.size, self.acc))

        if self.is_touching["platform"] or self.is_touching["rock"]:
            # self.source = "atlas://Imgs/Player/player/p1_stand"
            self.acc = Vector(0, 0)
            self.vel = Vector(0, 0)
            # move horizontally:
            if "right" in self.keys:
                sign = 1
                self.angle = 0
                self.is_walking = True
            elif "left" in self.keys:
                sign = -1
                self.angle = 180
                self.is_walking = True
            else:
                sign = 0
                self.is_walking = False
            self.vel.x = sign * self.speed
            # print("vel", self.vel)

            # Jump:
            if "spacebar" in self.keys:
                y = self.jump * self.width
                self.vel.y = (2 * self.gravity * y) ** 0.5
                self.is_touching["platform"] = False
            # print("55 update player mapx:%s, pos:%s, acc:%s" % (self.mapx, self.pos, self.acc))
        else:
            # Gravity:
            # print("apply grav")
            self.acc.y = -self.gravity
            self.source = "atlas://Imgs/Player/player/p1_jump"
        if self.is_grabbing:
            self.acc.y = -self.gravity
        # print("56 update player mapx:%s, pos:%s, vel:%s, acc:%s" % (self.mapx, self.pos, self.vel, self.acc))

        # Kinematic:
        self.vel += self.acc * dt
        # print("57 update player mapx:%s, pos:%s, vel:%s" % (self.mapx, self.pos, self.vel))
        self.mapx += self.vel.x * dt + 0.5 * self.acc.x * dt ** 2
        self.y += self.vel.y * dt + 0.5 * self.acc.y * dt ** 2

        # print("end update player mapx:%s, pos:%s" % (self.mapx, self.pos))

class Game(Screen):
    fps = kp.NumericProperty()
    paused = kp.BooleanProperty(False)
    win = kp.BooleanProperty(0)
    gold = kp.NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player(tile=(0, 0))
        self.add_widget(self.player)

    def new(self, map_name):
        self.paused = False
        self.win = 0
        self.button_over.opacity = 0
        self.button_over.disabled = 1
        self.clean_all_sprites()
        # load data:
        self.map = Map(map_name, self.player.tilesize)
        print("map", self.map.data)
        for row, tiles in enumerate(reversed(self.map.data)):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    print("player reposition", self.player.pos)
                    self.player.tile = (col, row)
                    self.player.new()
                    print(self.player.pos)
                elif tile == "P":
                    tile = Platform(tile=(col, row))
                    self.add_widget(tile)
                elif tile == "R":
                    tile = Rock(tile=(col, row))
                    self.add_widget(tile)
                elif tile == "C":
                    tile = Coin(tile=(col, row))
                    self.add_widget(tile)
                elif tile == "F":
                    tile = Flag(tile=(col, row))
                    self.add_widget(tile)
        self.camera = Camera(self.map.width)

    def update(self, dt):
        if self.paused:
            return
        self.fps = 1 / dt if abs(1 / dt - self.fps) > 5 else self.fps

        self.player.update(dt)
        if self.player.top < 0:
            self.over()

        # camera:
        self.camera.update(self.player)
        # print(self.camera.offset, self.player.mapx)
        self.camera.apply(self.player)
        for sprite in self.children:
            if not isinstance(sprite, Sprite):
                continue
            self.camera.apply(sprite)

        # collisions:
        self.player.is_touching["platform"] = False
        self.player.is_touching["rock"] = False
        self.player.is_grabbing = False
        # print("player mapx:%s, pos:%s" % (self.player.mapx, self.player.pos))
        # colissions:
        for sprite in self.children:
            # collision - platforms:
            if isinstance(sprite, Platform):
                # print(sprite, self.player, sprite == self.player)
                if self.player.collide_widget(sprite):
                    # print("collide")
                    if self.player.center_y < sprite.top:
                        continue
                    if self.player.vel.y <= 0:
                        self.player.y = sprite.top
                        self.player.is_touching["platform"] = True
            # collision - rocks:
            if isinstance(sprite, Rock):
                if self.player.collide_widget(sprite):
                    # print("collide with a rock")
                    dx1 = abs(self.player.right - sprite.x)
                    dx2 = abs(self.player.x - sprite.right)
                    dx = min(dx1, dx2)
                    dy1 = abs(self.player.top - sprite.y)
                    dy2 = abs(self.player.y - sprite.top)
                    dy = min(dy1, dy2)
                    if dx > dy:
                        # print("vertical", self.player.mapx, self.player.pos)
                        if dy1 < dy2:
                            self.player.top = sprite.y - 1
                            self.player.vel.y *= -1
                        elif dy1 > dy2:
                            self.player.y = sprite.top
                            self.player.vel = Vector(0, 0)
                            self.player.is_touching["rock"] = True
                    else:
                        # print("horizontal", self.player.mapx, self.player.pos)
                        if dx1 < dx2:
                            # print("player collide to the right")
                            self.player.mapx = -self.player.width + sprite.mapx
                            self.player.vel = Vector(0, 0)
                            self.player.is_touching["rock"] = True
                            self.player.is_grabbing = True
                        elif dx1 > dx2:
                            # print("player collide to the left")
                            self.player.mapx = sprite.mapx + sprite.width
                            self.player.vel = Vector(0, 0)
                            self.player.is_touching["rock"] = True
                            self.player.is_grabbing = True
            # collision - coins:
            if isinstance(sprite, Coin):
                if self.player.collide_widget(sprite):
                    print("coin", self.gold)
                    self.gold += 1
                    self.remove_widget(sprite)
                    print("coin", self.gold)
            # collision - flag:
            if isinstance(sprite, Flag):
                if self.player.collide_widget(sprite):
                    print("WIN")
                    self.win = 1
                    self.over()

        # print("player mapx:%s, pos:%s" % (self.player.mapx, self.player.pos))

    def over(self):
        self.paused = True
        self.player.is_walking = False
        self.button_over.opacity = 1
        self.button_over.disabled = 0
        if self.win:
            self.label_over.text = "YOU WIN"
            self.button_over.text = "next level"
        else:
            self.label_over.text = "GAME OVER"
            self.button_over.text = "Restart"

    def clean_all_sprites(self):
        print("clean_all_sprites")
        for sprite in self.children.copy():
            if not isinstance(sprite, Sprite) or sprite == self.player:
                continue
            self.remove_widget(sprite)
        self.label_over.text = ""

class MetaGame(ScreenManager):
    maps = kp.ListProperty(GAME.get("maps"))
    level = kp.NumericProperty(1)
    # def __init__(self, **kwargs):
    #     super().__init__()

    def start_a_game(self):
        self.current = "game_screen"
        self.game.new(self.maps[0])
        Clock.schedule_interval(self.game.update, 1 / GAME.get("fps", 60))

    def new_game(self):
        if self.game.win:
            self.level += 1
        if len(self.maps) >= self.level:
            map_name = self.maps[self.level - 1]
            self.game.new(map_name)
        else:
            self.game.label_over.text = "YOU END THE GAME!!!"
            self.game.button_over.opacity = 0
            self.game.button_over.disabled = 1
            self.game.win = 0



class GameApp(App):
    width = kp.NumericProperty(Window.width)
    height = kp.NumericProperty(Window.height)
    
    def build(self):
        self.meta_game = MetaGame()
        return self.meta_game

if __name__ == "__main__":
    GameApp().run()