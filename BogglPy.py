# -*- coding: utf-8 -*-
"""
Creates a boggle-inspired boggle game.


Created on Mon Jun  1 21:42:44 2020

@author: Birk Fritsch
"""

from random import shuffle, randint
from itertools import zip_longest
from time import sleep
import numpy as np
import itertools
import copy

def grouper(iterable, n, fillvalue=' '):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)



def make_board(extra_line=True, spacer_num = 4):
    """
    Creates a random 4x4 boggle board as string. 

    Returns
    -------
    field : str

    """
    #shuffle dices
    shuffle(dices)

    #create random board
    field = ''
    spaces = ' ' * spacer_num
    for dice_row in grouper(dices, 4):
       
        row = spaces.join((dice_dct[j][randint(0,5)] for j in dice_row))
        #adjust spacing
        row = _adjust_spacing(row, letter='Qu')

        field += row + '\n'
        
        #append extra line between letters
        if extra_line:
            field += '\n'
        
        
    return field
    
    
 
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
        
        field = make_board(extra_line=False, spacer_num=2)
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
    field : str
        boggle board as string as created by make_board()

    """
    #create the board
    field = make_board(extra_line=True, spacer_num = 4)
    #display
    print(field)
    #start the timer
    for i in range(MINUTES):
        min_left = MINUTES - i
        if min_left > 1:
            print(f'{min_left} minutes remain')
        else:
            print('Only one minute left')
        sleep(60)
    
    print('##### Time is over ######')
    return field


def _field_to_array(field):
    """
    Transforms a board-string to a numpy array

    Parameters
    ----------
    field : string
        board string as created by make_board().

    Returns
    -------
    field_array : np.array
        2D array

    """
    
    #remove possible double lines
    field = '\n'.join(field.split('\n\n'))
    #split on single line separator
    field_list = field.split('\n')
    #remove emtpy strings in field_list created by final linebreak
    field_list = [line for line in field_list if line != '']
    #remove spaces
    letter_list = [line.split() for line in field_list]
    #convert letter_list to numpy array
    field_array = np.array(letter_list)
    
    return field_array



def _check_word(word, field_array):
    """
    checks whether a sequence of letters (word) can be built based on field_array

    Parameters
    ----------
    word : string
        word of interest.
    field_array : np.array
        game board as array.

    Returns
    -------
    found : dict
        DESCRIPTION.

    """
    #ensure uppercase letters in word
    word = word.upper()
    
    #define step width
    neighbour_steps = [-1, 0, 1]
    #build all combinations and exclude (0,0)
    neighbour_moves = [c for c in itertools.product(neighbour_steps,
                                                    neighbour_steps)
                       if c != (0,0)]
    
    #check all possible starting coordinates for matching possibilities
    #get all possible starting coordinates
    first_letter = word[0]
    if word.startswith('Q'):
        first_letter = 'Qu'
    
    row, col = np.where(field_array == first_letter)
    found = {'words': [], 'paths':[]}
    for coordinate in zip(row, col):
        
        used_coordinates = []
        #append coordinate tuple
        used_coordinates.append(coordinate)
        #get all possible combinations starting from coordinate
        list_of_words, list_of_paths = _get_next_letter(first_letter,
                                             field_array,
                                             coordinate,
                                             neighbour_moves,
                                             used_coordinates)
        #now, iterate over all words until the required length is given
        
        letters_in_word = len(word)
        #account for Qu exception
        if 'QU' in word:
            letters_in_word -= 1
        #first letter is found already
        for _ in range(letters_in_word-2):
            
            next_bunch_of_words = []
            next_bunch_of_paths = []
            
            for w, p in zip(list_of_words.copy(),
                            list_of_paths.copy()):
                coordinate = p[-1]
                list_of_ws, list_of_ps = _get_next_letter(w,
                                     field_array,
                                     coordinate,
                                     neighbour_moves,
                                     p)
                #store new results
                next_bunch_of_words.extend(list_of_ws)
                next_bunch_of_paths.extend(list_of_ps)

            list_of_words = next_bunch_of_words.copy()
            list_of_paths = next_bunch_of_paths.copy()
        
        found['words'].extend(list_of_words)
        found['paths'].extend(list_of_paths)

    return found
            
    

def _get_next_letter(word,
                     field_array,
                     coordinate,
                     neighbour_moves,
                     used_coordinates):
    """
    append 'word' by adjacent letters that are not found in used_coordinates.

    Parameters
    ----------
    word : string
        starting word.
    field_array : np.array
        board as np array as created by __field_to_array().
    coordinate : tuple
        Tuple of integers, defining the position of the last letter in word on field_array.
    neighbour_moves : list
        List containing relative moves allowed to find adjacent letters. E.g. [(0,1),(1,1)]
    used_coordinates : list
        List containing tuples that describe already used coordinates. They are regarded as 'forbidden coordinates'.

    Returns
    -------
    list_of_words : list
        List of all possible new strings.
    list_of_coordinates : list
        List of the used coordinates to build the new strings.

    """
    #define boundary coordinates
    row_min = col_min = 0
    row_max, col_max = field_array.shape
    #create an output container
    list_of_words = []
    list_of_coordinates = []
    
    for move in neighbour_moves:
        #create a new list instead of merely a reference
        new_used_coordinates = copy.copy(used_coordinates)
        #get next coordinate
        next_coord = coordinate[0] + move[0], coordinate[1] + move[1]
        #ensure that next_coord contains valid coordinates
        if not all([row_min <= next_coord[0] < row_max,
                col_min <= next_coord[1] < col_max]):
            continue
        #ensure that the coordinate has not been used before:
        if next_coord in used_coordinates:
            continue
        
        #read out new letter
        letter = field_array[next_coord]
        #make new word
        new_word = word + letter
        #ensure uppercase (relevant because of "Qu")
        new_word = new_word.upper()
        #store new word and  new coordinate
        list_of_words.append(new_word)
        new_used_coordinates.append(next_coord)
        list_of_coordinates.append(new_used_coordinates)
        
    return list_of_words, list_of_coordinates
    
    

def check_words(words, field):
    """
    Routine to check whether a string pattern 'word' or a list of strings can be
    build on a boggle field using the boggle rules.
    Really slow for large words.
    

    Parameters
    ----------
    words : str, or list
        either a single string or a list of strings to be checked.
    field : str
        boggle board as created by make_board().

    Returns
    -------
    checked_results : dictionary
        Dictionary with the checked words as key and True/False as value.

    """
    #convert field to numpy array
    field_array = _field_to_array(field)
    
    #ensure that words is not a single string
    if type(words) == str:
        words = [words]
    
    ##check words 
    checked_results = {}
    #iterate over words and store in output dictionary
    for word in words:
        #returns a dictionary containing the keys 'words', 'paths'
        found_dict = _check_word(word, field_array)
        #check if word has been found
        checked_results[word] = word.upper() in found_dict['words']
        
        
    return checked_results
    
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
    field = play_boggle(MINUTES = 3)
    words = input('Please enter patterns of interest separated by a space: ')
    
    #convert words to list of words
    list_of_words = words.split()
    checked = check_words(list_of_words, field)
    print(checked)
    
