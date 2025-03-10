import socket

HOST = "100.72.143.10" # IP address of your Raspberry PI
PORT = 65432          # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        text = input("Enter your message: ") # Note change to the old (Python 2) raw_input
        if text == "quit":
            break
        s.send(text.encode())     # send the encoded message (send in binary format)
        print("data sent")
        data = s.recv(1024)
        print("from server: ", data)