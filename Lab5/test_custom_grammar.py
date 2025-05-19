#!/usr/bin/env python3

from grammar import Grammar

def test_custom_grammar():
    """
    Test the CNF conversion with a custom grammar.
    """
    print("Testing CNF conversion with a custom grammar")
    print("===========================================\n")
    
    # Define a custom grammar
    non_terminals = {'S', 'A', 'B'}
    terminals = {'a', 'b', 'c'}
    productions = {
        'S': ['AB', 'aB'],
        'A': ['a', 'aS', 'ε'],
        'B': ['b', 'bS', 'c']
    }
    start_symbol = 'S'
    
    custom_grammar = Grammar(non_terminals, terminals, productions, start_symbol)
    
    print("Original Grammar:")
    print(custom_grammar)
    print()
    
    # Convert to CNF
    cnf_grammar = custom_grammar.convert_to_cnf()
    
    print("Grammar in Chomsky Normal Form:")
    print(cnf_grammar)
    print()
    
    print("Conversion to Chomsky Normal Form completed successfully!")

if __name__ == "__main__":
    test_custom_grammar()
