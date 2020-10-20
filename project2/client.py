import threading
import time
import random
import socket
import sys

def retrieve_hostnames():
    hostnames = []
    with open("PROJI-HNS.txt") as infile:
        for _, line in enumerate(infile):
            hostnames.append(line)

    return hostnames

def write_output(responses):
    # print("IN WRITE OUTPUT")
    with open("RESOLVED.txt", "a") as infile:
        for response in responses:
            infile.write(response + '\n')
    # print("out of WRITE OUTPUT")

def retrieve_hostnames():
    hostnames = []
    with open("PROJ2-HNS.txt") as infile:
        for _, line in enumerate(infile):
            hostnames.append(line)

    return hostnames

def query_server(socket, line):
    # Sends hostname to TS server, and returns the corresponding output
    while True:
        if socket.send(line.encode('utf-8')) != 0:
            break
        else:
            print("err")
    # print("here")
    response = socket.recv(201) # assuming proper response format
    # print("response: "+ response.decode('utf-8'))
    return response.decode('utf-8')

def client():
    results = []
    try:
        ls_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ls_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
        print("[C]: RS socket created")
        # TS_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[C]: TS socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    ls_hostname = sys.argv[1]
    ls_port = sys.argv[2]

    hostnames = retrieve_hostnames()
    ls_host = socket.gethostbyname(socket.gethostname())
    time.sleep(1)
    ls_socket.connect((ls_host, 11111))

    for host in hostnames:
        response = query_server(ls_socket, host)
        if response != '':
            results.append(response)
    write_output(results)

    ls_socket.close()
        

client()

