from sys import exit

import east
import north
import south



def dead(why):

	print "game over, your loser!!!!!"
	exit(0)

def west():
	print """	Barly out of breath, you are facing the man.
	He is hovering, and there is reaking black fog from him
	Behind him is a little girl, she is scared.
	you can either run back or punsh the guy
	what do you do?"""
	
	ny_input = raw_input("> ")
	
	if ny_input == "punsh":
		print "You rescued the guy, the girl gave you a golden key"
		print "Well done, lets check out the north area of this city..."
	elif ny_input == "run back" or "run" or "flee":
		dead("game over, your loser!!!")		
		
	next = raw_input("> ")
	
	if next == "east":
		east.east()
	elif next == "south":
		south.south()
	elif next == "north":
		north.north()


