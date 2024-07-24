import tkinter as tk
from tkinter import ttk

def create_table(parent, columns):
    """Creates a Treeview table widget."""
    # Create the Treeview widget
    tree = ttk.Treeview(parent, columns=columns, show='headings')

    # Define the column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Create scrollbars for the Treeview
    scroll_y = tk.Scrollbar(parent, orient="vertical", command=tree.yview)
    scroll_x = tk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Pack the widgets
    tree.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

    return tree

def add_row(tree, row_data):
    """Adds a row to the table."""
    if len(row_data) == len(tree["columns"]):
        tree.insert('', 'end', values=row_data)
    else:
        raise ValueError("Row data must match the number of columns")

def remove_row(tree, item_id):
    """Removes a row from the table."""
    tree.delete(item_id)

def update_row(tree, item_id, new_data):
    """Updates a row in the table."""
    if len(new_data) == len(tree["columns"]):
        tree.item(item_id, values=new_data)
    else:
        raise ValueError("Row data must match the number of columns")