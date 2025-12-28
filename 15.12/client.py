# =========================
# client.py
# Асинхронный HTTP-клиент на asyncio.
# Требования задания:
#  - постоянно работает в цикле ввода в консоли
#  - вводим адрес страницы (/hello или /world)
#  - после ввода отправляет HTTP-запрос на сервер
#  - получает HTML и открывает его в отдельном окне/вкладке (графически как браузер)
# Важные требования:
#  - открытие окна не блокирует ввод в консоли
#  - можно открыть несколько окон одновременно
# =========================

import asyncio
import os
import tempfile
import webbrowser
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 9000


async def fetch(path: str) -> bytes:
    """
    Делает HTTP GET запрос на сервер и возвращает "сырые" bytes ответа.
    Мы используем asyncio.open_connection (TCP) + вручную формируем HTTP-запрос.
    """
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # В HTTP обязательно \r\n
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    # Отправляем запрос
    writer.write(request.encode("utf-8"))
    await writer.drain()

    # Читаем ответ полностью, пока сервер не закроет соединение (Connection: close)
    response = await reader.read(-1)

    # Закрываем соединение
    writer.close()
    await writer.wait_closed()

    return response


def extract_status_and_body(http_response: bytes) -> tuple[int, bytes]:
    """
    Очень простой парсер HTTP:
      - разделяет заголовки и тело по b"\r\n\r\n"
      - вытаскивает статус код из первой строки заголовков

    Возвращает (status_code, body_bytes).
    """
    header_part, _, body = http_response.partition(b"\r\n\r\n")

    # Первая строка заголовков: HTTP/1.1 200 OK
    first_line = header_part.splitlines()[0].decode("utf-8", errors="replace") if header_part else ""
    try:
        status_code = int(first_line.split()[1])
    except Exception:
        status_code = 0

    return status_code, body


def open_html_in_browser(html_bytes: bytes, title_hint: str = "page") -> None:
    """
    Открывает HTML в браузере:
      - сохраняем во временный уникальный файл (чтобы можно было открыть много окон)
      - открываем file://... через стандартный браузер
    """
    # mkstemp даёт уникальный путь и файловый дескриптор
    fd, path = tempfile.mkstemp(prefix=f"{title_hint}_", suffix=".html")
    os.close(fd)  # закрываем дескриптор, дальше работаем обычным open()

    with open(path, "wb") as f:
        f.write(html_bytes)

    # new=1 обычно открывает новую вкладку/окно (зависит от настроек браузера)
    webbrowser.open(f"file://{path}", new=1)


def normalize_input_to_path(user_input: str) -> str:
    """
    Позволяем пользователю вводить:
      - /hello
      - hello
      - http://127.0.0.1:9000/hello

    Возвращаем нормализованный путь, например "/hello".
    """
    s = user_input.strip()
    if not s:
        return ""

    # Если ввели полный URL
    if s.startswith("http://") or s.startswith("https://"):
        u = urlparse(s)
        return u.path or "/"

    # Если ввели просто "hello", добавим /
    if not s.startswith("/"):
        s = "/" + s

    return s


async def process_request(path: str) -> None:
    """
    Обрабатывает один запрос:
      - fetch(path) -> raw HTTP bytes
      - extract_status_and_body -> (status, body)
      - если 200, открываем HTML в браузере
    Важно: эту корутину мы будем запускать через asyncio.create_task,
           чтобы она шла параллельно вводу в консоли.
    """
    try:
        raw = await fetch(path)
        status, body = extract_status_and_body(raw)

        if status == 200 and body:
            # Открытие браузера может быть блокирующим на некоторых системах.
            # Поэтому вынесем в отдельный поток, чтобы не тормозить event loop.
            title_hint = path.strip("/").replace("/", "_") or "page"
            await asyncio.to_thread(open_html_in_browser, body, title_hint)
            print(f"Opened {path} in browser.")
        else:
            # Если не 200 — покажем текст ошибки в консоли
            text = body.decode("utf-8", errors="replace") if body else "(no body)"
            print(f"Server ответил {status} для {path}: {text}")

    except Exception as e:
        print(f"Client error for {path}: {e}")


async def console_loop() -> None:
    """
    Бесконечный цикл ввода:
      - input() блокирует, поэтому запускаем input в отдельном потоке:
        await asyncio.to_thread(input, "> ")
      - после ввода создаём параллельную задачу process_request(path),
        чтобы ввод продолжался без ожидания ответа и без ожидания открытия браузера
    """
    print("Client started.")
    print("Enter /hello or /world (or 'exit' to quit).")

    while True:
        # input() блокирует поток, но asyncio.to_thread переносит это в другой поток,
        # и event loop продолжает работать (можно параллельно обслуживать запросы)
        user_input = await asyncio.to_thread(input, "> ")
        user_input = user_input.strip()

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Bye.")
            return

        path = normalize_input_to_path(user_input)
        if not path:
            continue

        # Ключевой момент: НЕ await process_request(...)
        # Иначе ввод будет ждать, пока запрос выполнится и браузер откроется.
        #
        # create_task запускает корутину параллельно.
        asyncio.create_task(process_request(path))


async def main() -> None:
    await console_loop()


if __name__ == "__main__":
    asyncio.run(main())
