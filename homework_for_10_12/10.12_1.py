import asyncio
import os


HTML_FILENAME = '10.12.html'
async def handle_client(reader:asyncio.StreamReader,writer:asyncio.StreamWriter):
    try:
        data = await reader.read(1024)
        message = data.decode()
        request_line = message.splitlines()[0]
        method, path, _ = request_line.split()

        if path =='/page1':
            if os.path.isfile(HTML_FILENAME):
                with open(HTML_FILENAME,'r', encoding='utf-8') as f:
                    html_content = f.read()
                response= (
                'HTTP/1.1 200 OK\n'
                'Content-Type: text/html; charset=utf-8\r\n'
                f'Content-Length: {len(html_content.encode('utf-8'))}\r\n'
                '\r\n'
                f'{html_content}'
                )
            else:
                response = (
                'HTTP/1.1 500 Internal Server Error\r\n'
                'Content-Type: text/plain\r\n'
                '\r\n'
                'HTML file not found'
                 )
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "Page not found"
            )
        writer.write(response.encode('utf-8'))
        await writer.drain()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        writer.close()
        await writer.wait_closed()





async def main():
    server = await asyncio.start_server(handle_client, host='127.0.0.1',port=9000)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
