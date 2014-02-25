from collections import *
import pyglet
from pyglet.window import key
import lgames
import xml.etree.ElementTree as ET
import lgames.ltatm.uis

Point = namedtuple('Point', ['x', 'y'], verbose=False)

class Direction:
    Left = 0
    Up = 1
    Right = 2
    Down = 3

class LTATMHandler(lgames.GameHandler):
    def __init__(self, level = 0):
        self.load_assets()
        self.load_levels()
        self.reset_to_zero(level)

    def on_draw(self, window):
        lgames.mainWindow.set_caption('TATM game')

        level = self.levels.__getitem__(self.level)
        self.calculate_level_data(level)
        if level is not None:
            self.draw_grid(level)
            self.draw_image(self.asset_exit, level.exit.x, level.exit.y, self.xsize, self.ysize)
            self.draw_image(self.asset_minotaur, self.cminotaur.x, self.cminotaur.y, self.xsize, self.ysize)

            if self.sleep_status > 60:
                if self.sleep_status % 30 >= 15:
                    self.draw_image(self.asset_theseus_sleeping2, self.ctheseus.x, self.ctheseus.y, self.xsize, self.ysize)
                else:
                    self.draw_image(self.asset_theseus_sleeping, self.ctheseus.x, self.ctheseus.y, self.xsize, self.ysize)
            else:
                self.draw_image(self.asset_theseus_awake, self.ctheseus.x, self.ctheseus.y, self.xsize, self.ysize)

        self.sleep_status += 1

    def on_key_press(self, window, symbol, modifiers):
        level = self.levels.__getitem__(self.level)

        # handle move theseus
        if symbol == key.LEFT:
            self.handle_theseus_move(Direction.Left)
        elif symbol == key.RIGHT:
            self.handle_theseus_move(Direction.Right)
        elif symbol == key.UP:
            self.handle_theseus_move(Direction.Up)
        elif symbol == key.DOWN:
            self.handle_theseus_move(Direction.Down)
        elif symbol == key.R:
            self.reset_to_zero(self.level)
            return
        elif symbol != key.SPACE:
            return

        if self.ctheseus.x == level.exit.x and self.ctheseus.y == level.exit.y:
            self.level += 1
            self.next_level(self.levels.__getitem__(self.level))
        else:
            self.handle_minotaur_move()
            self.handle_minotaur_move()

            if self.ctheseus == self.cminotaur:
                lgames.gameHandler = lgames.ltatm.uis.deadHandler

        self.sleep_status = 0

    def load_assets(self):
        self.asset_exit = pyglet.resource.image('assets/Exit.png')
        self.asset_minotaur = pyglet.resource.image('assets/Minotaur.png')
        self.asset_theseus_awake = pyglet.resource.image('assets/Theseus_Awake.png')
        self.asset_theseus_sleeping = pyglet.resource.image('assets/Theseus_Sleeping.png')
        self.asset_theseus_sleeping2 = pyglet.resource.image('assets/Theseus_Sleeping2.png')
        self.asset_playable_grid = pyglet.resource.image('assets/PlayableGrid.png')

    def load_levels(self):
        self.levels = UserList()

        tree = ET.parse('assets/levels.xml')
        root = tree.getroot()

        for child in root:
            if child.tag == 'level':
                level = Level()

                for child2 in child:
                    if child2.tag == "theseus":
                        level.theseus = Point(int(child2.get('x')), int(child2.get('y')))

                    if child2.tag == "minotaur":
                        level.minotaur = Point(int(child2.get('x')), int(child2.get('y')))

                    if child2.tag == "exit":
                        level.exit = Point(int(child2.get('x')), int(child2.get('y')))


                    if child2.tag == "cells":
                        level.cells = Point(int(child2.get('x')), int(child2.get('y')))

                    if child2.tag == "walls":
                        for child3 in child2:

                            if child3.tag == 'right':
                                level.right_walls.append(Point( int(child3.get('x')), int(child3.get('y')) ))

                            if child3.tag == 'bottom':
                                level.bottom_walls.append(Point( int(child3.get('x')), int(child3.get('y')) ))


                self.levels.append(level)

    def calculate_level_data(self, level):
        self.xsize = lgames.mainWindow.width / (level.cells.x + 1)
        self.ysize = lgames.mainWindow.height / (level.cells.y + 1)

        self.bxsize = self.xsize / level.cells.x
        self.bysize = self.ysize / level.cells.y

    def next_level(self, level):
        self.cminotaur = Point(level.minotaur.x, level.minotaur.y)
        self.ctheseus = Point(level.theseus.x, level.theseus.y)

    def draw_image(self, image, xcoord, ycoord, width, height, xdiff = 0, ydiff = 0):
        image.blit(((xcoord * self.xsize) + (xcoord * self.bxsize) + (self.bxsize / 2)) + xdiff,
                   ((lgames.mainWindow.height - self.ysize) - ((ycoord * self.ysize) + (ycoord * self.bysize) + (self.bysize / 2))) - ydiff,
                    width=width, height=height)

    def handle_theseus_move(self, direction):
        if not self.is_wall(direction, self.ctheseus.x, self.ctheseus.y):
            if direction == Direction.Left:
                self.ctheseus = Point(self.ctheseus.x - 1, self.ctheseus.y)
            elif direction == Direction.Right:
                self.ctheseus = Point(self.ctheseus.x + 1, self.ctheseus.y)
            elif direction == Direction.Up:
                self.ctheseus = Point(self.ctheseus.x, self.ctheseus.y - 1)
            elif direction == Direction.Down:
                self.ctheseus = Point(self.ctheseus.x, self.ctheseus.y + 1)

    def is_wall(self, direction, xpos, ypos):
        level = self.levels.__getitem__(self.level)

        if direction == Direction.Down:
            for wall in level.bottom_walls:
                if wall.x == xpos and wall.y == ypos:
                    return True
            if ypos + 1 >= level.cells.y:
                return True

        if direction == Direction.Up:
            for wall in level.bottom_walls:
                if wall.x == xpos and wall.y == ypos - 1:
                    return True
            if ypos <= 0:
                return True

        if direction == Direction.Left:
            for wall in level.right_walls:
                if wall.x == xpos - 1 and wall.y == ypos:
                    return True
            if xpos <= 0:
                return True

        if direction == Direction.Right:
            for wall in level.right_walls:
                if wall.x == xpos and wall.y == ypos:
                    return True
            if xpos + 1 >= level.cells.x:
                return True


        return False

    def draw_grid(self, level):
        for cellx in range(0, level.cells.x):
            for celly in range(0, level.cells.y):
                if self.is_wall(Direction.Down, cellx, celly) and self.is_wall(Direction.Up, cellx, celly) and self.is_wall(
                        Direction.Right, cellx, celly) and self.is_wall(Direction.Left, cellx, celly):
                    pass
                else:
                    self.draw_image(self.asset_playable_grid, cellx, celly, self.xsize, self.ysize)
                    if not self.is_wall(Direction.Down, cellx, celly):
                        self.draw_image(self.asset_playable_grid, cellx, celly, self.xsize, self.bysize, ydiff=self.bysize)
                    if not self.is_wall(Direction.Right, cellx, celly):
                        self.draw_image(self.asset_playable_grid, cellx, celly, self.bxsize, self.ysize, xdiff=self.xsize)

    def handle_minotaur_move(self):
        if self.ctheseus.x < self.cminotaur.x:
            if not self.is_wall(Direction.Left, self.cminotaur.x, self.cminotaur.y):
                self.cminotaur = Point(self.cminotaur.x - 1, self.cminotaur.y)
                return

        if self.ctheseus.x > self.cminotaur.x:
            if not self.is_wall(Direction.Right, self.cminotaur.x, self.cminotaur.y):
                self.cminotaur = Point(self.cminotaur.x + 1, self.cminotaur.y)
                return

        if self.ctheseus.y < self.cminotaur.y:
            if not self.is_wall(Direction.Up, self.cminotaur.x, self.cminotaur.y):
                self.cminotaur = Point(self.cminotaur.x, self.cminotaur.y - 1)
                return

        if self.ctheseus.y > self.cminotaur.y:
            if not self.is_wall(Direction.Down, self.cminotaur.x, self.cminotaur.y):
                self.cminotaur = Point(self.cminotaur.x, self.cminotaur.y + 1)
                return

    def reset_to_zero(self, level=0):
        self.level = level
        self.next_level(self.levels.__getitem__(self.level))
        self.sleep_status = 0

class Level:
    def __init__(self):
        self.theseus = Point(None, None)
        self.minotaur = Point(None, None)
        self.exit = Point(None, None)
        self.cells = Point(None, None)
        self.right_walls = UserList()
        self.bottom_walls = UserList()

playableGameHandler = LTATMHandler()