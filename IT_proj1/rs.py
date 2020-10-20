import sys
import socket
import time

dns_table = {}
def populate_DNS(filename):
    with open(filename, "r") as fp:
        lines = fp.readlines()
        counter = 0
        for line in lines:
            line = line.rstrip()
            if counter == len(lines)-1:
                TS_hostname = line
                print("here")
                break
            temp = line.split(' ')
            dns_table[temp[0].lower()] = [temp[1], temp[2]]
            counter +=1
    return TS_hostname

def check_table(hostname, TS_hostname):
    if hostname.lower() in dns_table:
        ret = hostname + ' ' + dns_table[hostname.lower()][0] + ' A'
    else:
        print("TSHOSTNAME: "+ TS_hostname)
        ret = TS_hostname
    return ret

if __name__ == '__main__':
    TS_hostname = populate_DNS('PROJI-DNSRS.txt')
    rs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_no = int(sys.argv[1])
    rs_socket.bind((socket.gethostname(), port_no))
    rs_socket.listen(5)
    conn = 0
    addr = None
    while True:
        print(1)
        if conn == 0:
            conn, addr = rs_socket.accept()
        print(2)
        query = conn.recv(201).rstrip()
        print(3)
        query = query.decode('utf-8')
        print("query: " + query)
        result = check_table(query, TS_hostname)
        if query and len(query) > 0:
            temp = conn.send(result.encode('utf-8'))
        else:
            break
        # time.sleep()
        # if temp > 0:
        #     break
