from typing import List, Callable

def convertHSVtoRGB(colorListHSV: List[int | float]) -> List[int | float]:
	relativeHue = colorListHSV[0] % 60
	segment = int(colorListHSV[0] // 60)

	newRGB = [0,0,0]

	# Handling the Hue

	hueLerp = round((relativeHue/60)*255)

	match segment:
		case 0:
			newRGB[0] = 255
			newRGB[1] = hueLerp
		case 1:
			newRGB[0] = 255 - hueLerp
			newRGB[1] = 255
		case 2:
			newRGB[1] = 255
			newRGB[2] = hueLerp
		case 3:
			newRGB[1] = 255 - hueLerp
			newRGB[2] = 255
		case 4:
			newRGB[0] = hueLerp
			newRGB[2] = 255
		case 5:
			newRGB[0] = 255
			newRGB[2] = 255 - hueLerp
		case 6:
			newRGB[0] = 255

	# Handling the Saturation (lerping to 255)

	for i in range(3):
		newRGB[i] = newRGB[i] + round((1-colorListHSV[1]) * (255 - newRGB[i]))

	# Handling the Value (lerping to 0)

	for i in range(3):
		newRGB[i] = newRGB[i] + round((1-colorListHSV[2]) * (0 - newRGB[i]))

	return newRGB

def colorGradientHSV(color1HSV: List[int | float], color2HSV: List[int | float], steps: int, spread: float = 1.0) -> List[List[int]]:
	"""
	Takes two lists of HSV values and returns a list containing steps number of RGB values that form a gradient from color1HSV to color2HSV
	Arguments:
		color1HSV (List[int | float]): Starting color of the gradient (in HSV format)
		color2HSV (List[int | float]): Ending color of the gradient (in HSV format)
		steps (int): Number of intermediary colors in the gradient
		spread (float): spread values > 1 will make the color change more dense in the start. spread values < 1 will make the color change more dense in the end.
	"""

	colorGradientListRGB = []

	for i in range(steps):
		t = (i/steps)**spread
		intermediateHSV = [color1HSV[j] + (t)*(color2HSV[j]-color1HSV[j]) for j in range(3)]
		colorGradientListRGB.append(convertHSVtoRGB(intermediateHSV))

	return colorGradientListRGB

def colorGradientRGB(color1RGB: List[int | float], color2RGB: List[int | float], steps: int, spread: float = 1.0) -> List[List[int]]:
	"""
	Takes two lists of RGB values and returns a list containing steps number of RGB values that form a gradient from color1RGB to color2RGB
	Arguments:
		color1RGB (List[int | float]): Starting color of the gradient (in RGB format)
		color2RGB (List[int | float]): Ending color of the gradient (in RGB format)
		steps (int): Number of intermediary colors in the gradient
		spread (float): spread values > 1 will make the color change more dense in the start. spread values < 1 will make the color change more dense in the end.
	"""

	colorGradientListRGB = []
	
	for i in range(steps):
		t = (i/steps)**spread
		intermediateRGB = [color1RGB[j] + (t)*(color2RGB[j]-color1RGB[j]) for j in range(3)]
		colorGradientListRGB.append(intermediateRGB)

	return colorGradientListRGB