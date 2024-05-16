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
                return redirect("/")
    
    with create_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute("SELECT * FROM users WHERE userID = 1")
                name = cursor.fetchone()
                print(name["userName"])
                return render_template("signup.html", name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

app.run(debug=True)
