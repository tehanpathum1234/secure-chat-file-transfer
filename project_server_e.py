import socket, select, json, os, hashlib, secrets, time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9090
DB_FILE = 'user.json'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

inputs = [server]
clients = {}
names = {}

if os.path.isfile(DB_FILE) :
 with open(DB_FILE, 'r') as f :
  user_db = json.load(f)
 print(f'Loaded {len(user_db)} existing account from {DB_FILE}')
else :
 user_db = {}
 print('No existing account database found, starting fresh.')

def save_db() :
 with open(DB_FILE, 'w') as f :
  json.dump(user_db, f, indent = 2)

def hash_password(password, salt) :
 return hashlib.sha256((salt + password).encode()).hexdigest()

def timestamp():
 return datetime.now().strftime('%H:%M:%S')

MAX_ATTEMPTS = 5

attempt_count = {}
blocked_ips = set()

RATE_LIMIT_SECONDS = 2
last_attempt_time = {}

ADMIN_USERS = {'admin'}
banned_users = set()
banned_ip_by_user = {}

admin_sessions = set()
ADMIN_SALT = 'f2a37b75b3761f5d'
ADMIN_PASSWORD_HASH = '6a210bbc45398a5eb41abc1456bda31aead33ab5c1b2261ddd4558a295044696'


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
    print(f'[{timestamp()}] New', addr)

   else :
    data = s.recv(1024)

    if not data :
     uname = names.get(s, clients.get(s))
     print(f'[{timestamp()}] Client disconnect', uname);
     inputs.remove(s)
     del clients[s]
     del names[s]
     admin_sessions.discard(s)
     s.close()
     continue

    try :
     text = data.decode().strip()
     is_text = True
    except UnicodeDecodeError : 
     is_text = False
     text = None

    if names[s] is None :
     ip = clients[s][0]

     if ip in blocked_ips :
      s.sendall(b'ERROR: too many failed attempts, you are blocked')
      inputs.remove(s)
      del clients[s]
      del names[s]
      s.close()
      continue

     if ip in last_attempt_time :
      time_since_last = time.time() - last_attempt_time[ip]
      if time_since_last < RATE_LIMIT_SECONDS :
       s.sendall(b'ERROR: slow down, wait a moment before trying again')
       continue
     last_attempt_time[ip] = time.time()

     if not text.startswith('AUTH:') :
      s.sendall(b'ERROR: send AUTH:username:password first')
      continue
     try :
      _, uname, pwd = text.split(':', 2)
     except ValueError :
      s.sendall(b'ERROR: bad AUTH format')
      continue

     if uname in banned_users :
      s.sendall(b'ERROR: this account has been banned')
      inputs.remove(s)
      del clients[s]
      del names[s]
      s.close()
      continue

     if uname in user_db :
      stored = user_db[uname]
      test_hash = hash_password( pwd, stored['salt'] )
      if test_hash == stored['hash_password'] :
       names[s] = uname
       attempt_count[ip] = 0
       print(f'[{timestamp()}] {uname} logged in from {clients[s]}')
       s.sendall(f"[{timestamp()}] Welcome back, {uname}!".encode())
      else :
       print(f"[{timestamp()}] Failed login attempt for {uname} from {clients[s]}")

       if ip not in attempt_count :
        attempt_count[ip] = 0
       attempt_count[ip] = attempt_count[ip] + 1

       if attempt_count[ip] >= MAX_ATTEMPTS :
        blocked_ips.add(ip)
        print(f'[{timestamp()}] IP {ip} blocked after {MAX_ATTEMPTS} failed logins')

       s.sendall(b'ERROR: wrong password !')
       s.sendall("  Try again".encode())
       continue

     else :
      salt = secrets.token_hex(8)
      user_db[uname] = {
             'salt' : salt,
             'hash_password' : hash_password(pwd, salt)
             }
      save_db()
      names[s] = uname
      print(f'[{timestamp()}] {names[s]} registered from {clients[s]}')
      s.sendall(f"[{timestamp()}] Welcome, {names[s]}!".encode())
     continue

    if is_text and text.startswith('file:') :
     for c in clients : 
      if c is not s :
       try : c.sendall(f'[{timestamp()}] {names[s]} is sending a file : {text} '.encode())
       except : pass
     continue

    if text == '/WHO' :
     online = ', '.join(n for n in names.values() if n)
     s.sendall(f"Online: {online}".encode())
     continue

    if text.startswith('/msg') :
     parts = text.split(' ', 2)
     if len(parts) < 3 :
      s.sendall(b'ERROR: usage /msg <username> <message> ')
      continue
     _, target, pm = parts

     target_conn = None
     for c, n in names.items() :
      if n == target :
       target_conn = c
       break

     if target_conn is None :
      s.sendall(f'ERROR: {target} is not online'.encode())

     elif target_conn is s :
      s.sendall(b'ERROR: cannot message yourself')

     else :
      try :
       target_conn.sendall(f'[{timestamp()}] (private) {names[s]}: {pm}'.encode())
       s.sendall(f'[{timestamp()}] (private to {target}) {pm}'.encode())
      except :
       s.sendall(f'ERROR: could not deliver message to {target}'.encode())
     continue

    if text.startswith('/adminlogin') :
     parts = text.split(' ', 1)
     if len(parts) < 2 :
      s.sendall(b'ERROR: usage /adminlogin <password>')
      continue
     supplied_pwd = parts[1]

     if names[s] not in ADMIN_USERS : 
      s.sendall(b'ERROR: this account is not an admin account')
      continue

     if hash_password(supplied_pwd, ADMIN_SALT) == ADMIN_PASSWORD_HASH :
      admin_sessions.add(s)
      print(f'[{timestamp()}] {names[s]} elevated to admin session')
      s.sendall(b'Admin session unlocked')
     else :
      s.sendall(b'ERROR: wrong admin password')
     continue

    if text.startswith('/kick') or text.startswith('/ban') or text.startswith('/unban') or text.startswith('/announce') : 

     if s not in admin_sessions :
      s.sendall(b'ERROR: admin only command, run /adminlogin <password> first')
      continue

     if text.startswith('/announce') :
      announcement = text[len('/announce'):]
      for c in clients :
       try : c.sendall(f'[{timestamp()}] *** ANNOUNCEMENT from {names[s]} *** {announcement}'.encode())
       except : pass
      continue

     if text.startswith('/unban') :
      target = text[len('/unban'):].strip()
      banned_users.discard(target)
      if target in banned_ip_by_user :
       blocked_ips.discard(banned_ip_by_user[target])
       del banned_ip_by_user[target]
      s.sendall(f'{target} has been unbanned'.encode())
      continue

     is_ban = text.startswith('/ban')
     target = text[len('/ban'):].strip() if is_ban else text[len('/kick'):].strip()

     target_conn = None
     for c, n in names.items() :
      if n == target :
       target_conn = c
       break

     if target_conn is None :
      s.sendall(f'ERROR: {target} is not online'.encode())
      continue

     if target_conn is s :
      s.sendall(b'ERROR: cannot kick/ban yourself')
      continue

     if is_ban :
      banned_users.add(target)
      banned_ip = clients[target_conn][0]
      blocked_ips.add(banned_ip)
      banned_ip_by_user[target] = banned_ip

     action = 'banned' if is_ban else 'kicked'
     try : target_conn.sendall(f'[{timestamp()}] you have been {action} by {names[s]}'.encode())
     except : pass

     print(f'[{timestamp()}] {names[s]} {action} {target} ')
     inputs.remove(target_conn)
     del clients[target_conn]
     del names[target_conn]
     admin_sessions.discard(target_conn)
     try : target_conn.close()
     except : pass

     s.sendall(f'{target} has been {action}'.encode())
     continue

    msg = f"[{timestamp()}] {names[s]}: {text}".encode()
    for c in clients :
     if c is not s :
      try : c.sendall(msg)
      except : pass

except KeyboardInterrupt : 
 print(f'[{timestamp()}] Server shutting down')
finally :
 server.close()
