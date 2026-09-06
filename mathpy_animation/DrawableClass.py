import pyglet
import listMethods
import math
import colorFunctions
from typing import List, Callable
from pyglet.math import Vec2, Vec3
import customShapes as CS
from settings import *
from ParametricFunction import ParametricFunction2D, BezierCurve4Point2D, BezierCurve4Point2DParametricFunction

class Drawable2D:
	"""
	Creates an object that represents a drawable parametric curve.
	Attributes:
		center (Vec2): A vector that represents the center of the animation window.
		parametricFunction (Callable[[float], Vec2]): A parametric function which takes a float and returns a vector
		position (Vec2): A vector that displaces the Drawable2D object with respect to the center. By default, the object will be in the center.
		start (float): A float that represents the lower bound of the parametric function
		end (float): A float that represents the upper bound of the parametric function
		curvePoints (List[Vec2]): A list of the vectors that form the parametric curve
		steps (int): The number of points used to plot out the parametric curve
		color (List[int]): The RGBA values for the Drawable object
		width (float): The thickness of the multiline object
		batch (Batch): The batch that the calling object will be placed in
		lines (MultiLine): The MultiLine object to be drawn. This object will be stored in the Drawable2D object's instance
	"""
	

	def __init__(self, parametricFunction: ParametricFunction2D, center: Vec2 = CENTER, position: Vec2 = Vec2(), start: float = 0, end: float = 1, steps: int = 100, color: List[int] = [255, 255, 255, 255], width: float = 1, batch: pyglet.graphics.Batch = None):
		self.center = center
		self.parametricFunction = parametricFunction
		self.position = position
		self.start = start
		self.end = end
		self.curvePoints = []
		self.steps = steps
		self.color = color
		self.width = width
		self.batch = batch

		self.updateDrawing()

	def getParametricFunction(self) -> ParametricFunction2D:
		"""
		"""

		return self.parametricFunction

	def getWidth(self) -> float:
		return self.width

	def setWidth(self, newWidth: float) -> None:
		self.width = newWidth

	def getPosition(self) -> Vec2:
		"""
		Returns the position vector of this drawing object relative to the center vector
		"""

		return self.position

	def setPosition(self, newPosition: Vec2) -> None:
		"""
		Changes the position attribute to be newPosition
		"""

		self.position = newPosition

	def getCenter(self) -> Vec2:
		"""
		Returns the center vector of the drawing
		"""

		return self.center

	def setCenter(self, newCenter: Vec2) -> None:
		"""
		Changes the center vector of the drawing object
		"""

		self.center = newCenter

	def getAbsolutePosition(self) -> Vec2:
		"""
		Returns the actual position of the vector relative to the window's origin (the bottom left corner)
		"""

		return self.getPosition() + self.getCenter()

	def setAbsolutePosition(self, newAbsolutePosition: Vec2) -> None:
		"""
		Changes the position vector such that the drawing will be positioned at the newAbsolutePosition vector (relative to the window's coordinate system, whose origin is the bottom left corner)
		"""

		self.position = newAbsolutePosition - self.getCenter()

	def getColorRGB(self) -> List[int]:
		"""
		Returns the color list (length 3) and it does not include the alpha (opacity)
		"""

		return self.color[0:3]

	def setColorRGB(self, colorListRGB: List[int | float]) -> None:
		"""
		Sets the color attribute to the new colorList
		"""

		for i in range(3):
			self.color[i] = round(colorListRGB[i])

	def setColorHSV(self, colorListHSV: List[int | float]) -> None:
		"""
		Converts the given colorListHSV into RGB values and sets it as the new color

		Red = 255 on [0,60]U[300,360]
		Green = 255 on [60,180]
		Blue = 255 on [180,300]
		"""

		newRGB = colorFunctions.convertHSVtoRGB(colorListHSV)

		# Setting the new color

		for i in range(3):
			self.color[i] = newRGB[i]

	def getOpacity(self) -> int:
		"""
		Returns the alpha of the drawable object (opacity)
		"""

		return self.color[3]

	def setOpacity(self, newOpacity: int | float) -> None:
		"""
		Sets the alpha of the drawable object to newOpacity
		"""

		self.color[3] = round(newOpacity)

	def _calculateCurvePoints(self) -> None:
		"""
		Calculates the points that form the parametric curve
		"""

		points = self.parametricFunction.getNewCurvePoints(start=self.start, end=self.end, steps=self.steps)
		listMethods.displacePointsModify(self.getCenter() + self.getPosition(), points)

		self.curvePoints = points

	def _getCurvePoints(self) -> List[Vec2]:
		"""
		Returns the points that form the parametric curve
		"""

		return self.curvePoints

	def _calculateDrawing(self) -> pyglet.shapes.MultiLine:
		"""
		Recalculates and returns the multiline object produced the instance's parametric function
		"""

		self._calculateCurvePoints()
		lines = pyglet.shapes.MultiLine(*(self._getCurvePoints()), color=self.color, thickness=self.width, batch=self.batch)

		return lines

	def updateDrawing(self) -> None:

		self.lines = self._calculateDrawing()


# Make it so that the user is able to provide an optional parametric function (callable, not the object) which uses the BezierCurve4Point's evaluate() method along with some animation parameters
# You could also make a subclass of the parametricFunction2D class which contains a BezierCurve4Point2D object so that it can allow the user to provide animation parameters so that they can use the evaluate() method of the bezier curve and then apply additional functions onto it that use the animation parameters
# In truth, you just need to make a way for the Drawable4PointBezierCurve2D object to allow the user to provide a bezierCurve object and also possibly a function which uses the .evaluate() method of that bezierCurve object and takes animation parameters to then return a Vec2 object. Use whatever means necessary to do this. I need to go to sleep... ∫
class Drawable4PointBezierCurve2D(Drawable2D):

	def __init__(self, bezierCurveParametricFunction: BezierCurve4Point2DParametricFunction, center: Vec2 = CENTER, position: Vec2 = Vec2(), start: float = 0, end: float = 1, steps: int = 100, color: List[int] = [255, 255, 255, 255], width: float = 1.0, batch: pyglet.graphics.Batch = None):
		
		super().__init__(bezierCurveParametricFunction, center, position, start, end, steps, color, width, batch)

	def setControlPoints(self, newControlPoints: List[Vec2 | str]):

		self.parametricFunction.bezierCurve.setControlPoints(newControlPoints)




# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
# 0, 1, 2, 3, B, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
# How should I handle the 4-point bezier curves?
# Idea 1: Make a subclass of the ParametricFunction2D class to handle 4 point bezier curves
# It can have a helper method where it tries to break up the control points list into a 2d list of 4 point sequences
# If it sees a break, it will know to jump to the next point and restart the whole procedure.
# Then, the .evaluate() method of the bezier curve subclass of ParametricFunction2D can use the given parameter and identify which 4-point sequence to use (the floor(parameter) should give you the index of its corresponding 4-point sequence) and from there, you can use the CustomShapes' general bezier curve function and pass the 4-point sequence as its control points and then pass the parameter so that you can get the Vec2 from that curve and THEN you should be able to return that Vec2 in the .evaluate() method!
