from pyglet.math import Vec2
import math

I = Vec2(0,1)

def conj(vector: Vec2) -> Vec2:
	# Complex Conjugate
	return Vec2(vector[0], -vector[1])

def cMul(vector1: Vec2, vector2: Vec2) -> Vec2:
	# Complex Multiplication
	return Vec2(vector1[0]*vector2[0] - vector1[1]*vector2[1], vector1[0]*vector2[1] + vector1[1]*vector2[0])

def cDiv(vector1: Vec2, vector2: Vec2) -> Vec2:
	# Complex Division
	numerator = cMul(vector1, conj(vector2))
	denominator = norm(vector2)

	return (1/denominator) * numerator

def norm(vector: Vec2) -> float:
	return math.sqrt(vector[0]**2 + vector[1]**2)

def arg(vector: Vec2) -> float:
	if (vector[1] >= 0) or (vector[1] < 0 and vector[0] > 0):
		return (math.pi/2) - math.atan2(vector[0], vector[1])
	else:
		return -1*(3*math.pi/2 + math.atan2(vector[0],vector[1]))

def cPow(vector: Vec2, exponent: float) -> Vec2:
	# Complex Powers

	return (norm(vector)**exponent) * cExp(exponent*arg(vector)*I)

def cPowToComplex(vector1: Vec2, vector2: Vec2) -> Vec2:
	# Complex number being raised to the power of another complex number

	return cExp(cMul(Vec2(math.log(norm(vector1)), arg(vector1)), vector2))
	

def cExp(vector: Vec2) -> Vec2:
	# Complex exponentiation (e^z)

	real = math.exp(vector[0]) * math.cos(vector[1])
	imag = math.exp(vector[0]) * math.sin(vector[1])

	return Vec2(real, imag)

def cLn(vector):
	# Complex Natural Logarithm

	return Vec2(math.log(norm(vector)), arg(vector))


def cSin(vector: Vec2) -> Vec2:
	# Complex Sine

	step1 = cExp(cMul(I,vector)) - cExp(cMul(-I,vector))

	return cMul((-(1/2)*I), step1)

def cCos(vector: Vec2) -> Vec2:
	# Complex Cosine

	step1 = cExp(cMul(I,vector)) + cExp(cMul(-I,vector))

	return (1/2)*step1

def cTan(vector: Vec2) -> Vec2:
	# Complex Tangent

	return cDiv(cSin(vector),cCos(vector))

# Testing in main

v1 = Vec2(1,1)
v2 = Vec2(2,4)