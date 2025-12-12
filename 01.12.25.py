import os
import tkinter as tk
from asyncio import tasks
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter.font as tkfont
import asyncio
import aiofiles


#Асинхроная функция для читания файла
async def read_file(file_path, search_text, results):
    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read() #читаем вместимость файла
            if search_text  in content: #проверка на наявность контента
                results.append(content)  #добаляем путь к файлу в результат
    except Exception as e:
        print(f'Error {e}')

#Асинхроная функция для читания всех файлов в директории
async def read_all_files(dir, search_text):
    tasks = []
    results = []
    files = os.listdir(dir) #Получаем списко файлов в директории
    text_files = [os.path.join(dir, f) for f in files if f.endswith('.txt')]
    #Добавляем коррутину к списку
    for text_file in text_files:
        tasks.append(read_file(text_file, search_text, results))

    #запускаем все корутины
    await asyncio.gather(*tasks)
    #возращаем результат
    return results

#Функции для открытия директории
def open_dir():
    #открываем саму директорию
    directory = filedialog.askdirectory()
    if directory:
        search_text = text_area.get('1.0', tk.END).strip()
        if not search_text:
            messagebox.showwarning('Внимание', 'Напишите фрагмент текста для поиска')
            return

        try:
            #запускаем асинхроную функцию
            results = asyncio.run(read_all_files(directory, search_text))
            save_results_to_file(results) #сохраняем результат в файл
        except Exception as e:
            print(f'Error {e}')

def save_results_to_file(results):
    if results:
        with open('results.txt', 'w', encoding='utf-8') as result_file:
            for path in results:
                result_file.write(path + '\n') #записываем пути к файлу
            messagebox.showinfo('Успех', 'Результат сохранился в result.txt')
    else:
        messagebox.showinfo('Pезультаты', 'Не найдено ни одного текста ')



# Створення графічного вікна
root = tk.Tk()
root.title("Пошук у текстових файлах")

frame = tk.Frame(root)
frame.pack(pady=10)

text_area = tk.Text(frame, width=80, height=10)  # Багаторядкове текстове поле
text_area.pack(padx=10, pady=10)

button = tk.Button(frame, text="Вибрати папку", command=open_dir)  # Кнопка для вибору папки
button.pack()

root.mainloop()  # Запуск основного циклу програми




