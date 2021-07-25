from flask import Flask
import random
import string
import docker_helper

lobbies = {}
open_ports = []

def get_passcode(val):
    for code, value in lobbies.items():
         if val == value:
             return code
    return "passcode doesn't exist"

def create_passcode():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(6))

def get_server(passcode = ""):
    if passcode == "" and len(open_ports) > 0:
        new_passcode = create_passcode()
        lobbies[new_passcode] = open_ports.pop()
        return [new_passcode, lobbies[new_passcode]]
    elif passcode == "" and len(open_ports) == 0:
        return ["error", "Servers are full"]
    else:
        try:
            return [passcode, lobbies[passcode]]
        except:
            return ["error", "Invalid passcode"]

app = Flask(__name__)

@app.route("/")
def status():
    return {
        "lobbies": lobbies,
        "open ports": open_ports
    }

@app.route("/host")
def host():
    server = get_server()
    new_passcode = server[0]
    new_port = server[1]
    print(lobbies, open_ports)
    if server[0] == "error":
        return {
            "error": server[1]
        }
    return {
        "port": new_port,
        "passcode": new_passcode
    }

@app.route("/join/<passcode>")
def join(passcode):
    server = get_server(passcode)
    print(lobbies, open_ports)
    if server[0] == "error":
        return {
            "error": server[1]
        }
    return {
        "port": server[1]
    }

@app.route("/server/available/<port>")
def add_available_server(port):
    port = int(port)
    open_ports.append(port)
    lobbies.pop(get_passcode(port))
    print(lobbies, open_ports)
    return {
        "response": "opened"
    }

@app.route("/server/add/<port>")
def add_new_server(port):
    if not int(port) in open_ports:
        open_ports.append(int(port))
    print(lobbies, open_ports)
    return {
        "response": "added"
    }

@app.route("/server/remove/<port>")
def remove_server(port):
    print(lobbies, open_ports)
    for p in open_ports:
        if p == int(port):
            open_ports.remove(p)
    return {
        "response": "removed"
    }

@app.route("/server/start/all")
def start_all_servers():
    if not docker_helper.servers_running:
        docker_helper.start_servers()
        return "<h1>Starting Servers</h1><h3>Hang tight!</h3>"
    return "<h1>Servers have already been started<h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=56900, debug=True)