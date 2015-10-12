

#############
# Constants #
#############

# Index of the dependency property
MONSTER_AMOUNT = 3
HERO_AMOUNT = 4
VILLAGE_AMOUNT = 8

INDEX_NAME = 0
INDEX_TYPE = 1
INDEX_DEPENDENCIES = 2
INDEX_MAGIC_ATK = 3
INDEX_DISEASE = 4


# Class = [(cardname, [list of type], [list of dependencies], Have:magicAtk, Give:Disease)]
# if card have an "either-or" dependency, make it as a list
# Example: "Each player gains one disease unless they reveal a cleric or thief"
# WARNING: works only with type, not Have:magicAtk or Give:Disease


HEROES = set([
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


MONSTERS = set([
        ('Doomknight - Humanoid', ('Doomknight', 'Humanoid'), ('fighter',), False, False),
        ('Undead - Spirit', ('Undead', 'Spirit'), ('magicAtk',), False, False),
        ('Undead - Doom', ('Undead', 'Doom'), ('spell',), False, True),
        ('Dragon', ('dragon',), ('magicAtk',), False, False),
        ('Abyssal', ('abyssal',), ('magicAtk', 'cleric'), False, True),
        ('Humanoid', ('humanoid',), (), False, True),
        ('Ooze', ('ooze',), ('magicAtk',), False, False),
        ('Enchanted', ('enchanted',), ('magicAtk',), False, False)
        ])


VILLAGERS = set([
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

