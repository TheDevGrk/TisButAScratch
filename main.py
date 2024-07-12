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

      values = [1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5]

    else:
      word1 = r.word(word_min_length = 5, word_max_length = 5).upper()
      word2 = r.word(word_min_length = 5, word_max_length = 5).upper()

      if word2 == word1:
        word2 = r.word(word_min_length = 5, word_max_length = 5)

      cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5))
      db.commit()

      values = [1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5]
  elif request.method == "POST":
    values = []

    cursor.execute("SELECT * FROM game")
    valuesUnformatted = cursor.fetchall()

    valuesUnformatted = valuesUnformatted[0]
    for i in valuesUnformatted:
        values.append(i)
    values.append("")

    guess = request.form['guess'].upper()

    if "RESTART" in guess.upper():
      word1 = r.word(word_min_length = 5, word_max_length = 5).upper()
      word2 = r.word(word_min_length = 5, word_max_length = 5).upper()

      if word2 == word1:
        word2 = r.word(word_min_length = 5, word_max_length = 5)

      cursor.execute("UPDATE game SET turn = ?, word1 = ?, word2 = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5))
      db.commit()

      values = [1, word1, word2, "_ _ _ _ _", "_ _ _ _ _", 5, 5]

    elif values[0] == 1:

      if guess not in alphabet:
        values[7] = "Player One Forfeited Their Turn!"

      elif guess in values[1]:
        newSpaces = ["", "", "", "" , ""]

        for i in range(5):
          if values[1][i] == guess and values[3][i*2] != guess:

            values[6] -= 1
            newSpaces[i] = guess

            loopList = [0, 1, 2 ,3, 4]
            loopList.remove(i)

            for n in loopList:
              if len(values[3]) > 2 * n: 
                newSpaces[n] = values[3][2 * n]
              else:
                newSpaces[n] = values[3][2 * n -1]

            values[3] = str(newSpaces).replace("[", "").replace("]", "").replace(",", "").replace("'", "").strip()
            break
      values[0] = 2

    elif values[0] == 2:

      if guess not in alphabet:
        values[7] = "Player Two Forfeited Their Turn!"

      elif guess in values[2]:
        newSpaces = ["", "", "", "" , ""]

        for i in range(5):
          if values[2][i] == guess and values[4][i*2] != guess:

            values[5] -= 1
            newSpaces[i] = guess

            loopList = [0, 1, 2 ,3, 4]
            loopList.remove(i)

            for n in loopList:
              if len(values[4]) > 2 * n:
                newSpaces[n] = values[4][2 * n]
              else:
                newSpaces[n] += values[4][2 * n - 1]

            values[4] = str(newSpaces).replace("[", "").replace("]", "").replace(",", "").replace("'", "").strip()
            break
      values[0] = 1


    cursor.execute("UPDATE game SET turn = ?, spaces1 = ?, spaces2 = ?, health1 = ?, health2 = ?", (values[0], values[3], values[4], values[5], values[6]))
    db.commit()

    if values[5] < 0:
      values[5] = 0
    if values[6] < 0:
      values[6] = 0

    values.append("")
    if values[5] == 0:
      values[8] = "Congratulations Player Two! Tis No Longer But A Scratch on Player One! You Won The Battle!"
      values[0] = "Enter \"Restart\" To Start A New Game"
      values[7] = "The Game Has Ended!!!"
      
      newSpaces = ""
      for i in range(5):
        if values[3].replace(" ", "")[i] == values[1][i]:
          newSpaces = newSpaces + values[3].replace(" ", "")[i]
          continue
        else:
          newSpaces = newSpaces + "<p style = 'color: red;'>" + values[3].replace(" ", "")[i] + "</p>"

      values[3] = newSpaces
      print(values[3])
    elif values[6] == 0:
      values[8] = "Congratulations Player One!  Tis No Longer But A Scratch on Player Two! You Won The Battle!"
      values[0] = "Enter \"Restart\" To Start A New Game"
      values[7] = "The Game Has Ended!!!"

      newSpaces = ""
      for i in range(5):
        if values[4].replace(" ", "")[i] == values[2][i]:
          newSpaces = newSpaces + values[4].replace(" ", "")[i]
          continue
        else:
          newSpaces = newSpaces + "<p style = 'color: red;'>" + values[4].replace(" ", "")[i] + "</p>"

      values[4] = newSpaces
      print(values[4])


  values[5] = f"whiteKnight{values[5]}.png"
  values[6] = f"blackKnight{values[6]}.png"

  if values[0] == 1:
    values[0] = "Player One's Turn"
  elif values[0] == 2:
    values[0] = "Player Two's Turn"

  cursor.close()
  db.close()

  return render_template("index.html", values = values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)