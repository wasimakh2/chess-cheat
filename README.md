# Chess-Cheat
##### A tool to cheat at online chess

Launch Chess-Cheat, open your favourite chess website and the tool will dinamically overlay the best move for you.

![Example](https://raw.githubusercontent.com/GabrieleMaurina/chess-cheat/master/images/example.png)

### Install

Prerequisites to install:
* [Python 3](https://www.python.org/ "Python website")
* [Stockfish](https://stockfishchess.org/ "Stockfish website")

Then simply run:

`python -m pip install chess-cheat`

### Usage

Launch it as follow:

`python -m chess-cheat`

How the UI works:
* The switch "White/Black" allows you to tell Chess-Cheat if you are playing white or black.
* The "Board" button allows you to tell Chess-Cheat where the board is on the screen to facilitate recognition.
* The best move foy you is displayed both as an arrow and as a string.
* A green background indicates that it is working correctly.
* A red background indicates that it is not finding the board on the screen.

### Cloning this repo

To successfully clone Chess-Cheat from this repo and execute it you need to run:

`git clone https://github.com/GabrieleMaurina/chess-cheat.git`

Then install the following dependencies:
* [Python 3](https://www.python.org/ "Python website")
* [Tensorflow](https://pypi.org/project/tensorflow/ "Tensorflow for python")
* [Stockfish](https://stockfishchess.org/ "Stockfish website") installed in your system
* [Stockfish](https://pypi.org/project/stockfish/ "Stockfish for python") for python
* [Pillow](https://pypi.org/project/Pillow/ "Pillow for python")
* [Pyscreenshot](https://pypi.org/project/pyscreenshot/ "Pyscreenshot for python")
* [Timeout decorator](https://pypi.org/project/timeout-decorator/ "Timeout decorator for python")

### How it works

Chess-Cheat is based on [Tensorflow_Chessbot](https://github.com/Elucidation/tensorflow_chessbot "Tensorflow_Chessbot github") for recognizing the chessboard on your screen.

It uses [Stockfish](https://stockfishchess.org/ "Stockfish website") to compute the best move.

It displays the arrows and the buttons on the screen with [Tkinter](https://docs.python.org/3/library/tkinter.html "Tkinter documentation").
