
import threading
import queue
import time
import random

q = queue.Queue()

def producer():
    for i in range(10):
        nm = random.randint(1, 10)
        print(f'Producer {nm}')
        q.put(nm)
        time.sleep(5)


def consumer(thread_no):
    while True:
        #извлекаем число из очереди
        nm = q.get()
        if nm is None:
            break
        print(f'Consumer {thread_no} received {nm}')
        time.sleep(nm)
        print(f'Consumer {thread_no} finished waiting{nm} seconds')
        q.task_done()


#создаем вторичные потоки
consumers = []
for i in range(3):
    consumer_thread = threading.Thread(target=consumer, args=(i+1,))
    consumers.append(consumer_thread)
    consumer_thread.start()

#запускаем управляющий поток
producer_thread = threading.Thread(target=producer)
producer_thread.start()

#ждем завершение потока производителя
producer_thread.join()

#добавляем None к очереди для завершения потребителей
for some in consumers:
    q.put(None)


#ждем завершение всех потребительских потоков
for consumer_thread in consumers:
    consumer_thread.join()


print('End main')