import socket, select


HOST = '0.0.0.0'
PORT = 9090


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

inputs = [server]
clients = {}
names = {}

print('Chat server on', PORT)

try :

 while True :
  readable,_,_ = select.select(inputs, [], [])
  for s in readable :
   if s is server :
    conn, addr = server.accept()
    inputs.append(conn)
    clients[conn] = addr
    names[conn] = None
    print('New', addr)

   else :
    data = s.recv(1024)

    try :
     text = data.decode().strip()
     is_text = True
    except UnicodeDecodeError : 
     is_text = False
     text = None

    if names[s] is None :
     if text.startswith('NAME:') :
      uname = text[len('NAME:'):].strip()
      names[s] = uname if uname else f"User{clients[s][1]}"
     else :
      names[s] = f"User{clients[s][1]}"
     print(f'{names[s]} registered from {clients[s]}')
     s.sendall(f"Welcome, {names[s]}!".encode())
     continue

    if not data :
     uname = names.get(s, clients.get(s))
     print('Client disconnect', uname);
     inputs.remove(s)
     del clients[s]
     del names[s]
     s.close()
     continue

    if is_text and text.startswith('FILE:') :
     for c in clients : 
      if c is not s :
       try : c.sendall(f'{names[s]} is sending a file : {text} '.encode())
       except : pass
     continue

    for c in clients :
     if c is not s :
      try : c.sendall(data)
      except : pass

except KeyboardInterrupt : 
 print('Server shutting down')
finally :
 server.close()
