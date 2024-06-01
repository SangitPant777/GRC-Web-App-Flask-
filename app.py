from flask import Flask, render_template, request, redirect, url_for, flash
from firebase_admin import credentials, db, initialize_app
import hashlib
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase
cred = credentials.Certificate('C:/Users/Asus/Desktop/new/flaskapp/serviceaccount.json')
initialize_app(cred, {'databaseURL': 'https://grc-project-a0eba-default-rtdb.firebaseio.com/'})
firebase_db = db.reference()

# Password hash (replace this with your actual hash)
ACTUAL_PASSWORD_HASH = "6f5df9690af768d6a12c83ad028ed35078ed8e1b739acb47f9b8f6d8d8b21497"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        if hashed_password == ACTUAL_PASSWORD_HASH:
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect password!')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/risks', methods=['GET', 'POST'])
def risks():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        likelihood = request.form['likelihood']
        impact = request.form['impact']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        risk = {
            'name': name,
            'description': description,
            'likelihood': likelihood,
            'impact': impact,
            'timestamp': timestamp
        }
        firebase_db.child('risks').push(risk)
        flash('Risk added successfully!')
        
    risks = firebase_db.child('risks').get()
    return render_template('risks.html', risks=risks)

@app.route('/leadership_practices', methods=['GET', 'POST'])
def leadership_practices():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        lp = {
            'name': name,
            'description': description,
            'timestamp': timestamp
        }
        firebase_db.child('leadership_practices').push(lp)
        flash('Leadership Practice added successfully!')
        
    leadership_practices = firebase_db.child('leadership_practices').get()
    return render_template('leadership_practices.html', leadership_practices=leadership_practices)

@app.route('/compliances', methods=['GET', 'POST'])
def compliances():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        compliance = {
            'name': name,
            'description': description,
            'timestamp': timestamp
        }
        firebase_db.child('compliances').push(compliance)
        flash('Compliance added successfully!')
        
    compliances = firebase_db.child('compliances').get()
    return render_template('compliances.html', compliances=compliances)

if __name__ == '__main__':
    app.run(debug=True)
