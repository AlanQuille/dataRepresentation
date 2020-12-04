#!flask/bin/python
from flask import Flask, jsonify,  request, abort, make_response, session, abort, redirect, url_for, g
from zstudentDAO import studentDAO
from zstudentDAO import lecturerDAO
from googleAPI import googleAPI
import json

app = Flask(__name__,
            static_url_path='',
            static_folder='../')

app.secret_key = 'somesecretkeythatonlyishouldknow'

# for SQL connection
s = studentDAO
l = lecturerDAO

# determine which table is changed
# at the moment it is set to 0/student
# by default
table_var = 0

# for Gmail API
# this function dumps today's emails to a JSON file
# called 

def gmailAPI():
    googleAPI()
    with open('subjects_emails.json') as json_file:
        data = json_file.read()
        final = json.loads(data)
        #print(final)
    return final

#gmailAPI()

# read json file
#json.load(file object)



class User:
    id = 0
    def __init__(self, username, password):
        #self.id = id
        self.username = username
        self.password = password
        User.id += 1

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(username='root', password=''))
print(users)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

# change this using login or not depending
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
    
    print(return_string)
    return jsonify(return_string)

@app.route('/verify', methods=['GET'])
def verify():
    if not g.user:
        return jsonify("0")
    else:
        return jsonify("1")



# logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return jsonify("Successfully logged out, goodbye!")



@app.route('/gmail')
def gmail():
    global table_var
    list_of_subjects = gmailAPI()
    successful_entries = 0

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
            s.create(values)
        else:
            l.create(values)
        successful_entries += 1
    
    return jsonify("Number of successful entries is: {}".format(successful_entries))


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


  #  s.create(values)
# add in all tables from Gmail a/c
# dataRepresentation2020.gmail.com
# 
#@app.route('/gmail', methods=['POST'])
#def gmail():
   # list_of_subjects = gmailAPI()

   # for sub in list_of_subjects:
    #    list_split = sub[2].split (",")
    #    if(len(list_split) != 2):
    #        return jsonify("Error! Number of entries")
   #     else:
    #        values = (list_split[0], str(list_split[1]))
   #         s.create(values)
    #        return jsonify(list_split)
    

    
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
        s.create(values)
    else:
        l.create(values)
    return jsonify( {'student':student }),201



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
    if(table_var == 0):
        if(s.findByID(values)==None):
            student = "Error! ID not present."
        else:
            student["name"] = s.findByID(values)[1]
            student["age"] = s.findByID(values)[2]
    else:
        if(l.findByID(values)==None):
            student = "Error! ID not present."
        else:
            student["name"] = l.findByID(values)[1]
            student["age"] = l.findByID(values)[2]

    return jsonify(student),201
    #return jsonify(values),201


@app.route('/read2', methods=['GET'])
def read2():
    global table_var
    if(table_var == 0):
        return jsonify(s.getAll()),201
    else:
        return jsonify(l.getAll()),201
    #return jsonify(values),201


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
        if(s.findByID(test_values)==None):
            student = "Error! ID not present."
        else:
            s.update(values)
    else:
        if(l.findByID(test_values)==None):
            student = "Error! ID not present."
        else:
            l.update(values)

    return jsonify(student),201
    #return jsonify(values),201

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
        if(s.findByID(values)==None):
            student = "Error! ID not present."
        else:
            s.delete(values)
    else:
        if(l.findByID(values)==None):
            student = "Error! ID not present."
        else:
            l.delete(values)
    return jsonify(student),201
    #return jsonify(values),201

@app.route('/')
def is_user_logged_in():
    if not g.user:
        return redirect("login.html")
    return redirect("homepage.html")

if __name__ == '__main__':
    app.run(debug= True)