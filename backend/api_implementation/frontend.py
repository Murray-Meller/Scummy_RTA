from bottle import run, get, post, request
import requests

host_addr = "localhost"
frontend_port = 8080
backend_port = 8082

backend_str = "http://{host}:{port}".format(host=host_addr, port=backend_port)

@get('/')
def useradd():
    return '''
    	Login with a username and password
        <form action="/" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            Type:     <input name="persontype" type="text" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/')
def useradd():
    username = request.forms.get("username")
    password = request.forms.get("password")
    persontype = request.forms.get("persontype")

    # Call the back-end
    response = requests.post("{target}/api/useradd/{username}/{password}/{persontype}"
    	.format(target=backend_str, username=username, password=password, persontype=persontype))

    # Tell the user what the back-end thinks
    # Alternatively, reformat what the back-end thinks into a nicer page
    return response.text

@get('/test1')
def test1get():
    response = requests.post("{target}/api/userget/all"
    	.format(target=backend_str))
    print(response.text)
    return response.text

@get('/test2')
def test2get():
    response = requests.post("{target}/api/userget/d@d"
    	.format(target=backend_str))
    return response.text

@get('/test3')
def test3get():
    response = requests.post("{target}/api/userstring"
    	.format(target=backend_str))
    return response.text

run(host=host_addr, port=frontend_port)
