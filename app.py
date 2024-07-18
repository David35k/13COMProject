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

                cursor.execute("SELECT * FROM comments WHERE userID = %s", session["userID"])
                comments = cursor.fetchall()

    return render_template("profile.html", postNum = len(posts), likeCount = likeCount, commentNum=len(comments))

# lets a user create an account and inserts them into the database
@app.route("/user/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users (name, userName, email, password, image)
                        VALUES (%s, %s, %s, %s, %s);
                """
                values = (request.form["name"], request.form["userName"], request.form["email"], encrypt(request.form["password"]), saveFile(request.files["image"], "static/images/profilePictures/"))
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
                session["name"] = result["name"]
                session["userName"] = result["userName"]
                session["email"] = result["email"]
                session["userID"] = result["userID"]
                session["profilePicture"] = result["image"]

                flash("login successful!")
                return redirect("/home")
            else:
                flash("wrong password for username " + result["userName"])
        else:
            flash("no user with the username: " + request.form["userName"])
    
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
                sql = """UPDATE users SET name= %s, userName = %s, email = %s, image = %s
                        WHERE userID = %s
                """
                if(not request.files["image"]):
                    imagePath = session["profilePicture"]
                else:
                    if(session["profilePicture"]):
                        deleteFile(session["profilePicture"])
                    imagePath = saveFile(request.files["image"], "static/images/profilePictures/")

                values = (request.form["name"], request.form["userName"], request.form["email"], imagePath, session["userID"])

                session["name"] = request.form["name"]
                session["userName"] = request.form["userName"]
                session["email"] = request.form["email"]
                session["profilePicture"] = imagePath

                # TODO: make it so that it deletes the old image
                cursor.execute(sql, values)
                connection.commit()

                return redirect("/user")

    return render_template("editProfile.html")


@app.route("/user/posts")
def userPosts():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE userID = %s ORDER BY time DESC", session["userID"])
            posts = cursor.fetchall()

            cursor.execute("SELECT * FROM tags")
            tags = cursor.fetchall()

            cursor.execute("SELECT * FROM likes WHERE userID = %s", session["userID"])
            likes = cursor.fetchall()            

        return render_template("userPosts.html", posts=posts, tags=tags)

# main page users will spend the most time on, shows post feed and allat
@app.route("/home", methods = ["GET", "POST"])
def home():
    with create_connection() as connection:
            with connection.cursor() as cursor:

                # make user is logged in
                if (not "loggedIn" in session):
                    flash("You need to be logged in to browse OneBit")
                    return redirect("/user/login")

                # this is the default
                if(not "sortby" in request.args):
                    return redirect("/home?sortby=recent")
                
                # Base SQL query
                sql = "SELECT * FROM posts"

                # Check if search parameter is provided
                if "search" in request.form and request.form["search"]:
                    sql += " WHERE title LIKE '%" + request.form["search"] + "%'"
                    sql += " OR description LIKE '%" + request.form["search"] + "%'"

                    # get all related tags
                    thing = "SELECT * FROM tags WHERE tag LIKE '%" + request.form["search"] + "%'"
                    cursor.execute(thing)
                    tags = cursor.fetchall()

                    if tags:
                        idString = "(" + ",".join([str(tag["postID"]) for tag in tags]) + ")"
                        sql += " OR postID IN " + idString

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
                    if(post["image"]):
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

                flash("Post updated!")
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

                return render_template("editPost.html", post=post, tagString=tagString)

# actually lets the user view the post in a full page, leave comments and other stuff
@app.route("/post/view", methods = ["GET", "POST"])
def viewPost():
    if(request.method == "GET"):
        postID = request.args["postID"]

        if (not postID):
            flash("That post doesn't exist")
            return redirect("/home")

        # get the postID of the latest post
        with create_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT postID FROM posts ORDER BY time DESC")
                    latestPostID = cursor.fetchone()["postID"]

                    if (int(postID) > int(latestPostID)):
                        flash("That post doesn't exist")
                        return redirect("/home")

        with create_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM posts WHERE postID = %s", postID)
                    post = cursor.fetchone()

                    cursor.execute("SELECT * FROM comments JOIN users ON comments.userID = users.userID WHERE postID = %s ORDER BY time DESC", postID)
                    comments = cursor.fetchall()

                    counter = 0

                    for comment in comments:
                        counter += 1

                    return render_template("viewPost.html", post=post, comments=comments, commentCount=counter)
    elif (request.method == "POST"):
        postID = request.args["postID"]
        comment = request.form["comment"]

        link = '/post/comment?postID=' + str(postID) + '&comment=' + comment

        return redirect(link)

# epic commenting route
@app.route("/post/comment")
def comment():
    postID = request.args["postID"]
    comment = request.args["comment"]

    if (not postID):
        return redirect("/home")

    with create_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO comments (postID, comment, userID) VALUES (%s, %s, %s)", (postID, comment, session["userID"]))
            connection.commit()

    link = "/post/view?postID=" + str(postID)

    return redirect(link)

app.run(debug=True, host="0.0.0.0") # the host bit allows any computer on the network to access the flask server