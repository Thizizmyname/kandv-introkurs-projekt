#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Class = [(cardname, [list of type], [list of dependencies], Have:magicAtk, Give:Disease)]

import random

#############
# Constants #
#############

#Index of the dependency property 
MONSTERAMOUNT = 3
HEROAMOUNT = 4
VILLAGEAMOUNT = 8
CARDDEPENDENCIES = 2

class Selection(object):

    """Selection of 3 monster cards, 4 heroes and 8 village cards"""

    def __init__(self, m, h, v):
        """Needs lists of cards of each type"""

        # Initiate the internal lists
        self.m = m
        self.h = h
        self.v = v

    def validate(self):
        """True if all dependencies are met for this Selection
        :returns: Boolean

        """

        # List of all cards in the selection
        allCards = m + h + v

        for card in allCards:
            # Iterate over each cards dependencies
            for dep in card[CARDDEPENDENCIES]:
                if not depChk(dep, allCards):
                    # If any dependency is unmet, exit early
                    return False

        return True


def selectionHelper(subset, superset, length):
    """TODO: Docstring for selectionHelper.

    :subset: A set. A subset of superset. Could be empty.
    :superset: A set. A superset of subset.
    :length: A number. The desired cardinality of the returned set
    :returns: A set of cardinality length

    """

    subset_length = len(subset)
    if subset_length > length:
        return set(random.sample(subset, 3))
    elif subset_length < length:
        subset_complement = superset - subset
        return subset + set(random.sample(subset_complement, length - subset_length))

    return subset


def getSelection(m = set([]), h = set([]), v = set([])):
    """Generate a random selection according to the rules
    and satisfying all dependencies

    :m: set of monsters
    :h: list of heroes
    :v: list of villagers
    :returns: Selection
    """

    validated = False
    while validated is False:

        m = selectionHelper(m, monsters, MONSTERAMOUNT)
        h = selectionHelper(h, heroes, HEROAMOUNT)
        v = selectionHelper(v, villagers, VILLAGEAMOUNT)

        selection = Selection(m, h, v)

        validated = selection.validate()

    return selection
    




heroes = set([
        ('Chalice', ['fighter', 'cleric'], ['disease'], False, False),
        ('Redblade', ['fighter', 'thief'], [], False, False),
        ('Outlands', ['fighter'], [], False, False),
        ('Feayn', ['fighter', 'archer'], [], False, False),
        ('Regian', ['cleric'], [], True, False),
        ('Dwarf', ['fighter'], [], False, False),
        ('Selurin', ['wizard'], [], True, False),
        ('Elf', ['wizard'], [], True, False),
        ('Amazon', ['fighter', 'archer'], [], False, False),
        ('Lorigg', ['thief'], [], False, False),
        ('Thyrian', ['fighter'], [], False, False)
        ])


monsters = set([
        ('Doomknight - Humanoid', ['Doomknight', 'Humanoid'], ['fighter'], False, False),
        ('Undead - Spirit', ['Undead', 'Spirit'], ['magicAtk'], False, False),   # OBS kolla upp magicAtk-dependency
        ('Undead - Doom', ['Undead', 'Doom'], ['spell'], False, True), 
        ('Dragon', ['dragon'], ['magicAtk'], False, False),
        ('Abyssal', ['abyssal'], ['magicAtk', 'cleric'], False, True),
        ('Humanoid', ['humanoid'], [], False, True),
        ('Ooze', ['ooze'], ['magicAtk'], False, False),
        ('Enchanted', ['enchanted'], ['magicAtk'], False, False)
        ])


villagers = set([
        ('Flaming Sword', ['weapon', 'edged'], [], True, False),
        ('Arcane Energies', ['spell'], [], True, False),
        ('Short Sword', ['weapon', 'edged'], [], True, False),
        ('Spear', ['weapon', 'edged'], [], False, False),
        ('Fireball', ['spell'], [], True, False),
        ('Trainer', ['villager'], [], False, False),
        ('Town Guard', ['villager'], [], False, False),
        ('Battle Fury', ['spell'], [], False, False),
        ('Banish', ['spell'], [], False, False),
        ('Magical Aura', ['spell'], [], False, False),
        ('Lightstone Gem', ['item', 'light', 'magic'], [], False, False),
        ('Feast', ['item', 'food'], [], False, False),
        ('Goodberries', ['item', 'food', 'magic'], [], True, False),
        ('Hatchet', ['weapon', 'edged'], [], False, False),
        ('Pawnbroker', ['villager'], [], False, False),
        ('Barkeep', ['villager'], [], False, False),
        ('Lantern', ['item', 'light'], [], False, False),
        ('Warhammer', ['weapon', 'blunt'], [], False, False),
        ('Polearm', ['weapon', 'edged'], [], False, False)
        ])
