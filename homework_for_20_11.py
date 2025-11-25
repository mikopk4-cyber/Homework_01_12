from multiprocessing import Process
from tkinter import Tk, messagebox, filedialog, ttk
import shutil
import tkinter as tk
import os
import tkinter.font as tkfont


#with this function we can choose the directory which we want to archivate
def choose_dir(entry_widget:tk.Entry):
    dir_path = filedialog.askdirectory(title='Выберите директорию')  # Открыть диалог для выбора директории
    if dir_path:  # Если пользователь не отменил выбор
        entry_widget.delete(0, tk.END)  # Очистить поле ввода
        entry_widget.insert(0, dir_path)  # Вставить выбранный путь в поле ввода


#this is the archivator
def archive(parent_dir: str, folder_name:str):
    folder_path = os.path.join(parent_dir, folder_name)
    archive_path = os.path.join(parent_dir, folder_name)
    #сам процесс архивации
    shutil.make_archive(
        base_name=archive_path,
        format='zip',
        root_dir=parent_dir,
        base_dir=folder_name
    )

    messagebox.showinfo('Archive Complete', f'Archive Complete for {folder_name}')


def run_archiver(opened_dir_path:str):
    if not os.path.isdir (opened_dir_path):
        messagebox.showerror("Error", "Directory does not exist")
        return
    subdirs= [name for name in os.listdir(opened_dir_path)
              if os.path.isdir(os.path.join(opened_dir_path,name))]

    if not subdirs:
        messagebox.showerror("Error", "No subdirectories found")
        return

    processes = []
    for folder_name in subdirs:
        p = Process(target=archive, args=(opened_dir_path, folder_name))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    messagebox.showinfo("Archive Complete", "All done!")



def create_window():
    root = Tk()
    root.title('Archiver')
    root.resizable(True, True)
    root.geometry('700x400')

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill='both', expand=True)

    FONT = tkfont.Font(family="Segoe UI", size=11)

    label= ttk.Label(frame, text="Directory for archiving:", font=FONT)
    label.grid(row=0, column=0, sticky="w", pady=(0, 10))

    entry1 = ttk.Entry(frame, width=60, font=FONT)
    entry1.grid(row=1, column=0, sticky="w", pady=(0, 10),padx=(0, 8))

    btn2 = ttk.Button(frame, text="Choose the directory", command=lambda: choose_dir(entry1))
    btn2.grid(row=1, column=1, sticky="e")

    btn_archive = ttk.Button(
        frame,
        text='Archive',
        command=lambda: run_archiver(entry1.get())
    )
    btn_archive.grid(row=2, column=0, sticky="w", pady=(20, 0))

    root.mainloop()


if __name__ == '__main__':
    print('Start')
    create_window()
