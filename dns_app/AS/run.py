import json
import os
from socket import *

server_port = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('0.0.0.0', server_port))
print("The server is ready to receive")

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    message = json.loads(message.decode())

    # Registration
    if len(message) == 4:

        message_body = {
            "VALUE": message["VALUE"],
            "TYPE": message["TYPE"],
            "TTL": message["TTL"]
        }

        if (os.path.isfile("dns.json")):
            with open("dns.json", "r") as f:
                dns = json.load(f)
        else:
            dns = {}
        
        dns[message["NAME"]] = message_body

        with open("dns.json", "w") as f:
            json.dump(dns, f)
        # print(message)

    # DNS Query
    response = ""
    if len(message) == 2:
        # check query should include name and type
        if "NAME" in message and "TYPE" in message:
            if (os.path.isfile("dns.json")):
                with open("dns.json", "r") as f:
                    dns = json.load(f)
                if message["NAME"] in dns:
                    if dns[message["NAME"]]["TYPE"] == message["TYPE"]:
                        response = dns[message["NAME"]]
                        response["NAME"] = message["NAME"]
                        # print(response)
                        response = json.dumps(response)

    serverSocket.sendto(response.encode(), clientAddress)