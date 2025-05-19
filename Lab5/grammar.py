class Grammar:
    """
    A class to represent a context-free grammar and perform transformations to convert it to Chomsky Normal Form.
    
    Attributes:
        non_terminals (set): Set of non-terminal symbols
        terminals (set): Set of terminal symbols
        productions (dict): Dictionary mapping non-terminals to lists of productions
        start_symbol (str): The start symbol of the grammar
    """
    
    def __init__(self, non_terminals=None, terminals=None, productions=None, start_symbol=None):
        """
        Initialize a Grammar object with the given components.
        
        Args:
            non_terminals (set): Set of non-terminal symbols
            terminals (set): Set of terminal symbols
            productions (dict): Dictionary mapping non-terminals to lists of productions
            start_symbol (str): The start symbol of the grammar
        """
        self.non_terminals = non_terminals if non_terminals else set()
        self.terminals = terminals if terminals else set()
        self.productions = productions if productions else {}
        self.start_symbol = start_symbol
    
    def __str__(self):
        """
        Return a string representation of the grammar.
        
        Returns:
            str: String representation of the grammar
        """
        result = f"Non-terminals: {', '.join(sorted(self.non_terminals))}\n"
        result += f"Terminals: {', '.join(sorted(self.terminals))}\n"
        result += f"Start symbol: {self.start_symbol}\n"
        result += "Productions:\n"
        
        for nt in sorted(self.productions.keys()):
            for prod in sorted(self.productions[nt]):
                result += f"  {nt} -> {prod}\n"
        
        return result
    
    @classmethod
    def from_variant_25(cls):
        """
        Create a Grammar object from the grammar specified in Variant 25.
        
        Returns:
            Grammar: A Grammar object representing the grammar from Variant 25
        """
        non_terminals = {'S', 'A', 'B', 'C', 'D'}
        terminals = {'a', 'b'}
        productions = {
            'S': ['bA', 'BC'],
            'A': ['a', 'aS', 'bCaCa'],
            'B': ['A', 'bS', 'bCAa'],
            'C': ['ε', 'AB'],
            'D': ['AB']
        }
        start_symbol = 'S'
        
        return cls(non_terminals, terminals, productions, start_symbol)
    
    @classmethod
    def from_string(cls, grammar_str):
        """
        Create a Grammar object from a string representation.
        
        Args:
            grammar_str (str): String representation of the grammar
            
        Returns:
            Grammar: A Grammar object representing the grammar from the string
        """
        lines = grammar_str.strip().split('\n')
        
        # Parse non-terminals, terminals, and start symbol
        grammar_def = lines[0].strip()
        parts = grammar_def.split('=')
        if len(parts) < 2:
            raise ValueError("Invalid grammar definition format")
        
        grammar_parts = parts[1].strip().split()
        if len(grammar_parts) < 4:
            raise ValueError("Grammar definition must include VN, VT, P, and S")
        
        # Extract non-terminals
        vn_part = grammar_parts[0].strip()
        vn_content = vn_part.split('=')[1].strip()
        if vn_content.startswith('{') and vn_content.endswith('}'):
            vn_content = vn_content[1:-1]
        non_terminals = {nt.strip() for nt in vn_content.split(',')}
        
        # Extract terminals
        vt_part = grammar_parts[1].strip()
        vt_content = vt_part.split('=')[1].strip()
        if vt_content.startswith('{') and vt_content.endswith('}'):
            vt_content = vt_content[1:-1]
        terminals = {t.strip() for t in vt_content.split(',')}
        
        # Extract start symbol
        start_symbol = grammar_parts[3].strip()
        
        # Parse productions
        productions = {}
        for line in lines[1:]:
            if not line.strip() or '->' not in line:
                continue
            
            parts = line.strip().split('->')
            if len(parts) != 2:
                continue
            
            lhs = parts[0].strip()
            rhs = parts[1].strip()
            
            if lhs not in productions:
                productions[lhs] = []
            
            productions[lhs].append(rhs)
        
        return cls(non_terminals, terminals, productions, start_symbol)
    
    def eliminate_epsilon_productions(self):
        """
        Eliminate ε-productions from the grammar.
        
        Returns:
            Grammar: A new Grammar object without ε-productions
        """
        # Step 1: Find all nullable symbols (symbols that can derive ε)
        nullable = set()
        
        # Initially, add all symbols that directly produce ε
        for nt, prods in self.productions.items():
            if 'ε' in prods:
                nullable.add(nt)
        
        # Iteratively find all nullable symbols
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in nullable:
                    continue
                
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        nullable.add(nt)
                        changed = True
                        break
        
        # Step 2: Create new productions without ε-productions
        new_productions = {}
        
        for nt, prods in self.productions.items():
            new_prods = []
            
            for prod in prods:
                if prod == 'ε':
                    continue  # Skip ε-productions
                
                # Generate all possible combinations by removing nullable symbols
                self._add_combinations(prod, nullable, 0, '', new_prods)
            
            if new_prods:
                new_productions[nt] = new_prods
        
        # Create a new grammar without ε-productions
        new_grammar = Grammar(
            non_terminals=self.non_terminals.copy(),
            terminals=self.terminals.copy(),
            productions=new_productions,
            start_symbol=self.start_symbol
        )
        
        # If the start symbol is nullable, add a new production S' -> ε
        if self.start_symbol in nullable:
            if 'S0' not in new_grammar.non_terminals:
                new_grammar.non_terminals.add('S0')
                new_grammar.productions['S0'] = [self.start_symbol, 'ε']
                new_grammar.start_symbol = 'S0'
        
        return new_grammar
    
    def _add_combinations(self, prod, nullable, pos, current, result):
        """
        Helper method to generate all possible combinations by removing nullable symbols.
        
        Args:
            prod (str): The production to process
            nullable (set): Set of nullable symbols
            pos (int): Current position in the production
            current (str): Current combination being built
            result (list): List to store the resulting combinations
        """
        if pos == len(prod):
            if current:  # Don't add empty string as a production
                result.append(current)
            return
        
        symbol = prod[pos]
        
        # Always include the current symbol
        self._add_combinations(prod, nullable, pos + 1, current + symbol, result)
        
        # If the symbol is nullable, also try skipping it
        if symbol in nullable:
            self._add_combinations(prod, nullable, pos + 1, current, result)
    
    def eliminate_renaming(self):
        """
        Eliminate unit productions (renaming) from the grammar.
        
        Returns:
            Grammar: A new Grammar object without unit productions
        """
        # Find all unit pairs (A, B) such that A =>* B
        unit_pairs = {}
        
        # Initialize with direct unit productions
        for nt in self.non_terminals:
            unit_pairs[nt] = {nt}  # Every non-terminal can derive itself
            
            if nt in self.productions:
                for prod in self.productions[nt]:
                    if len(prod) == 1 and prod in self.non_terminals:
                        unit_pairs[nt].add(prod)
        
        # Find all unit pairs using transitive closure
        changed = True
        while changed:
            changed = False
            for a in self.non_terminals:
                for b in list(unit_pairs.get(a, set())):
                    for c in list(unit_pairs.get(b, set())):
                        if c not in unit_pairs.get(a, set()):
                            if a not in unit_pairs:
                                unit_pairs[a] = set()
                            unit_pairs[a].add(c)
                            changed = True
        
        # Create new productions without unit productions
        new_productions = {}
        
        for a in self.non_terminals:
            new_prods = []
            
            for b in unit_pairs.get(a, set()):
                if b in self.productions:
                    for prod in self.productions[b]:
                        # Skip unit productions
                        if len(prod) != 1 or prod not in self.non_terminals:
                            new_prods.append(prod)
            
            if new_prods:
                new_productions[a] = new_prods
        
        # Create a new grammar without unit productions
        return Grammar(
            non_terminals=self.non_terminals.copy(),
            terminals=self.terminals.copy(),
            productions=new_productions,
            start_symbol=self.start_symbol
        )
    
    def eliminate_inaccessible_symbols(self):
        """
        Eliminate inaccessible symbols from the grammar.
        
        Returns:
            Grammar: A new Grammar object without inaccessible symbols
        """
        # Find all accessible symbols starting from the start symbol
        accessible = {self.start_symbol}
        
        # Iteratively find all accessible symbols
        changed = True
        while changed:
            changed = False
            for nt in list(accessible):
                if nt in self.productions:
                    for prod in self.productions[nt]:
                        for symbol in prod:
                            if symbol not in accessible and (symbol in self.non_terminals or symbol in self.terminals):
                                accessible.add(symbol)
                                changed = True
        
        # Create new sets of non-terminals and terminals
        new_non_terminals = self.non_terminals.intersection(accessible)
        new_terminals = self.terminals.intersection(accessible)
        
        # Create new productions without inaccessible symbols
        new_productions = {}
        for nt in new_non_terminals:
            if nt in self.productions:
                new_prods = []
                for prod in self.productions[nt]:
                    # Check if all symbols in the production are accessible
                    if all(symbol in accessible or symbol == 'ε' for symbol in prod):
                        new_prods.append(prod)
                
                if new_prods:
                    new_productions[nt] = new_prods
        
        # Create a new grammar without inaccessible symbols
        return Grammar(
            non_terminals=new_non_terminals,
            terminals=new_terminals,
            productions=new_productions,
            start_symbol=self.start_symbol
        )
    
    def eliminate_non_productive_symbols(self):
        """
        Eliminate non-productive symbols from the grammar.
        
        Returns:
            Grammar: A new Grammar object without non-productive symbols
        """
        # Find all productive symbols
        productive = set()
        
        # Initially, add all terminals as productive
        for nt, prods in self.productions.items():
            for prod in prods:
                if all(symbol in self.terminals or symbol == 'ε' for symbol in prod):
                    productive.add(nt)
                    break
        
        # Iteratively find all productive symbols
        changed = True
        while changed:
            changed = False
            for nt, prods in self.productions.items():
                if nt in productive:
                    continue
                
                for prod in prods:
                    if all(symbol in productive or symbol in self.terminals or symbol == 'ε' for symbol in prod):
                        productive.add(nt)
                        changed = True
                        break
        
        # Create new sets of non-terminals
        new_non_terminals = self.non_terminals.intersection(productive)
        
        # Create new productions without non-productive symbols
        new_productions = {}
        for nt in new_non_terminals:
            if nt in self.productions:
                new_prods = []
                for prod in self.productions[nt]:
                    # Check if all non-terminals in the production are productive
                    if all(symbol in productive or symbol in self.terminals or symbol == 'ε' for symbol in prod):
                        new_prods.append(prod)
                
                if new_prods:
                    new_productions[nt] = new_prods
        
        # Create a new grammar without non-productive symbols
        return Grammar(
            non_terminals=new_non_terminals,
            terminals=self.terminals.copy(),
            productions=new_productions,
            start_symbol=self.start_symbol if self.start_symbol in productive else None
        )
    
    def convert_to_cnf(self):
        """
        Convert the grammar to Chomsky Normal Form.
        
        Returns:
            Grammar: A new Grammar object in Chomsky Normal Form
        """
        # Step 1: Eliminate ε-productions
        grammar = self.eliminate_epsilon_productions()
        
        # Step 2: Eliminate renaming (unit productions)
        grammar = grammar.eliminate_renaming()
        
        # Step 3: Eliminate inaccessible symbols
        grammar = grammar.eliminate_inaccessible_symbols()
        
        # Step 4: Eliminate non-productive symbols
        grammar = grammar.eliminate_non_productive_symbols()
        
        # Step 5: Convert to CNF
        new_non_terminals = grammar.non_terminals.copy()
        new_productions = {}
        terminal_map = {}  # Maps terminals to new non-terminals
        
        # Initialize productions
        for nt in grammar.non_terminals:
            new_productions[nt] = []
        
        # Process each production
        for nt, prods in grammar.productions.items():
            for prod in prods:
                if len(prod) == 1 and prod in grammar.terminals:
                    # Rule A -> a (already in CNF)
                    new_productions[nt].append(prod)
                elif len(prod) >= 2:
                    # Convert to CNF
                    new_prod = self._convert_production_to_cnf(prod, grammar.terminals, new_non_terminals, new_productions, terminal_map)
                    new_productions[nt].append(new_prod)
        
        # Create a new grammar in CNF
        return Grammar(
            non_terminals=new_non_terminals,
            terminals=grammar.terminals.copy(),
            productions=new_productions,
            start_symbol=grammar.start_symbol
        )
    
    def _convert_production_to_cnf(self, prod, terminals, non_terminals, productions, terminal_map):
        """
        Convert a production to CNF format.
        
        Args:
            prod (str): The production to convert
            terminals (set): Set of terminal symbols
            non_terminals (set): Set of non-terminal symbols
            productions (dict): Dictionary of productions
            terminal_map (dict): Maps terminals to new non-terminals
            
        Returns:
            str: The converted production in CNF format
        """
        # Replace terminals with new non-terminals
        symbols = []
        for symbol in prod:
            if symbol in terminals:
                if symbol not in terminal_map:
                    new_nt = f"T_{symbol}"
                    terminal_map[symbol] = new_nt
                    non_terminals.add(new_nt)
                    productions[new_nt] = [symbol]
                symbols.append(terminal_map[symbol])
            else:
                symbols.append(symbol)
        
        # If the production has only two symbols, it's already in CNF
        if len(symbols) == 2:
            return ''.join(symbols)
        
        # Otherwise, create new non-terminals for groups of symbols
        while len(symbols) > 2:
            new_nt = f"X_{len(non_terminals)}"
            non_terminals.add(new_nt)
            
            # Create a new production for the last two symbols
            last_two = ''.join(symbols[-2:])
            productions[new_nt] = [last_two]
            
            # Replace the last two symbols with the new non-terminal
            symbols = symbols[:-2] + [new_nt]
        
        return ''.join(symbols)
