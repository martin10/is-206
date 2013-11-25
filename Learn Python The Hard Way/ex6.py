# -- coding: utf-8 --
#Telling a joke. 
x = "There are %d types of people." % 10
binary = "binary"
do_not = "don't"
y = "Those who know %s and those who %s." % (binary, do_not)

#printing the joke with variables. 
print x
print y

#printing it seperatly, with new variables.
print "I said: %r." % x
print "I also said: '%s" % y

#Confirming that this joke is lame ;) 
hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

print joke_evaluation % hilarious 

w = "this is the left side of..."
e = " a string with right side."

#Adding two strings. Printing them as one. 
print w + e 
