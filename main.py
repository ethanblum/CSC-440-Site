import sqlite3
import bleach
from flask import Flask, request, session
from flask import render_template, Blueprint
import hashlib

app = Flask(__name__, template_folder='templates')
app.secret_key = 'CSC440Secret!'  # Don't know what to do with this it seems to be needed...


@app.route('/')
@app.route('/login')
def MainPage():
    return render_template('login.html')

@app.route('/login_form', methods=['POST'])
def loginPage():
    email1 = request.form['email']
    pwd = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()

    try:
        # Connect to the SQLite database
        with sqlite3.connect('SSQL_DBMS.db') as conn:

            cursor = conn.cursor()

            cursor.execute("SELECT username, passHash FROM UserInfo WHERE username = ?", (email1,))
            result_set = cursor.fetchall()

            if not result_set:
                return render_template('login.html', submitted_message="Email or Password is Incorrect")
            else:
                stored_username, stored_pass_hash = result_set[0]
                if stored_pass_hash != pwd:
                    return render_template('login.html', submitted_message="Email or Password is Incorrect")
                else:
                    conn.commit()
                    return render_template('homePage.html')

    except sqlite3.Error as e:
        print("SQLite error:", e)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signUp.html')

@app.route('/signup_form', methods=['POST'])
def signupForm():
    name = request.form['name']
    email1 = request.form['email']
    pwd1 = request.form['password1'].encode('utf-8')
    pwd2 = request.form['password2'].encode('utf-8')
    shaPassword1 = hashlib.sha256(pwd1).hexdigest()
    shaPassword2 = hashlib.sha256(pwd2).hexdigest()
    if shaPassword1 == shaPassword2:

        try:
            # Connect to the SQLite database
            with sqlite3.connect('SSQL_DBMS.db') as conn:

                cursor = conn.cursor()

                database = cursor.execute("SELECT username FROM UserInfo WHERE username LIKE ?", (email1,))

                if database.fetchall():

                    return render_template('signUp.html', submitted_message="Email Already In Use")
                else:
                    cursor.execute(
                        "INSERT INTO UserInfo (username, passHash, name) VALUES (?, ?, ?);",
                        (email1, shaPassword1, name)
                    )
                    conn.commit()
                    return render_template('homePage.html')

        except sqlite3.Error as e:
            print("SQLite error:", e)
    else:

        return render_template('signUp.html', submitted_message = "Passwords Do Not Match")


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
    return render_template('touchPoints.html')


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
                "INSERT INTO contactUS (username, email, message) VALUES (?, ?, ?);", (name, email,
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

