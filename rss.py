import socket as mysoc
import numpy as mypy
def rss():
    #Create the socket
    try:
        rssd = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('[RS]{} \n'.format("RS server socket open error ", err))
    #Bind the socket to my address and defined port
    server_binding=('',50007)
    rssd.bind(server_binding)
    #Listen for one connection at a time
    rssd.listen(1)
    #Wait for connection from client socket
    crsd,addr = rssd.accept()
    #Initialize lists that will collectively store the hostanmes, IP addresses, and Flag of each entry
    RS_table = [] # list of strings from the file
    RS_table_host = []
    RS_table_ip = []
    RS_table_flag = []
    #open file to read the hostnames, IP addresses, and Flags
    with open('PROJI-DNSRS.txt', 'r') as input_file:
        #go through input file line by line
        for line in input_file:
            #add to list of strings
            RS_table.append(line)
            #splits the string into the fields: hostnames, IP address, and Flag
            data = line.split()
            #add to list of hostnames
            RS_table_host.append(data[0])
            #add to list of IP addresses
            RS_table_ip.append(data[1])
            #add to list of flags
            RS_table_flag.append(data[2])
            print(data[0])
            print(data[1])
            print(data[2])
        print(RS_table_host)
        print(RS_table_ip)
        print(RS_table_flag)
    #wait for messages
    while True:
        #receive hostname client and decode to string form. Strip off white space on the beginning and end of the string.
        hnstring = crsd.recv(1048).decode('utf-8').strip()
        print('this is ' + '<'  + hnstring + '>')
   #checks if the hostname exist in the list of hostnames
        #host name exist
        if hnstring in RS_table_host:
            print('Found')
            print(RS_table_host.index(hnstring))
            #find the index of the hostname
            index = RS_table_host.index(hnstring)
            #use the index and grab the string
            entry = RS_table[index]
            #encode the string and send back to the client
            crsd.send(entry.encode('utf-8'))
        #host name does not exist
        else:
            print('Not HERE')
            #find the index of flag 'NS'
            index = RS_table_flag.index('NS')
            #use the index and grab the string
            entry = RS_table[index]
            #encode the NS string and send back to the client with the TS server hostname
            crsd.send(entry.encode('utf-8'))
    #close the server socket and exit
    rssd.close()
    exit()
#call server
rss()
