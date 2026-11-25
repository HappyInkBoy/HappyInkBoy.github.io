import pyglet
import math
from typing import List, Callable
from pyglet.math import Vec2, Vec3, Mat3


def project3DOnto2D(cameraPosition: Vec3, cameraDestination: Vec3, objectPoint: Vec3, projectionPlaneDistance: float = 0.5) -> Vec2:
	"""
	Projects the objectPoint vector onto the xy plane.
	"""

	# Defining the normal vector of the projection plane
	cameraDirection = (cameraDestination - cameraPosition).normalize()

	planeMidPoint = cameraPosition + projectionPlaneDistance*cameraDirection

	objectDifferenceVector = objectPoint - cameraPosition

	intersectionParameter = (cameraDirection.dot(planeMidPoint - cameraPosition))/(cameraDirection.dot(objectDifferenceVector))
	pointOfIntersection = cameraPosition + intersectionParameter*objectDifferenceVector

	# Defining the projected point relative to the mid point of the plane
	projectedObjectDifferenceVector = pointOfIntersection - planeMidPoint

	# Defining the basis vectors for the projection plane (will be used to undo the transformation)
	planeI = basisVectorI(cameraDirection)
	planeJ = basisVectorJ(cameraDirection, planeI)

	projectionPlaneMatrixList = []

	for i in range(3):
		projectionPlaneMatrixList.append(planeI[i])
		projectionPlaneMatrixList.append(planeJ[i])
		projectionPlaneMatrixList.append(cameraDirection[i])

	projectionPlaneMatrix = Mat3(*projectionPlaneMatrixList)

	# Computes the inverse of the matrix by computing the adjoint of the matrix
	m0 = planeJ[1]*cameraDirection[2]-cameraDirection[1]*planeJ[2]
	m1 = planeI[1]*cameraDirection[2]-cameraDirection[1]*planeI[2]
	m2 = planeI[1]*planeJ[2]-planeJ[1]*planeI[2]
	m3 = planeJ[0]*cameraDirection[2]-cameraDirection[0]*planeJ[2]
	m4 = planeI[0]*cameraDirection[2]-cameraDirection[0]*planeI[2]
	m5 = planeI[0]*planeJ[2]-planeJ[0]*planeI[2]
	m6 = planeJ[0]*cameraDirection[1]-cameraDirection[0]*planeJ[1]
	m7 = planeI[0]*cameraDirection[1]-cameraDirection[0]*planeI[1]
	m8 = planeI[0]*planeJ[1]-planeJ[0]*planeI[1]

	inverseProjectionMatrix = Mat3(m0,m1,m2,m3,m4,m5,m6,m7,m8)

	return inverseProjectionMatrix @ projectedObjectDifferenceVector
	




def basisVectorI(normalVector: Vec3) -> Vec3:
	vectorI = Vec3(1, 0, -(normalVector[0]/normalVector[2]))

	return vectorI.normalize()

def basisVectorJ(normalVector: Vec3, vectorI: Vec3) -> Vec3:
	vectorJ = normalVector.cross(vectorI)

	return vectorJ.normalize()

