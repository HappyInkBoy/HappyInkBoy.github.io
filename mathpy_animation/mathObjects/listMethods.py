import pyglet
from typing import List
from pyglet.math import Vec2, Vec3

def listAddition(list1: List[Vec2], list2: List[Vec2]):
	newList = []
	for i in range(len(list1)):
		newList.append(list1[i] + list2[i])

	return newList

def displacePointsReturn(vector, givenList):
	new_vectors = []
	for i in range(len(givenList)):
		new_vectors.append(givenList[i] + vector)

	return new_vectors

def displacePointsModify(vector: Vec2 | Vec3, givenList: List[Vec2 | Vec2]):

	if type(vector) == Vec2:
		for i in range(len(givenList)):
			givenList[i] = Vec2(givenList[i][0] + vector[0], givenList[i][1] + vector[1])
	elif type(vector) == Vec3:
		for i in range(len(givenList)):
			givenList[i] = Vec3(givenList[i][0] + vector[0], givenList[i][1] + vector[1], givenList[i][2] + vector[2])