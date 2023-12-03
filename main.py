import sqlite3
import bleach
from flask import Flask, request, session
from flask import render_template, Blueprint
import hashlib

app = Flask(__name__, template_folder='templates')
app.secret_key = 'CSC440Secret!'  # Don't know what to do with this it seems to be needed...


@app.route('/')
def MainPage():
    return render_template('login.html')

@app.route('/login_form', methods=['GET', 'POST'])
def loginPage():
    email1 = request.form['email']
    pwd = hashlib.sha256(request.form['password'])

    try:
        # Connect to the SQLite database
        with sqlite3.connect('SSQL_DBMS.db') as conn:

            cursor = conn.cursor()

            database = cursor.execute('SELECT * FROM UserInfo;')

            if email1 not in database:
                return render_template('login.html', info='Invalid User')
            else:
                if database[email1] != pwd:
                    return render_template('login.html', info='Invalid User')
                else:
                    return render_template('homePage.html', name=email1)

    except sqlite3.Error as e:
        print("SQLite error:", e)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signUp.html')


@app.route('/home')
def home():
    return render_template('homePage.html')


@app.route('/sql')
def sqlInjection():
    return render_template('sqlInjection.html')


@app.route('/overview')
def overview():
    return render_template('overviewPage.html')


@app.route('/touchpoint')
def touchPoint():
    return render_template('touchPoint.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # input and clean data from form
    name = bleach.clean(request.form['name'])
    email = bleach.clean(request.form['email'])
    message = bleach.clean(request.form['message'])

    submitted_message = session.pop('submitted_message', None)
    print(f"Name: {name}, Email: {email}, Message: {message}")
    session['submitted_message'] = 'Submitted successfully!'

    try:
        # Connect to the SQLite database
        with sqlite3.connect('SSQL_DBMS.db') as conn:

            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO contactUS (username, email, message) VALUES ('{}', '{}', '{}');".format(name, email,
                                                                                                     message))

            cursor.execute('SELECT * FROM contactUS;')

            print(cursor.fetchall())
            # Commit the changes
            conn.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)

    return render_template('homePage.html', submitted_message=submitted_message)


if __name__ == "__main__":
    app.run()

