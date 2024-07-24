import tkinter as tk

def pack_button(window, text, command):
	button = tk.Button(window, text=text, command=command)
	button.pack()
