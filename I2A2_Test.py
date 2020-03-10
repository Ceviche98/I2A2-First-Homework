
# Import libraries

import numpy as np
import pandas as pd
import unittest

# Priorities dictionary
Priorities={"ROYAL FLUSH":10,"STRAIGHT FLUSH":9,"FOUR OF A KIND":8,
            "FULL HOUSE":7,"FLUSH":6,"STRAIGHT":5,"THREE OF A KIND":4,
           "TWO PAIR":3,"ONE PAIR":2,"HIGH CARD":1}


# Choose the best ranked poker hand

def compare_tuples(x,y):
    if x==y:
        return "TIE"
    elif x>y: 
        return "WIN"
    else:
        return "LOSS"

def sort_frequencies(card_numbers):
    """
    Sorts the card numbers given the counts association. They are sorted in descending order
    by count, and if count is equal, then by rank of the card. Returned cards and counts sequences maintain the association.
    
    Input:
        card_numbers: Unsorted numbers in the poker hand
        type card_numbers: list of integers
    Output:
        return: cards and counts sorted packed
        return type: zip(cards,counts)
    """
    cards=list(set(card_numbers))
    dictionary=dict()
    for card in cards:
        dictionary[card]=card_numbers.count(card)
    data=pd.DataFrame(list(dictionary.items()),columns=["card","frequency"])
    data_sorted=data.sort_values(by=["frequency","card"],ascending=False)
    return zip(data_sorted["card"],data_sorted["frequency"])


def non_consecutive(card_numbers,suits):
    cards=list(set(card_numbers))
    dictionary=dict()
    for card in cards:
        dictionary[card]=card_numbers.count(card)
    frequencies=list(dictionary.values())
    if 4 in frequencies:
        return "FOUR OF A KIND"
    elif sorted(frequencies)==[2,3]:
        return "FULL HOUSE"
    elif len(set(suits))==1:
        return "FLUSH"
    elif 3 in frequencies:
        return "THREE OF A KIND"
    elif frequencies.count(2)==2:
        return "TWO PAIR"
    elif 2 in frequencies:
        return "ONE PAIR"
    else:
        return "HIGH CARD"

def special_consecutive(card_numbers):
    #Evaluating special case of consecutive numbers Ace(14)->1
    numbers_text=" ".join([str(x) for x in card_numbers])
    numbers_text=numbers_text.replace("14","1")
    temp_numbers=numbers_text.split(" ")
    temp_numbers=[int(x) for x in temp_numbers]
    return consecutive_numbers(temp_numbers)


def consecutive_numbers(card_numbers):
    return sorted(card_numbers)==list(range(min(card_numbers),max(card_numbers)+1))


def get_numbers_suits(cards):
    numbers_text=" ".join([x[0] for x in cards])
    numbers_text=numbers_text.replace("T","10")
    numbers_text=numbers_text.replace("J","11")
    numbers_text=numbers_text.replace("Q","12")
    numbers_text=numbers_text.replace("K","13")
    numbers_text=numbers_text.replace("A","14")
    numbers_text=numbers_text.split(" ")
    numbers=[int(x) for x in numbers_text]
    suits=[x[1] for x in cards]
    return numbers,suits


def evaluate_hand(numbers,suits):
    """
    Evaluate which is the best possible hand with the numbers and suits. First, it is evaluated if the cards have a consecutive
    order or a special consecutive order(A,2,3,4,5). As a result, if the cards have a consecutive order it is decided whether 
    it is "ROYAL FLUSH", "STRAIGHT FLUSH" or "STRAIGHT". Secondly, if there aren't five consecutive numbers, it is evaluated 
    which is the best hand excluding the aforementioned.
    
    Input:
        numbers: Unsorted numbers in the poker hand
        type numbers: list of integers
        
        suits: Card suits 
        type suits: list of characters
        
    Output:
        return: name of the best possible poker hand
        return type: string
    """
    #First let´s check if there is a sequence of 5 cards
    if consecutive_numbers(numbers):
        if (sum(numbers)==60)&(len(list(set(suits)))==1):
            return "ROYAL FLUSH"
        elif len(list(set(suits)))==1:
            return "STRAIGHT FLUSH"
        else:
            return "STRAIGHT"
    elif special_consecutive(numbers):
        if len(list(set(suits)))==1:
            return "STRAIGHT FLUSH"
        else:
            return "STRAIGHT"
        
    return non_consecutive(numbers,suits)      


class PokerHand:
    def __init__(self,text):
        self.cards=text.split(" ")
        if len(self.cards) != 5:
            raise ValueError("Invalid Poker Hand")
        numbers,suits=get_numbers_suits(self.cards)
        self.best_hand=evaluate_hand(numbers,suits)
        self.sorted_counts=sort_frequencies(numbers)
        self.special_consecutive=special_consecutive(numbers)
        
    def compare_with(self,poker_hand_2):
        """
        Return the result of the first poker hand versus the second poker hand. If the rank is the same, compare the highest
        card in both sorted_counts and hand with a bigger number wins.If there is a tie, continue with the next high card in
        the sorted_counts until there is a tiebreaker.If the hands are completely equal return "TIE".

        Input:
            self,poker_hand_2: Poker hands to compare
            type self,poker_hand_2: class PokerHand

        Output:
            return: "WIN","LOSS" or "TIE"
            return type: string
        """
        if Priorities[self.best_hand]==Priorities[poker_hand_2.best_hand]:
            if self.special_consecutive &poker_hand_2.special_consecutive:
                return "TIE"
            elif self.special_consecutive:
                return "LOSS"
            elif poker_hand_2.special_consecutive:
                return "WIN"

            if self.sorted_counts==poker_hand_2.sorted_counts:
                return "TIE"

            number_self_cards, _ =  zip(*self.sorted_counts)
            number_poker_hand2_cards, _=zip(*poker_hand_2.sorted_counts)
            for x,y in zip(number_self_cards,number_poker_hand2_cards):
                answer_temp=compare_tuples(x,y)
                if answer_temp=="TIE":
                    pass
                else:
                    return answer_temp

        elif Priorities[self.best_hand]>Priorities[poker_hand_2.best_hand]:
            return "WIN"

        else:
            return "LOSS"
    

class Result:
    WIN="WIN"
    LOSS="LOSS"


# UNIT TEST CASES

# UNIT TEST CASES FOR ATTRIBUTE "best_hand"
#Adapting the test cases FROM https://github.com/ninadpage/poker-hands-comparator/blob/master/test_poker_hands.py

class TestPokerHand(unittest.TestCase):
    def test_one_pair(self):
        h1 = PokerHand('KH KD 2C 5D 8D')
        h2 = PokerHand('KS 8H KC 2H 5S')
        h3 = PokerHand('KH KD TC 5D 8D')
        self.assertEqual(h1.best_hand, "ONE PAIR")
        self.assertEqual(h2.best_hand, "ONE PAIR")
        self.assertEqual(h3.best_hand, "ONE PAIR")
        
    def test_two_pair(self):
        h1 = PokerHand('KH KS JC JD 8D')
        h2 = PokerHand('KD KC 8C JH JS')
        h3 = PokerHand('8D 8S 5H 5S AS')
        self.assertEqual(h1.best_hand, "TWO PAIR")
        self.assertEqual(h2.best_hand, "TWO PAIR")
        self.assertEqual(h3.best_hand, "TWO PAIR")
        
    def test_three_of_a_kind(self):
        h1 = PokerHand('JH QH JC JD 8D')
        h2 = PokerHand('JD QH 8C JH JS')
        h3 = PokerHand('AD KS TH TD TS')
        self.assertEqual(h1.best_hand, "THREE OF A KIND")
        self.assertEqual(h2.best_hand, "THREE OF A KIND")
        self.assertEqual(h3.best_hand, "THREE OF A KIND")
        
    def test_straight(self):
        h1 = PokerHand('4H 5H 6C 7D 8D')
        h2 = PokerHand('4D 5S 6D 7H 8S')
        h3 = PokerHand('3D 4S 5H 6D 7S')
        h4 = PokerHand('AD 3S 5H 2D 4S')
        self.assertEqual(h1.best_hand, "STRAIGHT")
        self.assertEqual(h2.best_hand, "STRAIGHT")
        self.assertEqual(h3.best_hand, "STRAIGHT")
        self.assertEqual(h4.best_hand, "STRAIGHT")
        
    def test_straight_flush(self):
        h1 = PokerHand('8H 9H TH JH QH')
        h2 = PokerHand('QS JS TS 9S 8S')
        h3 = PokerHand('9D TD JD QD KD')
        self.assertEqual(h1.best_hand, "STRAIGHT FLUSH")
        self.assertEqual(h2.best_hand, "STRAIGHT FLUSH")
        self.assertEqual(h3.best_hand, "STRAIGHT FLUSH")
        
    def test_royal_flush(self):
        h1 = PokerHand('TD JD QD KD AD')
        h2 = PokerHand('TH JH QH KH AH')
        self.assertEqual(h1.best_hand,"ROYAL FLUSH")
        self.assertEqual(h1.best_hand, "ROYAL FLUSH")
        self.assertNotEqual(h1.best_hand, "STRAIGHT FLUSH")


# UNIT TEST CASES FOR HAND COMPARISON
#This test cases have been proposed by I2A2

class TestPokercomparison(unittest.TestCase):
    def test_comparison(self):
        self.assertTrue(PokerHand("TC TH 5C 5H KH").compare_with(PokerHand("9C 9H 5C 5H AC")) == Result.WIN)
        self.assertTrue(PokerHand("TS TD KC JC 7C").compare_with(PokerHand("JS JC AS KC TD")) == Result.LOSS)
        self.assertTrue(PokerHand("7H 7C QC JS TS").compare_with(PokerHand("7D 7C JS TS 6D")) == Result.WIN)
        self.assertTrue(PokerHand("5S 5D 8C 7S 6H").compare_with(PokerHand("7D 7S 5S 5D JS")) == Result.LOSS)
        self.assertTrue(PokerHand("AS AD KD 7C 3D").compare_with(PokerHand("AD AH KD 7C 4S")) == Result.LOSS)
        self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("AC AH AS AS KS")) == Result.WIN)
        self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("TC JS QC KS AC")) == Result.WIN)
        self.assertTrue(PokerHand("TS JS QS KS AS").compare_with(PokerHand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(PokerHand("AC AH AS AS KS").compare_with(PokerHand("TC JS QC KS AC")) == Result.WIN)
        self.assertTrue(PokerHand("AC AH AS AS KS").compare_with(PokerHand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(PokerHand("TC JS QC KS AC").compare_with(PokerHand("QH QS QC AS 8H")) == Result.WIN)
        self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("JH JC JS JD TH")) == Result.WIN)
        self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("4H 5H 9H TH JH")) == Result.WIN)
        self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == Result.WIN)
        self.assertTrue(PokerHand("7H 8H 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("4H 5H 9H TH JH")) == Result.WIN)
        self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("TS TH TD JH JD")) == Result.WIN)
        self.assertTrue(PokerHand("JH JC JS JD TH").compare_with(PokerHand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("7C 8S 9H TH JH")) == Result.WIN)
        self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == Result.LOSS)
        self.assertTrue(PokerHand("4H 5H 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(PokerHand("7C 8S 9H TH JH").compare_with(PokerHand("TS TH TD JH JD")) == Result.LOSS)
        self.assertTrue(PokerHand("7C 8S 9H TH JH").compare_with(PokerHand("JH JD TH TC 4C")) == Result.WIN)
        self.assertTrue(PokerHand("TS TH TD JH JD").compare_with(PokerHand("JH JD TH TC 4C")) == Result.WIN)

if __name__ == '__main__':
    unittest.main()



