from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt

#instantiate flask and bcrypt
app = Flask(__name__)
bcrypt = Bcrypt()

#instantiate and setup MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'boutique'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
mysql.init_app(app)

#set up secret key (discuss?)
app.secret_key = 'Secret Key'

#set up a route for the default page (root URL)
@app.route("/")
def main():
	return render_template('index.html')

#route to show signup page
@app.route("/showSignUp")
def showSignUp():
	return render_template("signUp.html")

#route to sign up new user
@app.route("/signUp", methods = ['POST'])
def signUp():

	try:
		#read the form data
		_email = request.form['email']
		_name = request.form['name']
		_pwd = request.form['password']

		#connect to the db
		cxn = mysql.connect()
		cursor = cxn.cursor()

		#hash the password
		hashed_pwd = bcrypt.generate_password_hash(_pwd)

		#insert into the db only if fields are not empty
		if(_email and _name and hashed_pwd):
			cursor.execute("INSERT INTO account(email, name, h_password) VALUES (%s, %s, %s)", (_email, _name, hashed_pwd))
			data = cursor.fetchall()
			if(len(data) == 0):
				cxn.commit()
				return redirect("/")
			else:
				return render_template("error.html", error = 'Something Went Wrong!')
		else:
			return render_template("error.html", error = 'A required field is missing!')

	#show the error page if anything goes wrong	
	except Exception:
		return render_template("error.html", error = 'Error Signing Up!')

	#close the cursor and db connection
	finally:
		cursor.close()
		cxn.close()
#todo - return proper response or redirect to correct page

#make sure the right script is being run
if __name__ == "__main__":
	#runs the application from the app variable
	app.run()