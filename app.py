from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'dbbenton'
mysql.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            email = request.form['email']
            email = request.form.get('email')
            print("Email app: " + email)

            password = request.form['password']     
            password = request.form.get('password')   
            print("Password app: " + password)

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

                if str(emailDB) == email and str(passwordDB) == password:
                    return "Logowanie zakończone powodzeniem"
                if str(emailDB) != email or str(passwordDB) != password:
                    return "Nieprawidłowy login lub hasło"
            else:
                return "Nieprawidłowy login lub hasło"
          
        return render_template("app.html")
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()
