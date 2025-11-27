import queue
import threading


q1 = queue.Queue()
q2 = queue.Queue()
q3 = queue.Queue()

def worker1(queue, thread_no):
    while True:
        #извлекаем сообшение из очереди
        message = queue.get()
        # Проверка, получено ли специальное сообшение для завершения потока
        if message is None:
            break #выходим из цикла если вывело None

        print(f'Thread {thread_no} : {message}')
        #указываем очереди что задача выполнина
        queue.task_done()



def control():
    while True:
        thread_no = int(input('Enter the number from 1-3\n'))
        if thread_no == 0:
            q1.put(None)
            q2.put(None)
            q3.put(None)
            break
        message = input('Enter the message: \n')
        if thread_no == 1:
            q1.put({'n': thread_no, 't': message})
        elif thread_no == 2:
            q2.put({'n': thread_no, 't': message})
        elif thread_no == 3:
            q3.put({'n': thread_no, 't': message})
        else:
            print('Invalid input')


t1 = threading.Thread(target=worker1, args=(q1, 1))
t2 = threading.Thread(target=worker1, args=(q2, 2))
t3 = threading.Thread(target=worker1, args=(q3, 3))

t1.start()
t2.start()
t3.start()

#Создание и запуск управляющего потока
control_thread = threading.Thread(target=control)
control_thread.start()

