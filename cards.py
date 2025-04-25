import random

# GLOBAL CONSTANTS
DECK_SIZE = 52

CARD_RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

CARD_SUITS_SYMBOLS = {
    "letters": ("S", "H", "C", "D"),
    "filled": ("\u2660", "\u2666", "\u2665", "\u2663")
}

CARD_SUITS = CARD_SUITS_SYMBOLS["filled"]

class Card(object):
    "A class representing a card"
    def __init__(self, index):
        """
        Initializes a Card with a rank and suit based on the given index.
        
        Args:
            index: An integer from 0 to 51 representing the card's position in a standard deck.
        
        Raises:
            TypeError: If index is not an integer.
        """       
        if isinstance(index, int):
            self.rank = index % 13
            self.suit = index // 13
        else:
            print ("ERROR: The card constructor must be called with an int")
            raise TypeError

    def get_rank(self):
        """
        Returns the rank index of the card.
        
        The rank is an integer from 0 (Ace) to 12 (King).
        """
        return self.rank

    def __str__(self):
        """
        Returns a string representation of the card formatted for display on a 2D board.
        
        Single-character ranks are padded with a trailing space for alignment.
        """
        symbol = CARD_RANKS[self.rank] + CARD_SUITS[self.suit]
        return CARD_RANKS[self.rank] + CARD_SUITS[self.suit] + (" " if len(CARD_RANKS[self.rank]) == 1 else "")

    def __repr__(self):
        """
        Returns a concise string representation of the card's rank and suit.
        """
        return CARD_RANKS[self.rank] + CARD_SUITS[self.suit]

class Deck(list):
    "A class representing a deck of cards"
    def __init__(self, indeces=None):
        """
        Initializes a deck with a list of card indices.
        
        Args:
            indeces: Optional list of integers representing card indices. If not provided, initializes an empty deck.
        
        Raises:
            ValueError: If more than 52 card indices are provided.
        """
        indeces = indeces or []
        if (len(indeces) > DECK_SIZE):
            # existing logic here
        Given a list of cards, creates a deck
        """ 
        if (len(indeces) > DECK_SIZE):
            print ("ERROR: A deck can only contain up to 52 cards")
            raise ValueError
        else: 
            self.deck = []
            self.indeces = indeces
            for index in indeces:
                self.deck.append(Card(index))

    def get_cards(self):
        """
        Returns all the cards in this deck
        """
        return self.deck

    def shuffle(self):
        """
        Shuffles the deck of cards
        """
        random.shuffle(self.indeces)
        return Deck(self.indeces)

    def draw_card(self):
        """
        Draws a card from the bunch of cards
        """
        if (len(self.indeces) > 0):
            return Card(self.indeces.pop())
        else:
            print ("ERROR: No more cards available to draw")
            raise ValueError 

    def __str__(self):
        """
        Returns a string representation
        """
        if (len(self.deck) == 0):
            return "The deck is empty"
        else:
            return " ".join([str(card) for card in self.deck])