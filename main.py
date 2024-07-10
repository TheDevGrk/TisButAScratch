from flask import Flask, render_template, request
import sqlite3
from wonderwords import RandomWord
r = RandomWord()

app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
  values = []
  alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  cursor.execute("CREATE TABLE IF NOT EXISTS game(turn INT, word1 TEXT, word2 TEXT, spaces1 TEXT, spaces2 TEXT, health1 INT, health2 INT)")
  db.commit()
  cursor.execute("SELECT * FROM game")
  test = cursor.fetchall()
  if test == []:
    cursor.execute("INSERT INTO game(turn, word1, word2, spaces1, spaces2, health1, health2) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, " ", " ", " ", " ", 5, 5))
    db.commit()
    word1 = r.word(word_min_length = 5, word_max_length = 5).upper()
    word2 = r.word(word_min_length = 5, word_max_length = 5).upper()
    if word2 == word1:
      word2 = r.word(word_min_length = 5, word_max_length = 5)
    cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_____", "_____", 5, 5))
    db.commit()
    values = ["Player One", "_ _ _ _ _", "_ _ _ _ _", "whiteKnight5.png", "blackKnight5.png"]
  else:
    word1 = r.word(word_min_length = 5, word_max_length = 5).upper()
    word2 = r.word(word_min_length = 5, word_max_length = 5).upper()
    if word2 == word1:
      word2 = r.word(word_min_length = 5, word_max_length = 5)
    cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_____", "_____", 5, 5))
    db.commit()
    values = ["Player One", "_ _ _ _ _", "_ _ _ _ _", "whiteKnight5.png", "blackKnight5.png"]
  if request.method == "POST":
    values = []
    cursor.execute("SELECT * FROM game")
    valuesUnformatted = cursor.fetchall()
    valuesUnformatted = valuesUnformatted[0]
    for i in valuesUnformatted:
      if i != valuesUnformatted[1] or valuesUnformatted[2]:
        values.append(i)
    print(values)
    if values[0] == 1:
      guess = request.form['guess'].upper()
      print("The guess is:", guess)
    if values[0] == 2:
      guess = request.form['guess'].upper()
      print("The guess is:", guess)

        
  return render_template("index.html", values = values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
