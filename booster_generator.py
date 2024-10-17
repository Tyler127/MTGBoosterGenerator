# Created on 1/27/24 with regular booster functionality
# Updated on 2/6/24 to add commander booster and staples functionality

import csv
import random
from tabulate import tabulate as tabulate_function

# Input and Output Options
INPUT_FILE_PATH = 'karlovcards.csv'
OUTPUT_FILE_PATH = 'boosters.txt'

# Booster Options
NUM_BOOSTERS = 10

# Singleton Options
IS_SINGLETON = False # If True, each card will be placed in a booster at most once.
CARDS_PER_BOOSTER = 20 

# Commander Options
IS_COMMANDER = False # Enables staples in each booster.
STAPLE_CARDS_PERCENT = .15 # The percent of cards in each booster that will be staples.
STAPLES_FILE_PATH = "staples.csv"

# Rarity Options
IGNORE_RARITIES = False # Allows cards of any rarity to be put in any slot.
MYTHIC_ODDS = .125 # The chance for the rare slots to be replaced by mythic slots.
MYTHICS_PER_BOOSTER = 1 # The maximum amount of rares that can be replaced by mythics, unless IGNORE_RARITIES is flagged in which case this many will appear
RARES_PER_BOOSTER = 1
UNCOMMONS_PER_BOOSTER = 3
COMMONS_PER_BOOSTER = 10

# Output Options
PRINT_ALL_CARDS = False # Prints all cards to the terminal
PRINT_BOOSTERS = True # Prints formatted boosters to the terminal
PRINT_MTG_PRINT_LIST = False # Print the cards in the boosters in a list formatted for use on mtgprint.net to the terminal
CREATE_OUTPUT_FILE = True 


'''
Commander Draft:
    - 12 packs
    - 20 cards per pack
    - Singleton
    - 25% staples per booster
'''


all_cards = []
mythic_cards = []
rare_cards = []
uncommon_cards = []
common_cards = []
staple_cards = []


class Card:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity


def print_all_cards():
    # Print the cards in each rarity list
    print("Mythic Cards: "  + str(len(mythic_cards)))
    for card in mythic_cards:
        print(f"    Name: {card.name}")

    print("\nRare Cards: "  + str(len(rare_cards)))
    for card in rare_cards:
        print(f"    Name: {card.name}")

    print("\nUncommon Cards: "  + str(len(uncommon_cards)))
    for card in uncommon_cards:
        print(f"    Name: {card.name}")

    print("\nCommon Cards: " + str(len(common_cards)))
    for card in common_cards:
        print(f"    Name: {card.name}")
    
    print("\nTotal Cards: " + str(len(all_cards)))


def validate_config():
    if IS_SINGLETON:
        minimum_cards = 0
        if IGNORE_RARITIES:
            if IS_COMMANDER:
                # Ensure there are enough staple cards for all boosters
                minimum_cards = int(CARDS_PER_BOOSTER * STAPLE_CARDS_PERCENT) * NUM_BOOSTERS 
                if minimum_cards > len(staple_cards):
                    print(f'ERROR: Not enough staple cards! Need at least {minimum_cards - len(staple_cards)} more unique staple cards.')
                    exit()

            minimum_cards = NUM_BOOSTERS * CARDS_PER_BOOSTER
            if minimum_cards > len(all_cards):
                print(f'ERROR: Not enough unique cards! Need at least {minimum_cards  - len(all_cards)} more unique cards.')
                exit()
        else:
            minimum_cards = NUM_BOOSTERS * MYTHICS_PER_BOOSTER
            if minimum_cards > len(mythic_cards):
                print(f'ERROR: Not enough unique mythic cards! Need at least {minimum_cards - len(mythic_cards)} more unique cards.')
                exit()

            minimum_cards = NUM_BOOSTERS * RARES_PER_BOOSTER
            if minimum_cards > len(rare_cards):
                print(f'ERROR: Not enough unique rare cards! Need at least {minimum_cards - len(rare_cards)} more unique cards.')
                exit()

            minimum_cards = NUM_BOOSTERS * UNCOMMONS_PER_BOOSTER
            if minimum_cards > len(uncommon_cards):
                print(f'ERROR: Not enough unique uncommon cards! Need at least {minimum_cards - len(uncommon_cards)} more unique cards.')
                exit()

            minimum_cards = NUM_BOOSTERS * COMMONS_PER_BOOSTER
            if minimum_cards > len(common_cards):
                print(f'ERROR: Not enough unique common cards! Need at least {minimum_cards - len(common_cards)} more unique cards.')
                exit()


def read_csv_and_sort_cards(file_path):
    with open(file_path, 'r') as csv_file:
        card_names_read = []
        csv_reader = csv.reader(csv_file)

        # Skip the header if exists
        next(csv_reader, None)

        for row in csv_reader:
            if len(row) >= 2:
                card_name = row[0]
                if IGNORE_RARITIES:
                    card_rarity = "I"
                else:
                    card_rarity = row[1]

                # Create a Card object
                card = Card(name=card_name, rarity=card_rarity)

                if card_name in card_names_read:
                    continue

                # Sort the card into the corresponding rarity list
                if card_rarity == 'M':
                    mythic_cards.append(card)
                elif card_rarity == 'R':
                    rare_cards.append(card)
                elif card_rarity == 'U':
                    uncommon_cards.append(card)
                elif card_rarity == 'C':
                    common_cards.append(card)

                # Add the card name to the set to track uniqueness
                all_cards.append(card)
                card_names_read.append(card_name)


def read_staple_cards_csv():
    with open(STAPLES_FILE_PATH, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header if exists
        next(csv_reader, None)

        for row in csv_reader:
            if len(row) >= 2:
                card_name = row[0]
                card_rarity = row[1]

                # Create a Card object
                card = Card(name=card_name, rarity=card_rarity)
                staple_cards.append(card)

    return staple_cards


def create_booster():
    # Draft Boosters (typically) have 10 commons, 3 uncommon_cardss, and 1 rare or mythic rare (these numbers don't include traditional foils, which aren't in every booster). 
    booster = []

    if IGNORE_RARITIES:
        booster.extend(random.sample(all_cards, (MYTHICS_PER_BOOSTER + RARES_PER_BOOSTER + UNCOMMONS_PER_BOOSTER + COMMONS_PER_BOOSTER)))
        return booster

    has_mythic = False
    if random.uniform(0.0, 1.0) <= MYTHIC_ODDS:
        has_mythic = True

    if has_mythic:
        booster.extend(random.sample(mythic_cards, MYTHICS_PER_BOOSTER))
    else: 
        booster.extend(random.sample(rare_cards, RARES_PER_BOOSTER))
    
    booster.extend(random.sample(uncommon_cards, UNCOMMONS_PER_BOOSTER))
    booster.extend(random.sample(common_cards, COMMONS_PER_BOOSTER))

    return booster


def create_singleton_booster(cards_per_booster=CARDS_PER_BOOSTER):
    booster = []

    if IGNORE_RARITIES:
        for i in range(cards_per_booster):
            card = all_cards.pop(random.randint(0, len(all_cards)-1))
            booster.append(card)
    
    else:
        for i in range(MYTHICS_PER_BOOSTER):
            card = mythic_cards.pop(random.randint(0, len(mythic_cards)-1))
            booster.append(card)
        for i in range(RARES_PER_BOOSTER):
            card = rare_cards.pop(random.randint(0, len(rare_cards)-1))
            booster.append(card)
        for i in range(UNCOMMONS_PER_BOOSTER):
            card = uncommon_cards.pop(random.randint(0, len(uncommon_cards)-1))
            booster.append(card)
        for i in range(COMMONS_PER_BOOSTER):
            card = common_cards.pop(random.randint(0, len(common_cards)-1))
            booster.append(card)

    return booster


# TODO: Implement functionality for using rarities and non-singleton boosters
def create_commander_booster():
    booster = []

    # Calculate the number of staple cards based on the specified percentage
    num_staples = int(CARDS_PER_BOOSTER * STAPLE_CARDS_PERCENT)

    # Use create_singleton_booster function to create a singleton booster
    if IGNORE_RARITIES and IS_SINGLETON:
        booster = create_singleton_booster(cards_per_booster=(CARDS_PER_BOOSTER - num_staples))

    # Add staple cards to the booster
    for i in range(num_staples):
        card = staple_cards.pop(random.randint(0, len(staple_cards)-1))
        booster.append(card)

    return booster


if __name__ == "__main__":
    # Read the CSV file and sort cards by rarity
    read_csv_and_sort_cards(INPUT_FILE_PATH)

    # Read and sort staple cards
    read_staple_cards_csv()

    # Ensure the config settings will work with the cards
    validate_config()

    if PRINT_ALL_CARDS:
        print_all_cards()

    boosters = []
    if IS_COMMANDER:
        boosters = [create_commander_booster() for i in range(NUM_BOOSTERS)]
    elif IS_SINGLETON:
        boosters = [create_singleton_booster() for i in range(NUM_BOOSTERS)]
    else:
        boosters = [create_booster() for i in range(NUM_BOOSTERS)]

    if PRINT_BOOSTERS:
        for i in range(NUM_BOOSTERS):
            print(f'\nBooster {i+1}:')
            table_data = [[card.rarity, card.name] for card in boosters[i]]
            print(tabulate_function(table_data, headers=["Rarity", "Name"], tablefmt="pretty"))

    if PRINT_MTG_PRINT_LIST:
        print('\n')
        for booster in boosters:
            for card in booster:
                print(f'1 {card.name}')

    if CREATE_OUTPUT_FILE:
        with open(OUTPUT_FILE_PATH, 'w') as file:
            for booster in boosters:
                for card in booster:
                    file.write(f'1 {card.name}\n')

    