import socket as sk
import errno
import sys

def client(host_ip, port):
    try: 
        client_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        print("Socket created")
    except sk.error as err:
        print("Socket creation failed with error: ", str(err))
    
    client_socket.connect((host_ip, port))  
      
    msg = input("Want to continue?(y/n) ")  
    msg = msg.lower()
    
    if msg=="y" :
        msg = input("-> ")
        
    elif not (msg=="y" or msg=="n")() :
        while not (msg=="y" or msg=="n"):
            print("Kindly only enter y/n")
            msg = input("Want to continue?(y/n) ")  
            msg = msg.lower()
            if msg=="y" :
                msg = input("-> ")
                break

    while msg!="n":
        
        client_socket.send(msg.encode())
        
        data = client_socket.recv(1024).decode()
        
        print("Recieved over the connection:", str(data))
        msg = input("Want to continue?(y/n) ")  
        msg = msg.lower()
        
        if msg=="y" :
            msg = input("-> ")
            
        elif not (msg=="y" or msg=="n") :
            while not (msg=="y" or msg=="n") :
                print("Kindly only enter y/n")
                msg = input("Want to continue?(y/n) ")  
                msg = msg.lower()
                if msg=="y" :
                    msg = input("-> ")
                    break
                
        
    client_socket.close()

host_ip = input("Enter host IP: ")
# host_ip = sk.gethostname()
port = int(input("Enter port: "))

client(host_ip, port)