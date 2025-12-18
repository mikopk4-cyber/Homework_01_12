import socket      # Модуль socket позволяет работать с сетевыми соединениями
import json

# Адрес и порт, на котором будет работать сервер
HOST = "localhost"
PORT = 9000

# Создаем TCP-сокет (AF_INET — IPv4, SOCK_STREAM — TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
# Теперь сервер "слушает" localhost:9000
server_socket.bind((HOST, PORT))

# Переводим сокет в режим ожидания подключений
# 5 — максимальное количество клиентов в очереди
server_socket.listen(5)

print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

# Вечный цикл — сервер работает постоянно и не завершается
while True:

    # accept() — блокирующий вызов
    # Сервер останавливается здесь и ждет подключения клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключился клиент: {client_address}")

    # Получаем данные от клиента (HTTP-запрос)
    # 1024 байта достаточно для учебного примера
    request = client_socket.recv(1024).decode("utf-8")

    # Если запрос пустой — закрываем соединение
    if not request:
        client_socket.close()
        continue

    # HTTP-запрос состоит из:
    # header \r\n\r\n body
    # Разделяем заголовки и тело запроса
    header, body = request.split("\r\n\r\n", 1)

    print("HEADER:\n", header)
    print("BODY:\n", body)

    # -------------------------------------------------
    # Обработка GET-запроса
    # -------------------------------------------------
    if header.startswith("GET"):
        # Формируем HTTP-ответ вручную
        # 200 OK — успешный статус
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Content-Length: 2\r\n"
            "\r\n"
            "OK"
        )

        # Отправляем ответ клиенту
        client_socket.send(response.encode())

    # Обработка POST-запроса
    elif header.startswith("POST"):
        try:
            # Пытаемся преобразовать тело запроса в JSON
            # Ожидается формат: [2, 3]
            data = json.loads(body)

            # Распаковываем числа из списка
            a, b = data

            # Проверяем деление на ноль
            if b == 0:
                # Формируем тело ответа с описанием ошибки
                response_body = json.dumps({
                    "error": "Internal server error: division by zero"
                })

                # Формируем HTTP-ответ со статусом 500
                response = (
                    "HTTP/1.1 500 Internal Server Error\r\n"
                    "Content-Type: application/json\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "\r\n"
                    f"{response_body}"
                )

            else:
                # Если деление возможно — выполняем операцию
                result = a / b

                # Преобразуем результат в JSON
                response_body = json.dumps(result)

                # Формируем успешный HTTP-ответ
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "\r\n"
                    f"{response_body}"
                )

        except json.JSONDecodeError:
            # Если тело запроса не удалось преобразовать в JSON
            response_body = json.dumps({
                "error": "Invalid JSON format"
            })

            # Формируем HTTP-ответ со статусом 400
            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )

        # Отправляем сформированный ответ клиенту
        client_socket.send(response.encode())

    # Закрываем соединение с клиентом
    client_socket.close()






