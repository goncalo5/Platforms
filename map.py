from kivy.core.window import Window


class Map(object):
    def __init__(self, filename, tilesize):
        self.filename = filename
        self.data = []
        with open(filename, "rt") as f:
            for line in f:
                # self.data.append(line.strip().split(","))
                self.data.append(line.strip())
    
        self.tilewidth = len(self.data[0])
        self.tilesize = tilesize
        self.width = self.tilewidth * self.tilesize


class Camera:
    def __init__(self, width):
        self.offset = 0
        self.width = width

    def update(self, target):
        x = -target.mapx + Window.width / 2
        # limit scrooling to map size:
        x = min(x, 0)  # left
        x = max(x, -(self.width - Window.width))  # right
        self.offset = x

    def apply(self, entity):
        # print("apply", entity, entity.x, entity.y, entity.mapx, entity.mapy)
        entity.x = entity.mapx + self.offset
