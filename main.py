import tkinter as tk
from tkinter import ttk
from controller.task_controll import TaskController

def main():
    
    root = tk.Tk()
    root.title("To-Do List")
    root.geometry("600x500")
    app = TaskController(root)
    root.mainloop()
    # enable_dark_mode(root)

if __name__ == '__main__':
    main()