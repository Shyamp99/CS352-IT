import sys
import socket
import time

table = {}

def populate_table(filename):
    with open(filename, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.rstrip()
            temp = line.split()
            table[temp[0].lower()] = [temp[1], temp[2]]

def check_table(hostname):
    if hostname in table.keys():
        temp = hostname + ' ' + table[hostname][0] + ' ' + table[hostname][1]
        print(temp)
        return temp
    return ''

if __name__ == "__main__":
    populate_table('PROJ2-DNSTS1.txt')
    ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
    portno = sys.argv[1]
    ts_hostname = socket.gethostname()
    ts_socket.bind(('', int(portno)))
    ts_socket.listen(5)
    print("ts is up")
    while True:
        conn, addr = ts_socket.accept()
        print(conn)
        query = conn.recv(1024)
        query = query.decode('utf-8')
        print("query: "+query)
        if len(query) == 0 or query == '':
            continue
        print(1)
        result = check_table(query.split()[0])
        print(2)
        if result != '':
            print(3)
            conn.sendall(query.encode('utf-8'))
        else:
            print(4)
            query = ''
            conn.send(query.encode('utf-8'))