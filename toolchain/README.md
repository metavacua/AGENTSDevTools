# Toolchain for Automated Development

This directory contains tools to support an automated development process guided by a "No Effects" principle. The goal is to build a toolchain that helps *construct* pure, side-effect-free code, rather than just detecting impurities after the fact.

## `refactor_to_pure.py`

This script is a constructive tool that performs a simple refactoring to make a Python function more pure. It demonstrates the principle of actively guiding development towards a side-effect-free style.

The tool works by transforming a function that contains `print()` statements into a new function that returns both its original result and a list of the messages that would have been printed. This separates the pure calculation from the impure I/O operation.

### Usage

To refactor a function, run the script from the repository root, providing the path to the Python file and the name of the function you want to refactor:

```bash
python toolchain/refactor_to_pure.py <path_to_python_file> <function_name>
```

### Example

If you have a file named `example.py` with the following content:
```python
def process_data(data):
    print(f"Processing {len(data)} items.")
    result = sum(data)
    print("Processing complete.")
    return result
```

Running the refactoring tool on the `process_data` function:
```bash
python toolchain/refactor_to_pure.py example.py process_data
```

Will produce the following output, showing the refactored, pure function:
```
--- Refactoring function 'process_data' in 'example.py' ---
Refactored function:
def process_data(data):
    result = sum(data)
    return (result, [f'Processing {len(data)} items.', 'Processing complete.'])

----------------------------------------------------

Note: This is a simplified refactoring. It has significant limitations,
such as only handling simple print statements and single return paths.
```

### Current Limitations

This is a proof-of-concept and its capabilities are intentionally limited to what can be implemented robustly in a single session. **It is not a comprehensive refactoring tool.**

The following limitations are known:

*   **Handles `print` only:** It can only extract `print` statements. It cannot handle other side-effects like file I/O, network requests, or global state mutation.
*   **Assumes a single `return` statement:** The logic is designed around functions with a single exit point at the end. It will not work correctly on functions with multiple `return` statements or complex control flow.
*   **Simple Return Value:** It assumes the function has a simple `return` statement. Functions without a return (`None`) or with more complex return logic may not be handled correctly.
*   **No Class or Method Support:** The tool is designed for standalone functions and has not been tested on methods within classes.

This tool serves as a functional first step towards a constructive, refactoring-based toolchain. Future work will focus on expanding its capabilities to handle more complex code patterns and a wider variety of side-effects.