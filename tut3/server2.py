import socket as sk
import errno
import sys
from _thread import *
import threading
# from SocketServer import ThreadingMixIn

class conn_thread(threading.Thread): 
 
    def __init__(self, address, port_conn, conn): 
        threading.Thread.__init__(self) 
        self.address = address 
        self.port_conn = port_conn 
        self.conn = conn
        print("connection from:", str(address), "port:", str(port_conn)) 
 
    def run(self): 
        while True:
            data = self.conn.recv(1024).decode()
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

            self.conn.send(str(msg).encode())
            

def server2(host_ip, port):
    
    try: 
        server2_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        print("Socket created")
    except sk.error as err:
        print("Socket creation failed with error: ", str(err))
        sys.exit()


    try:
        server2_socket.bind((host_ip, port))
        print("Socket binded with ip:", str(host_ip), "port:", str(port))
    except sk.error as err:
        if err.errno == errno.EADDRINUSE:
            print("Port already in use")
            sys.exit()
        else:
            print("Socket binding failed with error: ", str(err))
            sys.exit()
            
    threads = []
    while True:
        server2_socket.listen(5)
        print("Socket is listening")
        
        (conn, (address, port_conn)) = server2_socket.accept()
        
        print("connection from:", str(address), "port:", str(port_conn)) 
        
        # start_new_thread(thread_conn, (conn, ))
        newthread = conn_thread(address, port_conn, conn) 
        newthread.start() 
        threads.append(newthread)
        
    # server2_socket.close()
    for thread in threads:
        thread.join()

host_ip = input("Enter host IP: ")
# host_ip = sk.gethostname()
port = int(input("Enter port: "))

server2(host_ip, port)