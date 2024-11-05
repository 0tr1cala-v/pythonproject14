import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(10):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'User{i + 1}', f'example{i + 1}gmail.com', f'{(i + 1) * 10}', '1000'))
for n in range(1, 11, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500, f'User{n}'))

for k in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{k}',))

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
age_users = cursor.fetchall()
for user in age_users:
    print(f'Имя:{user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')


connection.commit()
connection.close()
