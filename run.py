from bottle import route, get, run, post, request, redirect, static_file, response
from Crypto.Hash import MD5
import re
import numpy as np
import string
#----------------------------DATABASE-STUFF-------------------------------------
users = [] #array of users
vehicles = [] #array of vehicles
destroyed_vehicles = [] #array of destoryed_vehicles

user_database = './database/users.txt'
vehicle_database = './database/vehicles.txt'
destroyed_vehicle_database = './database/destroyed_vehicles.txt'

user_database_num_fields = 6
vehicle_database_num_fields = 4
destroyed_vehicle_database_num_fields = 1

# Updates the 'Users' array to store all the contents of the file
# DONE: Muzz and Euan
def load_users():
    udb = open(user_database, 'r+')
    for line in udb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        users.append(line)
    udb.close()
    users.pop(0)
    return users

# Only use in when to save the whole 'Users' array to the csv file
# DONE: Muzz and Euan
def save_users():
    udb = open(user_database, 'a+')
    for user in users:
        count = 0
        for field in user:
            udb.write(str(field))
            count += 1
            if count != user_database_num_fields:
                udb.write(',')
        for i in range(user_database_num_fields - (count + 1)):
            udb.write(',')
        udb.write('\n')
    udb.close()

# loads in the vehicles file into a global array called vehicles,
# see vehciles.txt file for column detailsz
# Muzz
def load_vehicles():
    vdb = open(vehicle_database, 'a+')
    for line in vdb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        vehicles.append(line)
    vdb.close()
    if (len(vehicles) > 1):
        vehicles.pop(0)
    return vehicles

# saves the global array vehicles to the file
# should be called whenever you change a value in the array. (lame i know, but it works)
# Muzz
def save_vehicles():
    vdb = open(vehicle_database, 'a+')
    for vehicle in vehicles:
        count = 0
        for field in vehicle:
            vdb.write(str(field))
            count += 1
            if count != vehicle_database_num_fields:
                vdb.write(',')
        for i in range(vehicle_database_num_fields - (count + 1)):
            vdb.write(',')
        vdb.write('\n')
    vdb.close()

# loads in the destroyed_vehicles file into a global array called destroyed_vehicles,
# see destroyed_vehciles.txt file for column details
# Muzz
def load_destroyed_vehicles():
    dvdb = open(destroyed_vehicle_database, 'r+')
    for line in dvdb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        destroyed_vehicles.append(line)
    dvdb.close()
    if (len(vehicles) > 1):
        destroyed_vehicles.pop(0)
    return destroyed_vehicles

# saves the global array destroyed_vehicles to the file
# should be called whenever you change a value in the array. (lame i know, but it works)
# Muzz
def save_destroyed_vehicles():
    dvdb = open(destroyed_vehicle_database, 'a+')
    for vehicle in destroyed_vehicles:
        count = 0
        for field in vehicle:
            dvdb.write(str(field))
            count += 1
            if count != destroyed_vehicle_database_num_fields:
                dvdb.write(',')
        for i in range(destroyed_vehicle_database_num_fields - (count + 1)):
            dvdb.write(',')
        dvdb.write('\n')
    dvdb.close()

def load_database():
    load_users()
    load_vehicles()
    load_destroyed_vehicles()

def save_database():
    save_users()
    save_vehicles()
    save_destroyed_vehicles()

#--------------------------------------HASHING---------------------------------------
def hash_function(password):
    encodedPassword = password.encode()  # encodes the char to allow for hashing
    hash = MD5.new(encodedPassword)  # creates new MD5 hash reference
    hashedHex = hash.hexdigest()  # digests the MD5 reference into a hash.
    return hashedHex

#--------------------------------WEBSERVER OBJECT---------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
class FrameEngine:
    def __init__(this,
        template_path="templates/",
        template_extension=".html",
        **kwargs):
        this.template_path = template_path
        this.template_extension = template_extension
        this.global_renders = kwargs
        load_database()

    def load_template(this, filename):
        path = this.template_path + filename + this.template_extension
        file = open(path, 'r')
        text = ""
        for line in file:
            text+= line
        file.close()
        return text

    def simple_render(this, template, **kwargs):
        template = template.format(**kwargs)
        return  template

    def render(this, template, **kwargs):
        keys = this.global_renders.copy() #Not the best way to do this, but backwards compatible from PEP448, in Python 3.5+ use keys = {**this.global_renters, **kwargs}
        keys.update(kwargs)
        template = this.simple_render(template, **keys)
        return template

    def load_and_render(this, filename, header="header", tailer="tailer", **kwargs):
        template = this.load_template(filename)
        rendered_template = this.render(template, **kwargs)
        rendered_template = this.load_template(header) + rendered_template
        rendered_template = rendered_template + this.load_template(tailer)
        return rendered_template

# Allow image loading
@route('/img/<picture>')
def serve_pictures(picture):
    return static_file(picture, root='img/')

# Allow CSS
@route('/css/<css>')
def serve_css(css):
    return static_file(css, root='css/')

# Allow javascript
@route('/js/<js>')
def serve_js(js):
    return static_file(js, root='js/')

#--------------------------- USER REGISTER VEHICLE------------------------------
#user login register a vehicle page
@get('/register_vehicle')
def vehicle_register():
    return fEngine.load_and_render('register_vehicle')


#define values for the vehcile registration
def check_register_vehicle(vehicle):
    return fEngine.load_and_render('/user_profile')

@post('/register_vehicle')
def do_vehicle_registration():
    vehicle_registration_number = str(request.forms.get('number'))
    vehicles.append(vehicle_registration_number);
    save_vehicles()
    return check_register_vehicle(vehicle_registration_number)

#----------------------------------Manage vehicle-------------------------------
#Manage vehicle page
@get('/manage_vehicle')
def manage_vehicle():
    return fEngine.load_and_render('manage_vehicle')

@post('/manage_vehicle')
def compute_vehicle():
    #compute vehicle number
    vehicle_number = request.forms.get('number')
    #compute pay fine amount if paying fines is submitted
    if vehicle_number == None:
        return deduct_fines()
    return check_register_vehicle(vehicle_number)

#deduct fines
def deduct_fines():
    #TODO must update the total amount of fines to be payed to zero
    return fEngine.load_and_render('/user_profile')


#----------------apply for license and user merit points-----------------------
@get('/apply_license')
def manage_license():
    return fEngine.load_and_render('apply_license')

@post('/apply_license')
def compute_license():

    #compute whether they want to apply or renew
    #if applying will return Applying if renewing will return Renewing.
    application = request.forms.get('param', '')
    aplitcation = str(application)
    file = open(database, 'r')
    #TODO this is a basic check for if user is already applied etc...what needs to be done is correctly correlate this to the right user.
    if (application == "Applying" and ("Unlicensed" not in file)):
        file.close()
        return fEngine.load_and_render("invalid", reason="You already have a license or are applying for one.")
    elif (application == "Renewing" and ("Licensed" not in file)):
        file.close()
        return fEngine.load_and_render('invalid', reason="You are unlicensed or are applying for a license")
    elif (application == "Applying"):
        #TODO add to database
        return fEngine.load_and_render('user_profile')
    elif (application == "Renewing"):
        return fEngine.load_and_render('user_profile')
    #TODO sends this data to the database, if licensed is renewed will not update or if already has license cannot apply.
    return fEngine.load_and_render('user_profile')

#---------------------------register-------------------------------------
#WEBPAGES
#loads up register page
@get('/register')
def register():
    return fEngine.load_and_render('pre_register')

# Display the users register page
@get('/user_register')
def register():
    return fEngine.load_and_render("user_register")

# Display the employees register page
@get('/employee_register')
def register():
    return fEngine.load_and_render("employee_register")

# FUNCTIONALITY - Muzz and Euan and Adam
#attempt register
def register_a_person(username, password, person_type):
    if (check_vaild_username_password(username, password)):
        password = hash_function(password)
        users.append([len(users),username,password,person_type,"",""]) #TODO: fix ID: should use a global static variable
        save_users()
        return True
    return False

@post('/user_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (register_a_person(username, password, "User")):
        return fEngine.load_and_render("user_profile", username=username)
    return fEngine.load_and_render("invalid", reason="Your username and password did not follow our guidlines. Please try again.")


#attempt register employee
@post('/employee_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (register_a_person(username, password, "Employee")): #TODO: determin whether staff or not
        with open('./database/users.txt', "r") as f, open('./database/vehicles.txt', "r") as v, open('./database/destroyed_vehicles.txt',"r") as d:
            content = f.read()
            vechicle = v.read()
            destroyed = d.read()
            return fEngine.load_and_render("RTAlogin", username=username, content=content, vehicle=vehicle, destroyed=destroyed)

    return fEngine.load_and_render("invalid", reason="Your username and password did not follow our guidlines. Please try again.")

#-----------------
#Check the registering process
#Username and password validity
def check_vaild_username_password(username, password):
    username = str(username)
    password = str(password)
    if (username== "" or password ==""):
        return False
    #Check username avaiability
    for u in users:
        if (u[1] == username):
            return fEngine.load_and_render("invalid", reason="Please try another username.")

    #check password
    if (len(password) > 8 and username != password):
        #create bools corresponding to password requirements
        specialchar = False
        capitals = False
        numbers = False

        #create sets of strings that are used to check for password validity
        chars = set(string.ascii_uppercase)
        number = set(string.hexdigits)
        punc = set(string.punctuation)

        #check password validity
        if any((c in chars) for c in password):
            capitals = True
        if any((c in punc) for c in password):
            specialchar = True
        if any((c in number)for c in password):
            numbers = True
        if (numbers == True and specialchar == True and capitals == True):
            return True
        return False

#registeration checker for the employee
#TODO: Need to add special key for staff and employees
def check_do_register_employee(username, password, key):
    if (check_vaild_username_password(username, password)):
        users.append(username)
        password = hash_function(password)
        keycheck = False
        keychecka = False
        key = hash_function(key)
        #key for staff
        if key == "959594a5d046a97372e94ccdcd3b3d1f":
            keycheck = True
        #key for admin
        if key == "959594aewrgethr5yj6uye5hwt4gr3qfwetrhy5j76356h42565768575d046a97372e94ccdcd3b3d1f":
            keychecka = True

        #admin login
        if keychecka:
            with open('./database/users.txt', "r") as f, open('./database/vehicles.txt', "r") as v, open(
                    './database/destroyed_vehicles.txt', "r") as d:
                content = f.read()
                vechicle = v.read()
                destroyed = d.read()
                return fEngine.load_and_render("RTAlogin", username=username, content=content, vehicle=vehicle,destroyed=destroyed)
        #staff login
        if keycheck:
            with open('./database/users.txt', "r") as f, open('./database/vehicles.txt', "r") as v, open(
                    './database/destroyed_vehicles.txt', "r") as d:
                content = f.read()
                vechicle = v.read()
                destroyed = d.read()
                return fEngine.load_and_render("RTAlogin", username=username, content=content, vehicle=vehicle,destroyed=destroyed)
        #else:
    return fEngine.load_and_render("invalid", reason="Invalid password or username")

def register_a_person(username, password, person_type):
    if (check_vaild_username_password(username, password)):
        password = hash_function(password)
        users.append([len(users),username,password,person_type,"",""]) #TODO: fix ID: should use a global static variable
        save_users()
        return True
    return False

# DONE MUZZ AND EUAN
@post('/user_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if (register_a_person(username, password, "User")):
        return fEngine.load_and_render("user_profile", username=username)
    return fEngine.load_and_render("invalid", reason="Your username and password did not follow our guidlines. Please try again.")

# TODO: EUAN
#attempt register employee
@post('/employee_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    key = request.forms.get('key')
    if (register_a_person(username, password, "Employee")): #TODO: determin whether staff or not
        key = hash_function(key)
        with open('./database/users.txt', "r") as f, open('./database/vehicles.txt', "r") as v, open('./database/destroyed_vehicles.txt',"r") as d:
            content = f.read()
            vehicle = v.read()
            destroyed = d.read()
            return fEngine.load_and_render("RTAlogin", username=username, content=content, vehicle=vehicle, destroyed=destroyed)
    return fEngine.load_and_render("invalid", reason="Your username and password did not follow our guidlines. Please try again.")

#-----------------------------LOGIN------------------------------------------------
#WEBPAGES
# Redirect to login
@route('/')
@route('/home')
def index():
    return fEngine.load_and_render("index")

# Display the login page
@get('/login')
def login():
    return fEngine.load_and_render("pre_login")

# Display the users login page
@get('/user_login')
def login():
    return fEngine.load_and_render("user_login")

# Display the employees login page
@get('/employee_login')
def login():
    return fEngine.load_and_render("employee_login")

#FUNCTIONALITY
# Check the login credentials
def check_login(username, password):
    login = False
    password = hash_function(password)
    if (username== "" or password == ""):
        return "Incorrect, you think you could get in that easy",False
    for user in users:
        if user[1] == username:
            if password == user[2]:
                return "Success", True
    return "Unsuccessful, try again Alan", False

# Attempt the user login
@post('/user_login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    err_str, login = check_login(username, password)
    if login:
        return fEngine.load_and_render("user_profile")
    else:
        return fEngine.load_and_render("user_login", reason=err_str)


# Attempt the employee login
@post('/employee_login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    authenication = request.forms.get('authenication')

    #TODO: make an employee check login and use it here
    #TODO: it will probably need to load different pages based what kinda of staff member they are
    err_str, login = check_login(username, password)
    if login:
        #return fEngine.load_and_render("user_profile", flag=err_str)
        #TODO: NEED TO MAKE THIS Work for vaild and fail - also, need to make sure it works between the user and emplyoee pages
        with open('./database/users.txt', "r") as f, open('./database/vehicles.txt', "r") as v, open('./database/destroyed_vehicles.txt',"r") as d:
            content = f.read()
            vechicle = v.read()
            destroyed = d.read()
            return fEngine.load_and_render("RTAlogin", username=username, content=content, vehicle=vehicle, destroyed=destroyed)
    else:
        # return fEngine.load_and_render("user_profile", reason=err_str)
        return fEngine.load_and_render("employee_login", reason=err_str)

@get('/about')
def about():
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return fEngine.load_and_render("about", garble=np.random.choice(garble))

#-----------------------------------------------------------------------------

fEngine = FrameEngine()
run(host='localhost', port=8080, debug=True)
