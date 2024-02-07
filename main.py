from flask import Flask, redirect, url_for,render_template
from calculate import calculate_blueprint
from app import app_blueprint

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Set the secret key here
app.register_blueprint(calculate_blueprint, url_prefix='/calculate')
app.register_blueprint(app_blueprint, url_prefix='/app')

@app.route('/')
def root():
    #return redirect(url_for('app.index'))\
    return render_template('/home.html')
@app.route('/desi')  # Add this route for "desi.html"
def desi():
    return render_template('desi.html')

@app.route('/start')
def start():
    return redirect(url_for('app.index'))

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

