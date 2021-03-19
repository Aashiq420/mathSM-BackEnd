import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

#create database
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    c=conn.cursor()
    print("Opened database successfully")

    c.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);")
    conn.commit()

    c.execute("CREATE TABLE IF NOT EXISTS posts (post_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, message TEXT NOT NULL, image TEXT, poster TEXT)")
    conn.commit()

    c.execute("CREATE TABLE IF NOT EXISTS comments (comment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, post_id INTEGER NOT NULL, comment TEXT, comment-poster TEXT)")
    conn.commit()

    print("Tables created successfully")
  
    conn.commit()
    
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

#fetch all users
@app.route('/user-data/', methods=['GET'])
def select_all_users():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        print(data)
    return jsonify(data)

#fetch all posts
@app.route('/post-data/', methods=['GET'])
def select_all_posts():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        data = cursor.fetchall()
        print(data)
    return jsonify(data)

#fetch all comments
@app.route('/comment-data/', methods=['GET'])
def select_all_comments():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments")
        data = cursor.fetchall()
        print(data)
    return jsonify(data)
    
#login check thing
@app.route('/login-data/', methods=['GET'])
def landing_page():
    post_data = request.get_json()
    uname = post_data['uname']
    pword = post_data['pword']
    print(uname, pword)


    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(uname,pword))
        data = cursor.fetchall()
        print(data)
    return jsonify(data)

# Add new user
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

# Add new post
@app.route('/create-post/', methods=['POST'])
def add_new_post():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()

            title = post_data['title']
            msg = post_data['message']
            img = post_data['image']

            con = sqlite3.connect('database.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO posts (title, message, image) VALUES (?, ?, ?)", (title, msg, img))
            con.commit()
            msg = "Post successfully created."
            print(msg)
        except Exception as e:
            con.rollback()
            msg = "Error occurred in post creation: " + e
        finally:
            con.close()
            return jsonify(msg = msg)

# Add new comment
@app.route('/create-comment/', methods=['POST'])
def add_new_comment():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            post_id = post_data['title']
            msg = post_data['message']
            poster = post_data['poster']
         
            con = sqlite3.connect('database.db')
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("INSERT INTO comments (post_id, comment, comment-poster) VALUES (?, ?, ?)", (post_id, msg, poster))
            con.commit()
            msg = "Comment posted succesfully"
            print(msg)
        except Exception as e:
            con.rollback()
            msg = "Error occurred in comment creation: " + e
        finally:
            con.close()
            return jsonify(msg = msg)