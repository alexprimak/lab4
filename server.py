import socket
import ssl

# Налаштування SSL
server_cert = "server.crt"
server_key = "server.key"
client_cert = "client.crt"

# Створення контексту SSL
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_cert)
context.verify_mode = ssl.CERT_NONE  # Не вимагаємо клієнтський сертифікат

# Налаштування сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

print("Сервер очікує з'єднання...")

# Приймаємо клієнтів
while True:
    client_socket, addr = server_socket.accept()
    print(f"Підключено клієнта: {addr}")
    try:
        # Обгортка сокету в SSL
        ssl_client_socket = context.wrap_socket(client_socket, server_side=True)
        print("Захищене з'єднання встановлено.")
        
        while True:
            data = ssl_client_socket.recv(1024)
            if not data:
                print("З'єднання закрито клієнтом.")
                break
            print(f"Отримано: {data.decode()}")
            ssl_client_socket.sendall(b"Server received: " + data)
    except ssl.SSLError as e:
        print(f"SSL помилка: {e}")
    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        # Перевіряємо, чи існує ssl_client_socket перед закриттям
        if 'ssl_client_socket' in locals():
            ssl_client_socket.close()
        print("З'єднання закрито.")
