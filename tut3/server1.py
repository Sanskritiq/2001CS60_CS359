import socket as sk
import errno
import sys

def server1(host_ip, port):
    try: 
        server1_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        print("Socket created")
    except sk.error as err:
        print("Socket creation failed with error: ", str(err))
        sys.exit()


    try:
        server1_socket.bind((host_ip, port))
        print("Socket binded with ip:", str(host_ip), "port:", str(port))
    except sk.error as err:
        if err.errno == errno.EADDRINUSE:
            print("Port already in use")
            sys.exit()
        else:
            print("Socket binding failed with error: ", str(err))
            sys.exit()

    server1_socket.listen(1)
    print("Socket is listening")

    (conn, (address, port_conn)) = server1_socket.accept()
    print("connection from:", str(address), "port:", str(port_conn)) 

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        
        print("recieved over the connection:", str(data))
        msg = "try again"
        
        try:
            msg = eval(str(data))
        except SyntaxError as err:
            msg="Invalid syntax"
        except NameError as err:
            msg="Please write an expression"
        except ZeroDivisionError as err:
            msg = str(err)

        conn.send(str(msg).encode())
        
    conn.close()

host_ip = input("Enter host IP: ")
# host_ip = sk.gethostname()
port = int(input("Enter port: "))

server1(host_ip, port)