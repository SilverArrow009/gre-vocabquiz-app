# Vocabulary practice app for GRE

------------------------------------------------------

## About

This is a very simple python app with TUI to conduct a small MCQ quiz (Similiar to Magoosh's Vocabulary builder) except that you can add your own words for practice. Optionally, it woud be great if you could contribute to the excel spreadsheet to expand the utiity of this application. Please note that you need to **Export the CSV file with TAB as the deimiter and UNIX style line-endings (LF)**.

## Requirements

The script uses [`curses`](https://docs.python.org/3/library/curses.html#module-curses) module and [`tabulate`](https://pypi.org/project/tabulate/) module to implement the TUI and pretty print the output respectively. Please go through the links to find the instructions to setup the modules for your OS.

## Usage

After installing the dependencies, just run,

    python3 GRE_Vocab_quiz_app.py

To avoid potential cluttering of characters, it is recommended to go full-screen while running this app.
