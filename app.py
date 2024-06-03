from flask import Flask, render_template, request, session, flash, redirect
import pymysql
import hashlib
import uuid

app = Flask(__name__)

app.secret_key = "epicSecretKeyNeverCanCrackThisEpicCode//123#@%"

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="onebit",
        password="epicPassword",
        database="OneBit",
        cursorclass=pymysql.cursors.DictCursor
    )

# for encrypting your epic passwords
# cant write a function to go backwards so no one knows what the password is lawl
def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

# this is for saving images
# adds some randomness to avoid double ups
def saveFile(file, path, default = None):
    if file:
        randomness = str(uuid.uuid4())[:8] # only 8 characters
        filePath = path + randomness + "-" + file.filename
        file.save(filePath)
        return "/" + filePath
    else:
        return default

# main landing page when first visiting the website
@app.route("/")
def index():
    return render_template("index.html")

# lets a user create an account
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users (firstName, userName, email, password)
                        VALUES (%s, %s, %s, %s);
                """
                values = (request.form["firstName"], request.form["userName"], request.form["email"], encrypt(request.form["password"]),)
                cursor.execute(sql, values)
                connection.commit()
    
    return render_template("signup.html")

# logs an already existing user in
@app.route("/login", methods=["GET", "POST"])
def login():
    session["epic"] = "cool"
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM users
                WHERE userName=%s
                """
                values = (request.form["userName"])
                cursor.execute(sql, values)
                result = cursor.fetchone()
            
        if result:
            if result["password"] == encrypt(request.form["password"]):
                session["loggedIn"] = True
                session["firstName"] = result["firstName"]
                session["userName"] = result["userName"]
                session["userID"] = result["userID"]
                flash("login successful!")
                return redirect("/home")
            else:
                flash("wrong password for username " + result["userName"])
        else:
            flash("no user with username " + request.form["userName"])
    
    return render_template("login.html")

# logs the user out by clearing the session variables that contain info about them
@app.route("/logout")
def logout():
    session.clear()
    flash("logged out")
    return redirect("/login")

# main page users will spend the most time on, shows post feed and allat
@app.route("/home")
def home():
    with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts")
                result = cursor.fetchall()

                cursor.execute("SELECT * FROM tags")
                tags = cursor.fetchall()

                cursor.execute("SELECT * FROM likes WHERE userID = %s", session["userID"])
                likes = cursor.fetchall()

                likeArr = []
                count = 0

                for post in result:
                    for like in likes:
                        if like["userID"] == session["userID"] and post["postID"] == like["postID"]:
                            # do if the user liked the post:
                                if post["postID"] - count > 0:
                                    for n in range(post["postID"] - count):
                                        likeArr.append(False)
                                        count += 1

                                likeArr.append(True)
                                count += 1
                                break
                        
                    # count += 1
                    
                print(likeArr)

                
    return render_template("home.html", posts=result, tags=tags, likes=likes, likeArr=likeArr)

# for creating posts
@app.route("/createPost", methods=["GET", "POST"])
def createPost():
     if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO posts (userID, title, image, description) VALUES (%s, %s, %s, %s)"
                values = (session["userID"], request.form["title"], saveFile(request.files["image"], "static/images/postImages/"), request.form["description"])
                cursor.execute(sql, values)
                connection.commit()

                cursor.execute("SELECT postID FROM posts ORDER BY postID DESC")
                result = cursor.fetchone()

                tags = [x.strip() for x in request.form["tags"].split(',')]

                for tag in tags:
                    sql = "INSERT INTO tags (tag, postID) VALUES (%s, %s)"
                    values = (tag, result["postID"])
                    cursor.execute(sql, values)

                connection.commit()

     return render_template("createPost.html")

# for liking posts
@app.route("/like")
def like():
    with create_connection() as connection:
            with connection.cursor() as cursor:
                postID = request.args.get("postID")
                alreadyLiked = False;

                # check if the user already liked the post
                sql = "SELECT userID FROM likes WHERE postID = %s"
                cursor.execute(sql, postID)
                results = cursor.fetchall()

                for result in results:
                    if result["userID"] == session["userID"]:
                        # there is a match so it should "unlike"
                        alreadyLiked = True;
                        
                if alreadyLiked:
                    sql = "DELETE FROM likes where userID = %s AND postID = %s"
                    values = (session["userID"], postID)
                    cursor.execute(sql, values)

                    sql = "UPDATE posts SET likes = likes - 1 WHERE postID = %s"
                else:
                    # add a new like
                    sql = "INSERT INTO likes (userID, postID) VALUES (%s, %s)"
                    values = (session["userID"], postID)
                    cursor.execute(sql, values)

                    sql = "UPDATE posts SET likes = likes + 1 WHERE postID = %s"

                cursor.execute(sql, postID)
                connection.commit()

                cursor.execute("SELECT likes FROM posts WHERE postID = %s", postID)
                result = cursor.fetchone()

                return str(result["likes"])
    
app.run(debug=True, host="0.0.0.0") # the host bit allows any computer on the network to access the flask server