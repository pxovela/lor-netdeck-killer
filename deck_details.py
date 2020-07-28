# import neccessary libraries
import pandas as pd
from add_cards import all_cards
from lor_deckcodes import LoRDeck, CardCodeAndCount
#import seleniumtest

#load all decks
all_decks = pd.read_csv('results.csv')

#create list of all deck codes
all_deck_codes = all_decks['deck_code'].to_list()


#itirate through deck codes
deck_details = []
for deck_code in all_deck_codes:
    deck = LoRDeck.from_deckcode(deck_code)
    #iterate through each card of the deck
    df = []
    for card in deck.cards:
        d = {
            'cardCode' : card.card_code,
            'count' : card.count
        }
        df.append(d)
    current_deck = pd.DataFrame(df)
    current_deck = current_deck.join(all_cards.set_index('cardCode'), on='cardCode', how='left')
    deck_champions = current_deck.loc[(current_deck['supertype']=='Champion') & (current_deck['type']=='Unit')].drop_duplicates()
    deck_champions = deck_champions['name'].drop_duplicates()
    deck_regions = current_deck['region'].drop_duplicates()
    #find region 1
    try:
        region_1 = deck_regions.iloc[0]
    except:
        region_1 = 'None'
    #find region 2
    try:
        region_2 = deck_regions.iloc[1]
    except:
        region_2 = 'None'
    #find champ 1
    try:
        champion_1 = deck_champions.iloc[0]
    except:
        champion_1 = 'None'
    #find champ 2
    try:
        champion_2 = deck_champions.iloc[1]
    except:
        champion_2 = 'None'
    #find champ 2
    try:
        champion_3 = deck_champions.iloc[2]
    except:
        champion_3 = 'None'
    #find champ 2
    try:
        champion_4 = deck_champions.iloc[3]
    except:
        champion_4 = 'None'
    
    dd = {
        'deck_code' : deck_code,
        'region_1' : region_1,
        'region_2' : region_2,
        'champion_1' : champion_1,
        'champion_2' : champion_2,
        'champion_3' : champion_3,
        'champion_4' : champion_4
    }
    deck_details.append(dd)

deck_details = pd.DataFrame(deck_details)
all_decks = all_decks[['deck_code', 'matches_played']]
all_decks = deck_details.join(all_decks.set_index('deck_code'), on='deck_code', how='left')
all_decks.to_csv('deck_details.csv')
