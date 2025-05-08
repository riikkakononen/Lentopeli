from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from weather_service import get_weather_for_country
import mysql.connector
import json
import random

app = Flask(__name__)
CORS(app)

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        database='lentopeli',
        user='username',
        password='password',
        autocommit=True,
        collation='utf8mb4_unicode_ci'
    )

@app.route('/')
def index():
    return render_template('index.html')  # HUOM! index.html (ei .templates)

# API: Hae maat
@app.route('/api/countries', methods=['GET'])
def get_countries():
    try:
        yhteys = connect_db()
        cursor = yhteys.cursor()
        cursor.execute("SELECT maa FROM airports")
        maat = [row[0] for row in cursor.fetchall()]
        return jsonify(maat)  # ✅ Tämä on oikein
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'yhteys' in locals():
            yhteys.close()


# API: Hae kysymykset maalle
@app.route('/api/questions/<maa>', methods=['GET'])
def get_questions(maa):
    yhteys = None
    cursor = None
    try:
        yhteys = connect_db()
        cursor = yhteys.cursor()
        cursor.execute("SELECT id, kysymys, vaihtoehdot FROM questions WHERE maa = %s", (maa,))
        rows = cursor.fetchall()

        import random
        random.shuffle(rows)
        rows = rows[:3]

        kysymykset = []
        for row in rows:
            kysymykset.append({
                'id': row[0],
                'text': row[1],
                'options': list(json.loads(row[2]).values())
            })
        return jsonify(kysymykset)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()


# API: Tarkista vastaus
@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('userAnswer')

    yhteys = None
    cursor = None
    try:
        yhteys = connect_db()
        cursor = yhteys.cursor()
        cursor.execute("SELECT oikea_vastaus, vaihtoehdot FROM questions WHERE id = %s", (question_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Kysymystä ei löytynyt'})

        oikea_vaihtoehto_avain = row[0]  # esim. "A"
        vaihtoehdot = json.loads(row[1])
        oikea_vastaus = vaihtoehdot.get(oikea_vaihtoehto_avain)

        is_correct = user_answer == oikea_vastaus
        return jsonify({'correct': is_correct})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()

@app.route('/api/weather/<maa>', methods=['GET'])
def get_weather(maa):
    try:
        tila = get_weather_for_country(maa)
        return jsonify({'weather': tila})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8000)