# Chess-Cheat
##### A tool to cheat at online chess

Launch Chess-Cheat, open your favourite chess website and the tool will dinamically overlay the best move for you.

![Example](https://raw.githubusercontent.com/GabrieleMaurina/chess-cheat/master/example.png)

### Install

To successfully run Chess-Cheat first clone this repository with `git clone https://github.com/GabrieleMaurina/chess-cheat.git`

the you are going to need:
* [Python 3](https://www.python.org/ "Python website")
* [Tensorflow](https://pypi.org/project/tensorflow/ "Tensorflow for python")
* [Stockfish](https://stockfishchess.org/ "Stockfish website") installed in your system
* [Stockfish](https://pypi.org/project/stockfish/ "Stockfish for python") for python
* [Pyscreenshot](https://pypi.org/project/pyscreenshot/ "Pyscreenshot for python")
* [Timeout decorator](https://pypi.org/project/timeout-decorator/ "Timeout decorator for python")

### Usage

Once you have all the dependencies installed, clone this repository and lunch `chess-cheat.py` as follows:

`python chess-cheat.py`

### How it works

Chess-Cheat is based on [Tensorflow_Chessbot](https://github.com/Elucidation/tensorflow_chessbot "Tensorflow_Chessbot github") for recognizing the chessboard and it uses [Stockfish](https://stockfishchess.org/ "Stockfish website") to compute the best move.
