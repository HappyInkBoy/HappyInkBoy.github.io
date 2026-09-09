import math
from typing import List
import pyglet
from pyglet.clock import schedule_once, schedule_interval_for_duration
import testCurveAnimations
import testCurveAnimations2
from settings import *



@WINDOW.event
def on_draw():
	WINDOW.clear()

	testCurveAnimations2.BACKGROUND_BATCH.draw()
	testCurveAnimations2.BATCH.draw()

# ––––– #
# Main: #
# ––––– #

# DO THE LAMBDA THING FOR AVOIDING TO MAKE A startCurve2 method

schedule_interval_for_duration(testCurveAnimations2.updateTestCurve1, 1/FRAME_RATE, 2.0)

pyglet.app.run()