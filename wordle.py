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
        # self.key_word = self.word_dict[random.randrange(0, len(self.word_dict))]
        self.key_word = 'apple'
        self.word_so_far = '00000'
        self.num_guesses = 6
        self.guesses = []

        # model variables
        self.remaining_words = self.word_dict
        letters = "abcdefghijklmnopqrstuvwxyz"
        self.remaining_letters = letters
        char_freq_dict = {i: [0]*5 for i in letters}
        for word in self.word_dict:
            for i, char in enumerate(word):
                char_freq_dict[char][i] += 1
        self.char_freq_df = pd.DataFrame(char_freq_dict).transpose()
        self.row_sums = self.char_freq_df.sum(axis=1)

    # method to input guess and get results
    def guess_word(self, input):
        if self.num_guesses == 0:
            messagebox.showinfo("Error", "Out of guesses.")
            return
        
        guess = input.lower()
        if len(guess) > 5:
            messagebox.showinfo("Error", "Invalid Input: Too many characters.")
            return
        elif len(guess) < 5:
            messagebox.showinfo("Error", "Invalid Input: Too few characters.")
            return
        elif guess not in self.word_dict:
            messagebox.showinfo("Error", "Invalid Input: Not in Word List.")
            return
        
        self.guesses.append(guess)
        results_list = [0]*len(guess)
        letters = Counter(self.key_word)
        for i, char in enumerate(guess):
            if char == self.key_word[i]:
                results_list[i] = 2
                letters[char] -= 1
        for i, char in enumerate(guess):
            if (char in self.key_word) and (results_list[i] != 2) and (letters[char] > 0):
                results_list[i] = 1
                letters[char] -= 1
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
                    temp_remaining_words.append(word)
            self.remaining_words = temp_remaining_words

        # index of character in guess with result = '1'
        one_index = [i for i in range(len(results)) if results[i] == 1]
        if one_index:
            temp_remaining_words = []
            for index in one_index:
                temp_remaining_words.append([word for word in self.remaining_words if guess[index] in word])
            self.remaining_words = temp_remaining_words[0]

        # update character frequency dataframe
        char_freq_dict = {i: [0]*5 for i in self.remaining_letters}
        for word in self.remaining_words:
            for i, char in enumerate(word):
                char_freq_dict[char][i] += 1
        self.char_freq_df = pd.DataFrame(char_freq_dict).transpose()
        self.row_sums = self.char_freq_df.sum(axis=1)

        # get known letters string for pick_word method
        self.word_so_far = ""
        for i, char in enumerate(guess):
            if results[i] == 2:
                self.word_so_far += char
            else:
                self.word_so_far += '0'

    # method to calculate entropy for all words and pick best
    def pick_word(self):
        best_word = ""
        best_entropy = 0
        for word in self.remaining_words:
            word_entropy = 0
            seen_chars = set()
            for i, char in enumerate(word):
                green = self.char_freq_df.loc[char][i]
                if char not in seen_chars:
                    mask = [ch != char for ch in self.word_so_far]
                    yellow = sum(self.char_freq_df.loc[char][mask]) - green
                    seen_chars.add(char)
                else:
                    yellow = 0
                if self.row_sums[char] > len(self.remaining_words):
                    prob_list = [green, yellow, 0]
                    prob_list = [num / (green + yellow) for num in prob_list]
                else:
                    grey = len(self.remaining_words) - green - yellow
                    prob_list = [green, yellow, grey]
                    prob_list = [num / len(self.remaining_words) for num in prob_list]
                for j in prob_list:
                    word_entropy += self.entropy(j)
            if word_entropy > best_entropy:
                best_entropy = word_entropy
                best_word = word
        return best_word

    # method to calculate entropy for probability distribution
    def entropy(self, q):
        if q == 0 or q == 1:
            return 0
        else:
            return (-1 * q) * np.log2(q)

    # method to test model accuracy
    def test_model(self):
        guess = 'tares'
        while self.num_guesses > 0:
            if not guess:
                guess = self.pick_word()
            results = self.guess_word(guess)
            print(guess, "--- ", end="")
            print(results)
            self.narrow_search(guess, results)
            guess = ""

if __name__ == "__main__":
    
    new_game = Wordle()
    new_game.test_model()