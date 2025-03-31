# Lexer Implementation Report
## Formal Languages & Finite Automata

**Author:** Cretu Dumitru  
**Date:** March 31, 2025  
**Course:** Formal Languages & Finite Automata

## 1. Introduction

This report documents the implementation of a lexer (also known as a scanner or tokenizer) for a programming language as part of the Formal Languages & Finite Automata course. The lexer is designed to perform lexical analysis on code input, transforming raw text into meaningful tokens that can be further processed by a compiler or interpreter.

## 2. Theoretical Background

### 2.1 What is a Lexer?

A **lexer** (short for lexical analyzer) is the first phase in a compiler or interpreter that converts a sequence of characters into a sequence of tokens. Each token represents a lexical unit of the language, such as keywords, identifiers, numbers, operators, and delimiters.

The lexical analysis process involves:
1. Reading the input character by character
2. Grouping characters into meaningful lexemes
3. Categorizing these lexemes into specific token types
4. Passing the tokens to the next phase of compilation (usually syntax analysis)

### 2.2 Difference Between Lexemes and Tokens

- **Lexeme**: The actual string of characters from the source code that forms a syntactic unit
- **Token**: A categorized lexeme with additional metadata that represents its type and significance

For example, in the statement `x = 10;`:
- Lexemes: `x`, `=`, `10`, and `;`
- Tokens: `(IDENTIFIER, "x")`, `(OPERATOR, "=")`, `(NUMBER, "10")`, and `(DELIMITER, ";")`

### 2.3 Role in Compiler Design

The lexer serves as the front-end of a compiler pipeline and has several important roles:
- Removes whitespace and comments
- Validates lexical correctness of the source code
- Simplifies subsequent parsing by working with tokens instead of raw characters
- Often tracks position information for error reporting

## 3. Implementation Details

### 3.1 Architecture

The lexer implementation follows a character-by-character scanning approach and utilizes the following components:

1. **Token class**: Represents individual tokens with properties for type, value, and position
2. **Lexer class**: Contains the main scanning logic for token recognition
3. **Web interface**: Allows users to input code and visualize the tokenization process

### 3.2 Token Types

The lexer recognizes the following token types:

| Token Type | Description | Examples |
|------------|-------------|----------|
| KEYWORD | Reserved words in the language | `if`, `else`, `while`, `function` |
| IDENTIFIER | Variable and function names | `x`, `counter`, `calculateArea` |
| NUMBER | Integer and floating-point numbers | `10`, `3.14159`, `1.23e-4` |
| STRING | Text enclosed in quotes | `"hello"`, `'world'` |
| OPERATOR | Mathematical and logical operators | `+`, `-`, `*`, `/`, `==`, `!=` |
| DELIMITER | Syntax elements | `(`, `)`, `{`, `}`, `;`, `,` |
| FUNCTION | Built-in function names | `sin`, `cos`, `sqrt` |
| COMMENT | Single and multi-line comments | `// comment`, `/* comment */` |
| EOF | End of file marker | - |

### 3.3 Algorithm

The lexer uses a state-driven approach to scan the input text:

1. Initialize the scanner with input text and position at the first character
2. While not at the end of the file:
   - Skip whitespace
   - Identify the next token based on the current character:
     - If letter: Parse as identifier or keyword
     - If digit: Parse as number
     - If quote: Parse as string
     - If operator character: Parse as operator
     - If delimiter: Return as delimiter
     - If comment start: Parse as comment
   - Advance to the next character
3. Return the token sequence

### 3.4 Code Structure

The core of the implementation is the `Lexer` class which contains the following key methods:

```javascript
// Main methods
constructor(input)     // Initialize the lexer with input text
advance()              // Move to the next character
peek()                 // Look ahead without advancing
getNextToken()         // Get the next token
tokenize()             // Process all tokens in the input

// Token-specific methods
skipWhitespace()       // Skip spaces, tabs, newlines
skipComment()          // Handle comments
number()               // Parse integer and float numbers
identifier()           // Parse identifiers and keywords
string()               // Parse string literals
```

### 3.5 Handling Special Cases

The implementation includes special handling for:

1. **Floating-point numbers**: Supports both standard decimal notation and scientific notation (e.g., `1.23e-4`)
2. **Multi-character operators**: Recognizes operators like `==`, `!=`, `<=`, and `>=`
3. **String escape sequences**: Handles `\n`, `\t`, `\r`, `\"`, and `\\`
4. **Multi-line comments**: Properly processes comments enclosed in `/* ... */`
5. **Line and column tracking**: Maintains position information for error reporting

## 4. Implementation Examples

Here are some examples demonstrating the lexer's functionality:

### 4.1 Basic Mathematical Operations

```javascript
// Basic mathematical operations
let x = 10;
let y = 20.5;
let z = (x + y) * 2;
let result = z / 5;

// Trigonometric functions
let angle = 30;
let sinValue = sin(angle);
let cosValue = cos(angle);
```

### 4.2 Function Definitions and Calls

```javascript
// Function definition
function calculateArea(radius) {
    const PI = 3.14159;
    return PI * radius * radius;
}

// Function calls
let circleArea = calculateArea(5);
let circleVolume = 4/3 * 3.14159 * 5 * 5 * 5;

// Multiple functions
function celsius2fahrenheit(c) {
    return (c * 9/5) + 32;
}
```

### 4.3 Control Flow Statements

```javascript
// Control flow example
let temperature = 25;

if (temperature > 30) {
    console.log("It's hot!");
} else if (temperature > 20) {
    console.log("It's warm.");
} else {
    console.log("It's cool.");
}

// Loop example
let counter = 0;
while (counter < 5) {
    counter++;
    /* This is a 
    multi-line comment */
}
```

## 5. User Interface

The lexer implementation includes a web-based user interface with the following features:

1. **Code input area**: Allows users to enter custom code
2. **Example buttons**: Provides pre-defined code samples
3. **Token visualization**: Displays tokens in a tabular format
4. **Animation view**: Visual representation of token extraction
5. **Documentation**: Information about the lexer's functionality

## 6. Challenges and Solutions

### 6.1 Handling Ambiguity

One challenge in lexical analysis is resolving ambiguity between different token types. For example, identifiers and keywords follow the same pattern initially. The solution was to check if an identified lexeme matches any predefined keywords after parsing it as an identifier.

### 6.2 Position Tracking

Maintaining accurate line and column information was crucial for error reporting. The implementation includes logic to update these positions correctly, especially when handling newlines and multi-line constructs like comments.

### 6.3 Nested Components

Handling nested constructs, such as parentheses in expressions or complex string patterns, required careful state management and lookahead functionality to ensure correct tokenization.

## 7. Future Improvements

Several enhancements could be made to the current implementation:

1. **Error recovery**: Implement strategies to continue lexical analysis after encountering errors
2. **Performance optimization**: Improve efficiency for handling large input files
3. **Additional token types**: Support for more complex language features
4. **Integration with parser**: Connect the lexer with a syntax analyzer to form a complete frontend
5. **Custom language support**: Make the lexer configurable for different language syntax

## 8. Conclusion

This lexer implementation successfully demonstrates the principles of lexical analysis for a programming language. By breaking down source code into tokens, it provides the foundation for further language processing steps, such as parsing and compilation.

The interactive demonstration helps visualize the tokenization process, making it easier to understand how a lexer operates on different code constructs. This implementation covers all the basic requirements of a practical lexer while providing extensibility for future enhancements.

## 9. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd Edition). Addison-Wesley.
2. Cooper, K. D., & Torczon, L. (2011). Engineering a Compiler (2nd Edition). Morgan Kaufmann.
3. Slonneger, K., & Kurtz, B. L. (1995). Formal Syntax and Semantics of Programming Languages. Addison-Wesley.
4. Mak, R. (2011). Writing Compilers and Interpreters: A Software Engineering Approach (3rd Edition). Wiley.
5. Parr, T. (2010). Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages. Pragmatic Bookshelf.