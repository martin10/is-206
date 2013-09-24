from sys import exit

import east
import north
import west
import south

def north():
	print "There is a bear here."
	print "The bear has a bunch of honey."
	print "The fat bear is in front of another door."
	print "How are you going to move the bear?"
	bear_moved = False
	
	while True:
		next = raw_input("> ")
		
		if next == "take honey":
			dead("The bear looks at you then slaps your face off.")
		elif next == "taunt bear" and not bear_moved:
			print "The bear has moved from the door. You can go through."
			bear_moved = True
		elif next == "taunt bear" and bear_moved:
			dead("the bear gets pissed off and chews your leg off.")
		elif next == "open door" and bear_moved:
			south()
		else:
			print "I got no idea what that means."
			

			