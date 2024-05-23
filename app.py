# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from car import Car
import recommender
import time
import csv
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')


def save_log(fileName, variable):
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(fileName, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_datetime, variable])

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        przeznaczenie = request.form['przeznaczenie']
        ekonomia = request.form['ekonomia']
        wygoda = request.form['wygoda']
        min_price = request.form['min-price']
        max_price = request.form['max-price']
        styl_jazdy = request.form['styl_jazdy']
        session.pop('rating_submitted', None)
        if request.form['action'] == 'Dalej':
            user = User(przeznaczenie, ekonomia, wygoda, styl_jazdy, min_price, max_price)
            session['user'] = {
                'przeznaczenie': przeznaczenie,
                'ekonomia': ekonomia,
                'wygoda': wygoda,
                'styl_jazdy': styl_jazdy,
                'min_price': min_price,
                'max_price': max_price
            }
            start_time = time.time()
            car = recommender.recommend(user)
            end_time = time.time()
            execution_time = end_time - start_time
            save_log("debug/excTime.csv", execution_time)
            session['car'] = {
                'brand': car.brand,
                'model': car.model,
                'generation': car.generation,
                'version': car.version,
                'id': car.id
            }
            return redirect(url_for('results'))
    return render_template('form.html')


@app.route('/results')
def results():
    user_data = session.get('user')
    car_data = session.get('car')
    if user_data:
        car = Car(brand=car_data['brand'], model=car_data['model'], generation=car_data['generation'], version=car_data['version'])
        user = User(user_data['przeznaczenie'], user_data['ekonomia'], user_data['wygoda'], user_data['styl_jazdy'], user_data['min_price'], user_data['max_price'])
        return render_template('results.html', user=user, car=car)
    else:
        return "Brak danych użytkownika lub pojazdu"

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    rating = request.form.get('rating')
    user_data = session.get('user')
    car_data = session.get('car')
    if user_data:
        if 'rating_submitted' not in session:
            user = User(user_data['przeznaczenie'], user_data['ekonomia'], user_data['wygoda'], user_data['styl_jazdy'], user_data['min_price'], user_data['max_price'])
            car = Car(id = car_data['id'], brand=car_data['brand'], model=car_data['model'], generation=car_data['generation'],
                      version=car_data['version'])
            dec_user = user.decode()
            dec_user.save_user_rating(car.id, rating)
            session['rating_submitted'] = True
    return redirect(url_for('results'))


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
