from bottle import run, request, post, get
import re
import string

# Important globals
host = "localhost"
port = "8081"

# Debug mode to check whether or not attacks are working
# Start with it as "True", try the attack, flip it to false, try the attack again and see if your WAF blocked it
# Debug should be set to false when launching the final version
debug = False

@post('/waf/detect/<string_in:path>')
def detect_attack(string_in):
    if not debug:
        arrayOfChars = ['"',"'",">","<","!","/","(",")","=","{","}",":","-","&"]
        for char in arrayOfChars:
            if char in string_in:
                #string_in = string_in.replace(char, "") #remove character from string and replace it with ""
                return "False"
        return "True"
    return "False"

@post('/waf/email/<email:path>')
def verify_email(email):
    if '@' in email:
        return 'True'
    else:
        return "Not an email address"

@post('/waf/password/<password:path>')
def verify_password(password):
    print(len(password))
    if len(password) < 8:
        return "Password is too short"

    if not any(c in string.ascii_lowercase for c in password):
        return "Password must contain at least one lowercase character"

    if not any(c in string.ascii_uppercase for c in password):
        return "Password must contain at least one uppercase character"

    if not any(c in string.digits for c in password):
        return "Password must contain at least one digit"

    return 'True'

# Rather than using paths, you could throw all the requests with form data filled using the
# requests module and extract it here. Alternatively you could use JSON objects.

# Custom definition waf
@post('/waf/custom/field=<field:path>%20test=<test:path>')
def custom_waf(field, test):
    if re.search(test, field) is not None:
        return "True"
    return "False"

# Debug toggle
# TODO: remove this for final version as ALAN could call it to put it into debug mode
@post('/waf/debug')
def enable_debugger():
    global debug
    if debug:
        debug = False
    else:
        debug = True

# Run the server
run(host=host, port=port)
