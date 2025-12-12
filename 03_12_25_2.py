import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9000))
    try:
        while True:
            text = input('Enter a message(or q to quit): ')
            if text.lower == 'q':
                break
            client.send(text.encode())
    except (BrokenPipeError, OSError) as e:
        print(f'Error: {e}')
    finally:
        client.close()



if __name__ == '__main__':
    start_client()
