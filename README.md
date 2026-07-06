📌 Overview

The Secure Chat & File Transfer System allows multiple users to communicate in real time and transfer files over a TCP connection. The system also includes several security mechanisms to protect user accounts and improve overall application security.

This project was developed to strengthen practical knowledge in:

* Python Programming
* Socket Programming
* Computer Networks
* Client-Server Architecture
* Cybersecurity Fundamentals

⸻

✨ Features

🔐 Security Features

* User Registration
* Secure User Login
* Password Hashing using SHA-256
* Random Salt Generation
* Secure Password Storage
* Login Rate Limiting
* Brute-Force Attack Protection
* Automatic IP Blocking after multiple failed login attempts
* Admin Authentication
* User Ban & Unban
* User Kick Management
* Timestamped Server Logs

⸻

💬 Chat Features

* Multi-client chat
* Real-time messaging
* Private messaging
* Online user list
* Server announcements
* Broadcast messaging

⸻

📁 File Transfer

* File transfer between clients
* File transfer notifications

⸻

💾 Data Storage

* JSON-based user database
* Persistent user accounts

⸻

🛠️ Technologies Used

* Python 3
* TCP Socket Programming
* Select Module
* JSON
* Hashlib
* Secrets
* OS Module

  Secure-Chat-System/
│
├── server.py          # Server application
├── client.py          # Client application
├── users.json         # User database
├── README.md
└── screenshots/       # Project screenshots (optional)

👨‍💻 User Commands
Command

Description
/register

Register a new account

/login

Login to an existing account

/msg <username> <message>

Send a private message

/WHO

View online users

👮 Admin Commands
Command

Description
/adminlogin

Login as administrator

/announce

Send announcement to all users

/ban

Ban a user

/unban

Unban a user

/kick

Disconnect a user

🔒 Security Mechanisms

This project implements several security mechanisms including:

* SHA-256 password hashing
* Random salt generation
* Secure password verification
* Login rate limiting
* Brute-force attack protection
* Automatic IP blocking
* Administrative access control
* User management
* Activity logging
