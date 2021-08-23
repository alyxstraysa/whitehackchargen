import random

def select_random_occupation():
    occupations = """
    Actor,Advocate,Alchemist,
    Animal Handler,Apothecary,Architect,
    Archer,Archivist,Aristocrat,
    Armorer,Artisan,Artist,
    Astrologer,Baker,Banker,
    Barbarian,Barber,Bard,
    Barkeep,Barmaid,Beekeeper,
    Beer Seller,Beggar,Blacksmith,
    Boatman,Bookbinder,Bookseller,
    Brewer,Bricklayer,Brick Maker,
    Brigand,Brothel Keeper,Buckle Maker,
    Builder,Butcher,Caravan Leader,
    Carpenter,Cartographer,Chandler,
    Charioteer,Chatelaine,Chef,
    Chieftain,Chirurgeon,Clergyman,
    Clerk,Clockmaker,Clothworker,
    Cobbler,Commander,Concubine,
    Cook,Cooper,Copyist, Counselor,Courtesan,
    Courtier,Cowherd,Crossbowman,
    Cutler,Daimyo, Maid,
    Dancer,Dictator,Diplomat,
    Distiller,Diver,Diviner,
    Doctor, Emperor,Empress,
    Eunuch,Explorer,Farmer,
    Fighter,Fisherman,Fishmonger,
    Footman,Furrier,Galley Slave,
    Gardener,Geisha,General,
    Gladiator,Glovemaker,Goldsmith,
    Grocer,Groom,Guardsman,
    Guildmaster,Harness maker,Hatmaker,
    Hay merchant,Healer,Hearthwitch,
    Herald,Herbalist,Herder,
    Hermit,Highwayman,Historian,
    Housemaid,Hunter,Illuminator,
    Infantryman,Innkeeper,Interpreter,
    Inventor,Jailer,Jester,
    Jeweler, Judge,
    King,Kitchen Wench, Knight,
    Laborer,Lady,Lady in Waiting,
    Leatherworker,Librarian,Linguist,
    Locksmith,Longbowman,Longshoreman,
    Lord,Maidservant,Majordomo,
    Man at Arms,Mason,Masseur,
    Mayor,Mercer,Merchant,
    Messenger,Midwife,Miller,
    Miner,Minister,Minstrel,
    Monk,Mortician,Mourner,
    Musician,Necromancer,Noble,
    Nun,Nurse, Clothing Seller,
    Page,Painter,Pariah, Peasant,Perfumer,
    Philosopher,Physician,Pigkeeper,
    Pilgrim,Pirate,Plasterer,
    Potter, Priest, Priestess, Prince, Princess,
    Privateer,Professor,Prostitute,
    Pursemaker,Queen,Ranger,
    Ratcatcher,Reeve,Ronin,
    Roofer,Ropemaker,Royal Adviser,
    Rugmaker,Ruler,Saddler,
    Sailor,Samurai,Scabbard maker,
    Sculptor,Scavenger,Scholar,
    Scrivener,Seamstress,Servant,
    Shaman,Shepherd, Captain,
    Shoemaker,Silversmith,Slave,
    Slaver,Smith,Soldier,
    Sorcerer, Sorceress,Spice Merchant,Squire,
    Stablehand,Stevedore,Stonemason,
    Storyteller,Steward,Street Urchin, Street Sweeper,Student,
    Surgeon,Surveyor,Swordsman,
    Sycophant,Tailor,Tanner,
    Tavernkeeper,Tax Collector,Teacher,
    Teamster,Thatcher, Thief,
    Tinker, Torturer, Town Crier,
    Toymaker,Trapper,Vendor,
    Ratter,Veterinarian,Village Chief,
    Vintner,Viking,Warlock,
    Warrior,Water Carrier, Weaver,
    Wetnurse, Witch,
    Wizard, Woodcarver, Woodcutter, Writer
    """

    occupation = random.choice(occupations.split(','))

    return occupation.strip()

def select_random_race():
    races = [
        'High Elf',
        'Drow',
        'Dwarf',
        'Tiefling',
        'Kobold',
        'Gargoyle'
    ]

    return random.choice(races)

def select_random_group(char_dict):
    group_list = ['str_group', 'dex_group', 'con_group', 'int_group', 'wis_group']
    group_select = random.choice(group_list)

    if char_dict[group_select] == None:
        return group_select
    else:
        group_list.remove(group_select)
        return select_random_group(char_dict)


def roll_stats():
    stat_list = []

    for i in range(4):
        stat_list.append(random.randint(1,6))
    stat_list.remove(min(stat_list))

    return sum(stat_list)

def generate_random_character(user_id, race=False):
    archetype = random.choice(['Strong', 'Deft', 'Wise'])
    char_dict = {
        'user_id': user_id,
        'archetype': archetype,
        'group1': None,
        'group2': None,
        'group3': None,
        'group4': None,
        'group5': None,
        'stat_str': roll_stats(),
        'stat_dex': roll_stats(),
        'stat_con': roll_stats(),
        'stat_int': roll_stats(),
        'stat_wis': roll_stats(),
        'str_group': None,
        'dex_group': None,
        'con_group': None,
        'int_group': None,
        'wis_group': None,
        'ST': None,
        'HP': None,
        'AC': None,
        'MV': None,
        'AV': None
    }

    if archetype == 'Strong':
        char_dict['ST'] = 5
        char_dict['HP'] = random.randint(1, 6) + 2
        char_dict['MV'] = 30
        char_dict['AV'] = 11
    elif archetype == 'Deft':
        char_dict['ST'] = 7
        char_dict['HP'] = random.randint(1, 6)
        char_dict['MV'] = 30
        char_dict['AV'] = 10
    elif archetype == 'Wise':
        char_dict['ST'] = 6
        char_dict['HP'] = random.randint(1, 6) + 1
        char_dict['MV'] = 30
        char_dict['AV'] = 10

    occupation = select_random_occupation()

    if race==True:
        char_dict['group1'] = select_random_race()
        random_group = select_random_group(char_dict)
        char_dict[random_group] = char_dict['group1']

        char_dict['group2'] = occupation
        random_group = select_random_group(char_dict)
        char_dict[random_group] = char_dict['group2']
    else:
        char_dict['group1'] = occupation
        random_group = select_random_group(char_dict)
        char_dict[random_group] = char_dict['group1']

    return char_dict

if __name__ == '__main__':
    print(generate_random_character('Test123', False))