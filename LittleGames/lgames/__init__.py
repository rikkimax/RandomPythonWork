__author__ = 'rikki'
import pyglet


#
# public API
#
class GameHandler:

    def on_draw(self, window):
        pass
    def on_key_press(self, window, symbol, modifiers):
        pass
    def on_mouse_motion(self, window, x, y, dx, dy):
        pass
    def on_mouse_press(self, window, x, y, button, modifiers):
        pass

gameHandler = None
mainWindow = None

#
# private API
#

def start_window():
    global mainWindow
    mainWindow = pyglet.window.Window()

    @mainWindow.event
    def on_draw():
        mainWindow.clear()

        if gameHandler is not None:
            gameHandler.on_draw(mainWindow)

    @mainWindow.event
    def on_key_press(symbol, modifiers):
        if gameHandler is not None:
            gameHandler.on_key_press(mainWindow, symbol, modifiers)

    @mainWindow.event
    def on_mouse_motion(x, y, dx, dy):
        if gameHandler is not None:
            gameHandler.on_mouse_motion(mainWindow, x, y, dx, dy)

    @mainWindow.event
    def on_mouse_press(x, y, button, modifiers):
        if gameHandler is not None:
            gameHandler.on_mouse_press(mainWindow, x, y, button, modifiers)


    pyglet.app.run()

if __name__ == "__main__":
    raise Exception('Ok you can\'t run lgames package init file')