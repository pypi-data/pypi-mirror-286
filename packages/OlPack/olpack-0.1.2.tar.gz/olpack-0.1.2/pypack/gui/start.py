import tkinter as tk

def start_window(window):
	if isinstance(window, tk.Tk):
		window.mainloop()
	else:
		raise TypeError("Expected a Tkinter window instance.")
