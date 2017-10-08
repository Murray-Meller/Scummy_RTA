from bottle import route, get, run, post, request, redirect, static_file, response
from Crypto.Hash import MD5
import re
import numpy as np
import string

import requests

#Staff: Alan
#Admin: John

host_addr = "localhost"
frontend_port = 8080
waf_port = 8081


#TODO: temporary until cookies are used
global current_user
global current_user_type
current_user = ""
current_user_type = ""
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
    udb = open(user_database, 'r')
    for line in udb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        users.append(line)
    udb.close()
    return users

# Only use in when to save the whole 'Users' array to the csv file
# DONE: Muzz and Euan
def save_users():
    udb = open(user_database, 'w')
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
    vdb = open(vehicle_database, 'r')
    for line in vdb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        vehicles.append(line)
    vdb.close()

    return vehicles

# saves the global array vehicles to the file
# should be called whenever you change a value in the array. (lame i know, but it works)
# Muzz
def save_vehicles():
    vdb = open(vehicle_database, 'w')
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
    dvdb = open(destroyed_vehicle_database, 'r')
    for line in dvdb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        destroyed_vehicles.append(line)
    dvdb.close()
    return destroyed_vehicles

# saves the global array destroyed_vehicles to the file
# should be called whenever you change a value in the array. (lame i know, but it works)
# Muzz
def save_destroyed_vehicles():
    dvdb = open(destroyed_vehicle_database, 'w')
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

# Muzz
def load_database():
    load_users()
    load_vehicles()
    load_destroyed_vehicles()

# Muzz
def save_database():
    save_users()
    save_vehicles()
    save_destroyed_vehicles()

# Muz -- TODO: will use to allow for an admin reset
def admin_reset():
    dvdb = open(user_database, 'w')
    dvdb.write("ID,NAME,HASHED PASSWORD,LEVEL,LICENSE,LICENSE_EXPIRY\n")
    dvdb.close()
    dvdb = open(vehicle_database, 'w')
    dvdb.write("USER_ID,VEHICLE_ID,FINES,DEMERITS\n")
    dvdb.close()
    dvdb = open(destroyed_vehicle_database, 'w')
    dvdb.write("VEHICLE_ID")
    dvdb.close()

def get_users_string():
    content = ""
    for user in users:
        for field in user:
            content += "| " + str(field) + " " * (25 - len(str(field))) + " "
        content += "|\n"
    return content

def get_vehicles_string():
    vehicle = ""
    for car in vehicles:
        for field in car:
            vehicle += "| " + str(field) + " " * (20 - len(str(field))) + " "
        vehicle += "|\n"
    return vehicle

def get_destroyed_vehicle_string():
    destroyed = ""
    for car in destroyed_vehicles:
        for field in car:
            destroyed += "| " + str(field) + " " * (10 - len(str(field))) + " "
        destroyed += "|\n"
    return destroyed


# Check the login credentials
def check_login(username, password):
    login = False
    password = hash_function(password)

    if (username == "" or password == ""):
        return "Incorrect, you think you could get in that easy", False
    for user in users:
        if user[1] == username:
            if password == user[2]:
                return "Success", True
    return "Unsuccessful, try again Alan", False

# Checks if the cookie matches their user type - TODO: found a bug
def check_user_type(username, said_type):
    for user in users:
        if user[1] == username:
            if user[3] == said_type:
                print("Found user match. Has type: " + user[3])
                return True
    return False

#--------------------------------------HASHING---------------------------------------
# Adam?
def hash_function(password):
    encodedPassword = password.encode()  # encodes the char to allow for hashing
    hash = MD5.new(encodedPassword)  # creates new MD5 hash reference
    hashedHex = hash.hexdigest()  # digests the MD5 reference into a hash.
    return hashedHex

#--------------------------------WEBSERVER OBJECT---------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
# Alan - INFO2315
class FrameEngine:
    def __init__(this, template_path="templates/", template_extension=".html", **kwargs):
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
        current_user = ""

        if request.cookies.get('current_user', '0') != '0':
            current_user = request.cookies.get('current_user', '0')

        rendered_template = this.render(this.load_template(header), NAME=current_user) + rendered_template
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
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render('pre_register')

# Display the users register page
@get('/user_register')
def register():
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render("user_register")

# Display the employees register page
@get('/employee_register')
def register():
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render("employee_register")

# FUNCTIONALITY - Muzz and Euan and Adam
# Returns the hash meant for a given user
def hash_cookie(username, user_type):
    concate = user_type + username[:3]
    hash = MD5.new(concate.encode()).hexdigest()
    return hash

def get_employee_type(key):
    key = hash_function(key)
    employee_type = ""
    if key == "ec8b63c05f999a15a8c8567002a560a8":
        return "Staff"
    elif key == "61409aa1fd47d4a5332de23cbf59a36f":
        return "Admin"
    else:
        return None

def register_a_person(username, password, person_type):
    #Check special cases
    if (username=="" or " " in username or password ==""):
        return False

    #Check username avaiability
    for u in users:
        if (str(u[1]) == username):
            return False

    password = hash_function(password)
    users.append([len(users),username,password,person_type,"",""]) #TODO: fix ID: should use a global static variable
    save_users()

    return True

@post('/user_register')
def user_register():
    username = request.forms.get('username')
    password = request.forms.get('password')

    # check for no attacks in the strings
    reply = ""
    reply += waf.check_email(username)
    reply += waf.check_password(password)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    if (register_a_person(username, password, "User")):
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', "User")
        redirect("/user_profile")
    return fEngine.load_and_render("invalid", reason="This username cannot be used")

#attempt register employee
@post('/employee_register')
def employee_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    key = request.forms.get('key')

    #check for any attacks in the strings
    reply = ""
    reply += waf.check_email(username)
    reply += waf.check_password(password)
    reply += waf.check_attack(key)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    employee_type = get_employee_type(key)

    # register them anbd if it is succesful
    if (employee_type != None and register_a_person(username, password, employee_type)):
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', employee_type)
        redirect("/user_profile")
    return fEngine.load_and_render("employee_register", reason="Your username and password did not follow our guidlines. Please try again.")

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
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render("pre_login")

# Display the users login page
@get('/user_login')
def login():
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render("user_login")

# Display the employees login page
@get('/employee_login')
def login():
    # check if already logged in
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')
    if (current_user != "0" and current_user_type != "0"):
        redirect("/user_profile")

    return fEngine.load_and_render("employee_login")

#FUNCTIONALITY
# Attempt the employee login
@post('/employee_login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    key = request.forms.get('authentication')

    # check for any attacks in the string
    reply = ""
    reply += waf.check_email(username)
    reply += waf.check_password(password)
    reply += waf.check_attack(key)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    employee_type = get_employee_type(key)

    err_str, validLogin = check_login(username, password)
    if check_user_type(username, employee_type) and validLogin:
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', employee_type)
        redirect("/user_profile")
    return fEngine.load_and_render("employee_login", reason=err_str)

# Attempt the user login
@post('/user_login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    #check for any attacks in the username or passwords
    reply = ""
    reply += waf.check_email(username)
    reply += waf.check_password(password)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    # check the login is valid
    err_str, valid_login = check_login(username, password)

    if valid_login and check_user_type(username, "User"):
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', "User")
        redirect("/user_profile")
    else:
        return fEngine.load_and_render("user_login", reason=err_str)

@get('/user_profile')
def do_login():
    current_user = request.cookies.get('current_user', '0')
    current_user_type = request.cookies.get('current_user_type', '0')

    #TODO: check if cookies are empty in which case load the index
    if (current_user == "0" or current_user_type == "0"):
        return fEngine.load_and_render("index")

    #check for any attacks in the cookies
    reply = ""
    reply += waf.check_email(current_user)
    reply += waf.check_attack(current_user_type)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    #check the user and their type match
    print("Read in values: " + current_user + " " + current_user_type)
    if (not check_user_type(current_user, current_user_type)):
        return fEngine.load_and_render("invalid", reason="There is an issue with you and your cookies")

    if current_user_type == "Staff" or current_user_type == "Admin":
        return fEngine.load_and_render("RTAlogin", content=get_users_string(), vehicle=get_vehicles_string(), destroyed=get_destroyed_vehicle_string())
    elif current_user_type == "User":
        return fEngine.load_and_render("user_profile")
    else:
        return fEngine.load_and_render("index")

# Attempt the employee login
@get('/logout')
def logout():
    response.delete_cookie('current_user')
    response.delete_cookie('current_user_type')
    redirect("/")

@get('/about')
def about():
    return fEngine.load_and_render("about", garble="To be a very meme centered RTA")

@get('/invalid')
def invalid():
    return "Sorry, there was an error proceesing your request. It seems there was a potential threat to our site. Please try again"

#-------------------------------------------------------------------------------

class WAFCaller(object):
    def __init__(self, waf_address, waf_port):
        self.waf_port = waf_port
        self.waf_address = waf_address
        self.waf_string = "http://{address}:{port}".format(address=waf_address, port=waf_port)

    # --------------------------------------------------------------------------

    # Ideally every string sent to the server should first pass through the WAF
    # this is for general use: The attack vector is just the string that we want to parse.
    def check_attack(self, attack_vector):
        # Check for malicious code by sending vector to the waf server
        response = requests.post("{target}/waf/detect/{attack_vector}".format(target=self.waf_string, attack_vector=attack_vector))
        # Rather than redirecting, you can attempt to sanitise the string
        if response.text != "True":
            # TODO: IF TIME: Handle bad case here. Maybe strip the string of anything dodgy then return it
            # instead of just sending them to an invalid page
            redirect("/invalid")
        return ""

    # ----------------------------------------------------------------------

    def response_handler(self, response):
        if response != "True":
            return response
        return ""

    # ----------------------------------------------------------------------

    def check_email(self, email):
        # Check string for any attack
        self.check_attack(email)

        # Call the waf and check whether it is a valid email
        response = requests.post("{target}/waf/email/{email}".format(target=self.waf_string, email=email))
        return self.response_handler(response.text)

    def check_password(self, password):
        # Check string for any attack
        self.check_attack(password)

        # Check parsing format of the password
        response = requests.post("{target}/waf/password/{password}".format(target=self.waf_string, password=password))

        return self.response_handler(response.text)

waf = WAFCaller(host_addr, waf_port)

print("staff: " + hash_function("Alan"))
print("admin: " + hash_function("John"))

fEngine = FrameEngine()
run(host=host_addr, port=frontend_port, debug=True)
