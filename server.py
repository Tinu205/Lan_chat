import socket
import threading

host = socket.gethostbyname(socket.gethostname())
#port = 0                               
port = 55555                              # hve kept this for testing purposes, gotta keep it at 0 for implementation

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server_address = server.getsockname()
print(f'Server is Running on {server_address[0]}:{server_address[1]}')
server.listen()

clients = []
aliases = []

'''
def handle_msg(message,sender=None):
    #handle the messages that are empty characters

    while message != "":
        sender.send('Please enter some characters!!\n'.encode('utf-8'))
        message=sender.recv(1024).decode('utf-8')
    
    return message
'''

#handles sending messages to the clients
def broadcast(message, sender=None):
    
    '''we need to handle the handle the exception of 
    the client leaving the chatroom and hence the error'''
    for client in clients:
        if client != sender:
            client.send(message)



def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message,sender=client)
        except:
            index = clients.index(client)
            clients.remove(client)

            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat !'.encode('utf-8'))
            aliases.remove(alias)
            break


def receive():
    while True:
        print("Server is Listening ......")
        client, address = server.accept()
        print(f"Connection established {address[0]}:{address[1]}")
        
        client.send('alias?'.encode('utf-8'))
        #alias = handle_msg(client.recv(1024).decode('utf-8'),client)
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)

        broadcast(f'{alias} has entered the chatroom ......'.encode('utf-8'))

        clients.append(client)
        print(f'alias : {alias}')
        print('------------------------------------------------------------')
        
        client.send("You are now connected!".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()