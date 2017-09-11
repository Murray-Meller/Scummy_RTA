from bottle import route, get, run, post, request, redirect, static_file, response
from Crypto.Hash import MD5
import re
import numpy as np
import string
#-----------------------------------------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# If you are unsure how this is working, just
Users = [] #array of users
database = 'test.txt'
class FrameEngine:
    def __init__(this,
        template_path="templates/",
        template_extension=".html",
        **kwargs):
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
        rendered_template = this.load_template(header) + rendered_template
        rendered_template = rendered_template + this.load_template(tailer)
        return rendered_template

    # Updates the 'Users' array to store all the contents of the file
    def load_users():
        file = open(database, 'r')
        global Users
        Users = []
        for line in file:
            line = line.split(',')
            line[-1] = line[-1][:-1]
            Users.append(line)
        return Users

    # Only use in when to save the whole 'Users' array to the csv file
    def save_users():
        global Users
        file = open(database, 'w')
        file.truncate()

        for user in Users:
            for word in user:
                if word != user[-1]:
                    word += ','
                file.write(word)
            file.write('\n')

        file.close()

    def login_user(username, password):
        global Users
        for user in Users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def login_employee(username, password, key):
        global Users
        for user in Users:
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
        
#-----------------------------------------------------------------------------

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


#----------------------------------------------------------------
#RESGISter
#loads up register page
@get('/register')
def register():
    return fEngine.load_and_render('pre_register')

# Display the users register
@get('/user_register')
def register():
    return fEngine.load_and_render("user_register")

# Display the employees register page
@get('/employee_register')
def register():
    return fEngine.load_and_render("employee_register")

#attempt register
@post('/user_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    return check_do_register(username, password)

#attempt register employee
@post('/employee_register')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    key = request.forms.get('key')
    return check_do_register_employee(username, password, key)

#-----------------
#Check the registering process
#Username and password validity
def check_do_register(username, password):
    password = str(password)
    username = str(username)
    if (len(password) > 8 and username != password and username not in Users):

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

            #append username to end of list of usernames
            Users.append(username)
            return fEngine.load_and_render("RTAlogin", username=username)

    return fEngine.load_and_render("invalid", reason="Invalid password or username")

#registeration checker for the employee
def check_do_register_employee(username, password, key):
    password = str(password)
    username = str(username)
    #----------
    #TODO need to make sure that the key is processed
    if (len(password) > 8 and username != password and username not in Users):

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
            Users.append(username)
            return fEngine.load_and_render("RTAlogin", username=username)

    return fEngine.load_and_render("invalid", reason="Invalid password or username")


#-----------------------------------------------------------------------------

# Check the login credentials
def check_login(username, password):
    login = False ## TODO: NEED TO CHANGE THIS!!!!!!!!!!!!!!!!!!!!!!! JUST USING IT FOR TESTING
    if username != "admin": # Wrong Username
        err_str = "Incorrect Username"
        return err_str, login

    if password != "password":
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
