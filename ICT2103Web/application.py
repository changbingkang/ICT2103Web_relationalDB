#from copyreg import constructor
#url_for is function call to link css file
from flask import Flask, redirect, render_template, session, url_for, request, session, g
from database import get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os 
import sqlite3


# flask constructor
# pass the name of the application 
# assign the application as "app"
application = Flask(__name__)

#create session variable
application.config['SECRET_KEY'] = os.urandom(24)


@application.teardown_appcontext
def close_database(error):
    if hasattr(g, 'ICT2103Web_db'):
        g.ICT2103Web_db.close()

def get_active_user():
    user = None
    #if there is user in the session
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name =?', [user])
        user = user_cur.fetchone()

    return user

#start first page every single time
#route for starting page
#@application.route('/')
#create a function for the first page/starting route
# function to access home page
# def index():
#     user = get_active_user()
#     return render_template('home.html', user = user)


@application.route('/', methods = ["POST", "GET"])
def index():
    user = get_active_user()
    db = get_database()
    #retrieve empployee
    home_cur = db.execute('Select * from population')
    allpop = home_cur.fetchall()
    return render_template('home.html', user = user, allpop = allpop)

# create route and function call for login page
# post and get method is allow
@application.route('/login', methods=["POST", "GET"])
def userLogin():
    user = get_active_user()
    error = None
    db = get_database()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        #check user password input is same as the user retrieve
        if user:
            if check_password_hash(user['password'], password):
                #create session called user to store the user inout name
                session['user'] = user['name']
                return redirect(url_for('userDashboard'))
            else:
                error = "Username or Password not match"
        else:
            error = "Username or password did not match. Try Again."

    return render_template('login.html', loginfail = error, user = user)

# create route and function call for register page
# post and get method is allow
@application.route('/register', methods=["POST", "GET"])
def userRegister():
    user = get_active_user()
    db = get_database()
    error = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        privacy_password = generate_password_hash(password)

        #check user exist
        dbuser_cursor = db.execute('select * from users where name = ?', [name])
        existing_user = dbuser_cursor.fetchone()
        if existing_user:
            return render_template('register.html', registererror = 'username already taken, try different username.')

        # [name,password] is the input declared
        #insert user record
        db.execute('INSERT INTO users (name, password) values(?,?)', [name, privacy_password])
        db.commit()
        return redirect(url_for('index'))
    return render_template('register.html', user = user)

# create route and function call for Dashboard page
@application.route('/dashboard', methods = ["POST", "GET"])
def userDashboard():
    user = get_active_user()
    db = get_database()
    #retrieve empployee
    emp_cur = db.execute('Select * from emp')
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp = allemp)

# create route and function call for Add Employee page
@application.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    user = get_active_user()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('INSERT INTO emp (name, email, phone, address) values(?,?,?,?)', [name, email, phone, address])
        db.commit()
        return redirect(url_for('userDashboard'))
    return render_template('addnewemployee.html', user = user)

# create route and function call for single Employee page
@application.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_active_user()
    db = get_database()
    emp_cur = db.execute('SELECT * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('singleemployee.html', user = user, single_emp = single_emp)

#before update fetch all info from the id
@application.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_active_user()
    db = get_database()
    emp_cur = db.execute('SELECT * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)

# create route and function call for single Employee page
@application.route('/updateemployee', methods = ["POST","GET"] )
def updateemployee():
    user = get_active_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('UPDATE emp set name = ?, email = ?, phone = ?, address = ? where empid = ?', [name, email, phone, address, empid])
        db.commit()
        return redirect(url_for('userDashboard'))      
    return render_template('updateemployee.html', user = user)


@application.route('/deleteemployee/<int:empid>', methods = ["POST", "GET"])
def deleteemployee(empid):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('userDashboard'))
    return render_template('dashboard.html', user = user)

    
    return render_template('updateemployee.html', user = user)

# Retrieve population 
# create route and function call for Dashboard page
@application.route('/home', methods = ["POST", "GET"])
def home():
    user = get_active_user()
    db = get_database()
    #retrieve empployee
    home_cur = db.execute('Select * from population')
    allpop = home_cur.fetchall()
    return render_template('home.html', user = user, allpop = allpop)


# create route and function call for Add town population page
@application.route('/addnewtown', methods = ["POST", "GET"])
def addnewtown():
    user = get_active_user()
    if request.method == "POST":
        year = request.form['financial_year']
        town = request.form['town']
        population = request.form['population']
        db = get_database()
        db.execute('INSERT INTO population (financial_year, town, population) values(?,?,?)', [year, town, population])
        db.commit()
        return redirect(url_for('index'))
    return render_template('addtownpop.html', user = user)


@application.route('/deletetown/<string:town>', methods = ["POST", "GET"])
def deletetown(town):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from population where town = ?', [town])
        db.commit()
        return redirect(url_for('index'))
    return render_template('home.html', user = user)   

#before update fetch all info from the id
@application.route('/fetchonetown/<string:town>')
def fetchonetown(town):
    user = get_active_user()
    db = get_database()
    town_cur = db.execute('SELECT * from population where town = ?', [town])
    single_town = town_cur.fetchone()
    return render_template('updatetownpop.html', user = user, single_town = single_town)

# create route and function call for single Employee page
@application.route('/updatetownpop', methods = ["POST","GET"] )
def updatetownpop():
    user = get_active_user()
    if request.method == 'POST':
        year = request.form['financial_year']
        town = request.form['town']
        population = request.form['population']
        db = get_database()
        db.execute('UPDATE or ignore population set financial_year = ?, town = ?, population = ?' , [year, town, population])
        db.commit()
        return redirect(url_for('index'))      
    return render_template('updatetownpop.html', user = user)

# create route and function call for school info page
@application.route('/schoolinfo', methods = ["POST", "GET"])
def schoolinfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    school_cur = db.execute('Select * from school')
    allsch = school_cur.fetchall()
    return render_template('schoolDashboard.html', user = user, allsch = allsch)

# create route and function call for Add school page
@application.route('/addnewschool', methods = ["POST", "GET"])
def addnewschool():
    user = get_active_user()
    if request.method == "POST":
        name = request.form['name']
        website = request.form['url_address']
        address = request.form['address']
        postal = request.form['postal']
        phone = request.form['phone']
        email = request.form['email']
        mrt = request.form['mrt']
        bus = request.form['bus']
        town = request.form['town']
        zone = request.form['zone']
        type = request.form['type']
        nature = request.form['nature']
        level = request.form['mainlvl']
        db = get_database()
        db.execute('INSERT INTO school (name, url_address, address, postal, phone, email, mrt, bus, town, zone, type, nature, mainlvl) values(?,?,?,?,?,?,?,?,?,?,?,?,?)', [name, website, address, postal, phone, email, mrt, bus, town, zone, type, nature, level])
        db.commit()
        return redirect(url_for('schoolinfo'))
    return render_template('addschoolinfo.html', user = user)

#before update fetch all info from the name
@application.route('/fetchoneschool/<string:name>')
def fetchoneschool(name):
    user = get_active_user()
    db = get_database()
    school_cur = db.execute('SELECT * from school where name = ?', [name])
    single_school = school_cur.fetchone()
    return render_template('updateschoolinfo.html', user = user, single_school = single_school)

# create route and function call for single Employee page
@application.route('/updateschoolinfo', methods = ["POST","GET"] )
def updateschoolinfo():
    user = get_active_user()
    if request.method == 'POST':
        name = request.form['name']
        website = request.form['url_address']
        address = request.form['address']
        postal = request.form['postal']
        phone = request.form['phone']
        email = request.form['email']
        mrt = request.form['mrt']
        bus = request.form['bus']
        town = request.form['town']
        zone = request.form['zone']
        type = request.form['type']
        nature = request.form['nature']
        level = request.form['mainlvl']
        db = get_database()
        db.execute('UPDATE or IGNORE school set name = ?, url_address=?, address=?, postal=?, phone=?, email=?, mrt=?, bus=?, town=?, zone=?, type=?, nature=?, mainlvl=?' , [name, website, address, postal, phone, email, mrt, bus, town, zone, type, nature, level])
        db.commit()
        return redirect(url_for('schoolinfo'))      
    return render_template('updateschoolinfo.html', user = user)

@application.route('/deleteschool/<string:name>', methods = ["POST", "GET"])
def deleteschool(name):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from school where name = ?', [name])
        db.commit()
        return redirect(url_for('schoolinfo'))
    return render_template('schoolDashboard.html', user = user)   

# create route and function call for single Employee page
@application.route('/singleschool/<string:name>')
def singleschool(name):
    user = get_active_user()
    db = get_database()
    param =  '%'+name+'%'
    sch_cur = db.execute('SELECT * from school join cca on school.name = cca.name join subject on school.name = subject.name where school.name like ?', [param])
    # School inner join cca inner join 
    # Subject and CCA
    # single_sch = sch_cur.fetchone()
    all_sch_info = sch_cur.fetchall()
    print(all_sch_info)
    cca_list = []
    subject_list = []
    for item in all_sch_info:
        cca_list.append(item['cca_name'])
        subject_list.append(item['subject'])
    cca_list = list(dict.fromkeys(cca_list))
    subject_list = list(dict.fromkeys(subject_list))
    cca = '' + cca_list[0]
    subject = '' + subject_list[0]
    cca_size = len(cca_list)
    for i in range (1, cca_size):
        cca += ', ' + cca_list[i]
    subject_size = len(subject_list)
    for i in range (1, subject_size):
        subject += ', ' + subject_list[i]
    return render_template('singleschool.html', user = user, single_sch = all_sch_info[0], cca = cca, subject = subject)

# create route and function call for supermarket page
@application.route('/supermarketsinfo', methods = ["POST", "GET"])
def supermarketsinfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    super_cur = db.execute('Select * from supermarkets')
    allsuper = super_cur.fetchall()
    return render_template('supermarketDashboard.html', user = user, allsuper = allsuper)

#before update fetch all info from the name
@application.route('/fetchonesupermarket/<int:id>')
def fetchonesupermarket(id):
    user = get_active_user()
    db = get_database()
    supermarket_cur = db.execute('SELECT * from supermarkets where id = ?', [id])
    single_supermarket = supermarket_cur.fetchone()
    return render_template('updatesupermarketinfo.html', user = user, single_supermarket = single_supermarket)

# create route and function call for single supermarket page
@application.route('/updatesupermarketinfo', methods = ["POST","GET"] )
def updatesupermarketinfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        town = request.form['town']
        address = request.form['address']
        db = get_database()
        db.execute('UPDATE or IGNORE supermarkets set name = ?, town=?, address=? where id=?', [name, town, address, id])
        db.commit()
        return redirect(url_for('supermarketsinfo'))      
    return render_template('updatesupermarketinfo.html', user = user)


# create route and function call for Add supermarket page
@application.route('/addnewsupermarket', methods = ["POST", "GET"])
def addnewsupermarket():
    user = get_active_user()
    if request.method == "POST":
        name = request.form['name']
        town = request.form['town']
        address = request.form['address']
        db = get_database()
        db.execute('INSERT INTO supermarkets (name, town, address) values(?,?,?)', [name, town, address])
        db.commit()
        return redirect(url_for('supermarketsinfo'))
    return render_template('addsupermarketinfo.html', user = user)

@application.route('/deletesupermarket/<int:id>', methods = ["POST", "GET"])
def deletesupermarket(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from supermarkets where id = ?', [id])
        db.commit()
        return redirect(url_for('supermarketsinfo'))
    return render_template('supermarketDashboard.html', user = user)  

# Retrieve resale flat 
# create route and function call for resale flat page
@application.route('/resaleinfo', methods = ["POST", "GET"])
def resaleinfo():
    user = get_active_user()
    db = get_database()
    #retrieve resale flat
    resale_cur = db.execute('Select * from resaleflat')
    allresale = resale_cur.fetchall()
    return render_template('resaleDashboard.html', user = user, allresale = allresale)

# create route and function call for Add resale flat page
@application.route('/addnewresaleflat', methods = ["POST", "GET"])
def addnewresaleflat():
    user = get_active_user()
    if request.method == "POST":
        month = request.form['month']
        town = request.form['town']
        type = request.form['flat_type']
        block = request.form['block']
        street = request.form['street_name']
        storey = request.form['storey_range']
        size = request.form['sq_size']
        model = request.form['flat_model']
        lease = request.form['lease_commence_date']
        price = request.form['resale_price']
        db = get_database()
        db.execute('INSERT OR REPLACE INTO resaleflat (month, town, flat_type, block, street_name, storey_range, sq_size, flat_model, lease_commence_date, resale_price) values(?,?,?,?,?,?,?,?,?,?)', [month, town, type, block, street, storey, size, model, lease, price])
        db.commit()
        return redirect(url_for('resaleinfo'))
    return render_template('addresaleflat.html', user = user)

@application.route('/deleteresaleflat/<int:id>', methods = ["POST", "GET"])
def deleteresaleflat(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from resaleflat where id = ?', [id])
        db.commit()
        return redirect(url_for('resaleinfo'))
    return render_template('resaleDashboard.html', user = user)  

#before update fetch all info from the name
@application.route('/fetchoneresaleflat/<int:id>')
def fetchoneresaleflat(id):
    user = get_active_user()
    db = get_database()
    resaleflat_cur = db.execute('SELECT * from resaleflat where id = ?', [id])
    single_resaleflat = resaleflat_cur.fetchone()
    return render_template('updateresaleflatinfo.html', user = user, single_resaleflat = single_resaleflat)

# create route and function call for single supermarket page
@application.route('/updateresaleflatinfo', methods = ["POST","GET"] )
def updateresaleflatinfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        month = request.form['month']
        town = request.form['town']
        type = request.form['flat_type']
        block = request.form['block']
        street = request.form['street_name']
        storey = request.form['storey_range']
        size = request.form['sq_size']
        model = request.form['flat_model']
        lease = request.form['lease_commence_date']
        price = request.form['resale_price']
        db = get_database()
        db.execute('UPDATE or IGNORE resaleflat set month=?, town=?, flat_type=?, block=?, street_name=?, storey_range=?, sq_size=?, flat_model=?, lease_commence_date=?, resale_price=? where id=?', [month, town, type, block, street, storey, size, model, lease, price, id])
        db.commit()
        return redirect(url_for('resaleinfo'))      
    return render_template('updateresaleflatinfo.html', user = user)

# create route and function call for cca info page
@application.route('/ccainfo', methods = ["POST", "GET"])
def ccainfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    cca_cur = db.execute('Select * from cca')
    allcca = cca_cur.fetchall()
    return render_template('ccaDashboard.html', user = user, allcca = allcca)

# create route and function call for Add cca page
@application.route('/addnewcca', methods = ["POST", "GET"])
def addnewcca():
    user = get_active_user()
    if request.method == "POST":
        name = request.form['name']
        type = request.form['type']
        cca_group = request.form['cca_group']
        cca_name = request.form['cca_name']
        special_name = request.form['special_name']
        db = get_database()
        db.execute('INSERT INTO cca (name, type, cca_group, cca_name, special_name) values(?,?,?,?,?)', [name, type, cca_group, cca_name, special_name])
        db.commit()
        return redirect(url_for('ccainfo'))
    return render_template('addccainfo.html', user = user)

#before update fetch all info from the name
@application.route('/fetchonecca/<int:id>')
def fetchonecca(id):
    user = get_active_user()
    db = get_database()
    cca_cur = db.execute('SELECT * from cca where id = ?', [id])
    single_cca = cca_cur.fetchone()
    return render_template('updateccainfo.html', user = user, single_cca = single_cca)

# create route and function call for single supermarket page
@application.route('/updateccainfo', methods = ["POST","GET"] )
def updateccainfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        type = request.form['type']
        cca_group = request.form['cca_group']
        cca_name = request.form['cca_name']
        special_name = request.form['special_name']
        db = get_database()
        db.execute('UPDATE or IGNORE cca set name = ?, type=?, cca_group=?, cca_name=?, special_name=? where id=?', [name, type, cca_group, cca_name, special_name, id])
        db.commit()
        return redirect(url_for('ccainfo'))      
    return render_template('updateccainfo.html', user = user)

@application.route('/deletecca/<int:id>', methods = ["POST", "GET"])
def deletecca(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from cca where id = ?', [id])
        db.commit()
        return redirect(url_for('ccainfo'))
    return render_template('ccaDashboard.html', user = user)  

# create route and function call for subject info page
@application.route('/subjectinfo', methods = ["POST", "GET"])
def subjectinfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    subject_cur = db.execute('Select * from subject')
    allsubject = subject_cur.fetchall()
    return render_template('subjectDashboard.html', user = user, allsubject = allsubject)

# create route and function call for Add subject page
@application.route('/addnewsubject', methods = ["POST", "GET"])
def addnewsubject():
    user = get_active_user()
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['subject']
        db = get_database()
        db.execute('INSERT INTO subject (name, subject) values(?,?)', [name, subject])
        db.commit()
        return redirect(url_for('subjectinfo'))
    return render_template('addsubject.html', user = user)

@application.route('/deletesubject/<int:id>', methods = ["POST", "GET"])
def deletesubject(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from subject where id = ?', [id])
        db.commit()
        return redirect(url_for('subjectinfo'))
    return render_template('subjectDashboard.html', user = user)  

# create route and function call for subject info page
@application.route('/pharmacyinfo', methods = ["POST", "GET"])
def pharmacyinfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    pharmacy_cur = db.execute('Select * from pharmacy')
    allpharmacy = pharmacy_cur.fetchall()
    return render_template('pharmacyDashboard.html', user = user, allpharmacy = allpharmacy)

@application.route('/deletepharmacy/<int:id>', methods = ["POST", "GET"])
def deletepharmacy(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from pharmacy where id = ?', [id])
        db.commit()
        return redirect(url_for('pharmacyinfo'))
    return render_template('pharmacyDashboard.html', user = user)  

# create route and function call for subject info page
@application.route('/rentalinfo', methods = ["POST", "GET"])
def rentalinfo():
    user = get_active_user()
    db = get_database()
    #retrieve school info
    rental_cur = db.execute('Select * from rental')
    allrental = rental_cur.fetchall()
    return render_template('rentalDashboard.html', user = user, allrental = allrental)

@application.route('/deleterental/<int:id>', methods = ["POST", "GET"])
def deleterental(id):
    user = get_active_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from rental where id = ?', [id])
        db.commit()
        return redirect(url_for('rentalinfo'))
    return render_template('rentalDashboard.html', user = user)  

# create route and function call for single Employee page
@application.route('/singlepharm/<string:town>')
def singlepharm(town):
    user = get_active_user()
    db = get_database()
    param =  '%'+town+'%'
    pharm_cur = db.execute('SELECT * from pharmacy where town like ?', [town])
    all_pharm_info = pharm_cur.fetchall()
    print(all_pharm_info)
    return render_template('singlepharmacy.html', user = user, all_pharm_info = all_pharm_info)

#before update fetch all info from the name
@application.route('/fetchonepharmacy/<int:id>')
def fetchonepharmacy(id):
    user = get_active_user()
    db = get_database()
    pharmacy_cur = db.execute('SELECT * from pharmacy where id = ?', [id])
    single_pharmacy = pharmacy_cur.fetchone()
    return render_template('updatepharmacyinfo.html', user = user, single_pharmacy = single_pharmacy)

# create route and function call for single supermarket page
@application.route('/updatepharmacyinfo', methods = ["POST","GET"] )
def updatepharmacyinfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        town = request.form['town']
        pharmacy_name = request.form['pharmacy_name']
        incharge = request.form['incharge']
        address = request.form['address']
        db = get_database()
        db.execute('UPDATE or IGNORE pharmacy set town=?, pharmacy_name=?, incharge=?, address=? where id=?', [town, pharmacy_name, incharge, address, id])
        db.commit()
        return redirect(url_for('pharmacyinfo'))      
    return render_template('updatepharmacyinfo.html', user = user)

#before update fetch all info from the name
@application.route('/fetchonesubject/<int:id>')
def fetchonesubject(id):
    user = get_active_user()
    db = get_database()
    subject_cur = db.execute('SELECT * from subject where id = ?', [id])
    single_subject = subject_cur.fetchone()
    return render_template('updatesubjectinfo.html', user = user, single_subject = single_subject)

# create route and function call for single supermarket page
@application.route('/updatesubjectinfo', methods = ["POST","GET"] )
def updatesubjectinfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        subject = request.form['subject']
        db = get_database()
        db.execute('UPDATE or IGNORE subject set name=?, subject=? where id=?', [name, subject, id])
        db.commit()
        return redirect(url_for('subjectinfo'))      
    return render_template('updatesubjectinfo.html', user = user)

#before update fetch all info from the name
@application.route('/fetchonerental/<int:id>')
def fetchonerental(id):
    user = get_active_user()
    db = get_database()
    rental_cur = db.execute('SELECT * from rental where id = ?', [id])
    single_rental = rental_cur.fetchone()
    return render_template('updaterentalinfo.html', user = user, single_rental = single_rental)

# create route and function call for single supermarket page
@application.route('/updaterentalinfo', methods = ["POST","GET"] )
def updaterentalinfo():
    user = get_active_user()
    if request.method == 'POST':
        id = request.form['id']
        town = request.form['town']
        rent_date = request.form['rental_approve_date']
        block = request.form['block']
        street = request.form['street']
        room_type = request.form['type']
        monthly_rent = request.form['monthly_rent']
        db = get_database()
        db.execute('UPDATE or IGNORE rental set town=?, rental_approve_date=?, block=?, street=?, type=?, monthly_rent=? where id=?', [town, rent_date, block, street, room_type, monthly_rent, id])
        db.commit()
        return redirect(url_for('subjectinfo'))      
    return render_template('updaterentalinfo.html', user = user)

# create route and function call for Add supermarket page
@application.route('/addnewrental', methods = ["POST", "GET"])
def addnewrental():
    user = get_active_user()
    if request.method == "POST":
        town = request.form['town']
        rent_date = request.form['rent_approve_date']
        block = request.form['block']
        street = request.form['street']
        room_type = request.form['type']
        monthly_rent = request.form['monthly_rent']
        db = get_database()
        db.execute('INSERT INTO rental (town, rent_approve_date, block, street, type, monthly_rent) values(?,?,?,?,?,?)', [town, rent_date, block, street, room_type, monthly_rent])
        db.commit()
        return redirect(url_for('rentalinfo'))
    return render_template('addrental.html', user = user)

@application.route('/normaluserDashboard')
def normaluserDashboard():
    user = get_active_user()
    db = get_database()
    counttown_cur = db.execute('select count(town) from population')
    count_town_info = counttown_cur.fetchall()
    countT = count_town_info[0]
    countschool_cur = db.execute('select count(name) from school')
    count_school_info = countschool_cur.fetchall()
    countS = count_school_info[0]
    countsupermarket_cur = db.execute('select count(name) from supermarkets')
    count_super_info = countsupermarket_cur.fetchall()
    countSM = count_super_info[0]
    countpharm_cur = db.execute('select count(pharmacy_name) from pharmacy')
    count_super_info = countpharm_cur.fetchall()
    countPH = count_super_info[0]
    countrental_cur = db.execute('select count(id) from rental')
    count_rental_info = countrental_cur.fetchall()
    countRT = count_rental_info[0]
    countresale_cur = db.execute('select count(id) from resaleflat')
    count_resale_info = countresale_cur.fetchall()
    countRF = count_resale_info[0]
    countCCA_cur = db.execute('select count(Distinct(cca_name)) from cca')
    count_cca_info = countCCA_cur.fetchall()
    countCCA = count_cca_info[0]
    countSubject_cur = db.execute('select count(Distinct(subject)) from subject')
    count_subject_info = countSubject_cur.fetchall()
    countSubject = count_subject_info[0]
    print(count_town_info)
    return render_template('userDashboard.html', countT = countT,  countS = countS, countSM = countSM, countPH = countPH, countRT = countRT, countRF = countRF, countCCA = countCCA, countSubject = countSubject)

# Retrieve  
# create route and function call for Dashboard page
@application.route('/usertown', methods = ["POST", "GET"])
def usertown():
    user = get_active_user()
    db = get_database()
    #retrieve town for user
    home_cur = db.execute('Select * from population order by population desc')
    allpop = home_cur.fetchall()
    return render_template('usertownpopDashboard.html', user = user, allpop = allpop)

# create route and function call for single Employee page
@application.route('/singleuserschool/<string:town>')
def singleuserschool(town):
    user = get_active_user()
    db = get_database()
    param =  '%'+town+'%'
    userschool_cur = db.execute('SELECT * from school join population on school.town = population.town where school.town like ?', [town])
    all_userschool_info = userschool_cur.fetchall()
    countschool_cur = db.execute('select count(name) from school join population on school.town = population.town where school.town like ?', [town])
    count_school_info = countschool_cur.fetchall()
    countS = count_school_info[0]
    print(all_userschool_info)
    return render_template('userschoolDashboard.html', user = user, all_userschool_info = all_userschool_info, countS=countS)

# create route and function call for single Employee page
@application.route('/userschoolinfo/<string:name>')
def userschoolinfo(name):
    user = get_active_user()
    db = get_database()
    param =  '%'+name+'%'
    sch_cur = db.execute('SELECT * from school join cca on school.name = cca.name join subject on school.name = subject.name where school.name like ?', [param])
    # School inner join cca inner join 
    # Subject and CCA
    # single_sch = sch_cur.fetchone()
    all_sch_info = sch_cur.fetchall()
    print(all_sch_info)
    cca_list = []
    subject_list = []
    for item in all_sch_info:
        cca_list.append(item['cca_name'])
        subject_list.append(item['subject'])
    cca_list = list(dict.fromkeys(cca_list))
    subject_list = list(dict.fromkeys(subject_list))
    cca = '' + cca_list[0]
    subject = '' + subject_list[0]
    cca_size = len(cca_list)
    for i in range (1, cca_size):
        cca += ', ' + cca_list[i]
    subject_size = len(subject_list)
    for i in range (1, subject_size):
        subject += ', ' + subject_list[i] 
    return render_template('userschoolinfo.html', user = user, single_sch = all_sch_info[0], cca = cca, subject = subject)

# create route and function call for single Employee page
@application.route('/singleuserpharmsuper/<string:town>')
def singleuserpharmsuper(town):
    user = get_active_user()
    db = get_database()
    param =  '%'+town+'%'
    userpharmsuper_cur = db.execute('select pharmacy_name as name, address from pharmacy where town like ? union all select name, address from supermarkets where town like ?', [town,town])
    all_userpharmsuper_info = userpharmsuper_cur.fetchall()
    countsuper_cur = db.execute('select count(id) from supermarkets where town like ?', [town])
    count_super_info = countsuper_cur.fetchall()
    countSuper = count_super_info[0]
    countpharm_cur = db.execute('select count(id) from pharmacy where town like ?', [town])
    count_pharm_info = countpharm_cur.fetchall()
    countPharm = count_pharm_info[0]
    print(all_userpharmsuper_info)
    return render_template('userpharmsuperDashboard.html', user = user, all_userpharmsuper_info = all_userpharmsuper_info, countSuper = countSuper, countPharm = countPharm)

# create route and function call for single resale flat page
@application.route('/singleuserresale/<string:town>')
def singleuserresale(town):
    user = get_active_user()
    db = get_database()
    param =  '%'+town+'%'
    userresaleflat_cur = db.execute('select * from resaleflat where town like ?', [town])
    all_userresaleflat_info = userresaleflat_cur.fetchall()
    countresaleflat_cur = db.execute('select count(id) from resaleflat where town like ?', [town])
    count_resaleflat_info = countresaleflat_cur.fetchall()
    countResaleFlat = count_resaleflat_info[0]
    return render_template('userresaleflat.html', user = user, all_userresaleflat_info = all_userresaleflat_info, countResaleFlat = countResaleFlat)

# create route and function call for single Employee page
@application.route('/singleuserresaleflat/<int:id>')
def singleuserresaleflat(id):
    user = get_active_user()
    db = get_database()
    resale_cur = db.execute('SELECT * from resaleflat where id = ?', [id])
    all_resale_info = resale_cur.fetchall()
    return render_template('usersingleresaleflat.html', user = user, all_resale_info = all_resale_info[0])

# create route and function call for single resale flat page
@application.route('/singleuserRental/<string:town>')
def singleuserRental(town):
    user = get_active_user()
    db = get_database()
    param =  '%'+town+'%'
    userrental_cur = db.execute('select * from rental where town like ? order by monthly_rent asc', [town])
    all_userental_info = userrental_cur.fetchall()
    countrental_cur = db.execute('select count(id) from rental where town like ?', [town])
    count_rental_info = countrental_cur.fetchall()
    countRental = count_rental_info[0]
    return render_template('userrentalDashboard.html', user = user, all_userental_info = all_userental_info, countRental = countRental)

# create route and function call for single resale flat page
@application.route('/userallRental')
def userallRental():
    user = get_active_user()
    db = get_database()
    userrental_cur = db.execute('select * from rental order by monthly_rent desc')
    all_userental_info = userrental_cur.fetchall()
    countrental_cur = db.execute('select count(id) from rental')
    count_rental_info = countrental_cur.fetchall()
    countRental = count_rental_info[0]
    return render_template('userallrentalDashboard.html', user = user, all_userental_info = all_userental_info, countRental = countRental)

# create route and function call for single Employee page
@application.route('/singlealluserschool')
def singlealluserschool():
    user = get_active_user()
    db = get_database()
    userschool_cur = db.execute('SELECT * from school')
    all_userschool_info = userschool_cur.fetchall()
    countschool_cur = db.execute('select count(name) from school ')
    count_school_info = countschool_cur.fetchall()
    countS = count_school_info[0]
    print(all_userschool_info)
    return render_template('userallschoolsDashboard.html', user = user, all_userschool_info = all_userschool_info, countS=countS)

# create route and function call for single resale flat page
@application.route('/singlealluserresale')
def singlealluserresale():
    user = get_active_user()
    db = get_database()
    userresaleflat_cur = db.execute('select * from resaleflat')
    all_userresaleflat_info = userresaleflat_cur.fetchall()
    countresaleflat_cur = db.execute('select count(id) from resaleflat')
    count_resaleflat_info = countresaleflat_cur.fetchall()
    countResaleFlat = count_resaleflat_info[0]
    return render_template('userallresaleflatDashboard.html', user = user, all_userresaleflat_info = all_userresaleflat_info, countResaleFlat = countResaleFlat)

# create route and function call for single Employee page
@application.route('/singlealluserpharmsuper')
def singlealluserpharmsuper():
    user = get_active_user()
    db = get_database()
    userpharmsuper_cur = db.execute('select * from supermarkets')
    all_userpharmsuper_info = userpharmsuper_cur.fetchall()
    countsuper_cur = db.execute('select count(id) from supermarkets')
    count_super_info = countsuper_cur.fetchall()
    countSuper = count_super_info[0]
    print(all_userpharmsuper_info)
    return render_template('userallsupermarkets.html', user = user, all_userpharmsuper_info = all_userpharmsuper_info, countSuper = countSuper)

# create route and function call for single Employee page
@application.route('/singlealluserpharmsupermarket')
def singlealluserpharmsupermarket():
    user = get_active_user()
    db = get_database()
    userpharmsuper_cur = db.execute('select * from pharmacy')
    all_userpharmsuper_info = userpharmsuper_cur.fetchall()
    countsuper_cur = db.execute('select count(id) from pharmacy')
    count_super_info = countsuper_cur.fetchall()
    countSuper = count_super_info[0]
    print(all_userpharmsuper_info)
    return render_template('userallpharmacy.html', user = user, all_userpharmsuper_info = all_userpharmsuper_info, countSuper = countSuper)


@application.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('home.html')

if __name__ == '__main__':
    application.run(debug = True)


