from sys import exit # from sys import exit. Exit is a fuction that exits the program when called
# Import my other files, which will be used as rooms for this game
import east
import north
import west
import south

		
def dead(why): #A function to exit the program, if the player dies

	print "You walk around until you die, goodbye sir!"
	exit(0)
	
def start():#My main function, automaticly started when the file "hovedrom" is called. 
	print """
		Welcome to our humble town Rekssand.
		Many years ago Oggie Boogie casted darkness ouver our city.
		Within the darkness lies an evil power that makes the citizens insane.
		Help us get back our sunlight to rescue Rekssand!
		Press CTRL-C to cancel		
		or ENTER if you wish to start your journey. """
	
	continiue = raw_input("> ") #Raw input from user, used to determin the next direction in the game
	
	print """ 		You are standing in our main street, to your west you see man 
		running, you can also go east, north or south, which direction 
		do you take?"""
	
	next = raw_input("> ")
	
	if next == "east": # if input from user is east, go to file east, rund function get_winner
		east.get_winner()
	elif next == "south":
		south.south()
	elif next == "north":
		north.north()
	elif next == "west":
		west.west()	
	elif next == "play":
		east.game()
	else: 
		dead("You walk around until you die, goodbye sir!")
		
start()
