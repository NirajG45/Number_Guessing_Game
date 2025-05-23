from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize secret number
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0

    message = ''
    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1
            number = session['number']

            if guess < number:
                message = '🔼 Too low! Try again.'
            elif guess > number:
                message = '🔽 Too high! Try again.'
            else:
                message = f'🎉 Correct! You guessed it in {session["attempts"]} attempts.'
        except ValueError:
            message = "❗ Please enter a valid number."

    return render_template('index.html', message=message)

@app.route('/reset')
def reset():
    session.pop('number', None)
    session.pop('attempts', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
