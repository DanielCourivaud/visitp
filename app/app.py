from flask import Flask, request
from flask import render_template
from form import StreetForm
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'daramo'


@app.route('/', methods=['GET', 'POST'])
def street():
    form = StreetForm()
    if request.method == 'POST':
        print(request.form)
        db["visitp"]["manual"].insert_one({
            "number": request.form["num"],
            "street": request.form["street"],
            "name": request.form["name"],
        })
    return render_template('form.html', title='Sign In', form=form)


app.run(debug=True)
