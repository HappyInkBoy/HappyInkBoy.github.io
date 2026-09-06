import pyglet
from pyglet.math import Vec2, Vec3

"""
t*(1-(1-t)**2)+(1-t)*(t**2)
"""

def smoothStep(t: float) -> float:
  return t*(1-(1-t)**2)+(1-t)*(t**2)