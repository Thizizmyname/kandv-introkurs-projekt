# Class = [(cardname, [list of type], [list of dependencies], Have:magicAtk, Give:Disease)]


heroes = [
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
        ]


monsters = [
        ('Doomknight - Humanoid', ['Doomknight', 'Humanoid'], ['fighter'], False, False),
        ('Undead - Spirit', ['Undead', 'Spirit'], ['magicAtk'], False, False),   # OBS kolla upp magicAtk-dependency
        ('Undead - Doom', ['Undead', 'Doom'], ['spell'], False, True), 
        ('Dragon', ['dragon'], ['magicAtk'], False, False),
        ('Abyssal', ['abyssal'], ['magicAtk', 'cleric'], False, True),
        ('Humanoid', ['humanoid'], [], False, True),
        ('Ooze', ['ooze'], ['magicAtk'], False, False),
        ('Enchanted', ['enchanted'], ['magicAtk'], False, False)
        ]


villagers = [
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
        ]

CARDTYPE = 1
CARDMAGICATK = 3
CARDDISEASE = 4
    


def depchk(dep, cards):
    
    """
    dep = dependency (string)
    cards = list of tupels

    Controls if dependency is satisfied by the list of selected cards
    Returns : bool, true if all dependencies are met in any of the cards
    """




    if dep == 'fighter' or dep == 'cleric' or dep == 'spell':
        # se om något kort är av typ 'fighter' från lista
        for card in cards:
            if dep in cards(CARDTYPE):
                return True
        
        
    elif dep == 'magicAtk':
        # se om något kort innehåller boolen magicAtk == True
        for card in cards:
            if cards(CARDMAGICATK):
                return True

    elif dep == 'disease'
        # se om något kort innehåller boolen disease == True
        for card in cards:
            if cards(CARDDISEASE):
                return True






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
