from flask import Flask, render_template, request, session, flash, redirect
import pymysql
import hashlib
import uuid
import os

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

def deleteFile(filePath):
    os.remove(os.path.dirname(os.path.abspath(__file__)) + filePath)

# main landing page when first visiting the website
@app.route("/")
def index():
    return render_template("index.html")

# a page where the user can check and edit their profile 
@app.route("/user")
def profile():
    with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts WHERE userID = %s", session["userID"])
                posts = cursor.fetchall()

                likeCount = 0

                for post in posts:
                    likeCount += int(post["likes"])

    return render_template("profile.html", postNum = len(posts), likeCount = likeCount)
    

# lets a user create an account and inserts them into the database
@app.route("/user/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users (firstName, userName, email, password, image)
                        VALUES (%s, %s, %s, %s, %s);
                """
                values = (request.form["firstName"], request.form["userName"], request.form["email"], encrypt(request.form["password"]), saveFile(request.files["image"], "static/images/profilePictures/"))
                cursor.execute(sql, values)
                connection.commit()

                return redirect("login")
    
    return render_template("signup.html")

# logs an already existing user in
@app.route("/user/login", methods=["GET", "POST"])
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
                session["email"] = result["email"]
                session["userID"] = result["userID"]
                session["profilePicture"] = result["image"]

                flash("login successful!")
                return redirect("/home")
            else:
                flash("wrong password for username " + result["userName"])
        else:
            flash("no user with username " + request.form["userName"])
    
    return render_template("login.html")

# logs the user out by clearing the session variables that contain info about them
@app.route("/user/logout")
def logout():
    session.clear()
    flash("logged out")
    return redirect("/user/login")

# lets the user update their profile
@app.route("/user/edit", methods = ["GET", "POST"])
def updateProfile():

    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """UPDATE users SET firstName= %s, userName = %s, email = %s, image = %s
                        WHERE userID = %s
                """
                if(not request.files["image"]):
                    imagePath = session["profilePicture"]
                else:
                    deleteFile(session["profilePicture"])
                    imagePath = saveFile(request.files["image"], "static/images/profilePictures/")

                values = (request.form["firstName"], request.form["userName"], request.form["email"], imagePath, session["userID"])

                session["firstName"] = request.form["firstName"]
                session["userName"] = request.form["userName"]
                session["email"] = request.form["email"]
                session["profilePicture"] = imagePath

                # TODO: make it so that it deletes the old image
                cursor.execute(sql, values)
                connection.commit()

    return render_template("editProfile.html")


@app.route("/user/posts")
def userPosts():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE userID = %s", session["userID"])
            posts = cursor.fetchall()

            cursor.execute("SELECT * FROM tags")
            tags = cursor.fetchall()

            cursor.execute("SELECT * FROM likes WHERE userID = %s", session["userID"])
            likes = cursor.fetchall()            

        return render_template("userPosts.html", posts=posts, tags=tags)

# main page users will spend the most time on, shows post feed and allat
@app.route("/home")
def home():
    with create_connection() as connection:
            with connection.cursor() as cursor:

                # this is the default
                if(not "sortby" in request.args):
                    print("ohio")
                    return redirect("/home?sortby=recent")
                
                    # Base SQL query
                sql = "SELECT * FROM posts"

                # Check if search parameter is provided
                if "search" in request.args and request.args["search"]:
                    sql += " WHERE title LIKE '%" + request.args["search"] + "%'"

                # Check for sorting parameter
                if "sortby" in request.args:
                    if request.args["sortby"] == "recent":
                        sql += " ORDER BY time DESC"
                    elif request.args["sortby"] == "likes":
                        sql += " ORDER BY likes DESC"
                    elif request.args["sortby"] == "oldest":
                        sql += " ORDER BY time ASC"
                        
                cursor.execute(sql)

                posts = cursor.fetchall()

                cursor.execute("SELECT * FROM tags")
                tags = cursor.fetchall()

                cursor.execute("SELECT * FROM likes WHERE userID = %s", session["userID"])
                likes = cursor.fetchall()

                likeArr = []

                for post in posts:
                    for like in likes:
                        if like["userID"] == session["userID"] and post["postID"] == like["postID"]:
                            # do if the user liked the post:
                            likeArr.append(post["postID"])


                print(likeArr)

    return render_template("home.html", posts=posts, tags=tags, likes=likes, likeArr=likeArr, sortby=request.args["sortby"])

# for creating posts
@app.route("/post/create", methods=["GET", "POST"])
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
@app.route("/post/like")
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

@app.route("/post/delete")
def deletePost():
    with create_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM posts WHERE postID = %s", request.args["postID"])
            post = cursor.fetchone()

            cursor.execute("DELETE FROM posts WHERE postID = %s AND userID = %s", (request.args["postID"], session["userID"]))
            connection.commit()

            deleteFile(post["image"])
            
            return redirect("/user/posts")

@app.route("/post/edit", methods = ["GET", "POST"])
def editPost():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts WHERE postID = %s", request.args["postID"])
                post = cursor.fetchone()

                if(not request.files["image"]):
                    imagePath = post["image"]
                else:
                    deleteFile(post["image"])
                    imagePath = saveFile(request.files["image"], "static/images/postImages/")

                sql = "UPDATE posts SET title= %s, image = %s, description = %s WHERE postID = %s"
                values = (request.form["title"], imagePath, request.form["description"], post["postID"])

                cursor.execute(sql, values)
                cursor.execute("DELETE FROM tags WHERE postID = %s", post["postID"])

                tags = [x.strip() for x in request.form["tags"].split(',')]

                for tag in tags:
                    sql = "INSERT INTO tags (tag, postID) VALUES (%s, %s)"
                    values = (tag, post["postID"])
                    cursor.execute(sql, values)

                connection.commit()

                return redirect("/user/posts")
    else:
        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM posts WHERE postID = %s", request.args["postID"])
                post = cursor.fetchone()

                cursor.execute("SELECT * FROM tags WHERE postID = %s", post["postID"])
                tags = cursor.fetchall()
                tagString = ""
                
                for tag in tags:
                    tagString += tag["tag"] + ","

                tagString = tagString[:-1]

                print(tagString)

                return render_template("editPost.html", post=post, tagString=tagString)


app.run(debug=True, host="0.0.0.0") # the host bit allows any computer on the network to access the flask server