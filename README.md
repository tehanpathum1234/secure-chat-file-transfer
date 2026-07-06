Secure Chat & File Transfer System

A secure multi-client chat and file transfer application developed in Python using TCP socket programming. This project demonstrates networking concepts while implementing essential cybersecurity features such as secure authentication, password hashing, brute-force protection, and administrative controls.

⸻

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

⸻

📂 Project Structure

Secure-Chat-System/
│
├── server.py          # Server application
├── client.py          # Client application
├── users.json         # User database
├── README.md
└── screenshots/       # Project screenshots (optional)

⸻

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/yourusername/Secure-Chat-System.git

⸻

2. Navigate to the Project

cd Secure-Chat-System

⸻

3. Start the Server

python server.py

⸻

4. Start the Client

Open another terminal and run:

python client.py

Run additional clients to connect multiple users.

⸻

👨‍💻 User Commands

Command	Description
/register	Register a new account
/login	Login to an existing account
/msg <username> <message>	Send a private message
/WHO	View online users

⸻

👮 Admin Commands

Command	Description
/adminlogin	Login as administrator
/announce	Send announcement to all users
/ban	Ban a user
/unban	Unban a user
/kick	Disconnect a user

⸻

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

⸻

📚 Learning Outcomes

Through this project I gained practical experience in:

* TCP Client-Server Communication
* Multi-client Networking
* Socket Programming
* Secure Authentication
* Password Hashing
* Cybersecurity Best Practices
* Python Network Programming
* Access Control
* Secure User Management

⸻

🚧 Future Improvements

The following features are planned for future releases:

* End-to-End Encryption (E2EE)
* AES File Encryption
* TLS/SSL Secure Communication
* GUI Application (Tkinter or PyQt)
* Group Chat
* File Integrity Verification
* Database Integration (SQLite/MySQL)
* Message History
* Secure Session Tokens
* Two-Factor Authentication (2FA)

⸻

📸 Screenshots

You can add screenshots here.

screenshots/
    login.png
    chat.png
    admin.png
    file_transfer.png

Example:

## Login
![Login](screenshots/login.png)
## Chat
![Chat](screenshots/chat.png)

⸻

🤝 Contributions

Contributions, suggestions, and feedback are welcome. Feel free to fork this repository and submit a pull request.

⸻

📄 License

This project is licensed under the MIT License.

⸻

👤 Author

Pathum Tehan

* 🎓 Undergraduate Student
* 💻 Interested in Cybersecurity, Networking, and Python Development

⸻

⭐ If you found this project helpful or interesting, consider giving it a Star on GitHub!
