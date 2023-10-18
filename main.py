from flask import Flask, request, session
from flask import render_template
import bleach

app = Flask(__name__, template_folder='templates' )
app.secret_key = 'CSC440Secret!' #Don't know what to do with this

@app.route('/')
@app.route('/home')
def home():
    return render_template('homePage.html')

@app.route('/sql')
def sqlInjection():
    return render_template('sqlInjection.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    #input and clean data from form. bleach prevents SQL XSS etc.
    name = bleach.clean(request.form['name'])
    email = bleach.clean(request.form['email'])
    message = bleach.clean(request.form['message'])

    submitted_message = session.pop('submitted_message', None)
    print(f"Name: {name}, Email: {email}, Message: {message}")
    session['submitted_message'] = 'Submitted successfully!'

    return render_template('homePage.html', submitted_message=submitted_message)

if __name__ == "__main__":
    app.run()