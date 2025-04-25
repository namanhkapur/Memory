# locally created module
import cards
import random
from collections import defaultdict

class Memory(object):
	"A class representing a game of memory"
	def __init__(self, n):
		"""
		Initializes a new Memory game with an n x n board.
		
		Raises:
			ValueError: If n is not even or if the board size exceeds the available deck size.
		"""
		# checks if not enough cards to fill a (n x n)
		if (n % 2 != 0):
			print ("ERROR: 'n' must be an even number")
			raise ValueError
		if (n * n > cards.DECK_SIZE):
			print ("ERROR: There aren't enough cards to fill an (" + str(n) + " x " + str(n) + ") board")
			raise ValueError
		self.indeces = list(range(cards.DECK_SIZE))
		random.shuffle(self.indeces)
		self.rows = n
		self.cols = n
		self.board = [[0 for j in range(self.cols)] for i in range(self.rows)]
		self.solution = [[0 for j in range(self.cols)] for i in range(self.rows)]
		self.cards_for_board = self.get_cards_for_board()
		self.init_board()

	def get_cards_for_board(self):
		"""
		Selects and returns a shuffled deck containing pairs of cards with matching ranks to fill the game board.
		
		Returns:
			A shuffled deck of cards, each rank appearing exactly twice, suitable for the current board size.
		"""
		added_cards = []
		num_total_cards = len(self.indeces)
		num_unique_ranks = int((self.rows * self.rows) / 2)
		for i in range(num_unique_ranks):
			for j in range(i + 1, num_total_cards):
				if ((self.indeces[i] % 13) == (self.indeces[j] % 13)):
					card = self.indeces.pop(j)
					added_cards.append(card)
					break
			added_cards.append(self.indeces[i])

		return cards.Deck(added_cards).shuffle()

	def init_board(self):
		"""
		Initializes the game board by hiding all cards and assigning solution cards to each position.
		
		Sets all positions on the visible board to hidden and fills the solution board with cards drawn from the prepared deck.
		"""
		for r in range(self.rows):
			for c in range(self.cols):
				# hidden means 'X'
				self.board[r][c] = ' X '
				self.solution[r][c] = self.cards_for_board.draw_card()

	def show_board(self):
		"""
		Displays the current visible state of the game board with row and column indices.
		"""
		row = 0
		col = "  ".join(list(map(lambda s: " " + s + " ", (list(map(str, range(self.cols)))))))
		print()
		print ("\t  ", col)
		for arr in self.board:
			print ("\t" + str(row) + "  ", end="")
			print (*arr, sep="  ") 
			row += 1
		print()

	def update_board(self, row, col):
		"""
		Reveals the card at the specified position on the visible board.
		
		Args:
			row: The row index of the card to reveal.
			col: The column index of the card to reveal.
		"""
		self.board[row][col] = self.solution[row][col]

	def show_wrong_guess(self, row1, col1, row2, col2):
		"""
		Temporarily reveals two cards for an incorrect guess, then hides them again.
		
		Args:
			row1: Row index of the first card.
			col1: Column index of the first card.
			row2: Row index of the second card.
			col2: Column index of the second card.
		"""
		self.board[row1][col1] = self.solution[row1][col1]
		self.board[row2][col2] = self.solution[row2][col2]
		self.show_board()
		self.board[row1][col1] = ' X '
		self.board[row2][col2] = ' X '
		self.show_board()

	def check_guess(self, row1, col1, row2, col2):
		"""
		Checks if two selected cards on the board have matching ranks.
		
		If the cards match, reveals them on the board and returns True along with the card objects. If not, temporarily reveals both cards, then hides them again, and returns False.
		
		Args:
			row1: Row index of the first card.
			col1: Column index of the first card.
			row2: Row index of the second card.
			col2: Column index of the second card.
		
		Returns:
			A tuple (matched, card1, card2), where matched is True and card1/card2 are the matched cards if the guess is correct; otherwise, matched is False and card1/card2 are None.
		"""
		if (self.solution[row1][col1].get_rank() == self.solution[row2][col2].get_rank()):
			self.update_board(row1, col1)
			self.update_board(row2, col2)
			self.show_board()
			return (True, self.solution[row1][col1], self.solution[row2][col2])
		else:
			self.show_wrong_guess(row1, col1, row2, col2)
			return (False, None, None)

	# Removed broken method: show_cards
# def show_cards(self):
		"""
		Shows all the cards in the game <should never be called by
		players of the game>
		"""
		print ("There are " + str(len(self.cards)) + " cards on the table:")
		[print (str(d)) for d in self.decks]

	def all_pairs_found(self):
		"""
		Returns True if all card pairs have been found and revealed.
		
		The game is considered complete when the visible board matches the solution board.
		"""
		return self.board == self.solution

	def get_card_from_board(self, row, col):
		"""
		Returns the visible value at the specified board position.
		
		Args:
			row: Row index of the board.
			col: Column index of the board.
		
		Returns:
			The card or hidden marker at the given (row, col) position on the visible board.
		"""
		return self.board[row][col]

class Player(object):
	"A class representing a player of memory"
	def __init__(self, name):
		"""
		Initializes a player with the given name, zero score, and an empty hand.
		
		Args:
			name: The player's name.
		"""
		self.name = name
		self.score = 0
		self.cards = []

	def get_name(self):
		"""
		Returns the player's name.
		"""
		return self.name

	def get_score(self):
		"""
		Returns the current score of the player.
		"""
		return self.score

	def increment_score(self):
		"""
		Increases the player's score by one.
		"""
		self.score += 1

	def add_card_to_hand(self, card):
		"""
		Adds a matched card to the player's hand.
		
		Args:
			card: The card object to add to the player's hand.
		"""
		self.cards.append(card)

	def get_hand(self):
		"""
		Returns the list of cards currently held by the player.
		"""
		return self.cards

def main():
	"""
	Runs the interactive console-based Memory card game.
	
	Prompts for player names and board size, manages game setup, and handles the main game loop, including player turns, input validation, scorekeeping, and determining the winner. The game continues until all card pairs are found.
	"""
	print ("Welcome to the card game 'Memory' - made with \u2665 by Namanh Kapur")
	while True:
		names = str(input("Who all is playing today? [Provide names seperated by spaces]: ")).split()
		if (len(names) < 1):
			print ("We need at least one person at the table.")
			continue
		else:
			break
	players = [Player(name) for name in names]
	random.shuffle(players)
	# to print out names with correct punctuation
	print ("Good to have you with us, ", end="")
	if (len(names) == 1):
		print (names[0] + ".")
	elif (len(players) == 2):
		print (names[0] + " and " + names[1] + ".")
	else:
		print (", ".join(names[:-1]), end=", and " + names[-1] + ".\n")
	while True:
		try:
		    n = int(input("We need an (n x n) board to play the game. Please specify an even integer 'n':  "))
		except ValueError:
			print ("That wasn't an integer.")
			continue
		if (n % 2 != 0):
			print ("That wasn't an even integer.")
			continue
		elif (n * n > cards.DECK_SIZE):
			print ("Couldn't construct an (" + str(n) + " x " + str(n) + ") board with a deck of 52 cards. Please specify a smaller even integer 'n':  ")
		else:
			# n was successfully parsed!
			break
	memory = Memory(n)
	print ("All members are present. The deck has been shuffled. A random order of turns has been set. Let the game begin!")
	memory.show_board()
	while True:
		player_index = 0
		while (player_index < len(players)):
			player = players[player_index]
			print ("It's " + player.get_name() + "'s turn.")
			while True:
				try:
					guess = list(map(int, input("Please input your two guesses followed by spaces 'row_one' 'col_one' 'row_two' 'col_two':  ").split()))
				except ValueError:
					print ("Please make sure your guesses are integers.")
					continue
				if (len(guess) != 4):
					print ("Please input 4 guesses.")
					continue
				elif guess[0] == guess[2] and guess[1] == guess[3]:
					print ("Your guesses must correspond to different cards.")
					continue
				elif (guess[0] >= memory.rows or guess[1] >= memory.rows or guess[2] >= memory.rows or guess[3] >= memory.rows):
					print ("Please ensure the 4 guesses are all integers less than " + str(n) + ", which is dimension of the board.")
					continue
                elif ('X' not in str(memory.get_card_from_board(guess[0], guess[1]))  or
                      'X' not in str(memory.get_card_from_board(guess[2], guess[3]))):
                    print("You can't guess a card that is already uncovered.")
                    continue
				else:
					break
			player_index += 1
			output_of_guess = memory.check_guess(guess[0], guess[1], guess[2], guess[3])
			if (output_of_guess[0]):
				player_index -= 1
				player.increment_score()
				print ("Good guess. You correctly matched a pair of cards.")
				player.add_card_to_hand(output_of_guess[1])
				player.add_card_to_hand(output_of_guess[2])
				print ("The pair of cards has been added to your hand: " + str(player.get_hand()))
			else:
				print ("Incorrect guess. Your turn is over.")
				print ("Your hand remains: " + str(player.get_hand()))
			print ("Your score is: " + str(player.get_score()) + "\n")
			if (memory.all_pairs_found()):
				scores = defaultdict(list)
				for p in players:
					scores[p.get_score()].append(p.get_name())
				max_score = max(scores.keys())
				if (len(scores[max_score]) > 1):
					print ("There was a tie between <", end="")
					print (", ".join(scores[max_score]), end=">/n")
				else:
					print ("The winner is: " + scores[max_score][0])
				print ("Thanks so much for playing - hope you sharpened those memory skills. Come back soon!")
				return 

if (__name__ == '__main__'):
	"""
	Runs the main routine
	"""
	main()