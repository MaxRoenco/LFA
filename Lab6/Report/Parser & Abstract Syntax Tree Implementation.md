# Parser & Abstract Syntax Tree Implementation

## Course: Formal Languages & Finite Automata
## Author: Roenco Maxim

## Theory
The process of gathering syntactical meaning or performing syntactical analysis over text is known as parsing. Parsing typically results in a parse tree that can contain semantic information useful for subsequent stages of compilation.

An Abstract Syntax Tree (AST) is a hierarchical data structure that represents the structure of input text through abstraction layers. These layers represent the constructs or entities that form the initial text. ASTs are particularly useful in program analysis and compilation processes.

## Objectives:
* Understand parsing concepts and implementation techniques
* Implement a TokenType enum for categorizing tokens using regular expressions
* Design and implement data structures for an Abstract Syntax Tree
* Create a parser program to extract syntactic information from input text
* Build upon the lexical analyzer from the previous lab work

## Implementation Description

### TokenType Enum and Regular Expressions
The first step in the implementation was to create a `TokenType` enum to categorize different types of tokens in the input text. Each token type is associated with a regular expression pattern for identification.

```python
class TokenType(Enum):
    """
    Enum representing the different types of tokens that can be identified in the input text.
    """
    # Numbers
    INTEGER = auto()      # Integer numbers (e.g., 42, 100)
    FLOAT = auto()        # Floating point numbers (e.g., 3.14, 2.5)
    
    # Operators
    PLUS = auto()         # Addition operator (+)
    MINUS = auto()        # Subtraction operator (-)
    MULTIPLY = auto()     # Multiplication operator (*)
    DIVIDE = auto()       # Division operator (/)
    POWER = auto()        # Power operator (^)
    
    # Parentheses
    LPAREN = auto()       # Left parenthesis (
    RPAREN = auto()       # Right parenthesis )
    
    # Functions
    SIN = auto()          # Sine function
    COS = auto()          # Cosine function
    TAN = auto()          # Tangent function
    LOG = auto()          # Logarithm function
    
    # Other
    IDENTIFIER = auto()   # Variable names or other identifiers
    WHITESPACE = auto()   # Spaces, tabs, newlines
    COMMA = auto()        # Comma separator
    EOF = auto()          # End of file/input
    UNKNOWN = auto()      # Unknown token type
```

The regular expressions for each token type are defined as follows:

```python
TOKEN_PATTERNS = [
    (TokenType.FLOAT, r'\d+\.\d+'),
    (TokenType.INTEGER, r'\d+'),
    (TokenType.PLUS, r'\+'),
    (TokenType.MINUS, r'-'),
    (TokenType.MULTIPLY, r'\*'),
    (TokenType.DIVIDE, r'/'),
    (TokenType.POWER, r'\^'),
    (TokenType.LPAREN, r'\('),
    (TokenType.RPAREN, r'\)'),
    (TokenType.SIN, r'sin'),
    (TokenType.COS, r'cos'),
    (TokenType.TAN, r'tan'),
    (TokenType.LOG, r'log'),
    (TokenType.COMMA, r','),
    (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
    (TokenType.WHITESPACE, r'[ \t\n\r]+'),
]
```

These patterns are compiled into a single regex for efficient matching:

```python
TOKEN_REGEX = '|'.join('(?P<%s>%s)' % (token_type.name, pattern) for token_type, pattern in TOKEN_PATTERNS)
COMPILED_REGEX = re.compile(TOKEN_REGEX)
```

### Lexer Implementation
The lexer processes input text and generates a stream of tokens. Each token contains its type, value, and position in the input text.

```python
class Token:
    """
    Represents a token identified by the lexer.
    """
    def __init__(self, token_type, value, position):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', pos={self.position})"

class Lexer:
    """
    Lexical analyzer that converts input text into a stream of tokens.
    """
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.tokens = []
    
    def tokenize(self):
        """
        Process the input text and generate a list of tokens.
        """
        self.tokens = []
        
        # Use regex to find all tokens in the input text
        for match in COMPILED_REGEX.finditer(self.text):
            token_type_name = match.lastgroup
            token_value = match.group()
            token_position = match.start()
            
            # Convert the token type name to the corresponding enum value
            token_type = TokenType[token_type_name]
            
            # Create a token and add it to the list
            token = Token(token_type, token_value, token_position)
            self.tokens.append(token)
        
        # Add EOF token at the end
        self.tokens.append(Token(TokenType.EOF, "", len(self.text)))
        
        return self.tokens
    
    def get_tokens(self, skip_whitespace=True):
        """
        Return the list of tokens, optionally filtering out whitespace tokens.
        """
        if not self.tokens:
            self.tokenize()
        
        if skip_whitespace:
            return [token for token in self.tokens if token.type != TokenType.WHITESPACE]
        else:
            return self.tokens
```

### AST Data Structures
The Abstract Syntax Tree is built using a hierarchy of node classes, each representing a different type of expression or operation.

```python
class ASTNode:
    """
    Base class for all AST nodes.
    """
    def __init__(self):
        pass
    
    def __str__(self):
        return self.__class__.__name__

class NumberNode(ASTNode):
    """
    AST node representing a numeric literal (integer or float).
    """
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __str__(self):
        return f"Number({self.value})"

class BinaryOpNode(ASTNode):
    """
    AST node representing a binary operation (e.g., addition, multiplication).
    """
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"

class UnaryOpNode(ASTNode):
    """
    AST node representing a unary operation (e.g., negation).
    """
    def __init__(self, operator, operand):
        super().__init__()
        self.operator = operator
        self.operand = operand
    
    def __str__(self):
        return f"UnaryOp({self.operator}, {self.operand})"

class FunctionCallNode(ASTNode):
    """
    AST node representing a function call (e.g., sin, cos).
    """
    def __init__(self, function_name, arguments):
        super().__init__()
        self.function_name = function_name
        self.arguments = arguments  # List of argument nodes
    
    def __str__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"FunctionCall({self.function_name}, [{args_str}])"

class IdentifierNode(ASTNode):
    """
    AST node representing a variable or identifier.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return f"Identifier({self.name})"

class ProgramNode(ASTNode):
    """
    Root node of the AST representing the entire program or expression.
    """
    def __init__(self, expression):
        super().__init__()
        self.expression = expression
    
    def __str__(self):
        return f"Program({self.expression})"
```

### Parser Implementation
The parser uses recursive descent parsing with precedence climbing to build the AST from the token stream.

```python
class Parser:
    """
    Parser that constructs an Abstract Syntax Tree (AST) from a stream of tokens.
    Uses recursive descent parsing with precedence climbing for expressions.
    """
    def __init__(self, text=None, tokens=None):
        if text is not None:
            self.lexer = Lexer(text)
            self.tokens = self.lexer.get_tokens()
        elif tokens is not None:
            self.tokens = tokens
        else:
            raise ValueError("Either text or tokens must be provided")
        
        self.current_token_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
    
    def parse(self):
        """
        Parse the token stream and return the AST.
        """
        if not self.tokens:
            return None
        
        # Start parsing from the highest level (program)
        ast = self.parse_program()
        
        # Check if we've consumed all tokens (except EOF)
        if self.current_token.type != TokenType.EOF:
            raise SyntaxError(f"Unexpected token at position {self.current_token.position}: {self.current_token}")
        
        return ast
    
    def parse_program(self):
        """
        Parse the entire program/expression.
        program ::= expression EOF
        """
        expression = self.parse_expression()
        return ProgramNode(expression)
    
    def parse_expression(self):
        """
        Parse an expression with operator precedence.
        expression ::= term (('+' | '-') term)*
        """
        return self.parse_binary_expression(0)
    
    def parse_binary_expression(self, min_precedence):
        """
        Parse a binary expression using precedence climbing.
        """
        left = self.parse_primary()
        
        while (
            self.current_token.type in (TokenType.PLUS, TokenType.MINUS, 
                                       TokenType.MULTIPLY, TokenType.DIVIDE, 
                                       TokenType.POWER)
            and self.get_precedence(self.current_token.type) >= min_precedence
        ):
            operator_token = self.current_token
            operator_precedence = self.get_precedence(operator_token.type)
            
            # Consume the operator token
            self.advance()
            
            # For right-associative operators like power (^), use precedence - 1
            next_min_precedence = operator_precedence
            if operator_token.type == TokenType.POWER:
                next_min_precedence = operator_precedence - 1
            else:
                next_min_precedence = operator_precedence + 1
            
            right = self.parse_binary_expression(next_min_precedence)
            
            # Create a binary operation node
            left = BinaryOpNode(left, operator_token.value, right)
        
        return left
    
    def parse_primary(self):
        """
        Parse a primary expression (number, identifier, function call, or parenthesized expression).
        primary ::= number | identifier | function_call | '(' expression ')'
        """
        token = self.current_token
        
        if token.type == TokenType.INTEGER or token.type == TokenType.FLOAT:
            # Parse a number
            self.advance()
            value = float(token.value) if token.type == TokenType.FLOAT else int(token.value)
            return NumberNode(value)
        
        elif token.type == TokenType.IDENTIFIER:
            # Parse an identifier (variable)
            self.advance()
            return IdentifierNode(token.value)
        
        elif token.type in (TokenType.SIN, TokenType.COS, TokenType.TAN, TokenType.LOG):
            # Parse a function call
            function_name = token.value
            self.advance()
            
            # Expect an opening parenthesis
            if self.current_token.type != TokenType.LPAREN:
                raise SyntaxError(f"Expected '(' after function name at position {self.current_token.position}")
            self.advance()
            
            # Parse arguments (comma-separated expressions)
            arguments = []
            if self.current_token.type != TokenType.RPAREN:
                arguments.append(self.parse_expression())
                
                while self.current_token.type == TokenType.COMMA:
                    self.advance()  # Consume the comma
                    arguments.append(self.parse_expression())
            
            # Expect a closing parenthesis
            if self.current_token.type != TokenType.RPAREN:
                raise SyntaxError(f"Expected ')' at position {self.current_token.position}")
            self.advance()
            
            return FunctionCallNode(function_name, arguments)
        
        elif token.type == TokenType.LPAREN:
            # Parse a parenthesized expression
            self.advance()  # Consume '('
            expression = self.parse_expression()
            
            # Expect a closing parenthesis
            if self.current_token.type != TokenType.RPAREN:
                raise SyntaxError(f"Expected ')' at position {self.current_token.position}")
            self.advance()  # Consume ')'
            
            return expression
        
        elif token.type == TokenType.MINUS:
            # Parse a unary negation
            self.advance()  # Consume '-'
            operand = self.parse_primary()
            return UnaryOpNode('-', operand)
        
        elif token.type == TokenType.PLUS:
            # Parse a unary plus (optional, doesn't change the value)
            self.advance()  # Consume '+'
            return self.parse_primary()
        
        else:
            raise SyntaxError(f"Unexpected token at position {token.position}: {token}")
    
    def get_precedence(self, token_type):
        """
        Get the precedence level of an operator.
        Higher values mean higher precedence.
        """
        precedence = {
            TokenType.PLUS: 1,
            TokenType.MINUS: 1,
            TokenType.MULTIPLY: 2,
            TokenType.DIVIDE: 2,
            TokenType.POWER: 3,
        }
        return precedence.get(token_type, 0)
    
    def advance(self):
        """
        Advance to the next token.
        """
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None
```

### Testing and Validation
To validate the implementation, a comprehensive test suite was created to test various expressions, including:
- Simple arithmetic expressions
- Expressions with floating-point numbers
- Expressions with unary operators
- Expressions with function calls
- Complex expressions with nested operations
- Expressions with power operators
- Expressions with multiple function arguments
- Error cases

```python
def test_expression(expression):
    """
    Test the lexer, parser, and AST with a given expression.
    """
    print(f"\n{'=' * 50}")
    print(f"Testing expression: '{expression}'")
    print(f"{'=' * 50}")
    
    # Tokenize the expression
    print("\nTokenization:")
    tokens = tokenize_text(expression)
    for token in tokens:
        print(f"  {token}")
    
    # Parse the expression and build the AST
    print("\nParsing and AST construction:")
    try:
        ast = parse_text(expression)
        print("\nAST Structure:")
        print_ast(ast)
        print("\nParsing successful!")
    except Exception as e:
        print(f"\nParsing error: {e}")
```

## Results
The implementation successfully tokenizes input text, builds an AST, and handles various expressions and error cases. Here are some example results:

### Example 1: Simple Arithmetic
Input: `2 + 3`
```
AST Structure:
Program:
  BinaryOp: +
    Left:
      Number: 2
    Right:
      Number: 3
```

### Example 2: Complex Expression with Function Call
Input: `2 * sin(0.5) + 3 * cos(3.14)`
```
AST Structure:
Program:
  BinaryOp: +
    Left:
      BinaryOp: *
        Left:
          Number: 2
        Right:
          FunctionCall: sin
            Arguments:
              Arg 0:
                Number: 0.5
    Right:
      BinaryOp: *
        Left:
          Number: 3
        Right:
          FunctionCall: cos
            Arguments:
              Arg 0:
                Number: 3.14
```

### Example 3: Nested Expression with Parentheses
Input: `(2 + 3) * sin(0.5 + 0.1)`
```
AST Structure:
Program:
  BinaryOp: *
    Left:
      BinaryOp: +
        Left:
          Number: 2
        Right:
          Number: 3
    Right:
      FunctionCall: sin
        Arguments:
          Arg 0:
            BinaryOp: +
              Left:
                Number: 0.5
              Right:
                Number: 0.1
```

### Example 4: Error Handling
Input: `2 +`
```
Parsing error: Unexpected token at position 3: Token(TokenType.EOF, '', pos=3)
```

## Conclusions
This project successfully implements a parser and Abstract Syntax Tree for mathematical expressions, building upon the lexical analyzer from the previous lab work. The implementation includes:

1. A `TokenType` enum with regular expressions for token identification
2. A lexer that converts input text into a stream of tokens
3. AST data structures for representing expressions
4. A parser that builds the AST from tokens
5. Comprehensive testing and validation

The parser correctly handles operator precedence, function calls, nested expressions, and error cases. The AST provides a clear representation of the syntactic structure of the input expressions, which could be used for further processing such as evaluation or code generation.

This implementation demonstrates the fundamental concepts of parsing and abstract syntax trees, which are essential components in compilers, interpreters, and other language processing tools.

## References
1. [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)
2. [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
3. [Recursive Descent Parsing](https://en.wikipedia.org/wiki/Recursive_descent_parser)
4. [Operator-precedence Parser](https://en.wikipedia.org/wiki/Operator-precedence_parser)
