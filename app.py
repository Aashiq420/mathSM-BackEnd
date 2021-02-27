import sqlite3
from flask import Flask, render_template, request, jsonify
from flask import request

def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c=conn.cursor()
    print("Opened database successfully")

    c.execute("""CREATE TABLE IF NOT EXISTS users 
    (user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    full_name TEXT, 
    username TEXT, 
    email TEXT, 
    password TEXT);""")
    print("Table created successfully")

    c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Aashiq Adams','ash1','adams.aashiq@gmail.com','letmein');""")
    c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Roronoa Zoro','zoro','3sword@mugiwara.com','katana');""")

    print("user added")

    c.execute("""SELECT * FROM users;""")
    row = c.fetchall()
    for i in range(len(row)):
        print(row[i])
    conn.close()

init_sqlite_db()

app = Flask(__name__)

@app.route('/')
def landing_page():
    msg = "successful"
    return msg

@app.route('/main/', methods=['GET'])
def main_page():
    username = request.form['username']
    pasword = request.form['password']

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
        cur.fetchall()
        con.commit()
        msg = "All records Processed"
        return msg

# @app.route('/register/')
# def register():
#     fullname = request.form['fullname']
#     username = request.form['username']
#     email = request.form['email']
#     password = request.form['password']
#     data = fullname, username, email, password
#     print(data)
#     return render_template('register.html')

#where there is a post:
@app.route('/route/', methods=['POST','PUT','DELETE'])
def add_item():
    if request.method =='POST':
        msg = None
        try:
            post_data = request.get_json()

            firstname = post_data['firstname']
        except:
            print("error")
        finally:
            pass