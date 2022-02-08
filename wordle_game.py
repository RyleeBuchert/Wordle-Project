from collections import Counter
from wordle import Wordle
from tkinter import messagebox
from tkinter import *
from turtle import update
import pandas as pd
import numpy as np
import random

class Wordle_Game:

    def __init__(self):

        # create wordle cgame
        self.wordle = Wordle()

        # initiate wordle tkinter gui
        self.wordle_window = Tk()
        self.wordle_window.title("RYLEE WORDLE")
        self.wordle_window.geometry('400x600')

        # create a frame for the box grid
        frame = Frame(self.wordle_window, width=400, height=600)
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

   # method to launch gui for playing the game
    def launch_game(self):
        self.wordle_window.mainloop()

    # method to obtain input from entry box and color the grid boxes
    def get_input(self):
        wordle_guess = self.wordle_input.get().lower()
        if self.wordle.num_guesses == 0:
            messagebox.showinfo("Error", "Out of guesses.")
            return
        if len(wordle_guess) > 5:
            messagebox.showinfo("Error", "Invalid Input: Too many characters.")
            return
        elif len(wordle_guess) < 5:
            messagebox.showinfo("Error", "Invalid Input: Too few characters.")
            return
        elif wordle_guess not in self.wordle.word_dict:
            messagebox.showinfo("Error", "Invalid Input: Not in Word List.")
            return
        
        results = self.wordle.guess_word(wordle_guess)
        self.guess_entry.delete(0, END)
        if results is None:
            return
        else:
            for i in range(len(wordle_guess)):
                if results[i] == 0:
                    self.box_list.iloc[self.current_row][i].configure(font=('Helvetica', 50))
                elif results[i] == 1:
                    self.box_list.iloc[self.current_row][i].configure(bg='yellow', font=('Helvetica', 50))
                elif results[i] == 2:
                    self.box_list.iloc[self.current_row][i].configure(bg='green', font=('Helvetica', 50))
                self.box_list.iloc[self.current_row][i].insert("1.0", wordle_guess[i].upper())
                self.box_list.iloc[self.current_row][i].tag_add("center", "1.0", "end")
            self.current_row += 1
            if (len(np.unique(results)) == 1) and (results[0] == 2):
                    messagebox.showinfo("Wowza", "You got it right :)")
        return results


if __name__ == "__main__":

    new_game = Wordle_Game()
    new_game.launch_game()