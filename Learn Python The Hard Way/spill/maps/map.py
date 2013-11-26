from random import randint


class RoomError(Exception):
    pass

class Room(object):
	
    def __init__(self, name, description): #defining how many arguments init should take. 
        self.name = name # name, will be viewed at the top of the webpage		
        self.description = description # main story, which will be in the middle of the page
        self.paths = {}

    def go(self, direction):
        return self.paths.get(direction, None)

    def add_paths(self, paths):
        self.paths.update(paths)
        



#defining that central_corridor is a room, as well as the name
central_corridor = Room("Do you dare?", 
#description.
"""
Welcome to our humble town Rekssand.
Many years ago Oggie Boogie casted darkness ouver our city.
Within the darkness lies an evil power that makes the citizens insane. 
Help us get back our sunlight to rescue Rekssand!
Shut down your browser if you wish to cancel.		
Write go on, if you wish to start your journey.


    
                              /       /
                           .'<_.-._.'<
                          /           \      .^.
        ._               |  -+- -+-    |    (_|_)
     r- |\                \   /       /      // 
   /\ \\  :                \  -=-    /       \\
    `. \\.'           ___.__`..;._.-'---...  //
      ``\\      __.--"        `;'     __   `-.  
        /\\.--""      __.,              ""-.  ".
        ;=r    __.---"   | `__    __'   / .'  .'
        '=/\\""           \             .'  .'
            \\             |  __ __    /   |
             \\            |  -- --   //`'`'
              \\           |  -- --  ' | //
               \\          |    .      |// 


"""
)
                        
hovedrom = Room("Main Street",
"""		
You are standing in our main street, to your west you see man 
running. Run west after him. 
"""
)

west = Room("West",
"""
Barly out of breath, you are facing the man.
He is hovering, and there is reaking black fog from him
Behind him is a little girl, she is scared.
you can either run back or punsh the guy
what do you do?
     

"""
	
)
punsh = Room("You hit him hard!", 
"""
You killed the guy, the girl gave you a golden key
Well done, lets check out the north area of this city...

"""
)

north = Room("North", 
"""
There is a big door here. On the bottom of the door, there is another door. 
A small door, with a keyhole. Do you insert golden key or flee?

insert or flee? 

"""
)
castle = Room("Castle", 
"""
YES! We are inside the castle. 
What do we do now? We need to catch Oggie Boogie to rescue the city!!
There is a sylinder in front of you with som encrypted text...
Deccode it, and tell me the secret code, and then we will see what happens? 

Cryptic code: cHl0aG9u

Write hint if you need help! 
"""
)

hint = Room("Hint", 
"""
The code was cHl0aG9u it is Base64 encrypted, 
find an online convertor en decode the message and give it to me..
Be fast! 
"""
)

oggie = Room("Oggies dungeon",
"""
The code worked! A door opens to your left, 
it leeds down to Oggies dungeon! 
But we need a good weapon to beat him.
I think the weapon is in the SOURCE some where, go look for it!
"""
)

dungeon = Room("The dungeon",
"""
We got the weapon, now kill him!! KILL HIM!
            	
"""
)

win = Room("Finish",
"""
You rescued the city...Oggie is dead. Thanks for playing!
 
"""
)

#death message
generic_death = Room("death", "You died")

#error message, serves the same purpose as death. 
error = Room("I'm sorry", "you entered an invalid input. Farewell")

#Adding paths. Takes user input from html form and direct them to the right room. 
hovedrom.add_paths({
	'west': west,
	'north': north,
})

west.add_paths({
	'punsh': punsh,
	'run back': hovedrom,	
})
north.add_paths({
	'punsh': punsh,
	'west': west,
	'flee': generic_death,
	'insert': castle,
		
})
central_corridor.add_paths({
    'go on': hovedrom,
  
})
punsh.add_paths({
    'north': north,
    'dodge!': generic_death
   
})

castle.add_paths({
    'python': oggie,
    'hint': hint,
   
})

hint.add_paths({
	'python': oggie,
	'north': north,
	'west': west,
		
})
oggie.add_paths({
	'sword': dungeon,
		
})
dungeon.add_paths({
	'kill': win,
	
})

#Defines where the users starts, in this case it is at room central_corridor.
START = central_corridor