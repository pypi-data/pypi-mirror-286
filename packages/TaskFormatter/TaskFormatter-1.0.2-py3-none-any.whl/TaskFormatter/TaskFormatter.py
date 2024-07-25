import time
import sys
import multiprocessing
from functools import wraps
import signal
import io

# Global counter for function numbering
function_counter = multiprocessing.Value('i', 0)

def spinner(function_number, func_name, spinner_done, print_lock):
    spinner_gen = spinner_gen_func()
    while not spinner_done.is_set():
        with print_lock:
            sys.stdout.write(f"\r\033[1m\033[4m\033[94m{function_number}. {func_name} Running [{next(spinner_gen)}] \033[0m")
            sys.stdout.flush()
        time.sleep(0.1)

def spinner_gen_func():
    while True:
        for cursor in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
            yield cursor

def format_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with function_counter.get_lock():
            function_counter.value += 1
            function_number = function_counter.value

        start_time = time.time()
        func_name = func.__name__
        spinner_done = multiprocessing.Event()
        print_lock = multiprocessing.Lock()

        spin_process = multiprocessing.Process(target=spinner, args=(function_number, func_name, spinner_done, print_lock))
        spin_process.start()

        def handle_exit(signum, frame):
            raise SystemExit("Process exited")

        signal.signal(signal.SIGTERM, handle_exit)
        signal.signal(signal.SIGINT, handle_exit)

        buffer = io.StringIO()
        original_stdout = sys.stdout
        sys.stdout = buffer

        try:
            func(*args, **kwargs)
            duration = time.time() - start_time
            spinner_done.set()
            spin_process.join()
            sys.stdout = original_stdout
            with print_lock:
                sys.stdout.write(f"\r\033[1m\033[4m\033[92m{function_number}. {func_name} Completed [✓] in {duration:.2f}s\033[0m\n")
                sys.stdout.flush()
                output = buffer.getvalue().strip()
                if output:
                    sys.stdout.write(output + "\n")
                sys.stdout.write('\n---\n')  # Add separator before the next function
        except SystemExit as e:
            duration = time.time() - start_time
            spinner_done.set()
            spin_process.join()
            sys.stdout = original_stdout
            with print_lock:
                sys.stdout.write(f"\r\033[1m\033[4m\033[91m{function_number}. {func_name} Failed [✗] in {duration:.2f}s\033[0m\n")
                sys.stdout.flush()
                output = buffer.getvalue().strip()
                if output:
                    sys.stdout.write(output + "\n")
                print(f"\033[91m\033[4m{e}\033[0m")
                sys.stdout.write('\n---\n')  # Add separator before the next function
            raise e
        except Exception as e:
            duration = time.time() - start_time
            spinner_done.set()
            spin_process.join()
            sys.stdout = original_stdout
            with print_lock:
                sys.stdout.write(f"\r\033[1m\033[4m\033[91m{function_number}. {func_name} Failed [✗] in {duration:.2f}s\033[0m\n")
                sys.stdout.flush()
                output = buffer.getvalue().strip()
                if output:
                    sys.stdout.write(output + "\n")
                print(f"\033[91m\033[4m{e}\033[0m")
                sys.stdout.write('\n---\n')  # Add separator before the next function
            raise e

    return wrapper
