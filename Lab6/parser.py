from token_types import TokenType
from lexer import Lexer
from ast_nodes import (
    NumberNode, BinaryOpNode, UnaryOpNode, FunctionCallNode, 
    IdentifierNode, ProgramNode, print_ast
)

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


def parse_text(text):
    """
    Helper function to parse input text and return the AST.
    """
    parser = Parser(text=text)
    return parser.parse()


if __name__ == "__main__":
    # Example usage
    sample_text = "2 + 3.14 * sin(0.5)"
    ast = parse_text(sample_text)
    
    print(f"Input: {sample_text}")
    print("AST:")
    print_ast(ast)
