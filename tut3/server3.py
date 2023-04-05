import socket as sk
import errno
import sys
import select
import queue

def server3(host_ip, port):

    try: 
        server3_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        print("Socket created")
    except sk.error as err:
        print("Socket creation failed with error: ", str(err))
        sys.exit()
    server3_socket.setblocking(0)
    
    try:
        server3_socket.bind((host_ip, port))
        print("Socket binded with ip:", str(host_ip), "port:", str(port))
    except sk.error as err:
        if err.errno == errno.EADDRINUSE:
            print("Port already in use")
            sys.exit()
        else:
            print("Socket binding failed with error: ", str(err))
            sys.exit()
            
    server3_socket.listen(5)
    print("Socket is listening")
    
    inputs = [server3_socket]
    outputs = []
    msg_q = {}

    while inputs:
        
        (readable, writable, exceptional) = select.select(inputs, outputs, inputs)
        
        for server in readable:
            
            if server is server3_socket:
                (conn, (address, port_conn)) = server.accept()
                print("connection from:", str(address), "port:", str(port_conn)) 
                conn.setblocking(0)
                
                inputs.append(conn)
                msg_q[conn] = queue.Queue()
                
            else:
                msg = "try again"
                data = server.recv(1024).decode()
                
                if data:
                    print("recieved over the connection:", str(data))
                    try:
                        msg = eval(str(data))
                    except SyntaxError as err:
                        msg="Invalid syntax"
                    except NameError as err:
                        msg="Please write an expression"
                    except ZeroDivisionError as err:
                        msg="Do not divide with 0"
                    msg_q[server].put(msg)
                    
                    if server not in outputs:
                        outputs.append(server)
                        
                else:
                    if server in outputs:
                        outputs.remove(server)
                    inputs.remove(server)
                    server.close()
                    del msg_q[server]

        for server in writable:
            try:
                next_msg = msg_q[server].get_nowait()
            except queue.Empty:
                outputs.remove(server)
            else:
                server.send(str(next_msg).encode())

        for server in exceptional:
            inputs.remove(server)
            if server in outputs:
                outputs.remove(server)
            server.close()
            del msg_q[server]
        
        
host_ip = input("Enter host IP: ")
# host_ip = sk.gethostname()
port = int(input("Enter port: "))

server3(host_ip, port)