import pyglet
import listMethods
import math
import colorFunctions
import customShapes as CS
from typing import List, Callable
from pyglet.math import Vec2, Vec3
from settings import *
from abc import ABC, abstractmethod

class DrawableGradient(ABC):

	def __init__(self, center: Vec2 = CENTER, position: Vec2 = Vec2(), numberOfShapes: int = 10, gradientOfColors: List[List[int]] | None = None, batch: pyglet.graphics.Batch = None, group: pyglet.graphics.Group = None):
		self.center = center
		self.position = position
		self.numberOfShapes = numberOfShapes

		if gradientOfColors == None:
			self.gradientOfColors = [[255,255,255,255] for i in range(numberOfShapes)]
		else:
			self.gradientOfColors = gradientOfColors
		self.batch = batch
		self.group = group
		

	def setPosition(self, newPosition: Vec2):
		self.position = newPosition

	def setGradientOfColorsRGBA(self, newGradientOfColors: List[List[int]]):
		"""
		Sets a new gradientOfColors list (in RGBA format)
		"""
		self.gradientOfColors = newGradientOfColors

	def setColorGradientFrom2ColorsHSV(self, color0: List[int | float], color1: List[int | float], spread: float = 1.0) -> None:
		"""
		Takes two lists of HSV values and sets the colorGradient to be a list containing self.numberOfShapes number of RGB values that form a gradient from colorOuterHSV to colorInnerHSV
		Arguments:
			colorOuterHSV (List[int | float]): Starting color of the gradient (in HSV format)
			colorInnerHSV (List[int | float]): Ending color of the gradient (in HSV format)
			spread (float): spread values > 1 will make the color change more dense in the start. spread values < 1 will make the color change more dense in the end.
		"""

		newColorGradient = colorFunctions.colorGradientHSV(color0, color1, self.numberOfShapes, spread)

		for i in range(len(self.gradientOfColors)):
			for j in range(3):
				self.gradientOfColors[i][j] = newColorGradient[i][j]

	def setColorGradientFrom2ColorsRGB(self, color0: List[int | float], color1: List[int | float], spread: float = 1.0) -> None:
		"""
		Takes two lists of RGB values and sets the colorGradient to be a list containing self.numberOfShapes number of RGB values that form a gradient from colorOuterRGB to colorInnerRGB
		Arguments:
			colorOuterHSV (List[int | float]): Starting color of the gradient (in RGB format)
			colorInnerHSV (List[int | float]): Ending color of the gradient (in RGB format)
			spread (float): spread values > 1 will make the color change more dense in the start. spread values < 1 will make the color change more dense in the end.
		"""

		newColorGradient = colorFunctions.colorGradientRGB(color0, color1, self.numberOfShapes, spread)

		for i in range(len(self.gradientOfColors)):
			for j in range(3):
				self.gradientOfColors[i][j] = newColorGradient[i][j]

	def setOpacity(self, opacityValue: int | float) -> None:
		for i in range(self.numberOfShapes):
			self.gradientOfColors[i][3] = round(opacityValue)

	def setOpacityGradientFrom2Values(self, opacity1: int | float, opacity2: int | float, spread: float = 1.0) -> None:
		"""
		Takes two opacity values and makes a gradient from them.
		Opacity ranges from 0 to 255

		spread (float): spread values > 1 will make the opacity change more dense in the start. spread values < 1 will make the opacity change more dense in the end.
		"""

		for i in range(self.numberOfShapes):
			t = (i/self.numberOfShapes)**spread
			intermediateOpacity = opacity1 + t*(opacity2-opacity1)
			self.gradientOfColors[i][3] = intermediateOpacity


	@abstractmethod
	def _calculateDrawings(self) -> List[pyglet.shapes.ShapeBase]:
		pass 

	@abstractmethod
	def updateDrawings(self) -> None:
		pass
	


class DrawableCircleGradient(DrawableGradient):

	def __init__(self, center: Vec2 = CENTER, position: Vec2 = Vec2(), initialRadius: float = 0, finalRadius: float = 1.0, numberOfShapes: int = 10, radiusSpread: float = 1.0, gradientOfColors: List[List[int]] | None = None, batch: pyglet.graphics.Batch = None, group: pyglet.graphics.Group = None):
		super().__init__(center, position, numberOfShapes, gradientOfColors, batch, group)

		self.initialRadius = initialRadius
		self.finalRadius = finalRadius
		self.radiusSpread = radiusSpread

	def setColorGradientFrom2ColorsRGB(self, colorOuter: List[int | float], colorInner: List[int | float], spread: float = 1.0) -> None:
		super().setColorGradientFrom2ColorsRGB(color0=colorOuter, color1=colorInner, spread=spread)

	def setColorGradientFrom2ColorsHSV(self, colorOuter: List[int | float], colorInner: List[int | float], spread: float = 1.0) -> None:
		super().setColorGradientFrom2ColorsHSV(color0=colorOuter, color1=colorInner, spread=spread)

	def _calculateDrawings(self) -> List[pyglet.shapes.Circle]:
		"""
		Recalculates and returns the Circle objects
		"""

		absolutePosition = self.center + self.position

		newCirclesList = []

		for i in range(self.numberOfShapes):
			t = (i/self.numberOfShapes)**self.radiusSpread
			intermediateRadius = self.finalRadius + t*(self.initialRadius - self.finalRadius)

			newCirclesList.append(pyglet.shapes.Circle(x=absolutePosition[0], y=absolutePosition[1], radius=intermediateRadius, color=self.gradientOfColors[i], batch=self.batch))

		return newCirclesList

	def updateDrawings(self) -> None:
		self.circlesList = self._calculateDrawings()

class DrawableRectangleGradient(DrawableGradient):

	def __init__(self, center = CENTER, bottomLeftPoint: Vec2 = Vec2(), width: int | float = 20, height: int | float = 20, numberOfShapes: int = 10, gradientOfColors: List[List[int]] | None = None, angle: float = 0, batch: pyglet.graphics.Batch = None, group: pyglet.graphics.Group = None):
		super().__init__(center = center, numberOfShapes = numberOfShapes, gradientOfColors = gradientOfColors, batch = batch)

		self.bottomLeftPoint = bottomLeftPoint
		self.width = width
		self.height = height
		self.angle = angle

	def _calculateDrawings(self) -> List[pyglet.shapes.Circle]:
		"""
		Recalculates and returns the rectangle objects.
		The polygons will be rotated by self.angle radians with the pivot point being the bottom left point
		"""

		newRectanglesList = []

		verticalChange = self.height/self.numberOfShapes
		rectangleWidth = self.width

		for i in range(self.numberOfShapes):
			currentBottomLeftPoint = self.bottomLeftPoint + (Vec2(0, i*verticalChange)).rotate(self.angle)
			currentBottomRightPoint = currentBottomLeftPoint + Vec2(rectangleWidth, 0).rotate(self.angle)
			currentTopRightPoint = currentBottomRightPoint + Vec2(0, i*verticalChange).rotate(self.angle)
			currentTopLeftPoint = currentTopRightPoint + Vec2(-rectangleWidth, 0).rotate(self.angle)

			newRectanglesList.append(pyglet.shapes.Polygon(currentBottomLeftPoint+self.center, currentBottomRightPoint+self.center, currentTopRightPoint+self.center, currentTopLeftPoint+self.center, color=self.gradientOfColors[i], batch=self.batch, group=self.group))

			#newRectanglesList.append(pyglet.shapes.Rectangle(x=currentBottomLeftPoint[0], y=currentBottomLeftPoint[1], width=rectangleWidth, height=verticalChange, color=self.gradientOfColors[i], batch=self.batch))

		return newRectanglesList

	def updateDrawings(self) -> None:
		self.rectanglesList = self._calculateDrawings()