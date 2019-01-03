from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost/HealthyLife'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    dates = db.Column(db.Date, unique = True)
    active_or_rest = db.Column(db.String(120))
    workouts = db.Column(db.String(120))
    calorie_intake = db.Column(db.Integer)
    step_count = db.Column(db.Integer)
    weight_ins = db. Column(db.Float)

    def __init__(self, dates, active_or_rest, workouts, calorie_intake, step_count, weight_ins):
        self.dates = dates
        self.active_or_rest = active_or_rest
        self.workouts = workouts
        self.calorie_intake = calorie_intake
        self.step_count = step_count
        self.weight_ins = weight_ins

@app.route("/")
def index():
    return render_template("index.j2")

@app.route("/submitted", methods = ['POST'])
def submitted():
    if request.method == 'POST':
        date_of_entry = request.form["date_today"]
        workout = request.form["workout_yn"]
        type_of_workout = request.form["workout_type"]
        calories = request.form["calories_eaten"]
        steps = request.form["steps_taken"]
        weight = request.form["current_weight"]
        if db.session.query(Data).filter(Data.dates == date_of_entry).count() == 0:
            new_info = Data(date_of_entry, workout, type_of_workout, calories, steps, weight)
            db.session.add(new_info)
            db.session.commit()
            return render_template("submitted.j2")
    return render_template("index.j2", text = "We already have data for that date. Please check it and try again.")

@app.route("/the_data")
def the_data():
    return render_template("the_data.j2")

if __name__ == '__main__':
    app.debug = True
    app.run()