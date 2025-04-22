import pickle
import sqlite3

# Загрузка данных
with open('masculine_brainrots.pkl', 'rb') as file:
    data = pickle.load(file)
print(data)

# Подключение к базе данных
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER UNIQUE, iq INTEGER, rot_count INTEGER, pic_count INTEGER)''')


conn.commit()
conn.close()