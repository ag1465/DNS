import socket as mysoc
def tss():
    try:
        tssd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('[TS]{} \n'.format("TS server socket open error ", err))
    server_binding=('',50007)
    tssd.bind(server_binding)
    #Listen for one connection at a time
    tssd.listen(1)
    #Wait for connection from client socket
    ctsd,addr = tssd.accept()
    while True:
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
        hnstring = ctsd.recv(1048).decode('utf-8')
        if hnstring in TS_table_host:
            print(TS_table_host.index(hnstring))
            index = TS_table_host.index(hnstring)
            entry = TS_table[index]
            crsd.send(entry.encode('utf-8'))
        else:
            print('Not HERE')
            entry = hnstring + 'Error:HOST NOT FOUND'
            crsd.send(entry.encode('utf-8'))
    tssd.close()
    exit()
tss()
