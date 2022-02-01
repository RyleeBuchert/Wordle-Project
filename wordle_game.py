import random

class Wordle:

    def __init__(self):
        with open('data\\word_dict.txt') as file:
            self.word_dict = [x.replace('\n','') for x in file.readlines()]
        self.key_word = self.word_dict[random.randrange(0, len(self.word_dict))]
        self.num_guesses = 6

    def guess_word(self, input):
        if self.num_guesses == 0:
            return 'Out of Guesses --- LOSER!!!'
        
        if input not in self.word_dict:
            return 'Invalid Input --- Not in Word List'
        elif len(input) > 5:
            return 'Invalid Input --- Too Big'
        elif len(input) < 5:
            return 'Invalid Input --- Too Small'
        
        results_list = [0]*len(input)
        for i in range(len(input)):
            if input[i] == self.key_word[i]:
                results_list[i] = 2
            elif input[i] in self.key_word:
                results_list[i] = 1
            else:
                results_list[i] = 0
        self.num_guesses -= 1

        print(input)
        for i in results_list:
            print(i, end="")
        print()


if __name__ == "__main__":
    
    new_game = Worldle()
    new_game.guess_word("ADIEU")
