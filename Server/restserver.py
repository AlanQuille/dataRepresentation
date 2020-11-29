#!flask/bin/python
from flask import Flask, jsonify,  request, abort, make_response
from zstudentDAO import studentDAO

app = Flask(__name__,
            static_url_path='',
            static_folder='../')

s = studentDAO

@app.route('/create', methods=['POST'])
def create():
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
    #return jsonify(values),201


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


# sample test
# curl -i -H "Content-Type:application/json" -X POST -d '{"reg":"12 D 1234","make":"Fiat","model":"Punto","price":3000}' http://localhost:5000/cars
# for windows use this one
# curl -i -H "Content-Type:application/json" -X POST -d "{\"reg\":\"12 D 1234\",\"make\":\"Fiat\",\"model\":\"Punto\",\"price\":3000}" http://localhost:5000/cars
@app.route('/cars/<string:reg>', methods =['PUT'])
def update_car(reg):
    foundCars=list(filter(lambda t : t['reg'] ==reg, cars))
    if len(foundCars) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'make' in request.json and type(request.json['make']) != str:
        abort(400)
    if 'model' in request.json and type(request.json['model']) is not str:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not int:
        abort(400)
    foundCars[0]['make']  = request.json.get('make', foundCars[0]['make'])
    foundCars[0]['model'] =request.json.get('model', foundCars[0]['model'])
    foundCars[0]['price'] =request.json.get('price', foundCars[0]['price'])
    return jsonify( {'car':foundCars[0]})
#curl -i -H "Content-Type:application/json" -X PUT -d '{"make":"Fiesta"}' http://localhost:5000/cars/181%20G%201234
# for windows use this one
#curl -i -H "Content-Type:application/json" -X PUT -d "{\"make\":\"Fiesta\"}" http://localhost:5000/cars/181%20G%201234

@app.route('/cars/<string:reg>', methods =['DELETE'])
def delete_car(reg):
    foundCars = list(filter (lambda t : t['reg'] == reg, cars))
    if len(foundCars) == 0:
        abort(404)
    cars.remove(foundCars[0])
    return  jsonify( { 'result':True })

@app.errorhandler(404)
def not_found404(error):
    return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
    return make_response( jsonify( {'error':'Bad Request' }), 400)


if __name__ == '__main__' :
    app.run(debug= True)