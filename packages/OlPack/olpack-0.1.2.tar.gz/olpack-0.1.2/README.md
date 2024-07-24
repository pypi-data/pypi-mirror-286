# PyPack

A collection of tools to simplify your python experience!

## Requirements

- Python 3.6 or higher
- Tkinter (usually included with Python)

## Installation

To install this package, you can use pip:

```bash
pip install .
```

## Available Functions

### start_window(window)

The `start_window` function uses `window.mainloop` to start the windows main loop.

| Parameter | Description | Example |
|-----------|------------|------------|
|`window`|The window to use `[window].mainloop()`| `start_window(root)` (Initializes the main loop for root)

### initialize_window(title="My App", size="300x200")

The `intialize_window` function creates a window that the user can run with the `start(window)` function.

| Parameter | Description | Example |
|-----------|------------|------------|
|`title`| The title of the window that is created. | `My App` (App Name)
|`size`|The size of the window created (In Pixels)| `300x200` Pixels

### pack_button(window, text, command)

The `pack_button` function adds a button to the Tkinter window with the specified text and command. Below is a description of each parameter.

| Parameter | Description                                  | Example Usage        |
|-----------|----------------------------------------------|-----------------------|
| `window`  | The Tkinter window where the button will be added. | `root` (main application window) |
| `text`    | The label text to display on the button.     | `"Click Me"`          |
| `command` | The function to call when the button is clicked. | `button_clicked` (a function that gets executed on click) |

### Example Usage
```python
from PyPack import initialize_window, pack_button, start_window

def on_button_clicked(): 
    print("Hello, world!")

# Creates a window with the title 'My App' and size '300x200' pixels.
window = initialize_window("My App", "300x200")

# Adds a button to the window
pack_button(window, "Click me!", on_button_clicked)

# Starts the main loop
start_window(window)
```

## License

This project is licensed under a Custom License. You are free to use, modify, and fork the code. Redistribution under the same name as the original software is not permitted. Any distribution or use must provide proper attribution to the original author. See the [LICENSE](LICENSE) file for details.
