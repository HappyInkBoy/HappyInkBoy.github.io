import pyglet

FRAME_RATE = 60
WIDTH = 1200
HEIGHT = 750

CENTER = pyglet.math.Vec2(WIDTH, HEIGHT)

# Due to pyglet's handling of retina screen on mac, the width and height are doubled for the window object.
WINDOW = pyglet.window.Window(width=WIDTH, height=HEIGHT)