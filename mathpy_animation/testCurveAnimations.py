import math
import pyglet
from pyglet.math import Vec2, Vec3
import listMethods
import customShapes as CS
from animationFunctions import smoothStep
from settings import *
from DrawableClass import Drawable2D
from ParametricFunction import ParametricFunction2D


# –––––––––––––––– #
# Global Variables #
# –––––––––––––––– #

ZERO_VECTOR = Vec2()

# –––––––––– #
# Parameters #
# –––––––––– #

animationParameters1 = [0, 0]



control_points = [
	Vec2(100,400),
	Vec2(300,400),
	Vec2(600,400),
	Vec2(500,0),
	Vec2(400,400),
	Vec2(700,400),
	Vec2(900,400)
]

#control_points2 = listMethods.displacePointsReturn(Vec2(500,100),control_points)

#curve_points = CS.createPointsFromParametric(CS.generalBezierCurve, steps=100, controlPoints=control_points)
#lines1 = pyglet.shapes.MultiLine(*curve_points)

# Creating the drawable objects
functionForParametricStep1 = lambda t, animParams: Vec2(20*t, 20*t**2).rotate(animParams[0])
functionForParametricStep2 = lambda t, animParams: functionForParametricStep1(t, animParams).lerp(ZERO_VECTOR, animParams[1])
parametricFunction1 = ParametricFunction2D(functionForParametricStep2, animationParameters=animationParameters1)


originalPos = ZERO_VECTOR

line1 = Drawable2D(center=CENTER, parametricFunction=parametricFunction1, position=originalPos, start=-5, end=5, color=[100,100,0,255])
destination = Vec2(200,150)

# ––––––––––––––––– #
# Updater Functions #
# ––––––––––––––––– #

def updateTestCurve1(dt):
	global line1, animationParameters1
	animationParameters1[0] += 0.5*dt

	newPos = (originalPos).lerp(other=(destination), amount=smoothStep(animationParameters1[0]))

	line1.setPosition(newPos)

	"""
	new_control_points = [control_points[i].lerp(other=control_points2[i], amount=smoothStep(t)) for i in range(len(control_points))]

	curve_points = CS.createPointsFromParametric(CS.generalBezierCurve, steps=100, controlPoints=new_control_points)
	lines1 = pyglet.shapes.MultiLine(*curve_points)
	"""

def updateTestCurve2(dt):
	global line1, animationParameters1

	animationParameters1[1] += 0.25*dt

	newPos = (destination).lerp(other=ZERO_VECTOR, amount=smoothStep(animationParameters1[1]))
	line1.setPosition(newPos)
