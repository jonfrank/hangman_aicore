'''
Make sure you complete all the TODOs in this file.
The prints have to contain the same text as indicated, don't add any more prints,
or you will get 0 for this assignment.
'''

import random
import re
import urllib.request
import json

class Hangman:
    '''
    A Hangman Game that asks the user for a letter and checks if it is in the word.
    It starts with a default number of lives and a random word from the word_list.

    
    Parameters:
    ----------
    word_list: list
        List of words to be used in the game
    num_lives: int
        Number of lives the player has
    
    Attributes:
    ----------
    word: str
        The word to be guessed picked randomly from the word_list
    word_guessed: list
        A list of the letters of the word, with '_' for each letter not yet guessed
        For example, if the word is 'apple', the word_guessed list would be ['_', '_', '_', '_', '_']
        If the player guesses 'a', the list would be ['a', '_', '_', '_', '_']
    num_letters: int
        The number of UNIQUE letters in the word that have not been guessed yet
    num_lives: int
        The number of lives the player has
    list_letters: list
        A list of the letters that have already been tried

    Methods:
    -------
    check_letter(letter)
        Checks if the letter is in the word.
    ask_letter()
        Asks the user for a letter.
    '''
    def __init__(self, word_list, num_lives=5):
        try:
            random_word = urllib.request.urlopen("https://random-word-api.herokuapp.com/word?swear=0").read()
            random_word = random_word.decode()
            self.word = json.loads(random_word)[0]
        except:
            print("failed to get random word from the API - using one from the list instead")
            self.word = random.choice(word_list)
        self.word_guessed = ['_'] * len(self.word)
        self.num_letters = len(set(self.word))
        self.num_lives = num_lives
        self.list_letters = []
        print(f"The mistery word has {self.num_letters} characters")  # mystery not corrected for fear of failing the marking algorithm ;-)
        # also this is a bit ambiguous for the player - sounds like the length of the word rather than the number of distinct letters
        print(' '.join(self.word_guessed))

    def check_letter(self, letter) -> None:
        '''
        Checks if the letter is in the word.
        If it is, it replaces the '_' in the word_guessed list with the letter.
        If it is not, it reduces the number of lives by 1.

        Parameters:
        ----------
        letter: str
            The letter to be checked

        '''
        if letter in self.word:
            for idx,let in enumerate(self.word):
                if let == letter:
                    self.word_guessed[idx] = letter
            self.num_letters -= 1
            print(f"Nice! {letter} is in the word!")
            print(' '.join(self.word_guessed))
        else:
            self.num_lives -= 1

    def ask_letter(self):
        '''
        Asks the user for a letter and checks two things:
        1. If the letter has already been tried
        2. If the character is a single character
        If it passes both checks, it calls the check_letter method.
        '''
        while True:
            letter = input("Enter a letter to guess: ")
            letter = letter.lower()
            if not re.match(r'^[A-Za-z]$', letter):
                print("Please, enter just one character") # "which must be a letter"
            elif letter in self.list_letters:
                print(f"{letter} was already tried")
            else:
                break
        self.list_letters.append(letter)
        self.check_letter(letter) 

def play_game(word_list):
    # As an aid, part of the code is already provided:
    game = Hangman(word_list, num_lives=5)
    while game.num_lives > 0 and game.num_letters > 0:
        game.ask_letter()
        # print(f"Your guesses so far: {' '.join(game.word_guessed)}")
        # print(f"You have {game.num_lives} lives remaining, and you've got {game.num_letters} letters left to guess.")
        # print(f"Guessed letters so far: {', '.join(game.list_letters)}\n")
    if game.num_lives == 0:
        print(f"You lost! The word was {game.word}")
    else:
        print("Congratulations! You won!")

if __name__ == '__main__':
    word_list = ['apple', 'banana', 'orange', 'pear', 'strawberry', 'watermelon']
    play_game(word_list)
# %%

# %%
