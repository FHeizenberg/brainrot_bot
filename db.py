import pickle
import sqlite3


def load_db():
  # with open('feminine_brainrots.pkl', 'rb') as file:
  with open('masculine_brainrots.pkl', 'rb') as file:
      data = pickle.load(file)

  conn = sqlite3.connect('my_database.db')
  cursor = conn.cursor()

  cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER UNIQUE, iq INTEGER, rot_count INTEGER, pic_count INTEGER)''')

  cursor.execute('''CREATE TABLE IF NOT EXISTS verbs (id INTEGER PRIMARY KEY AUTOINCREMENT, verb TEXT NOT NULL);''')

  cursor.execute('SELECT COUNT(*) FROM verbs')
  count = cursor.fetchone()[0]

  if count == 0:
    cursor.executemany('''INSERT INTO verbs (verb) VALUES (?)''', [(v,) for v in data])
    print("db created")

  conn.commit()
  conn.close()

