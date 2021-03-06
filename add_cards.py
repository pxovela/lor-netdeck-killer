# imnport libraries
import glob
import pandas as pd

# get file names of files with card data
card_data_files = glob.glob("lor cards/*")

#create empty dataframe to store all cards data
all_cards = pd.DataFrame()

# iterate through card data files and append all data to all_cards dataframe
for sets in card_data_files:
    current_set = pd.read_json(sets, orient=str)
    current_set = current_set[['cardCode','cost', 'spellSpeed', 'type', 'supertype', 'name', 'region']]
    all_cards = all_cards.append(current_set)

champions = all_cards.loc[(all_cards['supertype']=='Champion') & (all_cards['type']=='Unit')]
champions = champions[['name', 'region']].drop_duplicates()
#print(champions)