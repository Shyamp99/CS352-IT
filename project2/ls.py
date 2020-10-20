import threading
import time
import socket
import sys
import select


def accept_handler(ts1, ts2, msg):
    ts1.send(msg)
    ts2.send(msg)
    ts1.setblocking(5)
    start_time = time.perf_counter()
    ts1_response = ''
    ts2_response = ''
    while True:
        print('time: ', time.perf_counter())
        ready = select.select([ts1], [], [], 5)
        if ready[0]:
            ts1_response = ts1.recv(1024)
        ready = select.select([ts2], [], [], 5)
        if ready[0]:
            ts2_respone = ts2.recv(1024)
        print(1)
        if start_time-time.perf_counter() > 5 or len(ts1_response) > 2 or len(ts2_respone) > 2:
            break
    print("outside while")
    if len(ts1_response) > 2:
        return ts1_response
    elif len(ts2_respone) > 2:
        return ts2_respone
    else:
        return None


if __name__ == "__main__":
    #set up connections to both ts's and client
    ls_port = int(sys.argv[1])
    ts1_hostname = sys.argv[2]
    ts1_port = int(sys.argv[3])
    ts2_hostname = sys.argv[4]
    ts2_port = int(sys.argv[5])

    localhost_addr = socket.gethostbyname(socket.gethostname())
    print("ls is up")
    print(localhost_addr)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((localhost_addr, 11111))
    client_socket.listen()

    ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ts1_socket.setblocking(False)
    ts1_socket.connect((localhost_addr, ts1_port))


    ts2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ts2_socket.setblocking(False)
    ts2_socket.settimeout(5)
    ts2_socket.connect((localhost_addr, ts2_port))

    while True:
        print(1)
        client_conn, client_arr = client_socket.accept()
        client_query = client_conn.recv(1024)
        response = accept_handler(ts1_socket, ts2_socket, client_query)
        if response:
            print(response.decode('utf-8'))
            client_conn.send(response)
        else:
            temp = client_query.decode('utf-8')
            response = temp.split()[0] + ' - Error:HOST NOT FOUND'
            client_conn.send(response.encode('utf-8'))


    client_socket.close()
    ts1_socket.close()
    ts2_socket.close()

