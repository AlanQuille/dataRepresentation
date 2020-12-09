#!flask/bin/python
# import flask functions
from flask import Flask, jsonify,  request, abort, make_response, session, abort, redirect, url_for, g
# import mysql classes for connection to database
from tablesDAO import connectDAO
# import googleAPI to import gmail 
# messages
from googleAPI import googleAPI
# import json to read json files
import json

# create flask app
app = Flask(__name__,
            static_url_path='',
            static_folder='../')

# secret key for app session
app.secret_key = 'Gardenhill'

# for SQL connection, lecturer and student tables
c = connectDAO


# determine which table is changed
# at the moment it is set to 
# the value in default_value.txt
with open("default_value.txt") as d:
    data  = d.read()
    if(int(data)==0 or int(data)==1):
        table_var = int(data)
    else:
        table_var = 0

# load in messages from gmail account 
# "datarepresentation2020@gmail.com"
# the subjects are exported to json
# file called subject_emails.json
def gmailAPI():
    googleAPI()
    with open('subjects_emails.json') as json_file:
        data = json_file.read()
        final = json.loads(data)
    return final


# user class for login
class User:
    id = 0
    def __init__(self, username, password):
        self.username = username
        self.password = password
        User.id += 1

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
# sole login is root and password = ''
users.append(User(username='root', password=''))

# this function makes sure every function
# no matter what the app route
# knows that the user is logged in
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

# this logs the user in at login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = ''
    password = ''
    return_string = ''
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.json['username']
        password = request.json['password']

        username_list = []
        password_list = []
            
        for user in users:
            username_list.append(user.username)
            password_list.append(user.password)

        if(username in username_list and password in password_list):
            session['user_id'] = user.id
            return_string = "1"

        else:
            return_string = "0"
    
    
    return jsonify(return_string)

# this returns whether the user is logged
# in or not
@app.route('/verify', methods=['GET'])
def verify():
    if not g.user:
        return jsonify("0")
    else:
        return jsonify("1")



# logout the user
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify("Successfully logged out, goodbye!")


# this loads the subjects from email a/c
# into the sql table in question
@app.route('/gmail')
def gmail():
    global table_var
    return_str  = ""
    list_of_subjects = gmailAPI()
    successful_entries = 0
    errors = 0

    for i in list_of_subjects:
        cs_str= i[2]
        list_split = cs_str.split (",")
        entry1 = str(list_split[0])
        try:
            entry2 = int(list_split[1])
        # do nothing if error
        except ValueError as verr:
            continue
        # detto
        except Exception as ex:
            continue
   # if error free
        values = (entry1, entry2)
        if(table_var==0):
            return_str = str(c.create(values))
            if(return_str[:5]=="Error"):
                errors += 1
            else:
                successful_entries += 1    
        else:
            return_str = str(c.create_l(values))
            if(return_str[:5]=="Error"):
                errors += 1
            else:
                successful_entries +=  1
    
    return jsonify("Number of successful entries is {}, number of errors is {}".format(successful_entries, errors))


# change table from student
# to lecturer and vice versa
@app.route('/change_table', methods=['GET'])
def change_table():
    global table_var
    if(table_var==0):
        table_var = 1
        return jsonify("Table changed to lecturer table")
    elif(table_var==1):
        table_var = 0
        return jsonify("Table changed to student table")


# this function creates the student table
@app.route('/create_table_student', methods=['GET'])
def create_student():
    return(jsonify(c.create_student()))

# this function deletes the student table
@app.route('/delete_table_student', methods=['GET'])
def delete_student():
    return(jsonify(c.delete_student()))

# this function creates the student table
@app.route('/create_table_lecturer', methods=['GET'])
def create_lecturer():
    return(jsonify(c.create_lecturer()))

# this function creates the student table
@app.route('/delete_table_lecturer', methods=['GET'])
def delete_lecturer():
    return(jsonify(c.delete_lecturer()))

# thhis creates new rows in lecturer or
# student table    
@app.route('/create', methods=['POST'])
def create():
    global table_var
    #if not session.get('logged_in'):
    if not request.json:
        abort(400)
    if not 'name' in request.json:
        abort(400)
    student={
            "name":  request.json['name'],
            "age": request.json['age']
            }
    values = (student["name"], student["age"])
    if(table_var==0):
        return_str = c.create(values)
    else:
        return_str = c.create_l(values)

    if return_str == "Success":
        return jsonify( {'student':student }),201
    else:
        return jsonify(return_str)


# this returns a single row from
# either lecturer or student table
@app.route('/read1', methods=['POST'])
def read1():
    global table_var
    if not request.json:
        abort(400)
    if not 'id' in request.json:
        abort(400)
    student={
        "id":  request.json['id'],
    }
    values = student['id']
    test_str = ""
    if(table_var == 0):
        if(isinstance(c.findByID(values), str)):
            test_str = c.findByID(values)
        if(c.findByID(values)==None):
            student = "Error! ID not present."
        elif(test_str[:5] !="Error"):
            student["name"] = c.findByID(values)[1]
            student["age"] = c.findByID(values)[2]
        else:
            student = c.findByID(values)
    else:
        if(isinstance(c.findByID_l(values), str)):
            test_str = c.findByID_l(values)
        if(c.findByID_l(values)==None):
            student = "Error! ID not present."
        elif(test_str[:5] !="Error"):
            student["name"] = c.findByID_l(values)[1]
            student["age"] = c.findByID_l(values)[2]
        else:
            student = c.findByID_l(values)
            


    return jsonify(student),201
    #return jsonify(values),201


# returns all rows from either lecturer
# or student table
@app.route('/read2', methods=['GET'])
def read2():
    global table_var
    if(table_var == 0):
        return jsonify(c.getAll()),201
    else:
        return jsonify(c.getAll_l()),201
    #return jsonify(values),201


# inner join student and lecturer table
@app.route('/inner_join', methods=['GET'])
def inner_join():
    return jsonify(c.inner_join())
    #return jsonify(values),201


# update or change row in student 
# or lecturer table
@app.route('/update', methods=['POST'])
def update():
    global table_var
    if not request.json:
        abort(400)
    if not 'name' in request.json:
        abort(400)
    student={
        "name":  request.json['name'],
        "age": request.json['age'],
        "id" : request.json['id']
    }
    test_values = student["id"]
    values = (student["name"], student["age"], student["id"])
    if(table_var == 0):
        if(c.findByID(test_values)==None):
            student = "Error! ID not present."
        elif(c.findByID(test_values)[:5] != "Error"):
            c.update(values)
        else:
            student = s.update(values)
    else:
        if(c.findByID_l(test_values)==None):
            student = "Error! ID not present."
        elif(c.findByID_(test_values)[:5] != "Error"):
            #print(l.findByID(values)[:5])
            c.update_l(values)
        else:
            student = c.update_l(values)

    return jsonify(student),201
    #return jsonify(values),201

# delete each row from student
# or lecturer table
@app.route('/delete', methods=['POST'])
def delete():
    global table_var
    if not request.json:
        abort(400)
    if not 'id' in request.json:
        abort(400)
    student={
        "id" : request.json['id']
    }
    values = student["id"]
    if(table_var==0):
        if(c.findByID(values)==None):
            student = "Error! ID not present."
        elif(c.findByID(values)=="Success"):
            c.delete(values)
        else:
            student = c.delete(values)

    else:
        if(c.findByID_l(values)==None):
            student = "Error! ID not present."
        elif(c.findByID_l(values)=="Success"):
            c.delete_l(values)
        else:
            student = c.delete_l(values)
    return jsonify(student),201
    #return jsonify(values),201

# root page for web server
# if not logged in will 
# redirect to login.html
# otherwise will go to 
# homepage.html
@app.route('/')
def is_user_logged_in():
    if not g.user:
        return redirect("login.html")
    return redirect("homepage.html")

# run the app if this page is run
if __name__ == '__main__':
    app.run(debug= True)