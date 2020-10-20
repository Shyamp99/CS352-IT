import threading
import time
import random
import socket
import sys

def client():
    try:
        RS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        RS_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
        print("[C]: RS socket created")
        # TS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[C]: TS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()


    # local version - may need to be updated to remote func.
    # Define the port on which you want to connect to the server
    port = int(sys.argv[2])
    localhost_addr = socket.gethostbyname(sys.argv[1])

    # retrieve hostnames from PROJI-HNS.txt
    hostnames = retrieve_hostnames()

    # connect to the server on local machine - local version - may need to be updated to remote func.
    RS_server_binding = (sys.argv[1], port)
    RS_socket.connect(RS_server_binding)
    RS_socket_closed = False
    # TS_server_binding = (localhost_addr, port)
    # TS_socket.connect(TS_server_binding)

    # Send request to RS
    print(hostnames)
    for hostname in hostnames:
        print(hostname)
        RS_response = query_server(RS_socket, hostname)
        # Check received data of the format 'Hostname IPaddress A'
        if is_success(RS_response): # received 'A' and no need to query TS
            write_output(RS_response) # write to RESOLVED.txt
        else:
            print("handle ts")
            # RS_socket.close()
            RS_socket_closed = True
            TS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TS_hostname = RS_response.split()[0]
            # print(socket.gethostbyname(TS_hostname))
            port = int(sys.argv[3])
            TS_server_binding = (TS_hostname, port)
            TS_socket.connect(TS_server_binding)
            print('here')
            # We didn't find the hostname in RS - query TS
            TS_response = query_server(TS_socket, hostname)
            print(TS_response)
            write_output(TS_response) # write to RESOLVED.txt
            TS_socket.close()


    # close the sockets
    # if not RS_socket_closed:
    time.sleep(20)
    RS_socket.close()
    exit()

def query_server(socket, hostname):
    # Sends hostname to TS server, and returns the corresponding output
    while True:
        if socket.send(hostname.encode('utf-8')) != 0:
            break
        else:
            print("err")
    # print("here")
    response = socket.recv(201) # assuming proper response format
    # print("response: "+ response.decode('utf-8'))
    return response.decode('utf-8')

# Check received data of the format 'Hostname IPaddress A'
def is_success(response):
    response_split = response.split()
    return 'A' in response_split # naive check -- they

# Writes response to RESOLVED.txt
def write_output(response):
    print("IN WRITE OUTPUT")
    with open("RESOLVED.txt", "a") as infile:
        infile.write(response + '\n')
    print("out of WRITE OUTPUT")
# retrieve_hostnames : pulls hostnames from PROJI-HNS.txt and returns as a list of strings
def retrieve_hostnames():
    hostnames = []
    with open("PROJI-HNS.txt", "rw") as infile:
        for _, line in enumerate(infile):
            hostnames.append(line.rstrip())

    return hostnames

if __name__ == "__main__":

    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()
    time.sleep(5)
    sys.exit()
    print("Done.")
