from flask import Flask, render_template, request
import sqlite3
from wonderwords import RandomWord
r = RandomWord()

app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def index():
  alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()
  if request.method == "GET":
    values = []
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
      values = ["Player One", word1, word2, "_ _ _ _ _", "_ _ _ _ _", "whiteKnight5.png", "blackKnight5.png"]
  elif request.method == "POST":
    values = []
    cursor.execute("SELECT * FROM game")
    valuesUnformatted = cursor.fetchall()
    valuesUnformatted = valuesUnformatted[0]
    for i in valuesUnformatted:
        values.append(i)
    values.append("")
    if values[0] == 1:
      guess = request.form['guess'].upper()
      if guess not in alphabet:
        values[7] = "Player One Forfitted Their Turn!"
      elif guess in values[1]:
        values[6] -= 1
        index = values[1].index(guess)
        values[3] = values[3][:index] + guess + " " + values[3][index + 1:]
        print(0)
      print(0.1)
      values[0] = 2
      print(0.2)
    elif values[0] == 2:
      print(0.3)
      guess = request.form['guess'].upper()
      if guess not in alphabet:
        values[7] = "Player Two Forfitted Their Turn!"
      elif guess in values[2]:
        values[5] -= 1
        index = values[2].index(guess)
        values[4] = values[4][:index] + guess + " " + values[4][index + 1:]
      print(0.35)
      values[0] = 1
      print(0.4)

    print(1)
    cursor.execute("UPDATE game SET turn = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (values[0], values[3], values[4], values[5], values[6]))
    db.commit()
    print(2)

    values[3] = values[3].replace("_", "_ ")
    values[4] = values[4].replace("_", "_ ")

  return render_template("index.html", values = values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
