#Read the readme file if anything is confusing in this file
from sys import exit

import east
import north
import west
import south

def south():
	print """	This room is full of gold.  
	You need a little gold to buy a buss ticket to go further 
	How much do you take?"""
	
	next = raw_input("> ")
	if "0" in next or "1" in next:
		how_much = int(next)
	else: 
		dead("Man, learn to type a number.")
		
	if how_much < 50:
		print "Nice, you're not greedy, you win!"
		exit(0)
	else: 
		dead("You greedy bastard!")
