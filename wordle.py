from collections import Counter
from tkinter import messagebox
from tkinter import *
from turtle import update
import pandas as pd
import numpy as np
import random

class Wordle:

    def __init__(self):
        
        # get word dictionary from word_dict.txt
        with open('data\\word_dict.txt') as file:
            self.word_dict = [x.replace('\n','') for x in file.readlines()]

        # generate key word, number of remaining guesses, and guess list
        self.key_word = self.word_dict[random.randrange(0, len(self.word_dict))]
        self.num_guesses = 6
        self.guesses = []

        # model variables
        self.remaining_words = self.word_dict
        letters = "abcdefghijklmnopqrstuvwxyz"
        self.remaining_letters = letters
        char_freq_dict = {i: [0]*5 for i in letters}
        for word in self.word_dict:
            for i in range(len(word)):
                char_freq_dict[word[i]][i] += 1

    # method to input guess and get results
    def guess_word(self, input):
        if self.num_guesses == 0:
            messagebox.showinfo("Error", "Out of guesses.")
            return
        
        guess = input.lower()
        if guess not in self.word_dict:
            messagebox.showinfo("Error", "Invalid Input: Not in Word List.")
            return
        elif len(guess) > 5:
            messagebox.showinfo("Error", "Invalid Input: Too many characters.")
            return
        elif len(guess) < 5:
            messagebox.showinfo("Error", "Invalid Input: Too few characters.")
            return
        
        self.guesses.append(guess)
        results_list = [0]*len(guess)
        letters = Counter(self.key_word)
        for i in range(len(guess)):
            if guess[i] == self.key_word[i]:
                results_list[i] = 2
                letters[guess[i]] -= 1
        for i in range(len(guess)):
            if (guess[i] in self.key_word) and (results_list[i] != 2) and (letters[guess[i]] > 0):
                results_list[i] = 1
                letters[guess[i]] -= 1
        self.num_guesses -= 1
        return(results_list)

    # method to narrow search field based on results
    def narrow_search(self, guess, results):
        
        # get rid of characters with result = '0'
        bad_letters = "".join(sorted(set([guess[i] for i in range(len(guess)) if results[i] == 0])))
        if len(bad_letters) != 0:
            self.remaining_words = [word for word in self.remaining_words if len(set(word)) == (len(set(word) - set(bad_letters)))]
        self.remaining_letters = "".join(sorted(set(self.remaining_letters) - set(bad_letters)))

        # index of character in guess with result = '2'
        two_index = [i for i in range(len(results)) if results[i] == 2]
        if len(two_index) != 0:
            temp_remaining_words = []
            for word in self.remaining_words:
                word_status = 'Included'
                for index in two_index:
                    if word[index] != guess[index]:
                        word_status = 'Excluded'
                if word_status == 'Included':
                    temp_remaining_words.remaining_words.append(word)
            self.remaining_words = temp_remaining_words

        # index of character in guess with result = '1'
        one_index = [i for i in range(len(results)) if results[i] == 1]
        if len(one_index) != 0:
            temp_remaining_words = []
            for index in one_index:
                temp_remaining_words.append([word for word in self.remaining_words if guess[index] in word])
            self.remaining_words = temp_remaining_words[0]

if __name__ == "__main__":
    
    new_game = Wordle()
