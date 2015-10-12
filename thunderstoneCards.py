#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import random

#############
# Constants #
#############

# Index of the dependency property
MONSTER_AMOUNT = 3
HERO_AMOUNT = 4
VILLAGE_AMOUNT = 8

CARD_NAME = 0
CARD_TYPE = 1
CARD_DEPENDENCIES = 2
CARD_MAGIC_ATK = 3
CARD_DISEASE = 4

MAX_TRIES = 1000

EMPTY_SELECTOR = ClassSelector(set([]), set([]))


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
            string += card[CARD_NAME] + '\n'
        for card in self.h:
            string += card[CARD_NAME] + '\n'
        for card in self.v:
            string += card[CARD_NAME] + '\n'

        return string

    def validate(self):
        """True if all dependencies are met for this Selection
        :returns: Boolean

        """

        # List of all cards in the selection
        allCards = self.m | self.h | self.v

        for card in allCards:
            # Iterate over each cards dependencies
            for dep in card[CARD_DEPENDENCIES]:
                if not depChk(dep, allCards):
                    # If any dependency is unmet, exit early
                    return False

        return True


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
                 villager=EMPTY_SELECTOR,
                 maxTries=MAX_TRIES):
    """
    Generate a random selection according to the rules
    and satisfying all dependencies

    :m: set of monsters
    :h: list of heroes
    :v: list of villagers
    :returns: Selection
    """

    allowedMonsters = monsters - monster.blacklist
    preferredMonsters = monster.whitelist

    allowedHeroes = heroes - hero.blacklist
    preferredHeroes = hero.whitelist

    allowedVillagers = villagers - villager.blacklist
    preferredVillagers = villager.whitelist

    # Randomly generate selections until a valid selection is found
    # Maximum of maxTries tries
    counter = 0
    validated = False
    while validated is False:

        # If necessary, modify the input sets
        m = selectionHelper(preferredMonsters,
                            allowedMonsters,
                            MONSTER_AMOUNT)
        h = selectionHelper(preferredHeroes,
                            allowedHeroes,
                            HERO_AMOUNT)
        v = selectionHelper(preferredVillagers,
                            allowedVillagers,
                            VILLAGE_AMOUNT)

        # Increment counter after each selection process
        counter += 1

        # Make a selection object and valudate it
        selection = Selection(m, h, v)
        validated = selection.validate()

        # Exit if too many tries are needed
        if counter >= maxTries:
            break

    return selection


# Class = [(cardname, [list of type], [list of dependencies], Have:magicAtk, Give:Disease)]
# if card have an "either-or" dependency, make it as a list
# Example: "Each player gains one disease unless they reveal a cleric or thief"
# WARNING: works only with type, not Have:magicAtk or Give:Disease


heroes = set([
        ('Chalice', ('fighter', 'cleric'), ('disease',), False, False),
        ('Redblade', ('fighter', 'thief'), (), False, False),
        ('Outlands', ('fighter',), (), False, False),
        ('Feayn', ('fighter', 'archer'), (), False, False),
        ('Regian', ('cleric',), (), True, False),
        ('Dwarf', ('fighter',), (), False, False),
        ('Selurin', ('wizard',), (), True, False),
        ('Elf', ('wizard',), (), True, False),
        ('Amazon', ('fighter', 'archer'), (), False, False),
        ('Lorigg', ('thief',), (), False, False),
        ('Thyrian', ('fighter',), (), False, False)
        ])


monsters = set([
        ('Doomknight - Humanoid', ('Doomknight', 'Humanoid'), ('fighter',), False, False),
        ('Undead - Spirit', ('Undead', 'Spirit'), ('magicAtk',), False, False),
        ('Undead - Doom', ('Undead', 'Doom'), ('spell',), False, True),
        ('Dragon', ('dragon',), ('magicAtk',), False, False),
        ('Abyssal', ('abyssal',), ('magicAtk', 'cleric'), False, True),
        ('Humanoid', ('humanoid',), (), False, True),
        ('Ooze', ('ooze',), ('magicAtk',), False, False),
        ('Enchanted', ('enchanted',), ('magicAtk',), False, False)
        ])


villagers = set([
        ('Flaming Sword', ('weapon', 'edged'), (), True, False),
        ('Arcane Energies', ('spell',), (), True, False),
        ('Short Sword', ('weapon', 'edged'), (), True, False),
        ('Spear', ('weapon', 'edged'), (), False, False),
        ('Fireball', ('spell',), (), True, False),
        ('Trainer', ('villager',), (), False, False),
        ('Town Guard', ('villager',), (), False, False),
        ('Battle Fury', ('spell',), (), False, False),
        ('Banish', ('spell',), (), False, False),
        ('Magical Aura', ('spell',), (), False, False),
        ('Lightstone Gem', ('item', 'light', 'magic'), (), False, False),
        ('Feast', ('item', 'food'), (), False, False),
        ('Goodberries', ('item', 'food', 'magic'), (), True, False),
        ('Hatchet', ('weapon', 'edged'), (), False, False),
        ('Pawnbroker', ('villager',), (), False, False),
        ('Barkeep', ('villager',), (), False, False),
        ('Lantern', ('item', 'light'), (), False, False),
        ('Warhammer', ('weapon', 'blunt'), (), False, False),
        ('Polearm', ('weapon', 'edged'), (), False, False)
        ])


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
                if indvdep in card[CARD_TYPE]:
                    return True

    elif dep == 'fighter' or dep == 'spell':
        # se om något kort är av typ 'fighter' från lista
        for card in cards:
            if dep in card[CARD_TYPE]:
                return True

    elif dep == 'magicAtk':
        # se om något kort innehåller boolen magicAtk == True
        for card in cards:
            if card[CARD_MAGIC_ATK]:
                return True

    elif dep == 'disease':
        # se om något kort innehåller boolen disease == True
        for card in cards:
            if card[CARD_DISEASE]:
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
