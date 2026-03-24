from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
import pandas


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    # cafe = StringField('Cafe name', validators=[DataRequired()])
    CafeName = StringField('Cafe Name', validators=[DataRequired()])
    Location = StringField('Cafe Location on Google Map URL', validators=[DataRequired()])
    Opening = StringField('Opening Time', validators=[DataRequired()])
    Closing = StringField('Closing Time', validators=[DataRequired()])
    CoffeRating = StringField('Coffe Rating', validators=[DataRequired()])
    WifiStrength = StringField('Wifi strength', validators=[DataRequired()])
    Power = StringField('Power',validators=[DataRequired()])
    submit = SubmitField('Submit')

# --------------------------------------------------------------------------- #

#open and read the file after the appending:

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new = {
            "Cafe Name":form.CafeName.data,
            "Location":form.Location.data,
            "Open": form.Opening.data ,
            "Close":  form.Closing.data ,
            "Coffee":  form.CoffeRating.data ,
            "Wifi":  form.WifiStrength.data ,
            "Power": form.Power.data
        }
        new_data = pandas.DataFrame([new])
        data = pandas.read_csv("cafe-data.csv")
        data = pandas.concat([data,new_data],ignore_index=True)
        data.to_csv("cafe-data.csv",index= False)

    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
    data = pandas.read_csv("cafe-data.csv")
    return render_template('cafes.html', data=data)

@app.route('/index')
def index():
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
