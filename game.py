from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['won'] = False

    message = ''
    status = ''  # "success", "error", or ""

    if request.method == 'POST' and not session['won']:
        try:
            guess = int(request.form['guess'])
            session['attempts'] += 1
            number = session['number']

            if guess < number:
                message = '🔼 Too low! Try again.'
                status = 'error'
            elif guess > number:
                message = '🔽 Too high! Try again.'
                status = 'error'
            else:
                message = f'🎉 You got it in {session["attempts"]} tries!'
                session['won'] = True
                status = 'success'
        except ValueError:
            message = "❗ Please enter a valid number."
            status = 'error'

    return render_template('index.html', message=message, status=status, won=session['won'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
