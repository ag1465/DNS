import socket as mysoc
import numpy as mypy
def client():
    try:
    #[ first socket]
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    #[second socket]
	
    try:
        ctots=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

    port = 50007
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    server_binding=(sa_sameas_myaddr,port)
    ctors.connect(server_binding)
    #First Connect to RS server
    hostnames_arr = []
    #write to output
    with open('RESOLVED.txt', 'w') as output_file:
        #read file
        with open('PROJI-HNS.txt', 'r') as input_file:
            for line in input_file:
                hostnames_arr.append(line) #reads hostname to list
        #get number of hostnames in list
        length = len(hostnames_arr)
        #loop hostnames
        for i in range(length):
            hostname = hostnames_arr[i]
            print('send ' + hostname)
            ctors.send(hostname.encode('utf-8')) #send hostname to server
            dr=ctors.recv(1024).decode('utf-8') #receive back A or NS
            print(dr)
            data = dr.split()
            if data[2] == 'A':
                output_file.write(dr.strip() + '\n')
            elif data[2] == 'NS':
                TSname = data [0]
                server_binding=(TSname, 50008)
                
                try:
                    ctots.send(hostname.encode('utf-8'))
                except:
                    ctots.connect(server_binding)
                    ctots.send(hostname.encode('utf-8'))
                dr2 = ctots.recv(1024).decode('utf-8')
                data2 = dr2.split()
                if data2[2] == 'A': 
                    output_file.write(dr2.strip() + '\n')
                else:	
                    output_file.write(dr2.strip() + '\n')
                    print('Hostname - Error:HOST NOT FOUND')
    ctors.close()
    ctots.close()
    exit()
client()
