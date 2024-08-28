from flask import Flask, render_template, request, session, flash, redirect, make_response, jsonify
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

                for comment in comments:
                    likeCount += int(comment["likes"])

    return render_template("profile.html", postNum = len(posts), likeCount = likeCount, commentNum=len(comments))

# lets a user create an account and inserts them into the database
@app.route("/user/signup", methods=["GET", "POST"])
def signup():
    if("loggedIn" in session):
        flash("You're already logged in! What are you trying to do!?")
        return redirect("/user")

    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                # check if the username and/or email are taken
                cursor.execute("SELECT * FROM users;")
                users = cursor.fetchall()

                canSubmit = True

                for user in users:
                    if user["userName"] == request.form["userName"]:
                        flash("That username is already taken :( (try adding some numbers and stuff :) )")
                        canSubmit = False
                        break

                for user in users:
                    if user["email"] == request.form["email"]:
                        canSubmit = False
                        flash("An account with that email already exists!?!? What exactly are you trying to do mate 🧐🤔")
                        break

                if canSubmit:
                    sql = """INSERT INTO users (name, userName, email, password, image)
                            VALUES (%s, %s, %s, %s, %s);
                    """
                    if(not request.files["image"]):
                        values = (request.form["name"], request.form["userName"], request.form["email"], encrypt(request.form["password"]), "/static/images/websiteImages/pfpPlaceholder.jpg")
                    else:
                        values = (request.form["name"], request.form["userName"], request.form["email"], encrypt(request.form["password"]), saveFile(request.files["image"], "/static/images/profilePictures/"))
                    cursor.execute(sql, values)
                    connection.commit()

                    flash("Successfully created account!")
                    return redirect("login")
                else:
                    return redirect("/user/signup")
    elif request.method == "GET":
        return render_template("signup.html")


@app.route('/check_field', methods=['POST'])
def check_field():
    data = request.json
    field_name = data['field']
    field_value = data['value']

    with create_connection() as connection:
        with connection.cursor() as cursor:
            if field_name == 'userName':
                cursor.execute("SELECT * FROM users WHERE userName = %s", (field_value,))
            elif field_name == 'email':
                cursor.execute("SELECT * FROM users WHERE email = %s", (field_value,))
            
            result = cursor.fetchone()

            if result:

                return jsonify({'exists': True})
            else:
                return jsonify({'exists': False})

# logs an already existing user in
@app.route("/user/login", methods=["GET", "POST"])
def login():
    if("loggedIn" in session):
        flash("You're already logged in! What are you trying to do!?")
        return redirect("/user")

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

                flash("You have entered OneBit B)")
                return redirect("/home?sortby=recent")
            else:
                flash("wrong password for username " + result["userName"])
        else:
            flash("no user with the username: " + request.form["userName"])
    
    return render_template("login.html")

# logs the user out by clearing the session variables that contain info about them
@app.route("/user/logout")
def logout():
    session.clear()
    flash("Peace out ✌️")
    return redirect("/user/login")

# lets the user update their profile
@app.route("/user/edit", methods = ["GET", "POST"])
def updateProfile():

    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE users SET name= %s, userName = %s, email = %s, image = %s WHERE userID = %s"

                # this part is really weird
                # some things need the / in front of path, some dont its weird but it works
                # probably a nightmare to work on in the future

                if(request.form["usePlaceholder"] == '1'):
                    if(session["profilePicture"]):
                        if(not session["profilePicture"] == "/static/images/websiteImages/pfpPlaceholder.jpg"):
                            deleteFile(session["profilePicture"])
                    imagePath = "/static/images/websiteImages/pfpPlaceholder.jpg"
                elif (not request.files["image"]):
                    imagePath = session["profilePicture"]
                else:
                    if(session["profilePicture"]):
                        if(not session["profilePicture"] == "/static/images/websiteImages/pfpPlaceholder.jpg"):
                            deleteFile(session["profilePicture"])
                    imagePath = saveFile(request.files["image"], "static/images/profilePictures/")

                values = (request.form["name"], request.form["userName"], request.form["email"], imagePath, session["userID"])

                session["name"] = request.form["name"]
                session["userName"] = request.form["userName"]
                session["email"] = request.form["email"]
                session["profilePicture"] = imagePath

                cursor.execute(sql, values)
                connection.commit()

                flash("Profile updated. Looking good!")
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

                # make sure user is logged in
                if (not "loggedIn" in session):
                    flash("You need to be logged in to browse OneBit")
                    return redirect("/user/login")

                # this is the default
                if(not "sortby" in request.args):
                    flash("Sortby argument not found!")
                    return redirect("/home?sortby=recent")
                
                # Base SQL query
                sql = "SELECT * FROM posts"

                # Check if search parameter is provided
                if "search" in request.form and request.form["search"]:
                    sql += " WHERE title LIKE %s"
                    sql += " OR description LIKE %s"

                    # get all related tags
                    getTagsSQL = "SELECT * FROM tags WHERE tag LIKE %s"
                    cursor.execute(getTagsSQL, ("%" + request.form["search"] + "%"))
                    tags = cursor.fetchall()

                    if tags:
                        idString = "(" + ",".join([str(tag["postID"]) for tag in tags]) + ")"
                        sql += " OR postID IN " + idString

                if request.args["sortby"] == "recent":
                    sql += " ORDER BY time DESC"
                elif request.args["sortby"] == "likes":
                    sql += " ORDER BY likes DESC"
                elif request.args["sortby"] == "oldest":
                    sql += " ORDER BY time ASC"
                else:
                    flash("That's not a valid sortby argument mate :)")
                    return redirect("/home?sortby=recent")
                        
                if "search" in request.form and request.form["search"]:
                    cursor.execute(sql, (request.form["search"], request.form["search"]))
                else:
                    cursor.execute(sql)

                posts = cursor.fetchall()

                if len(posts) == 0:
                    flash("We couldn't find any posts that match your search :(")
                    return redirect("/home?sortby=recent")

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

                return redirect('/post/view?postID=' + str(result["postID"]))

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
            
            flash("Post deleted. Hope you didn't do that on accident!")
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
    # make sure user is logged in
    if (not "loggedIn" in session):
        flash("You need to be logged in to browse OneBit")
        return redirect("/user/login")

    if(request.method == "GET"):
        postID = request.args["postID"]

        if (not postID or not postID.isdigit()):
            flash("Invalid postID in address bar!")
            return redirect("/home?sortby=recent")

        with create_connection() as connection:
                with connection.cursor() as cursor:

                    cursor.execute("SELECT postID FROM posts;")
                    values = cursor.fetchall()

                    valid = False

                    for value in values:
                        if int(value["postID"]) == int(postID):
                            valid = True
                            break

                    if not valid:
                        flash("That post doesn't exist!")
                        return redirect("/home?sortby=recent")


                    # this is the default
                    if(not "sortby" in request.args):
                        return redirect("/post/view?postID=" + postID + "&sortby=recent")
                    
                    # Base SQL query
                    sql = "SELECT * FROM comments WHERE postID = " + str(postID)

                    if request.args["sortby"] == "recent":
                        sql += " ORDER BY time DESC"
                    elif request.args["sortby"] == "likes":
                        sql += " ORDER BY likes DESC"
                    elif request.args["sortby"] == "oldest":
                        sql += " ORDER BY time ASC"
                    else:
                        flash("That's not a valid sortby argument mate :)")
                        return redirect("/post/view?postID=" + postID + "&sortby=recent")

                    cursor.execute(sql)
                    comments = cursor.fetchall()
                    print(comments)

                    for comment in comments:
                        sql = "SELECT * FROM users WHERE userID = %s"
                        cursor.execute(sql, (comment["userID"]))
                        user = cursor.fetchone()
                        if(user == None):
                            comment["userName"] = "[Deleted User]"
                            comment["image"] = "/static/images/websiteImages/pfpPlaceholder.jpg"
                        else:
                            comment["userName"] = user["userName"]
                            comment["image"] = user["image"]


                    cursor.execute("SELECT * FROM posts WHERE postID = %s", postID)
                    post = cursor.fetchone()

                    cursor.execute("SELECT * FROM commentLikes WHERE userID = %s", session["userID"])
                    likes = cursor.fetchall()

                    counter = 0

                    for comment in comments:
                        counter += 1

                    likeArr = []

                    for comment in comments:
                        for like in likes:
                            if like["userID"] == session["userID"] and comment["commentID"] == like["commentID"]:
                                # do if the user liked the comment:
                                likeArr.append(comment["commentID"])

                    return render_template("viewPost.html", post=post, comments=comments, commentCount=counter, likeArr=likeArr, sortby=request.args["sortby"])

    elif (request.method == "POST"):
        postID = request.form.get("postID")
        comment = request.form.get("comment")

        if not postID:
            flash("postID wasn't given!")
            return redirect("/home?sortby=recent")

        with create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO comments (postID, comment, userID) VALUES (%s, %s, %s)", (postID, comment, session["userID"]))
                connection.commit()

        link = "/post/view?postID=" + str(postID)
        return redirect(link)

@app.route("/comment/like")
def likeComment():
    with create_connection() as connection:
        with connection.cursor() as cursor:
            commentID = request.args.get("commentID")
            alreadyLiked = False;

            # check if the user already liked the post
            sql = "SELECT * FROM commentLikes WHERE commentID = %s"
            cursor.execute(sql, commentID)
            results = cursor.fetchall()

            for result in results:
                if result["userID"] == session["userID"]:
                    # there is a match so it should "unlike"
                    alreadyLiked = True;
                    
            if alreadyLiked:
                sql = "DELETE FROM commentLikes where userID = %s AND commentID = %s"
                values = (session["userID"], commentID)
                cursor.execute(sql, values)

                sql = "UPDATE comments SET likes = likes - 1 WHERE commentID = %s"
            else:
                # add a new like
                sql = "INSERT INTO commentLikes (userID, commentID) VALUES (%s, %s)"
                values = (session["userID"], commentID)
                cursor.execute(sql, values)

                sql = "UPDATE comments SET likes = likes + 1 WHERE commentID = %s"

            cursor.execute(sql, commentID)
            connection.commit()

            cursor.execute("SELECT likes FROM comments WHERE commentID = %s", commentID)
            result = cursor.fetchone()

            return str(result["likes"])
            
app.run(debug=True, host="0.0.0.0") # the host bit allows any computer on the network to access the flask server