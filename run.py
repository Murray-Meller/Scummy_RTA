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
backend_port = 8082

backend_str = "http://{host}:{port}".format(host=host_addr, port=backend_port)

#----------------------------DATABASE-STUFF-------------------------------------

# loads a given database from the backend and returns an array
def load_database(location):
    db = []
    response = requests.post("{target}/api/{location}get/all"
    	.format(target=backend_str, location=location))
    textdb = response.text.splitlines()
    for line in textdb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        db.append(line)
    return db

# Muz -- TODO: will use to allow for an admin reset
def admin_reset():
    requests.post("{target}/api/adminreset"
        .format(target=backend_str))

def get_users_string():
    response = requests.post("{target}/api/userstring"
    	.format(target=backend_str))
    return response.text

def get_vehicles_string():
    response = requests.post("{target}/api/vehiclestring"
    	.format(target=backend_str))
    return response.text

def get_destroyed_vehicle_string():
    response = requests.post("{target}/api/destroyedstring"
    	.format(target=backend_str))
    return response.text


# Check the login credentials
def check_login(username, password):
    login = False
    password = hash_function(password)

    response = requests.post("{target}/api/usercheck/{username}/{password}"
    	.format(target=backend_str, username=username, password=password))
    result = response.text

    if result[-4:] == 'True':
        return "Success", True
    else:
        return result[:-6], False

# Checks if the cookie matches their user type - TODO: found a bug
def check_user_type(username, said_type):
    users = load_database('user')
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

    reply = ""
    reply += waf.check_rego(vehicle_registration_number)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    requests.post("{target}/api/vehicleadd/{vehicle}"
    	.format(target=backend_str, vehicle=vehicle_registration_number))
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
    # application = request.forms.get('param', '')
    # aplitcation = str(application)
    # file = open(database, 'r')
    #
    # #TODO this is a basic check for if user is already applied etc...what needs to be done is correctly correlate this to the right user.
    # if (application == "Applying" and ("Unlicensed" not in file)):
    #     file.close()
    #     return fEngine.load_and_render("invalid", reason="You already have a license or are applying for one.")
    # elif (application == "Renewing" and ("Licensed" not in file)):
    #     file.close()
    #     return fEngine.load_and_render('invalid', reason="You are unlicensed or are applying for a license")
    # elif (application == "Applying"):
    #     #TODO add to database
    #     return fEngine.load_and_render('user_profile')
    # elif (application == "Renewing"):
    #     return fEngine.load_and_render('user_profile')
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

    password = hash_function(password)

    response = requests.post("{target}/api/useradd/{username}/{password}/{persontype}"
    	.format(target=backend_str, username=username, password=password, persontype=person_type))

    if response.text == 'True':
        return True
    return False

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
        session_id = requests.post("{target}/api/session_id/new/{username}"
            .format(target=backend_str, username=username)).text
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', session_id)
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
        session_id = requests.post("{target}/api/session_id/new/{username}"
            .format(target=backend_str, username=username)).text
        response.set_cookie('current_user', username)
        response.set_cookie('current_user_type', session_id)
        redirect("/user_profile")
    else:
        return fEngine.load_and_render("user_login", reason=err_str)

@get('/user_profile')
def do_login():
    current_user = request.cookies.get('current_user', '0')
    session_id = request.cookies.get('current_user_type', '0')

    #TODO: check if cookies are empty in which case load the index
    if (current_user == "0" or session_id == "0"):
        return fEngine.load_and_render("index")

    #check for any attacks in the cookies
    reply = ""
    reply += waf.check_email(current_user)
    reply += waf.check_attack(session_id)
    if (reply != ""):
        return fEngine.load_and_render("invalid", reason=reply)

    #check the user and their type match
    print("Read in values: " + current_user + " " + session_id)
    response = requests.post("{target}/api/session_id/get/{username}/{session_id}"
        .format(target=backend_str, username=current_user, session_id=session_id))
    if (response.text == "Invalid Cookies"):
        return fEngine.load_and_render("invalid", reason="There is an issue with you and your cookies")

    current_user_type = response.text

    if current_user_type == "Staff" or current_user_type == "Admin":
        return fEngine.load_and_render("RTAlogin", content=get_users_string(), vehicle=get_vehicles_string(), destroyed=get_destroyed_vehicle_string())
    elif current_user_type == "User":
        return fEngine.load_and_render("user_profile")
    else:
        return fEngine.load_and_render("index")

# Attempt the employee login
@get('/logout')
def logout():
    username = request.cookies.get('current_user', '0')
    session_id = request.cookies.get('current_user_type', '0')
    requests.post('{target}/api/session_id/logout/{username}/{session_id}'
        .format(target=backend_str, username=username, session_id=session_id))
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

    def check_rego(self, rego):
        # Check string for any attack
        self.check_attack(rego)

        # Check parsing format of the password
        response = requests.post("{target}/waf/rego/{rego}".format(target=self.waf_string, rego=rego))

        return self.response_handler(response.text)


waf = WAFCaller(host_addr, waf_port)

print("staff: " + hash_function("Alan"))
print("admin: " + hash_function("John"))

fEngine = FrameEngine()
run(host=host_addr, port=frontend_port, debug=True)
