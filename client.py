import socket as mysoc
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
    ctors.connect(server_binding)#First Connect to RS server
    #filename = raw_input('Enter filename (Ex. PROJI-HNS.txt) :\n')
    hostnames_arr = []
    with open('HW1Out.txt', 'w') as output_file:
        with open('PROJI-HNS.txt', 'r') as input_file:
            for line in input_file:
                hostnames_arr.append(line)
        length = len(hostnames_arr)
        while True:
            for i in range(length):
                hostname = hostnames_arr[i]
                ctors.send(hostname.encode('utf-8'))
                dr=ctors.recv(1024).decode('utf-8')
                data = dr.split()
                if data[2] == 'A':
                    output_file.write(data.strip() + '\n')
                elif data[2] == 'NS':
                    TSname = data [0]
                    server_binding=(TSname, 50008)
                    ctots.connect(server_binding)
                    ctots.send(hostname.encode('utf-8'))
                    dr2 = ctots.recv(1024).decode('utf-8')
                    data2 = dr.split()
                    if data2[2] == 'A': 
                        output_file.write(data2.strip() + '\n')
                    else:
                        print('Hostname - Error:HOST NOT FOUND')
        ctors.close()
        ctots.close()
        exit()
client()
