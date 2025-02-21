import ast
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class FunctionInfo:
    """Store information about a function definition."""
    name: str
    args: List[str]
    decorators: List[str]
    docstring: Optional[str]
    start_line: int
    end_line: int
    source: str

class FunctionParser(ast.NodeVisitor):
    """Parser to extract function definitions from Python code."""
    
    def __init__(self):
        self.functions: List[FunctionInfo] = []
        self._source_lines: List[str] = []
    
    def parse(self, code: str) -> List[FunctionInfo]:
        """Parse Python code and return list of function information."""
        self.functions = []
        self._source_lines = code.splitlines()
        
        try:
            tree = ast.parse(code)
            self.visit(tree)
            return self.functions
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit a function definition node in the AST."""
        # Get function arguments
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Get decorators
        decorators = []
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name):
                    decorators.append(decorator.func.id)
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        # Get function source
        source_lines = self._source_lines[node.lineno-1:node.end_lineno]
        source = '\n'.join(source_lines)
        
        function_info = FunctionInfo(
            name=node.name,
            args=args,
            decorators=decorators,
            docstring=docstring,
            start_line=node.lineno,
            end_line=node.end_lineno,
            source=source
        )
        
        self.functions.append(function_info)
        
        # Continue visiting child nodes
        self.generic_visit(node)

def get_function_definitions(code: str) -> List[FunctionInfo]:
    """
    Extract function definitions from Python code string.
    
    Args:
        code: String containing Python code
        
    Returns:
        List of FunctionInfo objects containing details about each function
        
    Raises:
        ValueError: If the code string contains invalid Python syntax
    """
    parser = FunctionParser()
    return parser.parse(code)

# Example usage
if __name__ == "__main__":
    example_code = '''
@decorator
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello {name}!"

def add(a: int, b: int) -> int:
    return a + b
    '''
    
    functions = get_function_definitions(example_code)
    for func in functions:
        print(f"Function: {func.name}")
        print(f"Arguments: {', '.join(func.args)}")
        print(f"Decorators: {', '.join(func.decorators)}")
        print(f"Docstring: {func.docstring}")
        print(f"Source:\n{func.source}\n")