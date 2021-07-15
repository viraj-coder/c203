import socket
from threading import Thread
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip_address="127.0.0.1"
port=8000
server.bind((ip_address,port))
server.listen()
clients=[]
nicknames=[]
print("server is running")

def clientThread(conn,nickname):
  conn.send("welcome to this chatroom".encode("utf-8"))
  while True:
    try:
      message=conn.recv(2048).decode("utf-8")
      if message:
        #print("<"+addr[0]+">"+message)
        #message_to_send="<"+addr[0]+">"+message
        #broadcast(message_to_send,conn)
        print(message)
        broadcast(message,conn)

      else:
        remove(conn)
        removenickname(nickname)
    except:

      continue

def broadcast(message,conn):
  for client in clients:
    if client!=conn:
      try:
        client.send(message.encode("utf-8"))
      
      except:
        remove(client)

def remove(conn):
  if conn in clients:
    clients.remove(conn)

def removenickname(nickname):
  if nickname in nicknames:
    nicknames.remove(nickname)


while True:
  conn,addr=server.accept()
  conn.send("nickname".encode("utf-8"))
  nickname=conn.recv(2048).decode("utf-8")
  clients.append(conn)
  nicknames.append(nickname)
  message="{} joined!".format(nickname)
  print(message)
  broadcast(message,conn)


  new_thread=Thread(target=clientThread,args=(conn,nickname))
  new_thread.start()