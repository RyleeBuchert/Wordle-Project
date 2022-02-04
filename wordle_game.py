from collections import Counter
from tkinter import messagebox
from tkinter import *
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
        self.key_word = "elegy"
        self.num_guesses = 6
        self.guesses = []

        # initiate wordle tkinter gui
        wordle_window = Tk()
        wordle_window.title("RYLEE WORDLE")
        wordle_window.geometry('400x600')

        # create a frame for the box grid
        frame = Frame(wordle_window, width=400, height=600)
        frame.grid(row=0, column=0)
        frame.grid_propagate(0)

        # create the box grid, contains wordle guess letters
        self.current_row = 0
        self.box_list = pd.DataFrame(index=range(6), columns=range(5))
        for i in range(6):
            for j in range(5):
                frame.rowconfigure(i, weight=1)
                frame.columnconfigure(j, weight=1)
                grid_box = Text(frame, height=2, width=4, bg="light cyan", font=('Helvetica', 50))
                grid_box.tag_configure("center", justify='center')
                grid_box.grid(row= i, column= j, padx=5, pady=5)
                self.box_list.iloc[i][j] = grid_box

        # create guess entry box
        guess_label = Label(frame, text="Input Word")
        guess_label.grid(row=7, column=1, columnspan=3)

        self.wordle_input = StringVar()
        self.guess_entry = Entry(frame, textvariable=self.wordle_input)
        self.guess_entry.grid(row=8, column=1, columnspan=3)

        guess_button = Button(frame, text="Submit", command=self.get_input)
        guess_button.grid(row=9, column=2, pady=5)

        # run wordle window
        wordle_window.mainloop()    

    # method to obtain input from entry box and color the grid boxes
    def get_input(self):
        wordle_word = self.wordle_input.get()
        results = self.guess_word(wordle_word)
        self.guess_entry.delete(0, END)
        if results is None:
            return
        else:
            for i in range(len(wordle_word)):
                if results[i] == 0:
                    self.box_list.iloc[self.current_row][i].configure(font=('Helvetica', 50))
                elif results[i] == 1:
                    self.box_list.iloc[self.current_row][i].configure(bg='yellow', font=('Helvetica', 50))
                elif results[i] == 2:
                    self.box_list.iloc[self.current_row][i].configure(bg='green', font=('Helvetica', 50))
                self.box_list.iloc[self.current_row][i].insert("1.0", wordle_word[i].upper())
                self.box_list.iloc[self.current_row][i].tag_add("center", "1.0", "end")
            self.current_row += 1
            if (len(np.unique(results)) == 1) and (results[0] == 2):
                    messagebox.showinfo("Wowza", "You got it right :)")

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


if __name__ == "__main__":
    
    new_game = Wordle()
