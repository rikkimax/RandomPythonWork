import lgames
import pyglet
import lgames.ltatm.handler

class LTATMDeadHandler(lgames.GameHandler):
    def __init__(self):
        self.asset_tuffy = pyglet.font.add_file('assets/Tuffy.ttf')
        self.tuffy = pyglet.font.load('Tuffy')
        self.over_replay = False

    def on_draw(self, window):
        lgames.mainWindow.set_caption('TATM death screen')

        pyglet.text.Label('You died :(', font_name='Tuffy', font_size=24, x=lgames.mainWindow.width // 2,
                          y=lgames.mainWindow.height - (lgames.mainWindow.height // 4),
                          anchor_x='center', anchor_y='center').draw()

        if self.over_replay:
            pyglet.text.Label('Replay', font_name='Tuffy', font_size=16, x=lgames.mainWindow.width // 2,
                              y=lgames.mainWindow.height // 4, color=(226, 235, 59, 255),
                              anchor_x='center', anchor_y='center').draw()
        else:
            pyglet.text.Label('Replay', font_name='Tuffy', font_size=16, x=lgames.mainWindow.width // 2,
                              y=lgames.mainWindow.height // 4, color=(43, 171, 196, 255),
                              anchor_x='center', anchor_y='center').draw()

    def on_mouse_motion(self, window, x, y, dx, dy):
        self.over_replay = y < lgames.mainWindow.height // 3

    def on_mouse_press(self, window, x, y, button, modifiers):
        if self.over_replay:
            lgames.gameHandler = lgames.ltatm.handler.playableGameHandler
            lgames.ltatm.handler.playableGameHandler.reset_to_zero()


class LTATMIntroHandler(lgames.GameHandler):
    def __init__(self):
        self.asset_tuffy = pyglet.font.add_file('assets/Tuffy.ttf')
        self.tuffy = pyglet.font.load('Tuffy')
        self.over_play = False

    def on_draw(self, window):
        lgames.mainWindow.set_caption('Welcome to TATM game!')


        pyglet.text.Label('Lets play a game..', font_name='Tuffy', font_size=24, x=lgames.mainWindow.width // 2,
                          y=lgames.mainWindow.height - (lgames.mainWindow.height // 4),
                          anchor_x='center', anchor_y='center').draw()

        pyglet.text.Label('[left,right,up,down] arrow keys for moving Theseus', font_name='Tuffy', font_size=12, x=lgames.mainWindow.width // 2,
                          y=lgames.mainWindow.height - (lgames.mainWindow.height // 3) - 15,
                          anchor_x='center', anchor_y='center').draw()
        pyglet.text.Label('[space] to skip a turn', font_name='Tuffy', font_size=12,
                          x=lgames.mainWindow.width // 2,
                          y=lgames.mainWindow.height - (lgames.mainWindow.height // 3) - 30,
                          anchor_x='center', anchor_y='center').draw()
        pyglet.text.Label('[r] to restart the level', font_name='Tuffy', font_size=12,
                          x=lgames.mainWindow.width // 2,
                          y=lgames.mainWindow.height - (lgames.mainWindow.height // 3) - 45,
                          anchor_x='center', anchor_y='center').draw()

        if self.over_play:
            pyglet.text.Label('Go!', font_name='Tuffy', font_size=16, x=lgames.mainWindow.width // 2,
                              y=lgames.mainWindow.height // 4, color=(226, 235, 59, 255),
                              anchor_x='center', anchor_y='center').draw()
        else:
            pyglet.text.Label('Go', font_name='Tuffy', font_size=16, x=lgames.mainWindow.width // 2,
                              y=lgames.mainWindow.height // 4, color=(43, 171, 196, 255),
                              anchor_x='center', anchor_y='center').draw()

    def on_mouse_motion(self, window, x, y, dx, dy):
        self.over_play = y < lgames.mainWindow.height // 3

    def on_mouse_press(self, window, x, y, button, modifiers):
        if self.over_play:
            lgames.gameHandler = lgames.ltatm.handler.playableGameHandler
            lgames.ltatm.handler.playableGameHandler.reset_to_zero()

deadHandler = LTATMDeadHandler()
introHandler = LTATMIntroHandler()