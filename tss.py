import socket as mysoc
import numpy as mypy
def tss():
    try:
        tssd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('[TS]{} \n'.format("TS server socket open error ", err))
    server_binding=('', 50008)
    tssd.bind(server_binding)
    #Listen for one connection at a time
    tssd.listen(1)
    #Wait for connection from client socket
    ctsd,addr = tssd.accept()
    TS_table = []
    TS_table_host = []
    TS_table_ip = []
    TS_table_flag = []
    with open('PROJI-DNSTS.txt', 'r') as input_file:
        for line in input_file:
            TS_table.append(line)
            data = line.split()
            TS_table_host.append(data[0])
            TS_table_ip.append(data[1])
            TS_table_flag.append(data[2])
        print(TS_table_host)
        print(TS_table_ip)
        print(TS_table_flag)
        print(TS_table_host[2])
    while True:
        hnstring = ctsd.recv(1048).decode('utf-8').strip()
        print('this is ' + '<' + hnstring + '>')
        if hnstring in TS_table_host:
            print('found')
            index = TS_table_host.index(hnstring)
            print('index:' + str(index) )
            entry = TS_table[index]
            ctsd.send(entry.encode('utf-8'))
        else:
            print('Not HERE')
            entry = hnstring + ' - Error:HOST NOT FOUND'
            ctsd.send(entry.encode('utf-8'))
    tssd.close()
    exit()
tss()
