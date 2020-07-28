# import neccessary libraries
from flask import Flask, render_template, request, redirect
import add_cards as cards
import pandas as pd

#list of all champs and regions
regions = ['--none--', 'Bilgewater', 'Demacia', 'Freljord', 'Ionia', 'Noxus', 'Piltover & Zaun', 'Shadow Isles']
#list of all current decks
global deck_details
deck_details = pd.read_csv('deck_details.csv')

# define app
app = Flask(__name__)

# main page
@app.route('/')
def index():
        return render_template("index.html", regions=regions)

# capture selected regions
@app.route('/champ_select', methods=['POST'])
def champ_select():
    global deck_details
    global selected_regions
    global remaining_champs
    global tables
    if request.method == 'POST':
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
        deck_details = deck_details[['matches_played', 'champion_1', 'champion_2', 'champion_3', 'champion_4']]
        tables = deck_details.to_html(classes='data', header="true")
        return render_template("deck_select.html", remaining_champs=remaining_champs, tables=tables)

@app.route('/deck_select', methods=['POST'])
def deck_select():
    global deck_details
    global tables
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
        print(selected_champions)
        print(len(selected_champions))
         # filter deck list by champions
        if len(selected_champions)==4:
            deck_details = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3'].isin(selected_champions)) & (deck_details['champion_4'].isin(selected_champions))]
        elif len(selected_champions)==3:
            deck_details = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3'].isin(selected_champions)) & (deck_details['champion_4']=='None')]
        elif len(selected_champions)==2:
            deck_details = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2'].isin(selected_champions)) & (deck_details['champion_3']=='None')]
        elif len(selected_champions)==1:
            deck_details = deck_details[(deck_details['champion_1'].isin(selected_champions)) & (deck_details['champion_2']=='None')]
        tables = deck_details.to_html(classes='data', header="true")
    return render_template("deck_select.html", remaining_champs=remaining_champs, tables=tables)



# run page
if __name__ == '__main__':
    app.debug=True
    app.run()