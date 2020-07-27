# import neccessary libraries
from flask import Flask, render_template, request, redirect
import add_cards as cards

#list of all champs and regions
champions = ['Anivia', 'Ashe', 'Braum', 'Darius', 'Draven']
regions = ['--none--', 'Bilgewater', 'Demacia', 'Freljord', 'Ionia', 'Noxus', 'Piltover & Zaun', 'Shadow Isles']

# define app
app = Flask(__name__)

# main page
@app.route('/')
def index():
        return render_template("index.html", regions=regions)

# empty list for selected regions
selected_regions = []

# capture selected regions
@app.route('/deck_select', methods=['POST'])
def deck_select():
    if request.method == 'POST':
        selected_regions.append(request.form.get('region_1'))
        selected_regions.append(request.form.get('region_2'))
        print(selected_regions)
        remaining_champions = cards.champions[cards.champions['region'].isin(selected_regions)]
        remaining_champions = remaining_champions['name'].to_list()
        print(remaining_champions)
        return render_template("deck_select.html", remaining_champions=remaining_champions)

# run page
if __name__ == '__main__':
    app.debug=True
    app.run()