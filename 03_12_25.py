import threading
import socket

def handle_socket(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:  # если данных нет то закрываем соединение
                break
            print(f'Received {data.decode()}')
        except ConnectionResetError:
            # оброботка ошибки если клиент неожиданно отключился
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9000))
    server.listen()
    print('Listening on port 9000')
    try:
        while True:
            client_socket, client_address = server.accept()
            print(f'Accepted {client_address}')

            client_thread = threading.Thread(target=handle_socket, args=(client_socket,))
            client_thread.start()
    finally:
        server.close()

if __name__ == '__main__':
    start_server()



