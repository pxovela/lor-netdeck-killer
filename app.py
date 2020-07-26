# import neccessary libraries
from flask import Flask, render_template, request, redirect

#list of all champs and regions
champions = ['Anivia', 'Ashe', 'Braum', 'Darius', 'Draven']
regions = ['--none--', 'Bilgewater', 'Demacia', 'Freljord', 'Ionia', 'Noxus', 'Piltover & Zaun', 'Shadow Isles']
# define app
app = Flask(__name__)

# main page
@app.route('/')
def index():
        return render_template("index.html", regions=regions)

# check if regions are selected
@app.route('/deck_select', methods=['POST'])
def deck_select():
    if request.method == 'POST':
        print(request.form.get('region_1'))
        print(request.form.get('region_2'))
        return render_template("deck_select.html", champions=champions)

# run page
if __name__ == '__main__':
    app.debug=True
    app.run()