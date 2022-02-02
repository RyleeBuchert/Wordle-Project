from tkinter import *
from matplotlib.pyplot import grid
import pandas as pd

def get_input():
    global current_row
    wordle_word = wordle_input.get()
    for i in range(len(wordle_word)):
        box_list.iloc[current_row][i].configure(bg='green', font=('Helvetica', 50))
        box_list.iloc[current_row][i].insert("1.0", wordle_word[i].upper())
        box_list.iloc[current_row][i].tag_add("center", "1.0", "end")
    current_row += 1

if __name__ == "__main__":

    wordle_window = Tk()
    wordle_window.title('WORDLE')
    wordle_window.geometry('400x600')
    
    frame = Frame(wordle_window, width=400, height=600)
    frame.grid(row=0, column=0)
    frame.grid_propagate(0)
    
    box_list = pd.DataFrame(index=range(6), columns=range(5))
    for i in range(6):
        for j in range(5):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(j, weight=1)
            grid_box = Text(frame, height=2, width=4, bg="light cyan", font=('Helvetica', 50))
            grid_box.tag_configure("center", justify='center')
            grid_box.grid(row= i, column= j, padx=5, pady=5)
            box_list.iloc[i][j] = grid_box
    
    current_row = 0
    wordle_input = StringVar()

    guess_label = Label(frame, text="Input Word")
    guess_label.grid(row=7, column=1, columnspan=3)

    guess_entry = Entry(frame, textvariable=wordle_input)
    guess_entry.grid(row=8, column=1, columnspan=3)

    guess_button = Button(frame, text="Submit", command=get_input)
    guess_button.grid(row=9, column=2, pady=5)

    wordle_window.mainloop()
