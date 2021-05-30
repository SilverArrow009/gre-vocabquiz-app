#!/usr/bin/python3

import curses
from os import error
from tabulate import tabulate
import random
import re

class QuizPage :
    def __init__(self, stdscr, word, menu_list) :
        self.options = menu_list
        self.stdscr = stdscr
        self.position = 0
        self.word = word
        self.done = False
        self.answer = None

    def navigate (self, key_press) :
        if (self.position < 0 and key_press == curses.KEY_UP) :
            return
        elif (self.position == len(self.options) and key_press == curses.KEY_DOWN) :
            return
        else :
            if (key_press == curses.KEY_UP) :
                if(self.position > 0) :
                    self.position -= 1
                else :
                    pass
            elif (key_press == curses.KEY_DOWN) :
                if(self.position < len(self.options)-1) :
                    self.position += 1
                else :
                    pass
            elif (key_press == 10) :
                self.answer = self.options[self.position]
                self.done = True
    
    def draw (self, y, x) :
        x += 4
        y += 2
        while (True) :
            self.stdscr.clear()
            self.stdscr.box()
            self.stdscr.addstr(y,x, "Choose the best definition for the word : ")
            self.stdscr.addstr(self.word, curses.A_BOLD)
            pos_y = y+4
            # Redraw the entire menu
            self.stdscr.move(pos_y,x+8)
            for option in self.options :
                if (self.options[self.position] != option ) :
                    self.stdscr.addstr(option, curses.A_NORMAL)
                    pos_y+=2
                    self.stdscr.move(pos_y,x+8)
                else :
                    self.stdscr.addstr(option, curses.A_REVERSE)
                    pos_y+=2
                    self.stdscr.move(pos_y,x+8)
            self.stdscr.refresh()
            if(self.done) :
                break
            self.navigate(self.stdscr.getch())

# Read the data from the file
tsv_file = open("vocab_database.csv", 'r', encoding='utf-8-sig')

####################
### SANITY CHECK ###
####################

faults = []
uniqueWords = []
count = 0
tsvFileLines = tsv_file.readlines()
for lineIndex in range(len(tsvFileLines)):
    # fetch the regex
    # line --> check whether "word<tab>meaning" is followed"
    # word --> check for duplicates
    lineRegex = re.search(r'^\w*\b\t\b.*$', tsvFileLines[lineIndex])
    wordRegex = re.search(r'^\w*\t', tsvFileLines[lineIndex])
    if(lineRegex is None):
        faults.append(["DB Syntax", lineIndex, tsvFileLines[lineIndex]])
        count += 1
        continue
    elif(wordRegex.group() in uniqueWords):
        faults.append(["Duplicate", lineIndex, tsvFileLines[lineIndex]])
        count += 1
        continue
    else:
        uniqueWords.append(wordRegex.group())

# print all faults in DB
if(count):
    print(tabulate(faults, headers = ['Fault', 'Line #', 'Text']))
# reset character position in file
tsv_file.seek(0)


#################
### MAIN FLOW ###
#################

number_of_questions = int (input("Enter the number of questions you wish to practise : "))

stdscr = curses.initscr()
(V_MAX, H_MAX) = stdscr.getmaxyx()
curses.curs_set(0)
stdscr.keypad(True)

vocab_db = {}
# Populate the dictionary
for line in tsv_file:
    word_pair = line.split(sep='\t')
    vocab_db[word_pair[0]] = word_pair[1]
tsv_file.close()
# prepare the set of quesitons and options
words = random.sample(vocab_db.keys(), number_of_questions)
questions = {}
for word in words :
    options = random.sample(list(vocab_db.values()), 5)
    if (vocab_db[word] not in options) :
        options[random.randint(0, len(options)-1)] = vocab_db[word]
        questions[word] = options
    else :
        questions[word] = options
# Initialize the test
quiz = []
for word in words :
    quiz.append(QuizPage(stdscr, word, questions[word]))
# Start the test
score = []
errors = []
for i in range(len(quiz)) :
    quiz[i].draw(0, 0)
    if(quiz[i].done) :
        selected_ans = quiz[i].answer
        correct_ans = vocab_db[quiz[i].word]
        if (correct_ans == selected_ans) :
            score.append(1)
        else :
            score.append(0)
            errors.append([quiz[i].word, selected_ans, correct_ans])
curses.endwin()
# Report the result
total_score = sum(score)
print("Your score : {0}/{1}\tPercentage : {2}".format(total_score, len(score), total_score*100/len(score)))
if(total_score != len(score)) :
    print("Words you got wrong are :")
    print(tabulate(errors, headers=["Word", "Your answer", "Correct Answer"]))
