#!flask/bin/python
from flask import Flask, jsonify,  request, abort, make_response, session, abort, redirect, url_for, g
from zstudentDAO import studentDAO

app = Flask(__name__,
            static_url_path='',
            static_folder='../')

app.secret_key = 'somesecretkeythatonlyishouldknow'

s = studentDAO



example = 0


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
            return_string = "Success!"

        else:
            return_string = "Failure!"
    
    print(return_string)
    return jsonify(return_string)

@app.route('/verify', methods=['GET'])
def verify():
    if not g.user:
        return jsonify("0")
    else:
        return jsonify("1")



# logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return "Goodbye!"


# create /verify which uses GET and ajax
# pass logged_in_or_not of particular user
# if logged_in_or_not=0, redirect using javascript
# to login 

@app.route('/create', methods=['POST'])
def create():
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
    s.create(values)
    return jsonify( {'student':student }),201



@app.route('/read1', methods=['POST'])
def read1():
    if not request.json:
        abort(400)
    if not 'id' in request.json:
        abort(400)
    student={
        "id":  request.json['id'],
    }
    values = student['id']
    if(s.findByID(values)==None):
        student = "Error! ID not present."
    else:
        student["name"] = s.findByID(values)[1]
        student["age"] = s.findByID(values)[2]

    return jsonify(student),201
    #return jsonify(values),201


@app.route('/read2', methods=['GET'])
def read2():
    return jsonify(s.getAll()),201
    #return jsonify(values),201


@app.route('/update', methods=['POST'])
def update():
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
    if(s.findByID(test_values)==None):
        student = "Error! ID not present."
    else:
        s.update(values)
    return jsonify(student),201
    #return jsonify(values),201

@app.route('/delete', methods=['POST'])
def delete():
    if not request.json:
        abort(400)
    if not 'id' in request.json:
        abort(400)
    student={
        "id" : request.json['id']
    }
    values = student["id"]
    if(s.findByID(values)==None):
        student = "Error! ID not present."
    else:
        s.delete(values)
    return jsonify(student),201
    #return jsonify(values),201

@app.route('/')
def is_user_logged_in():
    if not g.user:
        return redirect("login.html")
    return redirect("homepage.html")

if __name__ == '__main__':
    app.run(debug= True)