from bottle import run, request, post, get

# Important globals
host = "localhost"
port = "8081"


# Our "Database"
users = {}

# API calls
@post('/api/useradd/<username:path>/<password:path>')
def useradd(username, password):
	global users
	if username in users:
		return "User already exists"
	users[username] = password
	return "User added"

@post('/api/userget/<username:path>')
def userget(username):
	if username in users:
		return users[username]
	else:
		return "User does not exist!"

@post('/api/userget/all')
def usergetall():
	r_string = ''
	for user in users:
		r_string += ', {username}'.format(username=user)
	return r_string


# Rather than using paths, you could throw all the requests with form data filled using the
# requests module and extract it here.

# Run the server
run(host=host, port=port)