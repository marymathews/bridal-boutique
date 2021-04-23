from flask import Flask, render_template, request, redirect, json
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

#route to show signin page
@app.route("/showSignIn")
def showSignIn():
	return render_template("signIn.html")

#route to sign in existing user
@app.route("/signIn", methods = ['POST'])
def signIn():

	try:
		#read the form data
		_email = request.form['email']
		_pwd = request.form['password']

		#connect to the db
		cxn = mysql.connect()
		cursor = cxn.cursor()

		if _email:
			cursor.execute("SELECT * FROM account WHERE email = %s", (_email))
			data = cursor.fetchall()
			is_same = bcrypt.check_password_hash(data[0][2], _pwd)

			if(is_same):
				return redirect("/")
			else:
				return render_template("error.html", error = 'Incorrect Details!')
		else:
			return render_template("error.html", error = 'A required field is missing!')

	#show the error page if anything goes wrong	
	except Exception:
		return render_template("error.html", error = 'Error Signing In!')

	#close the cursor and db connection
	finally:
		cursor.close()
		cxn.close()

@app.route("/checkExistingEmail/<string:email>", methods = ['GET'])
def checkExistingEmail(email):
	#connect to db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#check if email is already in db
	existingUser = False
	cursor.execute("SELECT * FROM account WHERE email = %s", email)
	if(len(cursor.fetchall()) > 0):
		existingUser = True

	cursor.close()
	cxn.close()

	if(existingUser):
		return json.dumps({'error': 'Existing Account'})
	else:
		return ('', 204)

#route for showing western category page
@app.route("/showWestern/<page>")
def showWestern(page):
	return render_template("western.html", data = getProducts('west', page))

#route for showing cosmetics category page
@app.route("/showCosmetics")
def showCosmetics():
	return render_template("cosmetics.html")

#route for showing jewellery category page
@app.route("/showJewellery")
def showJewellery():
	return render_template("jewellery.html")

#route for showing accessories and lingerie category page
@app.route("/showAccessories")
def showAccessories():
	return render_template("accessories.html")

#route for showing north indian category page
@app.route("/showNorthIndian")
def showNorthIndian():
	return render_template("north-indian.html")

#route for showing north indian category page
@app.route("/showSouthIndian")
def showSouthIndian():
	return render_template("south-indian.html")

#todo - add parameter to route with id for product, db query and send response to FE
#route for showing product details
@app.route("/showProductDetails") 
def showProductDetails():
	return render_template("product-details.html")

def getProducts(category, page):
	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#pagination - fetch 20 items per page, offset = 20 * page number - 20
	limit = 20
	page = int(page)
	offset = (page * limit) - limit
	cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.deleted <> 1 ORDER BY it.item_id LIMIT %s OFFSET %s", (category, limit, offset))

	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	cursor.close()
	cxn.close()

	return data

#make sure the right script is being run
if __name__ == "__main__":
	#runs the application from the app variable
	app.run()