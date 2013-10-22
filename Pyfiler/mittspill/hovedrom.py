from sys import exit

import east
import north
import west
import south

		
def dead(why):

	print "You walk around until you die, goodbye sir!"
	exit(0)
	
def start():
	print """
		Welcome to our humble town Rekssand.
		Many years ago Oggie Boogie casted darkness ouver our city.
		Within the darkness lies an evil power that makes the citizens insane.
		Help us get back our sunlight to rescue Rekssand!
		Press CTRL-C to cancel		
		or ENTER if you wish to start your journey. """
	
	continiue = raw_input("> ")
	
	print """ 		You are standing in our main street, to your west you see man 
		running, you can also go east, north or south, which direction 
		do you take?"""
	
	next = raw_input("> ")
	
	if next == "east":
		east.get_winner()
	elif next == "south":
		south.south()
	elif next == "north":
		north.north()
	elif next == "west":
		west.west()	
	else: 
		dead("You walk around until you die, goodbye sir!")
		
start()