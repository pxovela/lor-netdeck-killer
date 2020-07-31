# import neccessary libraries
from flask import Flask, render_template, request, redirect
import add_cards as cards
import pandas as pd
from lor_deckcodes import LoRDeck, CardCodeAndCount
from add_cards import all_cards

#list of all champs and regions
regions = ['--none--', 'Bilgewater', 'Demacia', 'Freljord', 'Ionia', 'Noxus', 'Piltover & Zaun', 'Shadow Isles']

# function to generate deck links
def make_clickable(val):
    return '<a href="/deck_select/{}">Select Deck</a>'.format(val)

# define app
app = Flask(__name__)

# main page
@app.route('/')
def index():
        return render_template("index.html", regions=regions)

# capture selected regions
@app.route('/region_select', methods=['POST'])
def region_select():
    global deck_details
    global selected_regions
    global remaining_champs
    if request.method == 'POST':
        #list of all current decks
        deck_details = pd.read_csv('deck_details.csv')
        deck_details['links'] = deck_details['deck_code'].apply(make_clickable)
        # empty list for selected regions
        selected_regions = []
        selected_regions.append(request.form.get('region_1'))
        selected_regions.append(request.form.get('region_2'))
        selected_regions = [region for region in selected_regions if region != '--none--']
        remaining_champs = ['--none--']
        remaining_champions = cards.champions[cards.champions['region'].isin(selected_regions)]
        remaining_champions = remaining_champions['name'].to_list()
        remaining_champs.extend(remaining_champions)
        # filter deck list by regions
        if len(selected_regions)==2:
            deck_details = deck_details[(deck_details['region_1'].isin(selected_regions)) & (deck_details['region_2'].isin(selected_regions))]
        elif len(selected_regions)==1:
            deck_details = deck_details[(deck_details['region_1'].isin(selected_regions)) & (deck_details['region_2']=='None')]
        deck_details = deck_details[['matches_played', 'champion_1', 'champion_2', 'champion_3', 'champion_4', 'links']]
        tables = deck_details.to_html(classes='data', header="true", escape=False)
        return render_template("deck_select.html", remaining_champs=remaining_champs, tables=tables)

@app.route('/champ_select', methods=['GET', 'POST'])
def champ_select():
    global deck_details_ch
    if request.method == 'POST':
        tables = deck_details.to_html(classes='data', header="true")
        # empty list for selected champions
        selected_champions = []
        # get list of champs selected
        selected_champions.append(request.form.get('champion_1'))
        selected_champions.append(request.form.get('champion_2'))
        selected_champions.append(request.form.get('champion_3'))
        selected_champions.append(request.form.get('champion_4'))
        selected_champions = [champ for champ in selected_champions if champ != '--none--']
         # filter deck list by champions
        if len(selected_champions)==4:
            deck_details_ch = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3'].isin(selected_champions)) & (deck_details['champion_4'].isin(selected_champions))]
        elif len(selected_champions)==3:
            deck_details_ch = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3'].isin(selected_champions)) & (deck_details['champion_4']=='None')]
        elif len(selected_champions)==2:
            deck_details_ch = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3']=='None')]
        elif len(selected_champions)==1:
            deck_details_ch = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2']=='None')]
        else:
            deck_details_ch = deck_details
        tables = deck_details_ch.to_html(classes='data', header="true", escape=False)
    return render_template("deck_select.html", remaining_champs=remaining_champs, tables=tables)


@app.route('/deck_select/<deck_code>', methods=['GET', 'POST'])
def deck_select(deck_code):
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
    current_deck = current_deck[['name', 'count', 'cost', 'type', 'supertype', 'spellSpeed']]
    current_deck.sort_values(by=['cost'], inplace=True)
    deck_table = current_deck.to_html(classes='data', header="true")
    round_num = 1
    mana = 1
    spellmana = 0
    all_checked = 'checked'
    return render_template('deck_test.html', deck_table=deck_table, round_num=round_num, mana=mana, spellmana=spellmana, all_checked=all_checked, deck_code=deck_code)

@app.route('/deck_filter/<deck_code>', methods=['GET', 'POST'])
def deck_filter(deck_code):
    round_num = request.args['turn']
    mana = request.args['mana']
    spellmana = request.args['spellmana']
    card_type = request.args['card_type']
    #iterate through each card of the deck
    deck = LoRDeck.from_deckcode(deck_code)
    df = []
    for card in deck.cards:
        d = {
            'cardCode' : card.card_code,
            'count' : card.count
        }
        df.append(d)
    current_deck = pd.DataFrame(df)
    current_deck = current_deck.join(all_cards.set_index('cardCode'), on='cardCode', how='left')
    current_deck = current_deck[['name', 'count', 'cost', 'type', 'supertype', 'spellSpeed']]
    current_deck.sort_values(by=['cost'], inplace=True)
    opp_deck = current_deck
    if card_type == 'all_cards':
        all_checked = 'checked'
        fast_checked = ''
        burst_checked = ''
        spells = opp_deck.query('type=="Spell" and cost<={mana}+{spellmana}'.format(mana=mana,spellmana=spellmana))
        units = opp_deck.query('type=="Unit" and cost<={mana}'.format(mana=mana))
        all_possible = pd.concat([spells,units])
    elif card_type == 'fast':
        all_checked = ''
        fast_checked = 'checked'
        burst_checked = ''
        spells = opp_deck.query('type=="Spell" and spellSpeed!="Slow" and cost<={mana}+{spellmana}'.format(mana=mana,spellmana=spellmana))
        all_possible = spells
    elif card_type == 'burst':
        all_checked = ''
        fast_checked = ''
        burst_checked = 'checked'
        spells = opp_deck.query('type=="Spell" and spellSpeed=="Burst" and cost<={mana}+{spellmana}'.format(mana=mana,spellmana=spellmana))
        all_possible = spells
    deck_table = all_possible.to_html(classes='table table-striped p-3 my-3 border table-hover', header="true")
    return render_template('deck_test.html', deck_table=deck_table, round_num=round_num, mana=mana, spellmana=spellmana, card_type=card_type, all_checked=all_checked, fast_checked=fast_checked, burst_checked=burst_checked, deck_code=deck_code)

# run page
if __name__ == '__main__':
    app.debug=True
    app.run()