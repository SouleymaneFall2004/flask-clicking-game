from datetime import timedelta

from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.permanent_session_lifetime = timedelta(days=365)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    score = db.Column(db.Integer, default=0)
    multiplier = db.Column(db.Integer, default=1)


@app.before_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    player = Player.query.filter_by(username=session['username']).first()
    return render_template('index.html', player=player)



@app.route('/click', methods=['POST'])
def click():
    player = Player.query.filter_by(username=session['username']).first()
    player.score += player.multiplier
    db.session.commit()
    return jsonify(score=player.score)


@app.route('/boost', methods=['POST'])
def boost():
    player = Player.query.filter_by(username=session['username']).first()
    cost = int(50 * (1.5 ** (player.multiplier - 1)))
    if player.score >= cost:
        player.score -= cost
        player.multiplier += 1
        db.session.commit()
        next_cost = int(50 * (1.5 ** (player.multiplier - 1)))
        return jsonify(multiplier=player.multiplier, score=player.score, cost=next_cost)
    return redirect(url_for('index'))


@app.route('/leaderboard')
def leaderboard():
    top_players = Player.query.order_by(Player.score.desc()).limit(10).all()
    return render_template('leaderboard.html', players=top_players)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        player = Player.query.filter_by(username=username).first()
        if not player:
            player = Player(username=username)
            db.session.add(player)
            db.session.commit()
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/reset')
def reset():
    player = Player.query.filter_by(username=session['username']).first()
    player.score = 0
    player.multiplier = 1
    db.session.commit()
    return redirect(url_for('index'))
