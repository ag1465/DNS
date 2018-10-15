import socket as mysoc
import numpy as mypy
def client():
    try:
    #[Create The First Socket]
        ctors=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ",err))
    #[Create The Second Socket]
    try:
        ctots=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    #Define the port and get hostname for local machine
    port = 50007
    sa_sameas_myaddr = mysoc.gethostbyname(mysoc.gethostname())
    #Connect to the RS server on the local machine
    server_binding=(sa_sameas_myaddr,port)
    ctors.connect(server_binding)
    #First Connect to RS server
    hostnames_arr = []
    #Open file to write
    with open('RESOLVED.txt', 'w') as output_file:
        #Open file to read the host name
        with open('PROJI-HNS.txt', 'r') as input_file:
            for line in input_file:
                hostnames_arr.append(line) #reads hostname to list
        #get number of hostnames in list
        length = len(hostnames_arr)
        #loop hostnames
        for i in range(length):
            hostname = hostnames_arr[i]
            print('send ' + hostname)
            #encode hostname string and send to RS server
            ctors.send(hostname.encode('utf-8'))
            #decode string that is received by RS server
            dr=ctors.recv(1024).decode('utf-8') 
            print(dr)
            #Split the string into array to get hostname, ip address, and flag
            data = dr.split()
            #check if flag is A or NS
            if data[2] == 'A':
                #If A, write to output file
                output_file.write(dr.strip() + '\n')
            elif data[2] == 'NS':
                #If NS, send hostname to TS Server by using hostname given by RS server. 
                TSname = data [0]
                #bind the socket to the given TS hostname and port
                server_binding=(TSname, 50008)
                #First time we would connect to the TS server and then send hostname.
                #Second time we see that there is a connection so we just send the hostname.
                try:
                    ctots.send(hostname.encode('utf-8'))
                except:
                    ctots.connect(server_binding)
                    #encode hostname string and send to TS server
                    ctots.send(hostname.encode('utf-8'))
                #decode string that is received by TS server.
                dr2 = ctots.recv(1024).decode('utf-8')
                #Split the string into array to get hostname, ip address, and flag
                data2 = dr2.split() 
                #check if flag is A or HostNotFound
                if data2[2] == 'A':
                    #If A, write to output file
                    output_file.write(dr2.strip() + '\n')
                else:
                    #If HostNotFound, write Hostname - Error:HOST NOT FOUND
                    output_file.write(dr2.strip() + '\n')
                    print('Hostname - Error:HOST NOT FOUND')
    # close the client socket to RS and TS  and exit 
    ctors.close()
    ctots.close()
    exit()
#call client
client()
