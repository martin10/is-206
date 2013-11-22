# -- coding: utf-8 --
#If you do not speak norwegian, try copying this script into google translate. 
from sys import argv

script, filename = argv

print "Nå skal vi slette filinnholdet i %r." % filename
print "Hvis ikke du vil det trykk CTRL-C."
print "Hvis du tørr gå videre trykk ENTER."

raw_input("?")

print "Åpner filen...."
target = open(filename, "w")

print "Tømmer filen..."
target.truncate()

print "Nå vil jeg at vi skriver noe morsomt i filen, jeg ber deg om 3 settninger"

line1 = raw_input("Linje 1: ")
line2 = raw_input("linje 2: ")
line3 = raw_input("linje 3: ")

print "FLOTT! Nå skal vi skrive dette inn i filen"

target.write(line1)
target.write("\n")
target.write(line2)
target.write("\n")
target.write(line3)
target.write("\n")

print "Da var det gjort, sjekk filen på skrivebordet"
target.close()
