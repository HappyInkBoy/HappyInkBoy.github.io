import pyglet
import listMethods
import math
from typing import List, Callable
from pyglet.math import Vec2, Vec3
import customShapes as CS

class ParametricFunction2D:
	"""
	Class representing a parametric function to be used for animating a Drawable object
	"""

	def __init__(self, function: Callable[[float, List[float] | None], Vec2], animationParameters: List[float] | None = None):
		self.function = function
		self.animationParameters = animationParameters

	def setFunction(self, newFunction: Callable[[float, List[float] | None], Vec2]) -> None:
		self.function = newFunction

	def evaluate(self, parameter: float) -> Vec2:
		"""
		Calls the object's parametric at some parameter (and passes along the animationParameters) and returns the Vec2 object from the parametric function.
		"""

		if self.animationParameters == None:
			return self.function(parameter)
		else: # THIS ASSUMES THAT animationParameters is a List of floats
			return self.function(parameter, self.animationParameters)

	def getNewCurvePoints(self, start: float, end: float, steps: int = 100) -> List[Vec2]:
		"""
		Uses the .evaluate() method to create a list of Vec2 objects 
		that trace the parametric function from the start parameter to the end parameter
		"""

		curvePoints = []

		for i in range(steps + 1):
			t = start + (i/steps)*(end-start)

			curvePoints.append(self.evaluate(t))

		return curvePoints

class BezierCurve4Point2D:

	def __init__(self, controlPoints: List[Vec2 | str]):
		self.setControlPoints(controlPoints)

	def setControlPoints(self, controlPoints: List[Vec2 | str]) -> None:
		self.controlPointsList = BezierCurve4Point2D.create4PointSequences(controlPoints)

	@staticmethod
	def create4PointSequences(controlPoints: List[Vec2 | str]) -> List[List[Vec2]]:
		"""
		Breaks up the controlPoints list into several lists of length 4 containing control points
		"""

		newSegmentedControlPoints = []

		breakListIndicator = "B"

		relative4PointIndex = 0

		numBreaks = 0
		for i in range(len(controlPoints)):
			if controlPoints[i] == breakListIndicator:
				numBreaks += 1

		for i in range(len(controlPoints)-1-numBreaks):

			controlPointSequence = []

			if ((i < (len(controlPoints) - 1)) and (controlPoints[i+1] == breakListIndicator)) or (controlPoints[i] == breakListIndicator):
				relative4PointIndex = 0
				continue
			if (relative4PointIndex % 3) != 0: # Makes sure that the nested for loop only gets executed iff i is at the index of the start of a sequence to form a 4 point bezier curve
				relative4PointIndex += 1
				continue
			for j in range(i, i + 4):
				controlPointSequence.append(controlPoints[j])

			newSegmentedControlPoints.append(controlPointSequence)
			relative4PointIndex += 1

		return newSegmentedControlPoints

	def evaluate(self, parameter: float):
		"""
		parameter ranges from 0 to the length of the controlPointsList attribute
		"""

		if (parameter > 0) and (parameter < len(self.controlPointsList)):
			currentControlPoints = self.controlPointsList[math.ceil(parameter) - 1]
		elif parameter >= len(self.controlPointsList):
			currentControlPoints = self.controlPointsList[-1]
		else:
			currentControlPoints = self.controlPointsList[0]

		relativeParameter = parameter % 1
		if (parameter == math.floor(parameter)) and (parameter != 0):
			"""
			This is done because if the parameter is the last possible value for the bezier curve, it will end up being modulo'd to 0 and
			then it be evaluating it at the start of the bezier curve of the last controlPoint list (when we want it to be at the END of that bezier curve) 
			"""
			relativeParameter = 1


		return CS.generalBezierCurve(relativeParameter, controlPoints = currentControlPoints)

class BezierCurve4Point2DParametricFunction(ParametricFunction2D):

	def __init__(self, bezierCurve: BezierCurve4Point2D, animationFunction: Callable[[float | List[float]], Vec2] | None = None, animationParameters = None):

		self.bezierCurve = bezierCurve
		self.function = animationFunction
		self.animationParameters = animationParameters

	def evaluate(self, parameter):

		"""
		if self.animationParameters == None:
			return self.bezierCurve.evaluate(parameter)
		else: # THIS ASSUMES THAT animationParameters is a List of floats
			return self.function(parameter, self.animationParameters)
		"""

		if self.animationParameters == None:
			return self.bezierCurve.evaluate(parameter)
		else: # THIS ASSUMES THAT animationParameters is a List of floats
			return self.function(parameter, self.animationParameters)

	def getNewCurvePoints(self, start, end, steps = 100):
		return super().getNewCurvePoints(start, end, steps)

# TESTING:

"""
l1 = [
	Vec2(0,0),
	Vec2(10,10),
	Vec2(20,20),
	Vec2(30,30),
	Vec2(40,40),
	Vec2(50,50),
	Vec2(60,60),
	"B",
	Vec2(70,70),
	Vec2(80,80),
	Vec2(90,90),
	Vec2(100,100),
	Vec2(110,110),
	Vec2(120,120),
	Vec2(130,130),
	"B",
	Vec2(140,140),
	Vec2(150,150),
	Vec2(160,160),
	Vec2(170,170)
]

b1 = BezierCurve4Point2D(l1)

for i in range(20):
	print(i, b1.evaluate(i/4))
"""