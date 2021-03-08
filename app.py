import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

#create database
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c=conn.cursor()
    print("Opened database successfully")

    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);")

    c.execute("CREATE TABLE IF NOT EXISTS posts (post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, message TEXT NOT NULL topic TEXT, image TEXT)")

    print("Table created successfully")
    #c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Aashiq Adams','ash','adams.aashiq@gmail.com','letmein');""")
    #c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Roronoa Zoro','zoro','3sword@mugiwara.com','katana');""")
    #c.execute("""INSERT INTO users (full_name, username, email, password) VALUES ('Vinsmoke Sanji','sanji','ladiesman@mugiwara.com','diablejamble');""")
    conn.commit()

    # c.execute("SELECT * FROM users;")
    # print(c.fetchall())
    
init_sqlite_db()

app = Flask(__name__)
CORS(app)

#function to convert database data to dictionary (i think)
app.config["DEBUG"] = True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#landing page using flask
@app.route('/user-data/', methods=['GET'])
def landing_page():
    post_data = request.get_json()
    uname = post_data['uname']
    pword = post_data['pword']


    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(uname,pword))
        data = cursor.fetchall()
        print(data)
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

            con = sqlite3.connect('database.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO users (full_name, username, email, password) VALUES (?, ?, ?, ?)", (fullname, username, email, password))
            con.commit()
            msg = "User "+fullname+" successfully added."
            print(msg)
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + e
        finally:
            con.close()
            return jsonify(msg = msg)

#sign in if user in database
@app.route('/user-login/' , methods=["GET"])
def login_user():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            get_data = request.get_json()
            username = get_data['username']
            password = get_data['password']
            print(username,password)

            with sqlite3.connect('database.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                cur.execute("SELECT * FROM users")
                conn.commit()
                response['body'] = cur.fetchall()
                response['msg'] = user+" logged in successfully."

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while verifying a record: " + str(e)

        finally:
            return response

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