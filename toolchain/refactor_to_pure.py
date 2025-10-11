import ast
import sys
import astunparse

class PrintExtractor(ast.NodeTransformer):
    """
    An AST transformer that extracts print calls from a function body,
    collects their arguments, and modifies the function's return statement.
    """
    def __init__(self):
        super().__init__()
        self.print_args = []

    def visit_Expr(self, node):
        """
        Identifies expression statements that are calls to 'print' and
        removes them, extracting their arguments.
        """
        # Check if the expression is a call to 'print'
        if isinstance(node.value, ast.Call):
            call_node = node.value
            if isinstance(call_node.func, ast.Name) and call_node.func.id == 'print':
                # It's a print statement. Extract args and remove the node.
                self.print_args.extend(call_node.args)
                return None  # Remove the entire Expr node from the function body

        # It's some other expression, leave it as is.
        return node

    def visit_Return(self, node):
        """Modifies the return statement to include the extracted print messages."""
        # Create a new list of the collected print arguments
        messages_list = ast.List(elts=self.print_args, ctx=ast.Load())

        original_return = node.value
        if original_return is None:
            # Handle "return" without a value by returning None explicitly
            original_return = ast.Constant(value=None)

        # Create a new tuple to be returned, containing the original return value and the list of messages
        new_return_tuple = ast.Tuple(elts=[original_return, messages_list], ctx=ast.Load())

        # Create a new return statement with the new tuple
        new_return_node = ast.Return(value=new_return_tuple)
        ast.copy_location(new_return_node, node)
        ast.fix_missing_locations(new_return_node)
        return new_return_node


def refactor_function_in_file(filepath, function_name):
    """
    Parses a Python file, finds a specific function, and refactors it
    to extract print statements.
    """
    print(f"--- Refactoring function '{function_name}' in '{filepath}' ---")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
            tree = ast.parse(source_code, filename=filepath)
    except (FileNotFoundError, SyntaxError) as e:
        print(f"Error: Could not read or parse file '{filepath}'.\n{e}", file=sys.stderr)
        sys.exit(1)

    function_to_refactor = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_to_refactor = node
            break

    if not function_to_refactor:
        print(f"Error: Function '{function_name}' not found in '{filepath}'.", file=sys.stderr)
        sys.exit(1)

    # Apply the transformation
    transformer = PrintExtractor()
    new_function_body = [transformer.visit(n) for n in function_to_refactor.body]
    # Filter out the None values that replaced the print calls
    function_to_refactor.body = [n for n in new_function_body if n is not None]

    # Unparse the modified function AST back to source code
    refactored_code = astunparse.unparse(function_to_refactor)

    print("Refactored function:")
    print(refactored_code)
    print("----------------------------------------------------")
    print("\nNote: This is a simplified refactoring. It has significant limitations,")
    print("such as only handling simple print statements and single return paths.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python toolchain/refactor_to_pure.py <path_to_python_file> <function_name>")
        sys.exit(1)

    file_to_analyze = sys.argv[1]
    func_to_refactor = sys.argv[2]
    refactor_function_in_file(file_to_analyze, func_to_refactor)