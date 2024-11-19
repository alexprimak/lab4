import socket
import ssl

# Налаштування SSL
server_cert = "server.crt"

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_verify_locations(cafile=server_cert)

# Підключення до сервера
server_address = ('localhost', 12345)
sock = socket.create_connection(server_address)
ssl_socket = context.wrap_socket(sock, server_hostname='localhost')
a
print("З'єднано з сервером.")

try:
    while True:
        message = input("Введіть повідомлення: ")
        if not message:
            break
        ssl_socket.sendall(message.encode())
        response = ssl_socket.recv(1024)
        print(f"Сервер відповів: {response.decode()}")
finally:
    ssl_socket.close()
