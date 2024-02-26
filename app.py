# app.py
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/ankieta', methods=['GET', 'POST'])
def ankieta():

    if request.method == 'POST':
        opcja_wybrana = request.form['opcje']
        if request.form['action'] == 'Dalej':
            print("Wybrana opcja: ", opcja_wybrana)
            return redirect(url_for('kolejny_krok'))
    return render_template('form1step.html')


@app.route('/kolejny_krok')
def kolejny_krok():
    # Tutaj możesz renderować kolejny krok ankiety
    return "Kolejny krok ankiety"


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
