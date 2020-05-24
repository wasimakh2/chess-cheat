# Chess-Cheat
##### A tool to cheat at online chess

Launch Chess-Cheat, open your favourite chess website and the tool will dinamically overlay the best move for you over your game.

### Install

To successfully run Chess-Cheat you are going to need:
* [Python 3](https://www.python.org/ "Python website")
* [Tensorflow](https://pypi.org/project/tensorflow/ "Tensorflow for python")
* Bs4 for python
* [Stockfish](https://stockfishchess.org/ "Stockfish website") installed in your system
* [Stockfish for python](https://pypi.org/project/stockfish/ "Stockfish for python")
* clone this repository with `git clone https://github.com/GabrieleMaurina/chess-cheat.git`

### Usage

Once you have all the dependencies installed, clone this repository and lunch `chess-cheat.py` as follows:

`python chess-cheat.py`

### How it works

Chess-Cheat is based on [Tensorflow_Chessbot](https://github.com/Elucidation/tensorflow_chessbot "Tensorflow_Chessbot github") for recognizing the chessboard and it uses [Stockfish](https://stockfishchess.org/ "Stockfish website") to compute the best move.
