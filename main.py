from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from wonderwords import RandomWord
import random
r = RandomWord()

app = Flask(__name__)

# Used to ChatGPT to help brainstorm ideas for debugging the duplicate letter guessing system, did not copy and paste code
@app.route('/game', methods = ["GET", "POST"])
def index():
  alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()

  cursor.execute("SELECT playerOneName FROM characters")
  p1Name = cursor.fetchone()[0]

  cursor.execute("SELECT playerTwoName FROM characters")
  p2Name = cursor.fetchone()[0]

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

    responses = ["It's Just A Flesh Wound!", "I'm Invincible!", "Come On Then!", "Alright then, we'll just call it a draw.", "T'is But A Scratch"]

    cursor.execute("SELECT * FROM game")
    valuesUnformatted = cursor.fetchall()

    valuesUnformatted = valuesUnformatted[0]
    for i in valuesUnformatted:
        values.append(i)
    values.append("")

    guess = request.form['guess'].upper()

    if "RESTART" in guess:
      return redirect(url_for('names'))

    elif values[0] == 1:

      if guess not in alphabet:
        values[7] = "Player One Forfeited Their Turn!"

      elif guess in values[1]:
        newSpaces = ["", "", "", "" , ""]

        for i in range(5):
          if values[1][i] == guess and values[3][i*2] != guess:

            values[6] -= 1
            values[7] = responses[random.randint(0, (len(responses) - 1))]
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
            values[7] = responses[random.randint(0, (len(responses) - 1))]
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
      values[8] = f"Congratulations {p2Name}! Tis No Longer But A Scratch on {p1Name}! You Won The Battle! {p1Name}'s Word Was {values[1]}"
      values[0] = "Enter \"Restart\" To Start A New Game"
      values[7] = "The Game Has Ended!!!"

    elif values[6] == 0:
      values[8] = f"Congratulations {p1Name}! Tis No Longer But A Scratch on {p2Name}! You Won The Battle! {p2Name}'s Word Was {values[2]}"
      values[0] = "Enter \"Restart\" To Start A New Game"
      values[7] = "The Game Has Ended!!!"



  cursor.execute("SELECT playerOne FROM characters")
  p1 = cursor.fetchone()[0]

  cursor.execute("SELECT playerTwo FROM characters")
  p2 = cursor.fetchone()[0]

  values[5] = f"{p1}{values[5]}.png"
  values[6] = f"{p2}{values[6]}.png"

  if values[0] == 1:
    values[0] = f"{p1Name}'s Turn"
  elif values[0] == 2:
    values[0] = f"{p2Name}'s Turn"

  cursor.close()
  db.close()

  return render_template("index.html", values = values)

@app.route('/characters', methods = ["GET", "POST"])
def characters():
  values = []

  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()

  reroute = False
  if request.method == "GET":
    cursor.execute("CREATE TABLE IF NOT EXISTS characters(playerOne TEXT, playerTwo TEXT, selectionTurn INT, playerOneName TEXT, playerTwoName TEXT)")
    db.commit()

    cursor.execute("SELECT * FROM characters")
    test = cursor.fetchall()

    if test == []:
      cursor.execute("INSERT INTO characters(playerOne, playerTwo, selectionTurn, playerOneName, playerTwoName) VALUES (?, ?, ?, ?, ?)", ("blackKnight", "whiteKnight", 1, "Player One", "Player Two"))
      db.commit()
    else:
      cursor.execute("UPDATE characters SET playerOne = ?, playerTwo = ?, selectionTurn = ?", ("blackKnight", "whiteKnight", 1))
      db.commit()

  elif request.method == "POST":
    cursor.execute("SELECT selectionTurn FROM characters")
    turn = cursor.fetchone()[0]

    if request.form["select"] == "Play As The Black Knight":
      if turn == 1:
        cursor.execute("UPDATE characters SET playerOne = ?, selectionTurn = ?", ("blackKnight", 2))
        db.commit()
      elif turn == 2:
        cursor.execute("UPDATE characters SET playerTwo = ?, selectionTurn = ?", ("blackKnight", 1))
        db.commit()
        reroute = True
      else:
        print("An error occurred when setting a player's character as blackKnight!")

    elif request.form["select"] == "Play As The White Knight":
      if turn == 1:
        cursor.execute("UPDATE characters SET playerOne = ?, selectionTurn = ?", ("whiteKnight", 2))
        db.commit()
      elif turn == 2:
        cursor.execute("UPDATE characters SET playerTwo = ?, selectionTurn = ?", ("whiteKnight", 1))
        db.commit()
        reroute = True
      else:
        print("An error occurred when setting a player's character as whiteKnight!")

    elif request.form["select"] == "Play As The Blue Knight":
      if turn == 1:
        cursor.execute("UPDATE characters SET playerOne = ?, selectionTurn = ?", ("blueKnight", 2))
        db.commit()
      elif turn == 2:
        cursor.execute("UPDATE characters SET playerTwo = ?, selectionTurn = ?", ("blueKnight",1))
        db.commit()
        reroute = True
      else:
        print("An error occurred when setting a player's character as blueKnight!")

    elif request.form["select"] == "Play As The Gray Knight":
      if turn == 1:
        cursor.execute("UPDATE characters SET playerOne = ?, selectionTurn = ?", ("grayKnight", 2))
        db.commit()
      elif turn == 2:
        cursor.execute("UPDATE characters SET playerTwo = ?, selectionTurn = ?", ("grayKnight", 1))
        db.commit()
        reroute = True
      else:
        print("An error occurred when setting a player's character as grayKnight!")

  cursor.execute("SELECT selectionTurn FROM characters")
  turn = cursor.fetchone()[0]

  if turn == 1:
    cursor.execute("SELECT playerOneName FROM characters")
    p1Name = cursor.fetchone()[0]

    values.append(f"{p1Name},")

  elif turn == 2:
    cursor.execute("SELECT playerTwoName FROM characters")
    p2Name = cursor.fetchone()[0]

    values.append(f"{p2Name},")

  if reroute:
    return redirect(url_for('index'))
  else:
    return render_template("characters.html", values = values)

@app.route('/', methods = ["GET", "POST"])
def names():
  db = sqlite3.connect("main.sqlite")
  cursor = db.cursor()

  reroute = False
  if request.method == "GET":
    cursor.execute("CREATE TABLE IF NOT EXISTS characters(playerOne TEXT, playerTwo TEXT, selectionTurn INT, playerOneName TEXT, playerTwoName TEXT)")
    db.commit()

    cursor.execute("SELECT * FROM characters")
    test = cursor.fetchall()

    if test == []:
      cursor.execute("INSERT INTO characters(playerOne, playerTwo, selectionTurn, playerOneName, playerTwoName) VALUES (?, ?, ?, ?, ?)", ("blackKnight", "whiteKnight", 1, "Player One", "Player Two"))
      db.commit()
    else:
      cursor.execute("UPDATE characters SET playerOne = ?, playerTwo = ?, selectionTurn = ?, playerOneName = ?, playerTwoName = ?", ("blackKnight", "whiteKnight", 1, "Player One", "Player Two"))
      db.commit()

  elif request.method == "POST":
    p1Name = request.form["p1"]
    p2Name = request.form["p2"]

    cursor.execute("UPDATE characters SET playerOneName = ?, playerTwoName = ?", (p1Name, p2Name))
    db.commit()

    reroute = True

  if reroute:
    return redirect(url_for('characters'))
  else:
    return render_template("names.html")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=37567)
