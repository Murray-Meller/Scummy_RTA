from bottle import run, get, post, request, redirect
import requests

host_addr = "localhost"
frontend_port = 8080
waf_port = 8081

users = {}


# ----------------------------------------------------------------------

class WAFCaller(object):
    def __init__(self, waf_address, waf_port):
        self.waf_port = waf_port
        self.waf_address = waf_address
        self.waf_string = "http://{address}:{port}".format(address=waf_address, port=waf_port)

    # ----------------------------------------------------------------------

    # Ideally every string sent to the server should first pass through the WAF
    # this is for general use: The attack vector is just the string that we want to parse.
    def check_attack(self, attack_vector):
        # Check for malicious code by sending vector to the waf server
        response = requests.post("{target}/waf/detect/{attack_vector}".format(target=self.waf_string, attack_vector=attack_vector))

        # Rather than redirecting, you can attempt to sanitise the string
        if response.text != "True":
            # TODO: IF TIME: Handle bad case here. Maybe strip the string of anything dodgy then return it
            # instead of just sending them to an invalid page
            redirect('/invalid')


    # ----------------------------------------------------------------------

    def response_handler(self, response):
        if response != "True":
            return response
        return None

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

#-----------------------------------------------------------------

# THE FOLLOWING CODE IS JUST A MOCK WEBSITE HE MADE.
# ALL WE WILL DO IS EVENTUALLY MOVE THE ABOVE CLASS INTO OUR MAIN FILE

# Potential attack string detected
@get('/invalid')
def defuse():
    return '''
        You attempted to pass an invalid input that contained a potential threat to this site.
        Please refrain from using any special characters.
    '''

#-----------------------------------------------------------------

@get('/')
def useradd():
    return '''
    	Login with a username and password
        <form action="/" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/')
def useradd():
    username = request.forms.get("username")
    password = request.forms.get("password")

    # Call the WAF
    username_check = waf.check_email(username)
    password_check = waf.check_password(password)

    if username_check is not None:
        return username_check

    if password_check is not None:
        return password_check

    return "User {username} registered!".format(username=username)

#-----------------------------------------------------------------

waf = WAFCaller(host_addr, waf_port)

run(host=host_addr, port=frontend_port)
