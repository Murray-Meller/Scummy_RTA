from bottle import run, get, post, request
import requests

host_addr = "localhost"
frontend_port = 8080
backend_port = 8081

backend_str = "http://{host}:{port}".format(host=host_addr, port=backend_port)

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
    
    # Call the back-end
    response = requests.post("{target}/api/useradd/{username}/{password}"
    	.format(target=backend_str, username=username, password=password))
    
    # Tell the user what the back-end thinks
    # Alternatively, reformat what the back-end thinks into a nicer page
    return response.text


run(host=host_addr, port=frontend_port)