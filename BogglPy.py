# -*- coding: utf-8 -*-
"""
Creates a boggle-inspired boggle game.


Created on Mon Jun  1 21:42:44 2020

@author: Birk Fritsch
"""

from random import shuffle, randint
from itertools import zip_longest
from time import sleep



def grouper(iterable, n, fillvalue=' '):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)



def make_board():
    """
    Prints a random 4x4 boggle board in the console. 

    Returns
    -------
    None.

    """
    #shuffle dices
    shuffle(dices)
    #create random board
    for dice_row in grouper(dices, 4):
        row = [dice_dct[i][randint(0,5)]+'  ' for i in dice_row]
        #adjust spacing
        row = [_adjust_spacing(r, letter='Qu') for r in row]
        
        #print board
        print(*row)
        print('')
    
    
 
def _adjust_spacing(row, letter='Qu'):
    """
    Adjusts the amount of spaces for letters longer than a single sign.

    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    letter : TYPE, optional
        DESCRIPTION. The default is 'Qu'.

    Returns
    -------
    row : str

    """
    #get length of letter
    length_of_letter = len(letter)
    #adjust amount of spaces which should be 1 less 
    spaces = ' ' * (length_of_letter - 1)
    #check for letter in row to adjust spaces:
    if letter in row:
        #ignore if row starts with letter:
        if row.startswith(letter):
            #remove spaces after letter
            row = letter.join(row.split(letter + spaces)) 
        else:
            #remove spaces before letter
            row = letter.join(row.split(spaces + letter))
    
    return row
    


def save_boards(amounts = 8):
    """
    Stores boggle-boards as boggle_i.txt, where i is an integer from [1; amounts].

    Parameters
    ----------
    amounts : int, optional
        Amount of boggle-board files to store as .txt file. The default is 8.

    Returns
    -------
    None.

    """
    for i in range(1,1+amounts):
        
        #shuffle dices
        shuffle(dices)
        #create random board
        field = ''
        for dice_row in grouper(dices, 4):
            row = '  '.join((dice_dct[j][randint(0,5)] for j in dice_row))
            #adjust spacing
            row = _adjust_spacing(row, letter='Qu')

            field += row + '\n'
        #write to file    
        with open(f'boggle_{i}.txt', 'w') as file:
            file.writelines(field)



def play_boggle(MINUTES = 3):
    """
    Prints a boggle-board to the console and instanciate a timer

    Parameters
    ----------
    MINUTES : int, optional
        Number of minutes for the timer to count down. The default is 3.

    Returns
    -------
    None.

    """
    #create the board
    make_board()
    #start the timer
    for i in range(MINUTES):
      min_left = MINUTES - i
      if min_left > 1:
        print(f'{min_left} minutes remain')
      else:
        print('Only one minute left')
      sleep(60)
    
    print('##### Time is over ######')


###definition of global variables:

#create dices
dices = list(range(16))

#letter combinations taken from German Boggle dices
dice_dct = {
      0:['R', 'I', 'S', 'N', 'E', 'H'],
      1:['U', 'N', 'E', 'L', 'Y', 'G'],
      2:['S', 'M', 'R', 'A', 'O', 'I'],
      3:['I', 'E', 'R', 'W', 'L', 'U'],
      4:['A', 'A', 'I', 'T', 'E', 'O'],
      5:['K', 'O', 'U', 'N', 'E', 'T'],
      6:['M', 'E', 'P', 'C', 'A', 'D'],
      7:['I', 'R', 'F', 'A', 'X', 'O'],
      8:['O', 'N', 'D', 'S', 'T', 'E'],
      9:['Qu', 'O', 'A', 'J', 'B', 'M'],
      10:['A', 'R', 'L', 'C', 'S', 'E'],
      11:['E', 'H', 'E', 'F', 'S', 'I'],
      12:['A', 'D', 'N', 'Z', 'V', 'E'],
      13:['G', 'V', 'I', 'T', 'E', 'N'],
      14:['A', 'B', 'R', 'L', 'I', 'T'],
      15:['P', 'S', 'E', 'U', 'T', 'L'],
}


if __name__ == '__main__':
    
    #save 4 boards 
    save_boards(amounts = 4)
    #start a game
    play_boggle(MINUTES = 3)