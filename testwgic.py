import socket

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.bind(('', 8001))
so.listen(1)
while True:
    conn, addr = so.accept()
    print("recv from ", addr)
    msg = b''
    while True:
        buff = conn.recv(1024)
        if not buff: break
        if len(buff) < 1024:
            msg += buff
            break

        msg += buff

    print(msg)
    conn.send(b"hello")
    conn.close()
