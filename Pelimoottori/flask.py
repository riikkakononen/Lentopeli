from flask import Flask, render_template, request, jsonify
from main import Pelaaja, CO2Manager, Peli  # Import the classes from main.py
import mysql.connector

app = Flask(__name__)


def connect_db():
    return mysql.connector.connect(
        host='localhost',
        database='lentopeli',
        user='user',
        password='password',
        autocommit=True,
        collation='utf8mb4_unicode_ci'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        # Connect to the database
        yhteys = connect_db()

        # Instantiate your game-related classes
        pelaaja = Pelaaja("Player1")
        peli = Peli(pelaaja, yhteys)

        # Start the game logic
        peli.aloita()  # Start the game

        return jsonify({'status': 'Game Started'})
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})

app.run(debug=True)