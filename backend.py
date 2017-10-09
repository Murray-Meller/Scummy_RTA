from bottle import run, request, post, get

# Important globals
host = "localhost"
port = "8082"


# Our "Database"
users = []
vehicles = []
destroyed_vehicles = []

user_database = './database/users.txt'
vehicle_database = './database/vehicles.txt'
destroyed_vehicle_database = './database/destroyed_vehicles.txt'

user_database_num_fields = 6
vehicle_database_num_fields = 4
destroyed_vehicle_database_num_fields = 1

def load_users():
	global users
	users = []
	udb = open(user_database, 'r')
	for line in udb:
		line = line.split(',')
		line[-1] = line[-1][:-1]
		users.append(line)
	udb.close()
	return users

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

def load_vehicles():
	global vehicles
	vehicles = []
	vdb = open(vehicle_database, 'r')
	for line in vdb:
		line = line.split(',')
		line[-1] = line[-1][:-1]
		vehicles.append(line)
	vdb.close()
	return vehicles

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

def load_destroyed_vehicles():
	global destroyed_vehicles
	destroyed_vehicles = []
	dvdb = open(destroyed_vehicle_database, 'r')
	for line in dvdb:
		line = line.split(',')
		line[-1] = line[-1][:-1]
		destroyed_vehicles.append(line)
	dvdb.close()
	return destroyed_vehicles

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

def load_database():
    load_users()
    load_vehicles()
    load_destroyed_vehicles()

def save_database():
    save_users()
    save_vehicles()
    save_destroyed_vehicles()

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

# API calls
@post('/api/useradd/<username:path>/<password:path>/<persontype:path>')
def useradd(username, password, persontype):
	load_users()
	global users
	for user in users:
		if user[1] == username:
			return "User already exists"
	users.append([len(users),username,password,persontype,"",""])
	save_users()
	return "User added"

@post('/api/userget/<username:path>')
def userget(username):
	load_users()
	for user in users:
		if user[1] == username:
			r_string = ''
			for field in user:
				r_string += field + ','
			return r_string[:-1]
	return "User does not exist!"

@post('/api/userget/all')
def usergetall():
	r_string = ''
	udb = open(user_database, 'r')
	count = 0
	for user in udb:
		count += 1
		if count != 1:
			r_string += user
	return r_string

@post('/api/usercheck/<username:path>/<password:path>')
def check_login(username, password):
	load_users()
	if (username == "" or password == ""):
		return "Incorrect, you think you could get in that easy False"
	for user in users:
		if user[1] == username:
			if password == user[2]:
				return "Success True"
	return "Unsuccessful, try again Alan False"

@post('/api/userstring')
def get_users_string():
	load_users()
	content = ""
	for user in users:
	    for field in user:
	        content += "| " + str(field) + " " * (25 - len(str(field))) + " "
	    content += "|\n"
	print(users)
	return content

@post('/api/vehicleadd/<vehicle:path>')
def vehicleadd(vehicle):
	load_vehicles()
	global vehicles
	vehicles.append(vehicle)
	save_vehicles()
	return "User added"

@post('/api/vehicleget/all')
def vehiclegetall():
	load_vehicles()
	r_string = ''
	cdb = open(vehicle_database, 'r')
	count = 0
	for car in cdb:
		count += 1
		if count != 1:
			r_string += car
	return r_string

@post('/api/vehiclestring')
def get_vehicles_string():
	load_vehicles()
	vehicle = ""
	for car in vehicles:
	    for field in car:
	        vehicle += "| " + str(field) + " " * (20 - len(str(field))) + " "
	    vehicle += "|\n"
	return vehicle

# TODO: currently no way to add destroyed car in frontend
# @post('/api/destroyedadd/<destroyed:path>')
# def destroyedadd(destroyed):
# 	load_destroyed_vehicles()
# 	global destroyed_vehicles
# 	users.append([destroyed_vehicle])
# 	save_users()
# 	return "User added"

@post('/api/destroyedget/all')
def destroyedgetall():
	r_string = ''
	cdb = open(destroyed_vehicle_database, 'r')
	count = 0
	for car in cdb:
		count += 1
		if count != 1:
			r_string += car
	return r_string

@post('/api/destroyedstring')
def get_destroyed_vehicle_string():
	load_destroyed_vehicles()
	destroyed = ""
	for car in destroyed_vehicles:
		for field in car:
			destroyed += "| " + str(field) + " " * (10 - len(str(field))) + " "
		destroyed += "|\n"
	return destroyed

# Rather than using paths, you could throw all the requests with form data filled using the
# requests module and extract it here.

# Run the server
run(host=host, port=port)
