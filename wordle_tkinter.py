from tkinter import *
import pandas as pd

def get_input():
    global current_row
    wordle_word = wordle_input.get()
    for i in range(len(wordle_word)):
        box_list.iloc[current_row][i].insert(INSERT, wordle_word[i])
        box_list.iloc[current_row][i].configure(bg='green')
    current_row += 1

if __name__ == "__main__":

    wordle_window = Tk()
    wordle_window.title('WORDLE')
    wordle_window.geometry('270x450')

    box_list = pd.DataFrame(index=range(6), columns=range(5))
    for i in range(6):
        for j in range(5):
            grid_box = Text(wordle_window, height=3, width=5, bg="light cyan")
            grid_box.grid(row= i, column= j, padx=5, pady=5)
            box_list.iloc[i][j] = grid_box

    current_row = 0
    wordle_input = StringVar()

    guess_label = Label(wordle_window, text="Input Word")
    guess_label.grid(row=7, column=1, columnspan=3)

    guess_entry = Entry(wordle_window, textvariable=wordle_input)
    guess_entry.grid(row=8, column=1, columnspan=3)

    guess_button = Button(wordle_window, text="Submit", command=get_input)
    guess_button.grid(row=9, column=2, pady=5)

    wordle_window.mainloop()
