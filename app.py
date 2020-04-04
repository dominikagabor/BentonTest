from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'dbbenton'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def login():      
        return render_template("app.html")

@app.route('/signup', methods=['GET'])
def signup():      
        return render_template("signup.html")

@app.route('/', methods=['POST'])
def login_post():
    try:
        if request.method == 'POST':
            email = request.form['email']
            email = request.form.get('email')
            print("Email app: " + email)

            password = request.form['password']     
            password = request.form.get('password')   
            print("Password app: " + password)

            if email == "" or password == "":
                return render_template("app.html", loginMessage = 'Login lub hasło nie mogą być puste')
            else:
                cur = mysql.connect().cursor()
                cur.execute("SELECT count(email) FROM login where email = " + "'" + email + "'")
                countEmailsDB = cur.fetchall()

                for row in countEmailsDB:
                    countEmailDB = row[0]

                if countEmailDB != 0:
                    cur = mysql.connect().cursor()
                    cur.execute("SELECT email FROM login where email = " + "'" + email + "'")
                    emailsDB = cur.fetchall()
                    for row in emailsDB:
                        emailDB = row[0]

                    cur = mysql.connect().cursor()
                    cur.execute("SELECT password FROM login where password = " + "'" + password + "'")
                    passwordDB = cur.fetchall()
                    for row in passwordDB:
                        passwordDB = row[0]
                        print("Password db: " + str(passwordDB))
            

                    cur = mysql.connect().cursor()
                    cur.execute("SELECT name FROM login where email = " + "'" + email + "'" + "and password = " + "'" + password + "'")
                    namesDB = cur.fetchall()

                    for row in namesDB:
                        nameDB = row[0]
                        print("Name db: " + str(nameDB))

                
                    if str(emailDB) == email and str(passwordDB) == password:
                        return render_template("main.html", name = nameDB)
                    if str(emailDB) != email or str(passwordDB) != password:
                        return render_template("app.html", loginMessage = 'Nieprawidłowy login lub hasło')
                else:
                    return render_template("app.html", loginMessage = 'Nieprawidłowy login lub hasło')
          
        return render_template("app.html", loginMessage = '')
    except Exception as e:
        return str(e)

@app.route('/signup', methods=['POST'])
def signup_post():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run()
