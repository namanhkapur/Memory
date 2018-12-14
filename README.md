# Memory

This is my coding challenge submission for the KP Engineering Fellows Program (Summer 2019). 

I implemented a complete, end-to-end game of Memory playable with multiple people. The rules are straightforward: someone picks a pair of cards, if the cards are of the same rank, the person gets a point and another turn, otherwise it’s another player’s turn – this continues until all the cards have been matched. 

## Getting Started

You need python 3 to run the game. First, make sure you are inside the folder. If your command for running python 3 is python3, simply write on the command line:
```
./memory
```
Otherwise, write the following: <your python 3 command> memory.py

## How To Play

The board will look something like this:

   	   0  1  2  3
	0  X  X  X  X
	1  X  X  X  X
	2  X  X  X  X
	3  X  X  X  X

You will be prompted for a guess in 'row_one' 'col_one' 'row__two' 'col_two' format. Make sure your guess is broken up with spaces. To guess the top-left corner card and the bottom-right corner card, for example, enter something like this: 0 0 3 3

## Design

I quickly realized, because this is a game, I can separate the pieces of the game with the dynamics of playing the game. In our case, the former category would simply be cards and decks and the latter would be the rules of Memory, the players, and general game flow. This structure also allows me to reuse the cards.py file for other games. In memory.py, I mainly used arrays to keep track of cards and the game-board and a hash map to relate players with their scores. I went ahead and also abstracted the internal workings of the Memory game – rules, guessing, updating the board – from the players of the game. Lastly, I had a ‘main’ method to play the game through the command line. 

## Libraries/Tools

I imported ‘random’ to implement shuffling and ‘collections’ for defaultdicts. Python is my language of choice because I'm extremely comfortable in the environment and it is highly readable. 