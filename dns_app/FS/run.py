import json
from flask import Flask
from flask import request
from flask import abort
from socket import *

app = Flask(__name__)

fib_arr = [0, 1]

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/register', methods=['PUT'])
def register():
# get info from body
    fs_hostname = request.form.get('hostname')
    fs_ip = request.form.get('ip')
    as_ip = request.form.get('as_ip')
    as_port = request.form.get('as_port')

    request_message = json.dumps({"NAME": fs_hostname, "VALUE": fs_ip, "TYPE": "A", "TTL": 10})

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(request_message.encode(), (as_ip, int(as_port)))

    return 'Registration is successful!', 201

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get('number')
    if number is None or not number.isdigit():
        abort(400)
    number = int(number)
    if number == 0:
        return '0', 200
    elif number == 1:
        return '1', 200
    else:
        return str(fibonacci(number-1) + fibonacci(number-2)), 200
    
def fibonacci(number):
    if number < len(fib_arr):
        return fib_arr[number]
    else:
        fib_arr.append(fibonacci(number - 1) + fibonacci(number - 2))
        return fib_arr[number]

app.run(host='0.0.0.0',
        port=9090,
        debug=True)