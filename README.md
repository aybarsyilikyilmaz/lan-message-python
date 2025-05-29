# LAN Message Python

A simple local area network (LAN) messaging application written in Python. This project was originally developed as a school assignment and is now open-sourced for educational and practical use.

## Features
- Peer discovery on the local network
- Secure and unsecure chat options
- Message history logging
- User status control
- Multi-threaded for responsive operation

## Requirements
- Python 3.7+
- `pyDes` library (for secure messaging)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/lan-message-python.git
   cd lan-message-python
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install pyDes
   ```

## Usage
Run the main program:
```bash
python main.py
```

Follow the on-screen instructions to:
- List users on the network
- View message history
- Start a chat (secure or unsecure)
- Exit the program

## File Descriptions
- `main.py` — Entry point, manages threads and program flow
- `service_announcement.py` — Announces service on the network
- `peer_discovery.py` — Discovers peers on the LAN
- `chat_initiator.py` — Handles user input and chat initiation
- `user_initiator.py` — Manages user setup
- `chat_responder.py` — Responds to incoming chat requests
- `tcp_sender.py` — Sends messages (secure/unsecure)
- `key_initializer.py` — Handles key exchange for secure messaging
- `chat_history.py` — Manages message history
- `list_users.py` — Lists users and their statuses
- `control_status.py` — Controls and displays user status

## License
This project is open source. Please add your preferred license here. 