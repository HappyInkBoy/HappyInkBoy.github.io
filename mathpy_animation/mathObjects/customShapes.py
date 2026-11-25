from typing import List, Callable
import math
import pyglet
from pyglet.math import Vec2, Vec3, Vec4

def generalBezierCurve(t, controlPoints):
	x=0
	y=0
	for i in range(len(controlPoints)):
		x += math.comb(len(controlPoints)-1, i) * (1-t)**(len(controlPoints)-1-i) * t**i * (controlPoints[i][0])
		y += math.comb(len(controlPoints)-1, i) * (1-t)**(len(controlPoints)-1-i) * t**i * (controlPoints[i][1])

	return Vec2(x, y)

def _createVectorFromDimension(dimension):
	"""
	Helper function
	"""
	if dimension == 2:
		point = Vec2()
	elif dimension == 3:
		point = Vec3()
	elif dimension == 4:
		point = Vec4()

	return point

def _interpolateMorePointsFromParametric(parametricFunction: Callable[[float], Vec2 | Vec3], steps, start: float, end: float, controlPoints: List[Vec2 | Vec3]=None) -> List[Vec2] | List[Vec3]:
	# THIS FUNCTION SUCKS BECAUSE IT DOES NOT USE THE DERIVATIVE OF THE PARAMETRIC

	newCurvePoints = []
	distanceScaling = 10

	for i in range(steps):
		paramInitial = start + (i/steps)*(end-start)
		paramFinal = start + ((i+1)/steps)*(end-start)

		if controlPoints == None:
			startPoint = parametricFunction(paramInitial)
			nextPoint = parametricFunction(paramFinal)

			newCurvePoints.append(startPoint)

			distance = (nextPoint - startPoint).length()
			additionalSteps = int(distance//distanceScaling)

			for j in range(additionalSteps+1):
				paramIntermediate = paramInitial + (j/additionalSteps)*(paramFinal-paramInitial)
				newCurvePoints.append(parametricFunction(paramIntermediate))
		else:
			startPoint = parametricFunction(paramInitial, controlPoints)
			nextPoint = parametricFunction(paramFinal, controlPoints)

			newCurvePoints.append(startPoint)

			distance = (nextPoint - startPoint).length()
			additionalSteps = int(distance//distanceScaling)

			for j in range(additionalSteps+1):
				paramIntermediate = paramInitial + (j/additionalSteps)*(paramFinal-paramInitial)
				newCurvePoints.append(parametricFunction(paramIntermediate, controlPoints))

	return newCurvePoints




def createPointsFromParametric(parametricFunction: Callable[[float], Vec2 | Vec3], start: float = 0, end: float = 1, steps=100, furtherInterpolation=False, controlPoints=None) -> List[Vec2] | List[Vec3]:
	"""
	This function takes a parametric function and will generate steps amount 
	of points between the start and end parametric values

	In case parametricFunction is a Bezier Curve, then the user can provide control points.
	"""

	curvePoints = []

	if furtherInterpolation == False:
		for i in range(steps + 1):
			t = start + (i/steps)*(end-start)
			if controlPoints == None:
				point = parametricFunction(t)
			else:
				point = parametricFunction(t, controlPoints)
			curvePoints.append(point)
	elif furtherInterpolation == True:
		curvePoints = _interpolateMorePointsFromParametric(parametricFunction, steps, start, end, controlPoints)

	return curvePoints



	

		

		
