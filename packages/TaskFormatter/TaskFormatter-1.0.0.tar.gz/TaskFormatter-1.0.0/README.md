# Formatter and Example

This project demonstrates the use of a Python decorator to format the output of functions, showing a running spinner, and indicating success or failure with colored and formatted text. It includes two files: `formatter.py` and `example.py`.

## Example Output


![](https://github.com/seanssmith/CLI-Formatter/blob/main/python_task_importer/pythonformatterexample.gif)


## Files

1. **formatter.py**: This file contains the `format_output` decorator that provides the desired formatting for function output.
2. **example.py**: This file demonstrates how to use the `format_output` decorator by applying it to two example functions, one that succeeds and one that fails.

## Features

- **Spinner Animation**: Displays a spinner animation while the function is running.
- **Success/Failure Indication**: Shows a green checkmark for successful completion and a red cross for failures.
- **Exception Handling**: Exceptions are displayed in red and underlined.
- **Function Numbering**: Each function is prefixed with a unique number.
- **Text Formatting**: Function names are displayed in bold and underlined.
- **Separation of Outputs**: Outputs from different functions are separated by a line for clarity.

## Usage

### 1. formatter.py

The `format_output` decorator is defined in this file. It wraps a function to display the running spinner, success/failure message, and handle exceptions.

### 2. example.py

The `example.py` file demonstrates the use of the `format_output` decorator. It includes two functions, one that succeeds and one that fails, to showcase the decorator's functionality.


## Running the Example

1. Save formatter.py and example.py in the same directory.
2. Run example.py using the command:
```
python example.py
```
You should see the spinner, success, and failure messages formatted as described, with appropriate separation and formatting for each function's output.
