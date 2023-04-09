from flask import Flask, render_template, request, redirect, flash
import sys
import os
from weather import get_weather, CityNotFoundError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  # City name

    def __repr__(self):
        return '<City %r>' % self.name


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']

        existing_city = City.query.filter_by(name=city_name).first()

        if not existing_city:
            try:
                get_weather(city_name)
                city = City(name=city_name)
                db.session.add(city)
                db.session.commit()
            except CityNotFoundError:
                flash("The city doesn't exist!")
        else:
            flash("The city has already been added to the list!")

    cities_weather_data = [get_weather(city.name, city.id) for city in City.query.all()]

    return render_template("index.html", cities_weather_data=cities_weather_data)


@app.route('/delete/<int:city_id>', methods=['POST'])
def delete_city(city_id):
    if request.method == 'POST':
        city_to_delete = City.query.filter_by(id=city_id).first()
        if city_to_delete:
            db.session.delete(city_to_delete)
            db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
