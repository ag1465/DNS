import socket as mysoc
import numpy as mypy
def rss():
    try:
        rssd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('[RS]{} \n'.format("RS server socket open error ", err))
    server_binding=('',50007)
    rssd.bind(server_binding)
    #Listen for one connection at a time
    rssd.listen(1)
    #Wait for connection from client socket
    crsd,addr = rssd.accept()
    RS_table = []
    RS_table_host = []
    RS_table_ip = []
    RS_table_flag = []
    with open('PROJI-DNSRS.txt', 'r') as input_file:
        for line in input_file:
            RS_table.append(line)
            data = line.split()
            RS_table_host.append(data[0])
            RS_table_ip.append(data[1])
            RS_table_flag.append(data[2])
            print(data[0])
            print(data[1])
            print(data[2])
        print(RS_table_host)
        print(RS_table_ip)
        print(RS_table_flag)
    while True:
        hnstring = crsd.recv(1048).decode('utf-8')
        host = str(hnstring)
        print('this is ' + hnstring)
        if host in RS_table_host:
            print('Found')
            print(RS_table_host.index(hnstring))
            index = RS_table_host.index(hnstring)
            entry = RS_table[index]
            crsd.send(entry.encode('utf-8'))
        else:
            print('Not HERE')
            index = RS_table_flag.index('NS')
            entry = RS_table[index]
            crsd.send(entry.encode('utf-8'))
    rssd.close()
    exit()
rss()
