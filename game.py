from flask import Flask, render_template, request, session, redirect, url_for, flash
import random
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session or 'attempts' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['won'] = False

    if request.method == 'POST' and not session['won']:
        guess = request.form.get('guess')

        if not guess or not guess.isdigit():
            flash("⚠️ Please enter a valid number between 1 and 100.", "error")
        else:
            guess = int(guess)
            if guess < 1 or guess > 100:
                flash("🚫 Number out of range! Choose 1–100.", "error")
            else:
                session['attempts'] += 1
                target = session['number']

                if guess < target:
                    flash("🔼 Too low! Try again.", "error")
                elif guess > target:
                    flash("🔽 Too high! Try again.", "error")
                else:
                    session['won'] = True
                    flash(f"🎉 Correct! You got it in {session['attempts']} attempts.", "success")

    return render_template('index.html', won=session['won'])

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
