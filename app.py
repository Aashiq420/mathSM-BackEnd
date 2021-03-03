import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#create database
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c=conn.cursor()
    print("Opened database successfully")

    c.execute("""  CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"full_name"	TEXT NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL);""")

  

    print("Table created successfully")

    #c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Roronoa Zoro','zoro','3sword@mugiwara.com','katana');""")
    #c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Vinsmoke Sanji','sanji','ladiesman@mugiwara.com','diablejamble');""")
    conn.commit()

    c.execute("""SELECT * FROM users;""")
    row = c.fetchall()
    for i in range(len(row)):
        print(row[i])
    conn.close()

init_sqlite_db()

#function to convert database data to dictionary (i think)
app.config["DEBUG"] = True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#landing page using flask
@app.route('/landing/', methods=['GET'])
def landing_page():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    return jsonify(data)#render_template('landing.html')


# Add new record
@app.route('/register/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            fullname = post_data['fullname']
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']
            data = fullname, username, email, password
            print(data)
            with sqlite3.connect('database.db') as con:
                con.row_factory = dict_factory

                cur = con.cursor()
                cur.execute("INSERT INTO users (full_name, username, email, password)VALUES (?, ?, ?, ?)", (fullname, username, email, password))
                con.commit()
                msg = "Record successfully added."
                print(msg)
        except Exception as e:
            return {'error': str(e)}
            # con.rollback()
            # msg = "Error occurred in insert operation: " + e
            # print(msg)
        finally:
            con.close()
            return {'msg': msg}

# @app.route('/main/', methods=['GET'])
# def main_page():
#     username = request.form['username']
#     pasword = request.form['password']

#     with sqlite3.connect('database.db') as con:
#         cur = con.cursor()
#         cur.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
#         cur.fetchall()
#         con.commit()
#         msg = "All records Processed"
#         return msg

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
# @app.route('/route/', methods=['POST','PUT','DELETE'])
# def add_item():
#     if request.method =='POST':
#         msg = None
#         try:
#             post_data = request.get_json()

#             firstname = post_data['firstname']
#         except:
#             print("error")
#         finally:
#             pass