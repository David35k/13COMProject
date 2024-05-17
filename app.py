from flask import Flask, render_template, request, session, flash, redirect
import pymysql

app = Flask(__name__)

app.secret_key = "epicSecretKeyNeverCanCrackThisEpicCode//123#@%"

def create_connection():
    return pymysql.connect(
        host="localhost",
        user="david",
        password="DavidGamerDD335",
        database="OneBit",
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        with create_connection() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO users (firstName, userName, email, password)
                        VALUES (%s, %s, %s, %s);
                """
                values = (request.form["firstName"], request.form["userName"], request.form["email"], request.form["password"],)
                cursor.execute(sql, values)
                connection.commit()
    

    return render_template("signup.html")

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
            if result["password"] == request.form["password"]:
                session["loggedIn"] = True
                session["firstName"] = result["firstName"]
                session["userName"] = result["userName"]
                flash("login successful!")
                return redirect("/")
            else:
                flash("wrong password for username " + result["userName"])
        else:
            flash("no user with username " + request.form["userName"])
    
    return render_template("login.html")

app.run(debug=True)
