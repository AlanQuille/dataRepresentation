from flask import Flask, url_for, request, redirect, abort, jsonify, render_template
from zstudentDAO import studentDAO

app = Flask(__name__,
            static_url_path='', 
            static_folder='../')


# instance of zstudentDAO object
s = studentDAO

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


if __name__ == "__main__":
    app.run(debug=True)


