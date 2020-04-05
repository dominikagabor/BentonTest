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

@app.route('/profile', methods=['GET'])
def profile():      
        return render_template("profile.html")

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
        actualEmail = email
        print("Actual email: " + actualEmail)
        return render_template("app.html", loginMessage = '')
    except Exception as e:
        return str(e)

@app.route('/signup', methods=['POST'])
def signup_post():
    try:
        if request.method == 'POST': 
            name = request.form['name']
            name = request.form.get('name')
            print("Name app: " + name)

            email = request.form['email']
            email = request.form.get('email')
            print("Email app: " + email)

            password = request.form['password']     
            password = request.form.get('password')   
            print("Password app: " + password)

            repeatPassword = request.form['repeatPassword']     
            repeatPassword = request.form.get('repeatPassword')   
            print("RepeatPassword app: " + repeatPassword)

            countEmails = 0
            cur = mysql.connect().cursor()
            cur.execute("SELECT email FROM login")
            emailsDB = cur.fetchall()
            for row in emailsDB:
                emailDB = row[0]
                print(emailDB)
                if emailDB == email:
                     countEmails = countEmails + 1
                     return render_template("signup.html", signupMessage = 'Taki email istnieje w bazie.')  

            if countEmails == 0:
                if name == "" or email == "" or password == "" or repeatPassword == "":
                    return render_template("signup.html", signupMessage = 'Wszystkie pola muszą być uzupełnione.')
                else:
                    if password == repeatPassword:
                        try:
                            cur = mysql.connect().cursor()
                            cur.execute("INSERT INTO login(email, password, name) values('" + email + "', '" + password + "', '" + name + "')")
                            print("INSERT INTO login(email, password, name) values('" + email + "', '" + password + "', '" + name + "')")
                            mysql.connect().commit()
                            cur.close()
                            print("zapisane w bazie")
                        except Exception as e:
                            return str(e)
                    
                    else:
                        return render_template("signup.html", signupMessage = 'Hasła różnią się od siebie.')  
        return render_template("app.html", correctSignupMessage = "Konto założone poprawnie. Zaloguj się!")
    except Exception as e:
        return str(e)

@app.route('/profile', methods=['POST'])
def profile_post(actualEmail):
    try:
        if request.method == 'POST': 
            print("Actual email: " + actualEmail)
            name = request.form['name']
            name = request.form.get('name')
            print("Name profile app: " + name)

            password = request.form['password']     
            password = request.form.get('password')   
            print("Password profile app: " + password)

            repeatPassword = request.form['repeatPassword']     
            repeatPassword = request.form.get('repeatPassword')   
            print("RepeatPassword profile app: " + repeatPassword)

            countEmails = 0
            cur = mysql.connect().cursor()
            cur.execute("SELECT email FROM login where email = " + "'" + actualEmail + "'")
            emailsDB = cur.fetchall()
            for row in emailsDB:
                emailDB = row[0]
                print(emailDB)
                if emailDB == actualEmail:
                     countEmails = countEmails + 1


            if countEmails == 1:
                    if password == repeatPassword:
                        cur = mysql.connect().cursor()
                        cur.execute("INSERT INTO login(password, name) values('" + password + "', '" + name + "') where email = " + "'" + actualEmail + "'")
                        print("INSERT INTO login(password, name) values('" + password + "', '" + name + "') where email = " + "'" + actualEmail + "'")
                        mysql.connect().commit()
                        print("zapisane w bazie")
                    else:
                        return render_template("profile.html", editMessage = 'Hasła różnią się od siebie.')  
        return render_template("main.html", correctEditMessage = "Dane zapisane poprawnie.")
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
