from flask import Flask, url_for , request, redirect, abort, jsonify, render_template
from zstudentDAO import studentDAO

app =  Flask(__name__, static_url_path='', static_folder='staticpages')

books=[
    { "id":1, "Title":"Harry Potter", "Author": "JK", "Price":10},
    { "id":2, "Title":"Some cook book", "Author": "Mr. Angry Man", "Price":20},
    { "id":3, "Title":"Python made easy", "Author": "Some liar", "Price":15}
]
nextId=4

#@app.route('/index.html')
#def render_static():
 #   output = "Rest server!"
 #   return render_template('index.html', output=output)


def create():
    global nextId
    if not request.json:
        abort(400)
    

    book = {
        "id": nextId,
        "Title": request.json["Title"],
        "Author": request.json["Author"],
        "Price": request.json["Price"]
    }
    books.append(book)
    nextId += 1
    return jsonify(book)

@app.route('/homepage.html')
def render_static():
    output = "Rest server!"
    return render_template('homepage.html', output=output)


# instance of zstudentDAO object
s = studentDAO

#@app.route('/books', methods=['POST'])
@app.route('/create.html')
def render_static_2():
    return render_template('create.html')


cars = []

@app.route('/cars', methods=['POST'])
def create_car():
    if not request.json:
        abort(400)
    if not 'reg' in request.json:
        abort(400)
    car={
        "reg":  request.json['reg'],
        "make": request.json['make'],
        "model":request.json['model'],
        "price":request.json['price']
    }
    cars.append(car)
    return jsonify( {'car':car }),201


print(cars)
   # name = request.form['name']
    #age = request.form['age']
    #print("Name is: {}".format(name))
    #print("Age is: {}".format(age))




 #   if request.method == 'POST':
#        name = request.form['name']
 #       age = request.form['age']
 #       print("Name is: {}".format(name))
 #       print("Age is: {}".format(age))
 #       return redirect(url_for('render_static_2'))
  #  else:

@app.route('/books/')
def getAll():
    return jsonify(books)

@app.route('/books/<int:id>')
def findByID(id):
    foundBooks  = list(filter (lambda t : t["id"]==id, books))
    if len(foundBooks) == 0:
        return jsonify({}), 204
    return jsonify(foundBooks[0])
    #return "served by update with id " + str(id)

# create
# curl -X POST -H "content-type:application/json" -d "{\"Title\":\"test\", \"Author\":\"soome guy\", "\"Price\":123"}" http://127.0.0.1:5000/books
#@app.route('/books', methods=['POST'])
#def create():
#    global nextId
#    if not request.json:
#        abort(400)
    

#    book = {
#        "id": nextId,
#        "Title": request.json["Title"],
#        "Author": request.json["Author"],
#        "Price": request.json["Price"]
#    }
#    books.append(book)
#    nextId += 1
#    return jsonify(book)

# update
#  curl -X PUT -H "content-type:application/json" -d "{\"Title\":\"new Title\", \"Author\":\"soome guy\", "\"Price\":999"}" http://127.0.0.1:5000/books/2
@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    foundBooks  = list(filter (lambda t : t["id"]==id, books))
    if len(foundBooks) == 0:
        return jsonify({}), 400
    
    currentBook = foundBooks[0]
    if 'Title' in request.json:
        currentBook['Title'] = request.json['Title']

    if 'Author' in request.json:
        currentBook['Author'] = request.json['Author']

    if 'Price' in request.json:
        currentBook['Price'] = request.json['Price']
    
    return jsonify(currentBook)

# delete
# curl -X DELETE http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['DELETE'])
def delete(id):
    foundBooks  = list(filter (lambda t : t["id"]==id, books))
    if len(foundBooks) == 0:
        return jsonify({}), 404
    books.remove(foundBooks[0])

    return jsonify({"done":True})



if __name__ == "__main__":
    app.run(debug=True)

