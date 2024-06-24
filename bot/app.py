from flask import Flask, request, render_template_string, flash, redirect, url_for
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
@app.route('/')
def home():
    return render_template_string(open('index.html').read())

#@app.route('/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    
    if username == 'admin' and password == '10':
        return f'Welcome {username}. Your password is: {password}'
    else:
        flash('Invalid credentials! Please try again.', 'error')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
