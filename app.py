from flask import Flask, render_template, request, redirect, json, session
from flaskext.mysql import MySQL
from flask_bcrypt import Bcrypt
import datetime
import math
import os
from werkzeug.utils import secure_filename

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

#set up secret key
app.secret_key = 'Secret Key'

#set defaults for search & filter to persist values across pages
minVal, maxVal, searchVal = 0, 5000, "All"

#Get current path
path = os.getcwd()
#For file Upload
UPLOAD_FOLDER_WEST = os.path.join(path, 'static/images/western')
UPLOAD_FOLDER_NORTH = os.path.join(path, 'static/images/north-indian')
UPLOAD_FOLDER_SOUTH = os.path.join(path, 'static/images/south-indian')
UPLOAD_FOLDER_JEWE = os.path.join(path, 'static/images/jewellery')
UPLOAD_FOLDER_COSM = os.path.join(path, 'static/images/cosmetics')
UPLOAD_FOLDER_ACLI = os.path.join(path, 'static/images/accessories')


#set up a route for the default page (root URL)
@app.route("/")
def main():
	isAdmin = None

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges and hide some functionality
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1

	cursor.close()
	cxn.close()

	return render_template('index.html', user_type = isAdmin)

#route to show signup page
@app.route("/signUpPage")
def signUpPage():
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
				session['email'] = _email
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

#route to show signin page
@app.route("/signInPage")
def signInPage():
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
				session['email'] = data[0][0]
				return redirect("/")
			else:
				return render_template("error.html", error = 'Incorrect Username or Password!')
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


#route to render new item page
@app.route("/newPage")
def newItemPage():
	isAdmin = None

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges and hide some functionality
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1
		
	if isAdmin == 1:
		return render_template("add-item.html")
	else:
		return render_template("error.html", error = 'You are not logged in OR You cannot access this page')

	cursor.close()
	cxn.close()	

#route to add new item
@app.route("/new", methods=['POST'])
def newItem():
	#retrieving data from the data dictionary used
	keys = request.form.keys()
	_name = request.form["name"]
	_price = request.form["price"]
	_category = request.form["categories"]
	_description = request.form["desc"]
	_deleted = request.form["delStatus"]

	#as there are multiple values of size & quantity, we store them in this dictionary
	_sizeInfo = {}
	for key in keys:
		if "size" in key:
			_sizeInfo[key] = request.form[key]

	#sizes is a dummy key used to allow further addition of sizes. So, we remove it here.
	del _sizeInfo['sizes']

	#save sizes with corresponding quantities
	_sizeQty = {}
	sKeys = _sizeInfo.keys()
	for key in sKeys:
		value = _sizeInfo[key]
		size_and_qty = value.split(' ')

		size_info = size_and_qty[0]
		size = size_info[5 :]
		qty_info = size_and_qty[1]
		qty = qty_info[9 :]
		_sizeQty[size] = qty

	#accessing files from file list and preprocessing them to handle images
	images = request.files.getlist('image_data')
	
	for img in images:
		fname = secure_filename(img.filename)
		if fname != '':
			if _category == 'west':
				img.save(os.path.join(UPLOAD_FOLDER_WEST, fname))
			elif _category == 'noin':
				img.save(os.path.join(UPLOAD_FOLDER_NORTH, fname))
			elif _category == 'soin':
				img.save(os.path.join(UPLOAD_FOLDER_SOUTH, fname))
			elif _category == 'acli':
				img.save(os.path.join(UPLOAD_FOLDER_ACLI, fname))
			elif _category == 'cosm':
				img.save(os.path.join(UPLOAD_FOLDER_COSM, fname))
			else:
				img.save(os.path.join(UPLOAD_FOLDER_JEWE, fname))

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#insert into item table
	cursor.execute("INSERT INTO item (price, category_id, item_name, item_description, deleted) VALUES (%s, %s, %s, %s, %s)", (float(_price), _category, _name, _description, _deleted))
	cxn.commit()

	#first retrieve item_id
	cursor.execute("SELECT item_id FROM item WHERE price = %s AND category_id = %s AND item_name = %s AND item_description = %s AND deleted = %s", (float(_price), _category, _name, _description, _deleted))
	data = cursor.fetchall()
	_id = data[0][0]

	#insert into item_images table
	for img in images:
		fname = secure_filename(img.filename)
		if fname != '':
			cursor.execute("INSERT INTO item_images VALUES (%s, %s)", (_id, fname))
			cxn.commit()

	#insert into item_size table
	for sq in _sizeQty:
		size = sq
		qty = _sizeQty[sq]
		cursor.execute("INSERT INTO item_size VALUES (%s, %s, %s)", (_id, size, qty))
		cxn.commit()

	return redirect(request.referrer)

#route to show edit item form
@app.route("/productInfo/<id>", methods = ['GET'])
def editProduct(id):
	isAdmin = None

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges and hide some functionality
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1
		
	if isAdmin == 1:
		#get product data from db
		cursor.execute("SELECT * FROM item WHERE item_id = %s", id)
		data = cursor.fetchall()

		cursor.execute("SELECT * FROM item_size WHERE item_id = %s", id)
		size_qty = cursor.fetchall()

		available = []
		for sq in size_qty:
			available.append(sq[1])

		cursor.execute("SELECT * FROM item_images WHERE item_id = %s", id)
		images = cursor.fetchall()

		cursor.close()
		cxn.close()

		all_sizes = ['one-size','0','2','4','6','8','10','12','14','16','18','20']

		return render_template("update-item.html", data = data, size_qty = size_qty, images = images, all_sizes = all_sizes, available = available)
		
	else:
		return render_template("error.html", error = 'You are not logged in OR You cannot access this page')

#route to update selected product
#as HTML does not allow PUT method, we are using POST to update data
@app.route("/productData/<id>", methods = ['POST'])
def productUpdate(id):
	isAdmin = None

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges and hide some functionality
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1
		
	if isAdmin == 1:
		#retrieving data from the data dictionary used
		_name = request.form["name"]
		_price = request.form["price"]
		_category = request.form["cate"]
		_description = request.form["desc"]
		_keys = request.form.keys()

		#as there are multiple values of size & quantity, we store them in this dictionary
		#similarly, we obtain the removed image file names
		_sizeInfo = {}
		_removedImgs = {}
		for key in _keys:
			if "size" in key:
				_sizeInfo[key] = request.form[key]
			if "removeImage_" in key:
				_removedImgs[key] = request.form[key]

		#sizes is a dummy key used to allow further addition of sizes. So, we remove it here.
		del _sizeInfo['sizes']

		#save sizes with corresponding quantities
		_sizeQty = {}
		sKeys = _sizeInfo.keys()
		for key in sKeys:
			value = _sizeInfo[key]
			size_and_qty = value.split(' ')

			#for those already present in the table
			if len(size_and_qty) == 4:
				size = size_and_qty[1]
				qty = size_and_qty[3]

			#for those newly entered/updated
			else:
				size_info = size_and_qty[0]
				size = size_info[5 :]
				qty_info = size_and_qty[1]
				qty = qty_info[9 :]

			_sizeQty[size] = qty

		#accessing files from file list and preprocessing them to handle images
		images = request.files.getlist('image_data')
		
		for img in images:
			fname = secure_filename(img.filename)
			if fname != '':
				if _category == 'west':
					img.save(os.path.join(UPLOAD_FOLDER_WEST, fname))
				elif _category == 'noin':
					img.save(os.path.join(UPLOAD_FOLDER_NORTH, fname))
				elif _category == 'soin':
					img.save(os.path.join(UPLOAD_FOLDER_SOUTH, fname))
				elif _category == 'acli':
					img.save(os.path.join(UPLOAD_FOLDER_ACLI, fname))
				elif _category == 'cosm':
					img.save(os.path.join(UPLOAD_FOLDER_COSM, fname))
				else:
					img.save(os.path.join(UPLOAD_FOLDER_JEWE, fname))

		#connect to the db
		cxn = mysql.connect()
		cursor = cxn.cursor()

		#update item table
		cursor.execute("UPDATE item SET price = %s, item_name = %s, item_description = %s WHERE item_id = %s", (float(_price), _name, _description, id))
		cxn.commit()

		#update item_images table
		#insert new images (if any)
		for img in images:
			fname = secure_filename(img.filename)
			if fname != '':
				cursor.execute("INSERT INTO item_images VALUES (%s, %s)", (id, fname))
				cxn.commit()

		#obtain list of any removed images
		imgNames = []
		for r_img in _removedImgs:
			name = r_img[12 :]
			imgNames.append(name)

		#delete identified images from the db
		for img in imgNames:
			cursor.execute("DELETE FROM item_images WHERE item_id = %s AND image_id = %s", (id, img))
			cxn.commit()

		for img in imgNames:
			if _category == 'west':
				os.remove(os.path.join(UPLOAD_FOLDER_WEST, img))
			elif _category == 'noin':
				os.remove(os.path.join(UPLOAD_FOLDER_NORTH, img))
			elif _category == 'soin':
				os.remove(os.path.join(UPLOAD_FOLDER_SOUTH, img))
			elif _category == 'acli':
				os.remove(os.path.join(UPLOAD_FOLDER_ACLI, img))
			elif _category == 'cosm':
				os.remove(os.path.join(UPLOAD_FOLDER_COSM, img))
			else:
				os.remove(os.path.join(UPLOAD_FOLDER_JEWE, img))

		#update item_size table
		#first we retrieve existing size entries from the table
		cursor.execute("SELECT size FROM item_size WHERE item_id = %s", id)
		sizeData = cursor.fetchall()
		
		table_sizes = []
		for sz in sizeData:
			table_sizes.append(sz[0])

		iKeys = _sizeQty.keys()
		input_sizes = []
		for key in iKeys:
			input_sizes.append(key)

		for sq in _sizeQty:
			size = sq
			qty = _sizeQty[sq]

			#we update size values for sizes modified by user
			if size in table_sizes:
				cursor.execute("UPDATE item_size SET quantity = %s WHERE item_id = %s AND size = %s", (qty, id, size))
				cxn.commit()

			#we insert size values if they do not exist already in the table
			else:
				cursor.execute("INSERT INTO item_size VALUES (%s, %s, %s)", (id, size, qty))
				cxn.commit()

		#we remove existing entries if they are now deleted by user
		for size in table_sizes:
			if size not in input_sizes:
				cursor.execute("DELETE FROM item_size WHERE item_id = %s AND size = %s", (id, size))
				cxn.commit()

		if _category == "west":
			return redirect('/westernHome')
		elif _category == "noin":
			return redirect('/northIndianHome')
		elif _category == "soin":
			return redirect('/southIndianHome')
		elif _category == "jewe":
			return redirect('/jewelleryHome')
		elif _category == "cosm":
			return redirect('/cosmeticsHome')
		else:
			return redirect('/accessoriesHome')

	else:
		return render_template("error.html", error = 'You are not logged in OR You cannot access this page')
	

#route to delete selected product - As it is soft delete, we use POST
@app.route("/product/<id>", methods = ['POST'])
def product(id):
	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#We toggle deletion status. So, we initially retrieve deleted flag
	cursor.execute("SELECT deleted FROM item WHERE item_id = %s", id)
	data = cursor.fetchall()

	#set delete flag (1-0 = 1 & 1-1 = 0) Toggles the value
	_deleted = 1 - data[0][0]

	#As the delete is soft delete, we just update the deleted flag
	cursor.execute("UPDATE item SET deleted = %s WHERE item_id = %s", (_deleted, id))
	cxn.commit()

	cursor.close()
	cxn.close()

	return redirect(request.referrer)


#route for showing default/home page for western category
@app.route("/westernHome")
def westernHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"

	products_info, total, isAdmin = getProducts('west', 1)
	if isAdmin:
		return render_template("western-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("western.html", data = products_info, page_count = math.ceil(total/20))

#route for showing western category page
@app.route("/western/<page>", methods = ['GET'])
def western(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('west', page, searchVal, minVal, maxVal)
	
	if isAdmin:
		return render_template("western-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("western.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)

#route for showing default/home page for cosmetics category
@app.route("/cosmeticsHome")
def cosmeticsHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"

	products_info, total, isAdmin = getProducts('cosm', 1)
	if isAdmin:
		return render_template("cosmetics-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("cosmetics.html", data = products_info, page_count = math.ceil(total/20))

#route for showing cosmetics category page
@app.route("/cosmetics/<page>", methods = ['GET'])
def cosmetics(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('cosm', page, searchVal, minVal, maxVal)

	if isAdmin:
		return render_template("cosmetics-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("cosmetics.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)


#route for showing default/home page for jewellery category
@app.route("/jewelleryHome")
def jewelleryHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"

	products_info, total, isAdmin = getProducts('jewe', 1)
	if isAdmin:
		return render_template("jewellery-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("jewellery.html", data = products_info, page_count = math.ceil(total/20))

#route for showing jewellery category page
@app.route("/jewellery/<page>", methods = ['GET'])
def jewellery(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('jewe', page, searchVal, minVal, maxVal)

	if isAdmin:
		return render_template("jewellery-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("jewellery.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)


#route for showing default/home page for accessories and lingerie category
@app.route("/accessoriesHome")
def accessoriesHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"

	products_info, total, isAdmin = getProducts('acli', 1)
	if isAdmin:
		return render_template("accessories-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("accessories.html", data = products_info, page_count = math.ceil(total/20))

#route for showing accessories and lingerie category page
@app.route("/accessories/<page>", methods = ['GET'])
def accessories(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('acli', page, searchVal, minVal, maxVal)
	if isAdmin:
		return render_template("accessories-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("accessories.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)


#route for showing default/home page for south indian category
@app.route("/southIndianHome")
def southIndianHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"

	products_info, total, isAdmin = getProducts('soin', 1)
	if isAdmin:
		return render_template("south-indian-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("south-indian.html", data = products_info, page_count = math.ceil(total/20))

#route for showing south indian category page
@app.route("/southIndian/<page>", methods = ['GET'])
def southIndian(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('soin', page, searchVal, minVal, maxVal)

	if isAdmin:
		return render_template("south-indian-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("south-indian.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)


#route for showing default/home page for north indian category
@app.route("/northIndianHome")
def northIndianHome():
	global minVal, maxVal, searchVal
	minVal, maxVal, searchVal = 0, 5000, "All"
	
	products_info, total, isAdmin = getProducts('noin', 1)
	if isAdmin:
		return render_template("north-indian-admin.html", data = products_info, page_count = math.ceil(total/20))
	else:
		return render_template("north-indian.html", data = products_info, page_count = math.ceil(total/20))

#route for showing north indian category page
@app.route("/northIndian/<page>", methods = ['GET'])
def northIndian(page):
	global minVal, maxVal, searchVal
	if(request.args):
		minVal = request.args['min-price']
		maxVal = request.args['max-price']
		searchVal = request.args['search']

	products_info, total, isAdmin = getCustomizedProducts('noin', page, searchVal, minVal, maxVal)
	if isAdmin:
		return render_template("north-indian-admin.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)
	else:
		return render_template("north-indian.html", data = products_info, page_count = math.ceil(total/20), search = searchVal, min = minVal, max = maxVal)

#route for showing product details
@app.route("/productDetails/<id>") 
def productDetails(id):
	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#query to fetch item data from the db
	cursor.execute("SELECT * FROM item WHERE item_id = %s", id) 
	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	#query to fetch item images from the db
	cursor.execute("SELECT * FROM item_images WHERE item_id = %s", id)
	desc = cursor.description
	column_names = [col[0] for col in desc]
	images = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	#query to fetch item size from the db
	cursor.execute("SELECT * FROM item_size WHERE item_id = %s", id)
	desc = cursor.description
	column_names = [col[0] for col in desc]
	sizes = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	return render_template("product-details.html", data = data, images = images, sizes = sizes)

def getProducts(category, page):
	isAdmin = None

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1

	#pagination - fetch 20 items per page, offset = 20 * page number - 20
	limit = 20
	page = int(page)
	offset = (page * limit) - limit

	if isAdmin:
		cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s ORDER BY it.item_id LIMIT %s OFFSET %s", (category, limit, offset))
	else:
		cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.deleted <> 1 ORDER BY it.item_id LIMIT %s OFFSET %s", (category, limit, offset))

	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

    #In home page, we should have navigation available for all other pages. So, we need count of total records in the database per category
	if isAdmin:
		cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s ORDER BY it.item_id", (category))
	else:
		cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.deleted <> 1 ORDER BY it.item_id", (category))
	
	count = len(cursor.fetchall())
	cursor.close()
	cxn.close()

	return data, count, isAdmin

def getCustomizedProducts(category, page, searchVal, minVal, maxVal):
	isAdmin = None

	#convert into suitable types
	minimum = float(minVal)
	maximum = float(maxVal)

	#connect to the db
	cxn = mysql.connect()
	cursor = cxn.cursor()

	#If admin, give special privileges
	if('email' in session):
		_email = session['email']
		cursor.execute("SELECT is_admin FROM account WHERE email = %s", (_email))
		user = cursor.fetchall()
		if(user[0][0] == 1): 
			isAdmin = 1

	#pagination - fetch 20 items per page, offset = 20 * page number - 20
	limit = 20
	page = int(page)
	offset = (page * limit) - limit

	#Obtains matching records per page
	if(searchVal.lower() == "All".lower()):
		if isAdmin:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s ORDER BY it.item_id LIMIT %s OFFSET %s", (category, minimum, maximum, limit, offset))
		else:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.deleted <> 1 ORDER BY it.item_id LIMIT %s OFFSET %s", (category, minimum, maximum, limit, offset))
		
	else:
		if isAdmin:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.item_description like %s ORDER BY it.item_id LIMIT %s OFFSET %s", (category, minimum, maximum, "%"+searchVal+"%", limit, offset))
		else:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.item_description like %s AND it.deleted <> 1 ORDER BY it.item_id LIMIT %s OFFSET %s", (category, minimum, maximum, "%"+searchVal+"%", limit, offset))
		
	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	#Obtains count of matching records
	if(searchVal.lower() == "All".lower()):
		if isAdmin:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s ORDER BY it.item_id", (category, minimum, maximum))
		else:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.deleted <> 1 ORDER BY it.item_id", (category, minimum, maximum))
	else:
		if isAdmin:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.item_description like %s ORDER BY it.item_id", (category, minimum, maximum, "%"+searchVal+"%"))
		else:
			cursor.execute("SELECT *, (SELECT image_id FROM item_images img WHERE img.item_id = it.item_id limit 1) AS image FROM item it WHERE it.category_id = %s AND it.price >= %s AND it.price <= %s AND it.item_description like %s AND it.deleted <> 1 ORDER BY it.item_id", (category, minimum, maximum, "%"+searchVal+"%"))
		
	#Finds total customized products
	count = len(cursor.fetchall())

	cursor.close()
	cxn.close()

	return data, count, isAdmin

#route to check if user is signed in
@app.route("/checkSignedIn")
def checkSignedIn():
	if('email' in session):
		return json.dumps({'message': 'Logged In'})
	else:
		return json.dumps({'message': 'Logged Out'})

#route to logout
@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect("/")

#route to user profile
@app.route("/userProfile")
def userProfile():
	if('email' in session):
		
		#connect to db and fetch user details
		cxn = mysql.connect()
		cursor = cxn.cursor()

		cursor.execute("SELECT * FROM account WHERE email = %s", (session.get('email')))
		desc = cursor.description
		column_names = [col[0] for col in desc]
		data = [dict(zip(column_names, row))  
        	for row in cursor.fetchall()]
		cursor.close()
		cxn.close()

		return render_template('profile.html', data = data)
	else:
		return redirect('/signInPage')

#route to add wishlist item
@app.route("/addToWishlist", methods = ['PUT'])
def addToWishlist():
	itemId = request.form.get('item_id')
	user = session.get('email')

	#connect to db and insert item
	cxn = mysql.connect()
	cursor = cxn.cursor()

	cursor.execute("INSERT INTO wishlist VALUES (%s, %s)", (user, itemId))

	if(len(cursor.fetchall()) == 0):
		cxn.commit()
		cursor.close
		cxn.close()
		return json.dumps({'success': 'Item added'})
	else:
		return json.dumps({'error': 'Item not added'})

#route to show user wishlist
@app.route("/showWishlist")
def showWishlist():
	user = session.get('email')

	#connect to db and fetch user wishlist
	cxn = mysql.connect()
	cursor = cxn.cursor()

	cursor.execute("SELECT w.email, w.item_id, i.price, i.category_id, i.item_name, i.item_description, (SELECT img.image_id FROM item_images img WHERE img.item_id = i.item_id LIMIT 1) AS image_id FROM wishlist w, item i WHERE w.email = %s AND w.item_id = i.item_id", user)
	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]
	cursor.close()
	cxn.close()

	return render_template('wishlist.html', data = data)

#route to delete from wishlist
@app.route("/deleteFromWishlist/<id>", methods = ['DELETE'])
def deleteFromWishlist(id):
	user = session.get('email')

	#connect to db and delete item from wishlist
	cxn = mysql.connect()
	cursor = cxn.cursor()

	try:
		cursor.execute("DELETE FROM wishlist WHERE email = %s AND item_id = %s", (user, id))
		cxn.commit()
		response = json.dumps({'success': 'Deleted'})
	except Exception as error:
		response = json.dumps({'error': str(error)})
	finally:
		cursor.close
		cxn.close()

	return response

#route to book appointment page
@app.route("/showBookAppointment")
def showBookAppointment():
	user = session.get('email')

	#connect to db and fetch user wishlist
	cxn = mysql.connect()
	cursor = cxn.cursor()

	cursor.execute("SELECT w.email, w.item_id, i.price, i.category_id, i.item_name, i.item_description, (SELECT img.image_id FROM item_images img WHERE img.item_id = i.item_id LIMIT 1) AS image_id FROM wishlist w, item i WHERE w.email = %s AND w.item_id = i.item_id", user)

	desc = cursor.description
	column_names = [col[0] for col in desc]
	items = cursor.fetchall()
	result = []

	for row in items:
		data = dict(zip(column_names, row))
		cursor.execute('SELECT * FROM item_size WHERE item_id = %s', row[1])
		desc_sizes = cursor.description
		column_names_sizes = [col[0] for col in desc_sizes]
		sizes = [dict(zip(column_names_sizes, row))  
        	for row in cursor.fetchall()]
		data['sizes'] = sizes
		result.append(data)

	cursor.close()
	cxn.close()

	return render_template('book-appt.html', data = result)

#route to get available dates and times for booking an apppointment
@app.route("/getDates")
def getDates():
	days = list()
	bookings = dict()
	times = set(('10', '12', '2', '4'))

	#get dates for next 4 days
	for i in range(1, 5):
		days.append((datetime.datetime.today() + datetime.timedelta(days = i)).strftime('%Y-%m-%d'))

	#connect to db and get booked times for these dates
	cxn = mysql.connect()
	cursor = cxn.cursor()

	for day in days:
		cursor.execute("SELECT appt_start_time FROM appointment WHERE appt_date = %s", day)
		data = cursor.fetchall()

		dbData = set()
		for item in data: 
			dbData.add(item[0])

		availableTimes = list(times.difference(dbData))
		if(len(availableTimes) > 0):
			bookings[day] = availableTimes
		
	cursor.close()
	cxn.close()

	if(len(bookings) > 0):
		return json.dumps(bookings)
	else:
		return json.dumps({'error': 'No appointments available'})

@app.route("/bookAppointment", methods = ['POST'])
def bookAppointment():
	req = request.form.to_dict()
	data = list(req.keys())[0]
	items = data.split(",")
	itemIds = list()
	itemSizes = list()
	itemQtys = list()

	for item in items:
		if("date" in item):
			date = item.split(":")[1]
		elif("time" in item):
			time = item.split(":")[1]
			time = time[0: len(time) - 2]
		elif("item_id" in item):
			itemId = item.split(":")[1]
			itemId = itemId[1 : len(itemId) - 1]
			itemIds.append(itemId)
		elif("item_size" in item):
			itemSize = item.split(":")[1]
			itemSize = itemSize[1 : len(itemSize) - 1]
			itemSizes.append(itemSize)
		elif("item_qty" in item):
			itemQty = item.split(":")[1]
			itemQty = itemQty[: len(itemQty) - 1]
			itemQtys.append(itemQty)

	cxn = mysql.connect()
	cursor = cxn.cursor()
	
	cursor.execute("INSERT INTO appointment(email, appt_date, appt_start_time) VALUES(%s, %s, %s)", (session.get('email'), date[1 : len(date) - 1], time[1 : len(time) - 1]))
	if(len(cursor.fetchall()) == 0):
		cxn.commit()

		cursor.execute("SELECT LAST_INSERT_ID()")
		apptId = cursor.fetchall()[0][0]
	
		for i in range(len(itemIds)):
			cursor.execute("INSERT INTO appointment_items VALUES (%s, %s, %s, %s)", (apptId, itemIds[i], itemSizes[i], itemQtys[i]))
		if(len(cursor.fetchall()) != 0):
			return json.dumps({'error': 'Not booked'})
		else:
			cxn.commit()

	else:
		return json.dumps({'error': 'Not booked'})

	return json.dumps({'success': 'Booked'})

#route to show appointment history
@app.route("/appointments")
def getAppointments():
	user = session.get('email')

	cxn = mysql.connect()
	cursor = cxn.cursor()

	cursor.execute("SELECT a.appt_date, a.appt_start_time, ai.item_id, ai.size, ai.quantity, i.price, i.category_id, i.item_name, (SELECT image_id FROM item_images img WHERE img.item_id = ai.item_id LIMIT 1) image_id FROM appointment a, appointment_items ai, item i WHERE email = %s AND a.appt_id = ai.appt_id AND i.deleted != 1 AND i.item_id = ai.item_id ORDER BY a.appt_date DESC, a.appt_start_time", user)
	
	desc = cursor.description
	column_names = [col[0] for col in desc]
	data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]

	cursor.close()
	cxn.close()

	return render_template('appointment-history.html', data = data)

#make sure the right script is being run
if __name__ == "__main__":
	#runs the application from the app variable
	app.run()
