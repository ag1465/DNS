import socket as mysoc
import numpy as mypy
def tss():
    #setup listening socket
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
    #initialize lists that will collectively store the 
    #hostname, IP address and Flag of each entry in PROJI-DNSTS.txt
    TS_table = []
    TS_table_host = []
    TS_table_ip = []
    TS_table_flag = []
    #iterate through PROJI-DNSTS.txt and populate our
    #lists with data from each entry in file
    with open('PROJI-DNSTS.txt', 'r') as input_file:
        for line in input_file:
            #TS_table holds the entire string for each line in file
            TS_table.append(line)
            #Split string into its 3 components Hostname, IP and flag
            #Store each substring in its corresponding list. 
            #the index of each list will be the same for each entry in
            #the original file
            data = line.split()
            TS_table_host.append(data[0])
            TS_table_ip.append(data[1])
            TS_table_flag.append(data[2])
        print(TS_table_host)
        print(TS_table_ip)
        print(TS_table_flag)
        print(TS_table_host[2])
    while True:
        #wait to recieve hostname from client
        hnstring = ctsd.recv(1048).decode('utf-8').strip()
        print('this is ' + '<' + hnstring + '>')
        if hnstring in TS_table_host:
            print('found')
            #find index of target hostname in TS_table_host
            index = TS_table_host.index(hnstring)
            print('index:' + str(index) )
            #grab target hostname, ip and flag from TS_table
            #using index found in last statement
            entry = TS_table[index]
            #send entry to client
            ctsd.send(entry.encode('utf-8'))
        else:
            print('Not HERE')
            #hostname couldn't be found, so we send back an error 
            entry = hnstring + ' - Error:HOST NOT FOUND'
            ctsd.send(entry.encode('utf-8'))
    tssd.close()
    exit()
tss()
