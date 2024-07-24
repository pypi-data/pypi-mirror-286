import tkinter as tk

def initialize_window(title="My App", size="300x200"):
	window = tk.Tk()
	window.title(title)
	window.geometry(size)
	return window
