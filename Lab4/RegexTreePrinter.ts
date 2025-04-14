import { RegexNode, RegexNodeType } from "./RegexNode";

export class RegexTreePrinter {
    static print(node: RegexNode, depth: number = 0): void {
        const indent = ' '.repeat(depth * 2);
        
        switch (node.type) {
            case RegexNodeType.Literal:
                console.log(`${indent}Literal: '${node.value}'`);
                break;
                
            case RegexNodeType.Alternation:
                console.log(`${indent}Alternation:`);
                node.children.forEach((child) => this.print(child, depth + 1));
                break;
                
            case RegexNodeType.Concatenation:
                console.log(`${indent}Concatenation:`);
                node.children.forEach((child) => this.print(child, depth + 1));
                break;
                
            case RegexNodeType.Repetition:
                const repInfo = `${node.minRepeat} to ${node.maxRepeat === -1 ? '∞' : node.maxRepeat}`;
                console.log(`${indent}Repetition (${repInfo}):`);
                node.children.forEach((child) => this.print(child, depth + 1));
                break;
        }
    }
    
    // Enhanced method to return a string representation of the tree
    static toString(node: RegexNode, depth: number = 0): string {
        const indent = ' '.repeat(depth * 2);
        let result = '';
        
        switch (node.type) {
            case RegexNodeType.Literal:
                result += `${indent}Literal: '${node.value}'\n`;
                break;
                
            case RegexNodeType.Alternation:
                result += `${indent}Alternation:\n`;
                node.children.forEach((child) => {
                    result += this.toString(child, depth + 1);
                });
                break;
                
            case RegexNodeType.Concatenation:
                result += `${indent}Concatenation:\n`;
                node.children.forEach((child) => {
                    result += this.toString(child, depth + 1);
                });
                break;
                
            case RegexNodeType.Repetition:
                const repInfo = `${node.minRepeat} to ${node.maxRepeat === -1 ? '∞' : node.maxRepeat}`;
                result += `${indent}Repetition (${repInfo}):\n`;
                node.children.forEach((child) => {
                    result += this.toString(child, depth + 1);
                });
                break;
        }
        
        return result;
    }
    
    // Method to visualize the tree with ASCII art
    static visualize(node: RegexNode): string {
        return this.visualizeNode(node, '', true, '');
    }
    
    private static visualizeNode(node: RegexNode, prefix: string, isLast: boolean, result: string): string {
        const connector = isLast ? '└── ' : '├── ';
        const newPrefix = prefix + (isLast ? '    ' : '│   ');
        
        let nodeDescription = '';
        switch (node.type) {
            case RegexNodeType.Literal:
                nodeDescription = `Literal: '${node.value}'`;
                break;
                
            case RegexNodeType.Alternation:
                nodeDescription = 'Alternation';
                break;
                
            case RegexNodeType.Concatenation:
                nodeDescription = 'Concatenation';
                break;
                
            case RegexNodeType.Repetition:
                const repInfo = `${node.minRepeat} to ${node.maxRepeat === -1 ? '∞' : node.maxRepeat}`;
                nodeDescription = `Repetition (${repInfo})`;
                break;
        }
        
        result += prefix + connector + nodeDescription + '\n';
        
        if (node.children.length > 0) {
            for (let i = 0; i < node.children.length; i++) {
                result = this.visualizeNode(
                    node.children[i], 
                    newPrefix, 
                    i === node.children.length - 1,
                    result
                );
            }
        }
        
        return result;
    }
    
    // Method to create a detailed step-by-step processing visualization
    static explainProcessing(pattern: string, node: RegexNode): string {
        let explanation = `Step-by-step processing of pattern '${pattern}':\n\n`;
        explanation += '1. Parsing the regular expression into a syntax tree\n';
        explanation += this.visualize(node);
        explanation += '\n2. Interpreting the syntax tree to generate valid strings\n';
        explanation += this.explainNodeProcessing(node, 1);
        return explanation;
    }
    
    private static explainNodeProcessing(node: RegexNode, step: number): string {
        let explanation = '';
        
        switch (node.type) {
            case RegexNodeType.Literal:
                explanation += `   ${step}. Process literal '${node.value}' - adds exactly this character\n`;
                break;
                
            case RegexNodeType.Alternation:
                explanation += `   ${step}. Process alternation - chooses one of the following options:\n`;
                let altStep = 1;
                node.children.forEach((child) => {
                    explanation += `      ${step}.${altStep++}. Option: `;
                    if (child.type === RegexNodeType.Literal) {
                        explanation += `'${child.value}'\n`;
                    } else if (child.type === RegexNodeType.Concatenation && child.children.length === 1 && 
                               child.children[0].type === RegexNodeType.Literal) {
                        explanation += `'${child.children[0].value}'\n`;
                    } else {
                        explanation += 'Complex subexpression\n';
                        explanation += this.explainNodeProcessing(child, step + 1);
                    }
                });
                break;
                
            case RegexNodeType.Concatenation:
                if (node.children.length > 0) {
                    explanation += `   ${step}. Process concatenation - combines results from each part in sequence:\n`;
                    let concatStep = 1;
                    node.children.forEach((child) => {
                        explanation += this.explainNodeProcessing(child, step + concatStep++);
                    });
                }
                break;
                
            case RegexNodeType.Repetition:
                const repInfo = node.minRepeat === 0 && node.maxRepeat === -1 ? '*' :
                               node.minRepeat === 1 && node.maxRepeat === -1 ? '+' :
                               node.minRepeat === 0 && node.maxRepeat === 1 ? '?' :
                               `{${node.minRepeat},${node.maxRepeat === -1 ? '' : node.maxRepeat}}`;
                               
                explanation += `   ${step}. Process repetition '${repInfo}' - repeats the following pattern ${node.minRepeat} to ${node.maxRepeat === -1 ? '5 (limited)' : node.maxRepeat} times:\n`;
                explanation += this.explainNodeProcessing(node.children[0], step + 1);
                break;
        }
        
        return explanation;
    }
}