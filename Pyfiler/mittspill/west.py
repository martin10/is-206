from sys import exit

import east
import north
import west
import south

def dead(why):

	print "game over, your loser!!!!!"
	exit(0)

def west():
	print "Barly out of breath, you are facing the man."
	print "He is hovering, and there is reaking black fog from him"
	print "Behind him is a little girl, she is scared."
	print "you can either run back or punsh the guy"
	print "what do you do?"
	
	ny_input = raw_input("> ")
	
	if ny_input == "punsh":
		print "You rescued the guy, the girl gave you a golden key"
		print "Well done, lets check out the east area of this city..."
	elif ny_input == "run back" or "run" or "flee":
		dead("game over, your loser!!!")		
	else:
		print "I don't understand what you mean, you can either punsh or run."
		
	next = raw_input("> ")
	
	if next == "east":
		east.east()
	elif next == "south":
		south.south()
	elif next == "north":
		north.north()
	elif next == "west":
		west.west()	
	else: 
		print "You stumble around until you starve."

