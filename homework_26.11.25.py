import random
import threading
import time

task = ('load', 'process', 'shutdown')
current_task = None
condition = threading.Condition()
active_workers = 0 # Счетчик активных рабочих потоков


def dispatcher():
    global current_task
    while True:
        time.sleep(5)
        with condition: # Захватываем условие для синхронизации
            current_task = random.choice(task)
            print(f'Current task: {current_task}')
            condition.notify() # Уведомляем один из рабочих потоков
            if current_task == 'shutdown' and active_workers == 0:
                break



def worker(n):
    global active_workers
    while True:
        with condition: # Захватываем условие для синхронизации
            active_workers += 1 # Увеличиваем количество активных потоков
            print(f'Worker {n} started')
            condition.wait() # Ожидание уведомления от диспетчера
            if current_task =='shutdown':
                active_workers -= 1
                break #выход из цикла при shutdown
            print(f'Worker {n} making the task: {current_task}')
            time.sleep(2)
            active_workers -=1

dispatcher_thread= threading.Thread(target=dispatcher)

worker_thread= [threading.Thread(target=worker,args=(i,)) for i in range(2)]


dispatcher_thread.start()
for t in worker_thread:
    t.start()

dispatcher_thread.join()
for t in worker_thread:
    t.join()






