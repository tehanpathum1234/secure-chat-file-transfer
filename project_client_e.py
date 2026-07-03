import socket, threading, argparse, sys, os

def recv_loop(sock) :
 while True :
  data = sock.recv(4096)
  if not data: break
  try :
   text = data.decode()
  except UnicodeError :
   continue

  if text.startswith('FILE:') :
   _, fname, fsize = text.split(':', 2)
   fsize = int(fsize)
   filedata = b''
   while len(filedata) < fsize :
    chunk = sock.recv(min(4096, fsize - len(filedata)))
    if not chunk : break
    filedata += chunk
   save_name = 'received_' + os.path.basename(fname)
   with open(save_name, 'wb') as f:
    f.write(filedata)
   print(f'\n< File saved as {save_name}\n> ', end = '', flush = True)
  else :
   print('\n<', data.decode(), '\n>', end = '', flush = True)

def send_file(sock, filepath) :
 if not os.path.isfile(filepath) :
  print(f'File not found: {filepath}')
  return
 filename = os.path.basename(filepath)
 with open(filepath, 'rb') as f :
  filedata = f.read()
 header = f'FILE:{filename}:{len(filedata)}'
 sock.sendall(header.encode())
 sock.sendall(filedata)
 print(f'Sent file : {filename} ({len(filedata)} bytes)')

if __name__ == '__main__' :
 parser = argparse.ArgumentParser()
 parser.add_argument('--host', default = '127.0.0.1')
 parser.add_argument('--port', type=int, default = 9090)
 args = parser.parse_args()
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.connect((args.host, args.port))
 username = input('Enter user name : ')
 s.sendall(f"NAME: {username}".encode())
 t = threading.Thread(target = recv_loop, args = (s,), daemon = True)
 t.start()

 try :
  while True :
   msg = input('> ')
   if not msg : break
   if msg.startswith('/sendfile') :
    filepath = msg[len('/sendfile'):].strip()
    send_file(s, filepath)
   else :
    s.sendall(msg.encode())
 except KeyboardInterrupt :
  pass
 finally :
  s.close()
