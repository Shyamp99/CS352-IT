import sys
import socket
import time

dns_table = {}

def populate_DNS(filename):
    with open(filename, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.rstrip()
            temp = line.split(' ')
            dns_table[temp[0].lower()] = [temp[1], temp[2]]


def check_table(hostname, ts_hostname):
    if hostname.lower() in dns_table:
        ret = hostname + ' ' + dns_table[hostname.lower()][0] + 'A'
    else:
        ret = hostname + ' - Error:HOST NOT FOUND'
    return ret

if __name__ == '__main__':
    populate_DNS('PROJI-DNSTS.txt')
    ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
    ts_hostname = socket.gethostname()
    port_no = sys.argv[1]
    ts_socket.bind((ts_hostname,int(port_no)))
    print(socket.gethostname())
    ts_socket.listen(5)

    while True:
        conn, addr = ts_socket.accept()
        query = conn.recv(1024)
        query = query.decode('utf-8')
        result = check_table(query, ts_hostname)
        temp = conn.send(result.encode('utf-8'))
        time.sleep(5)
