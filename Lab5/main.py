#!/usr/bin/env python3

from grammar import Grammar

def main():
    """
    Main function to demonstrate the conversion of a grammar to Chomsky Normal Form.
    """
    print("Chomsky Normal Form Converter")
    print("============================\n")
    
    # Create a grammar from Variant 25
    grammar = Grammar.from_variant_25()
    print("Original Grammar:")
    print(grammar)
    print()
    
    # Step 1: Eliminate ε-productions
    print("Step 1: Eliminate ε-productions")
    grammar_no_epsilon = grammar.eliminate_epsilon_productions()
    print(grammar_no_epsilon)
    print()
    
    # Step 2: Eliminate renaming (unit productions)
    print("Step 2: Eliminate renaming (unit productions)")
    grammar_no_renaming = grammar_no_epsilon.eliminate_renaming()
    print(grammar_no_renaming)
    print()
    
    # Step 3: Eliminate inaccessible symbols
    print("Step 3: Eliminate inaccessible symbols")
    grammar_no_inaccessible = grammar_no_renaming.eliminate_inaccessible_symbols()
    print(grammar_no_inaccessible)
    print()
    
    # Step 4: Eliminate non-productive symbols
    print("Step 4: Eliminate non-productive symbols")
    grammar_no_nonproductive = grammar_no_inaccessible.eliminate_non_productive_symbols()
    print(grammar_no_nonproductive)
    print()
    
    # Step 5: Convert to Chomsky Normal Form
    print("Step 5: Convert to Chomsky Normal Form")
    grammar_cnf = grammar_no_nonproductive.convert_to_cnf()
    print(grammar_cnf)
    print()
    
    print("Conversion to Chomsky Normal Form completed successfully!")

if __name__ == "__main__":
    main()
