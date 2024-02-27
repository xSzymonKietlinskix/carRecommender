# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from user import User

app = Flask(__name__)
app.config.from_pyfile('config.py')


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
        styl_jazdy = request.form['styl_jazdy']
        if request.form['action'] == 'Dalej':
            user = User(przeznaczenie, ekonomia, wygoda, styl_jazdy)
            session['user'] = {
                'przeznaczenie': przeznaczenie,
                'ekonomia': ekonomia,
                'wygoda': wygoda,
                'styl_jazdy': styl_jazdy
            }
            return redirect(url_for('results'))
    return render_template('form.html')


@app.route('/results')
def results():
    user_data = session.get('user')
    if user_data:
        user = User(user_data['przeznaczenie'], user_data['ekonomia'], user_data['wygoda'], user_data['styl_jazdy'])
        return render_template('results.html', user=user)
    else:
        return "Brak danych użytkownika"

@app.route('/submit-rating', methods=['POST'])
def submit_rating():
    rating = request.form.get('rating')
    print("Ocena: ", rating)
    return redirect(url_for('results'))


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
