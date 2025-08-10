# Silent Chat — Custom Binary Protocol Chat App

A simple 1-to-1 local chat application built in Python using a **custom binary protocol** over TCP sockets.

A mini internet chat system built from scratch using Python. This project demonstrates how machines communicate at a low level using custom binary protocols over raw TCP sockets. It features a simple packet structure, concurrency with threading for simultaneous send/receive, and clean connection handling.
You’ll gain hands-on experience with raw byte communication, protocol design, socket programming, and basic multithreading  foundational concepts in computer networking and software engineering.
---

## Features

- Custom binary packet design with start byte, command, length, data, and checksum
- Clean message parsing and building in `utils.py`
- Text chat with usernames
- Graceful connection close with `BYE` command to prevent socket errors
- Works on localhost or LAN
- Designed for learning how low-level machine communication protocols work

---

## How to Run

1. Create and activate your Python virtual environment  
2. Run `server.py` in one terminal and enter a username  
3. Run `client.py` in another terminal and enter a username  
4. Chat by typing messages, and type `bye` to end the chat gracefully

---

## Planned Features (Coming Soon)

- Add support for sending **files** and **custom emojis**  
- Embed **timestamps** and **message IDs** inside protocol packets  
- Build a **simple GUI** to improve chat experience  
- Support multiple clients and group chat  

---

## Technologies Used

- Python 3  
- TCP sockets  
- Multi-threading  
- Custom binary protocols

---

## How to Contribute

Feel free to open issues or pull requests. I welcome improvements, bug fixes, and feature additions!

---

## License

MIT License
