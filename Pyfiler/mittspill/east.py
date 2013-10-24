# -*- coding: UTF-8 -*-

import west
import south
import north
import re
import string
import random 



def game():
    print '''\nScissor Rock Paper!!
Good Luck'''
    while True:
        try:
            maxpoeng = input('\nHow Many points to win the game?\n > ')
            break
        except:
            print 'Please, write a number....'
    poengs = 0
    poengc = 0
    valg = ['rock','scissor','paper']
    while poengs < maxpoeng and poengc < maxpoeng:
        forsok = raw_input('Which weapon do you choose? (rock, scissor, paper)\n> ').lower()
        if forsok == 'quit':
            quit()
        comp = random.choice(valg)
        if forsok == 'rock':
            if comp == 'rock':
                pass
            elif comp == 'scissor':
                poengs += 1
            elif comp == 'paper':
                poengc += 1
        elif forsok == 'scissor':
            if comp == 'rock':
                poengc += 1
            elif comp == 'scissor':
                pass
            elif comp == 'paper':
                poengs += 1
        elif forsok == 'paper':
            if comp == 'scissor':
                poengc += 1
            elif comp == 'rock':
                poengs += 1
            elif comp == 'paper':
                pass
        else:
            print 'You can only choose rock, scissor or paper\n'
            continue
        print '\n-------------------------------------------------'
        print 'You choose: %s  -  The computer choose: %s' % (forsok.capitalize(),comp)
        print 'The count is:'
        print '   ',poengs,'            ',poengc
        print '-------------------------------------------------\n'
 
    if poengs < poengc:
        res = 'You lost...'
    else:
        res = 'You won!'
    print 'Do you want to play again?'
    
    if raw_input('do '+res+' you want to play again').lower() in ('y,yes,ok'):
        steinsakspapir()
    else:
        south.south()

 