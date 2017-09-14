from bottle import route, get, run, post, request, redirect, static_file, response
from Crypto.Hash import MD5
import re
import numpy as np
import string
#----------------------------DATABASE-STUFF-------------------------------------
users = [] #array of users
user_database = './database/users.txt'
user_database_num_fields = 6

# Updates the 'Users' array to store all the contents of the file
# DONE: MUZZ AND EUAN claim the victory (w dylans start work)
def load_users():
    udb = open(user_database, 'r+')
    for line in udb:
        line = line.split(',')
        line[-1] = line[-1][:-1]
        users.append(line)
    udb.close()
    print(users)
    return users

# Only use in when to save the whole 'Users' array to the csv file
# DONE: MUZZ AND EUAN claim the victory (w dylans start work)
def save_users():
    udb = open(user_database, 'w')
    for user in users:
        count = 0
        print("LENGTH OF USER:" + str(len(user)))
        for field in user:
            print(field)
            udb.write(str(field))
            count += 1
            if count != user_database_num_fields:
                udb.write(',')
        for i in range(user_database_num_fields - (count + 1)):
            udb.write(',')
        udb.write('\n')
    udb.close()

def login_user(username, password):
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

def login_employee(username, password, key):
    global users
    for user in users:
        if user[0] == username and user[1] == password:
            if user[2] == key:
                return True
    return False

def register_user(username, password):

    file = open(database, 'a')
    username += ','
    file.write(username)
    file.write(password)
    file.write('\n')
    read_doc()

def register_employee(username, password, key):
    file = open(database, 'a')
    username += ','
    file.write(username)
    password += ','
    file.write(password)
    file.write(key)
    file.write('\n')
    read_doc()

#--------------------------------------HASHING---------------------------------------
def hash_function(password):
    encodedPassword = password.encode()  # encodes the char to allow for hashing
    hash = MD5.new(encodedPassword)  # creates new MD5 hash reference
    hashedHex = hash.hexdigest()  # digests the MD5 reference into a hash.
    return hashedHex


#-----------------------------------------------------------------------------
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
        load_users()
        save_users()

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

#-----------------------------------------------------------------------------
#user login register a vehicle page
@get('/register_vehicle')
def vehicle_register():
    return fEngine.load_and_render('register_vehicle')


#define values for the vehcile registration
def check_register_vehicle(vehicle):
    return fEngine.load_and_render('/user_profile')

@post('/register_vehicle')
def do_vehicle_registration():
    vehicle_registration_number = request.forms.get('number')
    return check_register_vehicle(vehicle_registration_number)

#----------------------------------Manage vehicle--------------------------
#Manage vehicle page
@get('/manage_vehicle')
def manage_vehicle():
    return fEngine.load_and_render('manage_vehicle')

@post('/manage_vehicle')
def compute_vehicle():

#compute vehicle number ----------
    vehicle_number = request.forms.get('number')
#compute pay fine amount if paying fines is submitted ------------------
    if vehicle_number == None:
        return deduct_fines()
    return check_register_vehicle(vehicle_number)

#deduct fines--------
def deduct_fines():
    #TODO must update the total amount of fines to be payed to zero
    return fEngine.load_and_render('/user_profile')


#----------------apply for license and user merit points
@get('/apply_license')
def manage_license():
    return fEngine.load_and_render('apply_license')

@post('/apply_license')
def compute_license():

    #compute whether they want to apply or renew
    #if applying will return Applying if renewing will return Renewing.
    application = request.forms.get('param', '')
    aplitcation = str(application)
    print(application)
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


# FUNCTIONALITY
#attempt register
def register_a_person(username, passowrd, person_type):
    if (check_vaild_username_password(username, password)):
        password = hash_function(password)
        users.append([len(users),username,password,person_type,"",""]) #fix ID: should use a global static variable
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
        return fEngine.load_and_render("user_profile", username=username)
    return fEngine.load_and_render("invalid", reason="Your username and password did not follow our guidlines. Please try again.")

#-----------------
#Check the registering process
#Username and password validity
def check_vaild_username_password(username, password):
    username = str(username)
    password = str(password)

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
def check_do_register_employee(username, password, key):
    password = str(password)
    username = str(username)
    #----------
    #TODO need to make sure that the key is processed
    if (len(password) > 8 and username != password and username not in users):

        # create bools correspondisng to password requirements

        specialchar = False
        capitals = False
        numbers = False

        # create sets of strings that are used to check for password validity

        chars = set(string.ascii_uppercase)
        number = set(string.hexdigits)
        punc = set(string.punctuation)

        # check password validity

        if any((c in chars) for c in password):
            capitals = True
        if any((c in punc) for c in password):
            specialchar = True
        if any((c in number) for c in password):
            numbers = True
        if (numbers == True and specialchar == True and capitals == True):
            # append username to end of list of usernames
            users.append(username)
            password = hash_function(password)
            return fEngine.load_and_render("RTAlogin", username=username)

    return fEngine.load_and_render("invalid", reason="Invalid password or username")


#-----------------------------------------------------------------------------

# Check the login credentials
def check_login(username, password):
    login = False ## TODO: NEED TO CHANGE THIS!!!!!!!!!!!!!!!!!!!!!!! JUST USING IT FOR TESTING
    password = hash_function(password)
    if username != "admin": # Wrong Username
        err_str = "Incorrect Username"
        return err_str, login

    if password != "TODO compare to hash":
        err_str = "Incorrect Password"
        return err_str, login

    login_string = "Logged in!"
    login = True
    return login_string, login

#-----------------------------------------------------------------------------
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

# Attempt the user login
@post('/user_login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    err_str, login = check_login(username, password)
    if login:
        #return fEngine.load_and_render("valid page", flag=err_str)
        #TODO: NEED TO MAKE THIS Work for vaild and fail - also, need to make sure it works between the user and emplyoee pages
        return fEngine.load_and_render("user_profile")
    else:
        # return fEngine.load_and_render("invalid page", reason=err_str)
        return fEngine.load_and_render("user_profile")

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
        return fEngine.load_and_render("")
    else:
        # return fEngine.load_and_render("user_profile", reason=err_str)
        return fEngine.load_and_render("")

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
