import math
import pyglet
from pyglet.math import Vec2, Vec3
import listMethods
import customShapes as CS
import vectorFunctions as VF
from animationFunctions import smoothStep
from settings import *
from DrawableClass import Drawable2D, Drawable4PointBezierCurve2D
from ParametricFunction import ParametricFunction2D, BezierCurve4Point2D, BezierCurve4Point2DParametricFunction
from DrawableGradients import DrawableCircleGradient

# –––––––––––––––– #
# Global Variables #
# –––––––––––––––– #

ZERO_VECTOR = Vec2()
BATCH = pyglet.graphics.Batch() # Each animation file should come with its own batches. This will allow you to better manage individual animations and drawing batches of different animation files in the main.py

# –––––––––– #
# Parameters #
# –––––––––– #

animationParameters1 = [0, 0]



eye_control_points = [
	Vec2(200,0),
	Vec2(100,-175),
	Vec2(-100,-175),
	Vec2(-200,0),
	Vec2(-100,175),
	Vec2(100,175),
	Vec2(200,0)
]

# Creating the drawable objects

bc1 = BezierCurve4Point2D(controlPoints=eye_control_points)
#parametricFunction1 = lambda t, animParams: bc1.evaluate(t).rotate(math.tau * smoothStep(animParams[0]))
#line1 = Drawable4PointBezierCurve2D(CENTER, BezierCurve4Point2DParametricFunction(bc1, parametricFunction1, animationParameters1), start=0, end=2.0, batch=BATCH)
line1 = Drawable4PointBezierCurve2D(BezierCurve4Point2DParametricFunction(bc1), start=0, end=2.0, batch=BATCH)

circles1 = DrawableCircleGradient(center=CENTER, initialRadius=10, finalRadius=50, numberOfShapes=15, batch=BATCH)
circles1.setColorGradientFrom2ColorsHSV(colorOuter=[10,1,0.75], colorInner=[70,0,1], spread=1.1)
circles1.setOpacity(0)



# ––––––––––––––––– #
# Updater Functions #
# ––––––––––––––––– #

def updateTestCurve1(dt):
	global line1, animationParameters1, eye_control_points
	animationParameters1[0] += 0.5*dt
	smoothParam0 = smoothStep(animationParameters1[0])

	eye_control_points[1] = Vec2(100,-175 + (1-smoothParam0)*(175))
	eye_control_points[2] = Vec2(-100,-175 + (1-smoothParam0)*(175))
	eye_control_points[4] = Vec2(-100,175 + (1-smoothParam0)*(-175))
	eye_control_points[5] = Vec2(100,175 + (1-smoothParam0)*(-175))

	line1.setControlPoints(eye_control_points)
	line1.setOpacity(255*(smoothParam0**0.5))
	line1.updateDrawing()

	circles1.setOpacity(0.2*255*(animationParameters1[0]**3))
	circles1.updateDrawings()



