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
      cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5))
      db.commit()
      values = ["Player One", "_ _ _ _ _", "_ _ _ _ _", "whiteKnight5.png", "blackKnight5.png"]
    else:
      word1 = r.word(word_min_length = 5, word_max_length = 5).upper()
      word2 = r.word(word_min_length = 5, word_max_length = 5).upper()
      if word2 == word1:
        word2 = r.word(word_min_length = 5, word_max_length = 5)
      cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5))
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
        values[7] = "Player One Forfeited Their Turn!"
      elif guess in values[1]:
        values[6] -= 1
        newSpaces = ["", "", "", "" , ""]
        for i in range(len(values[1])):
          if values[1][i] == guess and values[3][i] != guess:
              newSpaces[i] = guess
              print("i", i, values[1][i], values[3][2*i], len(values[3]), values[3], "|")
              loopList = [0, 1, 2 ,3, 4]
              loopList.remove(i)
              for n in loopList:
                print("n", n, values[1][n], values[3][2*n], len(values[3]), values[3], "|")
                if len(values[3]) > 2 * n: 
                  newSpaces[n] = values[3][2 * n]
                else:
                  newSpaces[n] = values[3][2 * n -1]
              break
          # else:
          #     print("Test")
          #     if len(values[3]) > 2 * i: 
          #       newSpaces += values[3][2 * i] + " "
          #     else:
          #       newSpaces += "_ "
        print("|" + str(newSpaces).replace("[", "").replace("]", "").replace(",", "").replace("'", "").strip() + "|")
        values[3] = str(newSpaces).replace("[", "").replace("]", "").replace(",", "").replace("'", "").strip()
      values[0] = 2
    elif values[0] == 2:
      guess = request.form['guess'].upper()
      if guess not in alphabet:
        values[7] = "Player Two Forfeited Their Turn!"
      elif guess in values[2]:
        values[5] -= 1
        newSpaces = ["", "", "", "" , ""]
        for i in range(len(values[2])):
          if values[2][i] == guess and values[4][i] != guess:
              newSpaces[i] = guess
              print("i", i, values[2][i], values[4][2*i], len(values[4]), values[4], "|")
              loopList = [0, 1, 2 ,3, 4]
              loopList.remove(i)
              for n in loopList:
                print("n", n, values[2][n], values[4][2*n], len(values[4]), values[4], "|")
                if len(values[4]) > 2 * n:
                  newSpaces[n] = values[4][2 * n]
                else:
                  newSpaces[n] += values[4][2 * n - 1]
              break
          # else:
          #     print("test")
          #     if len(values[4]) > 2 * i:
          #       newSpaces += values[4][2 * i] + " "
          #     else:
          #       newSpaces += "_ "
        values[4] = str(newSpaces).replace("[", "").replace("]", "").replace(",", "").replace("'", "").strip()
      values[0] = 1

    cursor.execute("UPDATE game SET turn = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (values[0], values[3], values[4], values[5], values[6]))
    db.commit()

    values[5] = f"whiteKnight{values[5]}.png"
    values[6] = f"blackKnight{values[6]}.png"
    values[3] = values[3].replace("_", "_ ")
    values[4] = values[4].replace("_", "_ ")

  cursor.close()
  db.close()
  return render_template("index.html", values = values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
