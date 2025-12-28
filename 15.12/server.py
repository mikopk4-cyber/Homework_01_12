import asyncio
import os

HOST = '127.0.0.1'
PORT = 9000

ROUTERS = {
    '/hello':'html',
    '/world' :'html',
}

def http_response(status_line: str, body:bytes, content_type: str = 'text/html; charset=utf-8') -> bytes:
    headers = [
        status_line,
        f'Content-Type: {content_type}',
        f'Content-Length: {len(body)}',
        f'Connection: closed',
        '\r\n',
    ]
    return ('\r\n'.join(headers)).encode('utf-8') + body

async def handle_client(reader:asyncio.StreamReader, writer:asyncio.StreamWriter)-> None:
    try:
        data = await reader.read(4096)

        #если клиент подключился и сразу отключился
        if not data:
            writer.close()
            await writer.wait_closed()
            return
        #декодируем запрос в текст (если вдруг мусор - не упадем)
        request_text = data.decode('utf-8', 'replace')

        lines = request_text.splitlines()
        if not lines:
            body = 'Bad request'.encode('utf-8')
            resp = http_response('HTTP/1.1 404 Bad request', body, 'text/plain; charset=utf-8')
            writer.write(resp)
            await writer.drain()
            return
        request_line = lines[0]
        parts = request_line.split()

        #ожидаем минимум 2 части: METHOD and PATH
        # (обычно 3 METHOD PATH HTTP/VERSION)
        if len(parts) < 2:
            body = 'Bad request'.encode('utf-8')
            resp = http_response('HTTP/1.1 404 Bad request', body, 'text/plain; charset=utf-8')
            writer.write(resp)
            await writer.drain()
            return
        method = parts[0].upper()
        path = parts[1]
        #если пользователь введет /hello нам нужен только путь без query string
        path = path.split('?', 1)[0]
        #проверяем есть ли такой маршрут
        if path in ROUTERS:
            filename = ROUTERS[path]

            #проверяемб есть ли файл в папке
            if os.path.isfile(filename):
                #читаем файл как bytes, чтобы Content Legth был точным
                with open(filename, 'rb') as f:
                    body = f.read()
                resp = http_response(
                    'HTTP/1.1 200 OK',
                    body,
                    'text/html; charset=utf-8',
                )

            else:
                #маршрут есть, но файла нет => ошибка сервера (неправильная конфигурация)
                body ='HTTP file not found'.encode('utf-8')
                resp = http_response(
                    'HTTP/1.1 500 Internal Server Error',
                    body,
                    'text/plain; charset=utf-8',
                )
        else:
            body = 'Page not found'.encode('utf-8')
            resp = http_response(
                'HTTP/1.1 404 Not Found',
                body,
                'text/plain; charset=utf-8',
            )
        #отправляем отет клиенту
        writer.write(resp)
        await writer.drain()
    except Exception as e:
        print(f'Server Error: {e}')
    finally:
        #закрываем соединение
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Serving on http://{addr[0]}:{addr[1]}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())




