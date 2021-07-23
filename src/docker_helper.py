import docker
import os

available_ports = [i for i in range(56901, 56911)]

image_tag = "godot-server"

client = docker.from_env()
homedir = os.path.expanduser("~")

path_to_dockerfile = homedir + '/godot/multiplayer/docker'

servers_running = False

def get_image():
    try:
        print("getting image " + image_tag)
        client.get(image_tag)
    except docker.errors.ImageNotFound:
        print("image " + image_tag + " not found, building...")
        client.images.build(path=path_to_dockerfile, rm=True, tag=image_tag)
    except:
        print("Could not get or build the image " + image_tag)

def run_container(port):
    try:
        print("running container with image " + image_tag + ", and port " + str(port))
        client.containers.run(
            image=image_tag, 
            detach=True, 
            environment={"PORT": port}, 
            ports={str(port) + '/tcp': port, str(port) + '/udp': port}
        )
    except docker.errors.ImageNotFound:
        get_image()
        print("Image not found error when running")
        return "retry"
    except:
        return "error"

def start_servers():
    global servers_running
    for port in available_ports:
        container = run_container(port)
        if container == "retry":
            run_container(port)
    servers_running = True
