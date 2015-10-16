#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import random
import tCards


class ClassSelector(object):
    
    """selector for forced or blacklisted cards"""
    
    def __init__(self, whitelist, blacklist):
        """
        :whitelist: through gui-defined cards that is wanted in selection
        :blacklist: through gui-defined cards that is excluded from selection
        """
        
        self.whitelist = whitelist
        self.blacklist = blacklist
        

class Selection(object):

    """Selection of 3 monster cards, 4 heroes and 8 village cards"""

    def __init__(self, m, h, v):
        """Needs lists of cards of each type"""

        # Initiate the internal lists
        self.m = m
        self.h = h
        self.v = v

    def __str__(self):
        string = ''
        for card in self.m:
            string += card[tCards.INDEX_NAME] + '\n'
        for card in self.h:
            string += card[tCards.INDEX_NAME] + '\n'
        for card in self.v:
            string += card[tCards.INDEX_NAME] + '\n'

        return string

    def validate(self):
        """True if all dependencies are met for this Selection
        :returns: Boolean

        """

        # List of all cards in the selection
        allCards = self.m | self.h | self.v

        for card in allCards:
            # Iterate over each cards dependencies
            for dep in card[tCards.INDEX_DEPENDENCIES]:
                if not depChk(dep, allCards):
                    # If any dependency is unmet, exit early
                    return False

        return True


MAX_TRIES = 1000

EMPTY_SELECTOR = ClassSelector(set([]), set([]))


def selectionHelper(subset, superset, length):
    """
    Make a subset of a given length.

    :subset: A set. A subset of superset. Could be empty.
    :superset: A set. A superset of subset.
    :length: A number. The desired cardinality of the returned set
    :returns: A set of cardinality length

    """

    # The original length of the subset
    subset_length = len(subset)

    # If the subset has too many items
    if subset_length > length:
        # Randomly take 'length' number of unique items from subset
        return set(random.sample(subset, length))

    # Else, if the subset is too small
    elif subset_length < length:
        # Add random unique elements from the complement until given length
        subset_complement = superset - subset
        return subset | set(random.sample(
            subset_complement, length - subset_length))

    # If none of the conditions apply, just return the subset
    return subset


def getSelection(monster=EMPTY_SELECTOR,
                 hero=EMPTY_SELECTOR,
                 village=EMPTY_SELECTOR,
                 maxTries=MAX_TRIES):
    """
    Generate a random selection according to the rules
    and satisfying all dependencies

    :m: set of monsters
    :h: list of heroes
    :v: list of villagers
    :returns: Selection
    """

    allowedMonsters = tCards.MONSTERS - monster.blacklist
    preferredMonsters = monster.whitelist

    allowedHeroes = tCards.HEROES - hero.blacklist
    preferredHeroes = hero.whitelist

    allowedVillagers = tCards.VILLAGERS - village.blacklist
    preferredVillagers = village.whitelist

    # Randomly generate selections until a valid selection is found
    # Maximum of maxTries tries
    counter = 0
    validated = False
    while validated is False:

        # If necessary, modify the input sets
        m = selectionHelper(preferredMonsters,
                            allowedMonsters,
                            tCards.MONSTER_AMOUNT)
        h = selectionHelper(preferredHeroes,
                            allowedHeroes,
                            tCards.HERO_AMOUNT)
        v = selectionHelper(preferredVillagers,
                            allowedVillagers,
                            tCards.VILLAGE_AMOUNT)

        # Increment counter after each selection process
        counter += 1

        # Make a selection object and valudate it
        selection = Selection(m, h, v)
        validated = selection.validate()

        # Exit if too many tries are needed
        if counter >= maxTries:
            break

    return selection


def depChk(dep, cards):

    """
    dep = dependency (string)
    cards = list of tupels

    Controls if dependency is satisfied by the list of selected cards
    Returns : bool, true if all dependencies are met in any of the cards
    """

    if isinstance(dep, tuple):
        # se om dep är en lista (vilket härleder en "either or-dependency")
        # kollar sedan om något av kriterierna blir bemötta.
        for card in cards:
            for indvdep in dep:
                if indvdep in card[tCards.INDEX_TYPE]:
                    return True

    elif dep == 'fighter' or dep == 'spell':
        # se om något kort är av typ 'fighter' från lista
        for card in cards:
            if dep in card[tCards.INDEX_TYPE]:
                return True

    elif dep == 'magicAtk':
        # se om något kort innehåller boolen magicAtk == True
        for card in cards:
            if card[tCards.INDEX_MAGIC_ATK]:
                return True

    elif dep == 'disease':
        # se om något kort innehåller boolen disease == True
        for card in cards:
            if card[tCards.INDEX_DISEASE]:
                return True
    elif dep == 'cleric':
        return True

    return False

"""
construct selection
input lists (of monsters, heroes and villagers)
output object (with the randomized selected cards

check if valid
input (self)
output bool (if selected cards are an acceptable choice)

if bool
    contine program (display choice)
else
    redo selection
"""
