from flask import Flask
from flask import request
from flask import abort
from socket import *
import json
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if hostname is None or fs_port is None or number is None or as_ip is None or as_port is None:
        abort(400)

    request_message = json.dumps({'TYPE': 'A', 'NAME': hostname})

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.sendto(request_message.encode(), (as_ip, int(as_port)))
    response_IP, serverAddress = clientSocket.recvfrom(2048)
    response_IP = response_IP.decode()
    print(response_IP)
    clientSocket.close()

    response = requests.get('http://' + response_IP + '/fibonacci?number=' + number)
    print(response.text)
    return response


app.run(host='0.0.0.0',
        port=8080,
        debug=True)