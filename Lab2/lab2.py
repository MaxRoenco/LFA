class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn  # Non-terminal symbols
        self.Vt = Vt  # Terminal symbols
        self.P = P    # Production rules
        self.S = S    # Start symbol
    
    def classify_chomsky(self):
        """Classify grammar based on Chomsky hierarchy"""
        # Type 3 (Regular Grammar): A->a or A->aB
        type3 = True
        # Type 2 (Context-Free Grammar): A->α where α is a string of terminals and non-terminals
        type2 = True
        # Type 1 (Context-Sensitive Grammar): αAβ->αγβ where |γ|≥1
        type1 = True
        # Type 0 (Unrestricted Grammar): α->β
        
        for left, right_list in self.P.items():
            for right in right_list:
                # Check Type 3 (Regular)
                if len(left) != 1 or left not in self.Vn:
                    type3 = False
                
                if type3:
                    if len(right) > 2:
                        type3 = False
                    elif len(right) == 2 and (right[0] not in self.Vt or right[1] not in self.Vn):
                        type3 = False
                    elif len(right) == 1 and right not in self.Vt:
                        type3 = False
                
                # Check Type 2 (Context-Free)
                if len(left) != 1 or left not in self.Vn:
                    type2 = False
                
                # Check Type 1 (Context-Sensitive)
                if len(right) < len(left) and right != 'ε':
                    type1 = False
        
        if type3:
            return "Type 3: Regular Grammar"
        elif type2:
            return "Type 2: Context-Free Grammar"
        elif type1:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"


class FiniteAutomaton:
    def __init__(self, Q, Sigma, delta, q0, F):
        self.Q = Q          # Set of states
        self.Sigma = Sigma  # Alphabet
        self.delta = delta  # Transition function
        self.q0 = q0        # Initial state
        self.F = F          # Set of final states
    
    def is_deterministic(self):
        """Check if the finite automaton is deterministic"""
        for state in self.Q:
            for symbol in self.Sigma:
                # Get transitions for this state and symbol
                transitions = self.get_transitions(state, symbol)
                # If there are multiple transitions for the same state and symbol
                # or no transition at all, the automaton is non-deterministic
                if len(transitions) > 1:
                    return False
        return True
    
    def get_transitions(self, state, symbol):
        """Get all states reachable from a given state using a given symbol"""
        transitions = []
        for (s, sym), next_states in self.delta.items():
            if s == state and sym == symbol:
                if isinstance(next_states, list):
                    transitions.extend(next_states)
                else:
                    transitions.append(next_states)
        return transitions
    
    def to_regular_grammar(self):
        """Convert finite automaton to regular grammar"""
        Vn = self.Q
        Vt = self.Sigma
        P = {}
        S = self.q0
        
        # Initialize production rules dictionary
        for state in self.Q:
            P[state] = []
        
        # Add production rules based on transitions
        for (state, symbol), next_states in self.delta.items():
            if isinstance(next_states, list):
                for next_state in next_states:
                    # For each transition q -a-> p, add rule q -> aP
                    if next_state in self.F:
                        P[state].append(symbol)  # q -> a if p is final
                    P[state].append(symbol + next_state)  # q -> ap
            else:
                next_state = next_states
                if next_state in self.F:
                    P[state].append(symbol)  # q -> a if p is final
                P[state].append(symbol + next_state)  # q -> ap
        
        # Add ε-productions for final states (if needed)
        for state in self.F:
            if state != S:  # Avoid adding S -> ε unless necessary
                P[state].append('ε')
        
        return Grammar(Vn, Vt, P, S)
    
    def to_dfa(self):
        """Convert NDFA to DFA"""
        if self.is_deterministic():
            return self  # Already a DFA
        
        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = []
        
        # Start with the initial state
        unmarked_states = [{self.q0}]
        dfa_states = [frozenset({self.q0})]
        
        while unmarked_states:
            current_state_set = unmarked_states.pop(0)
            current_state_frozen = frozenset(current_state_set)
            
            for symbol in self.Sigma:
                next_state_set = set()
                for state in current_state_set:
                    # Get all next states for this state and symbol
                    next_states = self.get_transitions(state, symbol)
                    next_state_set.update(next_states)
                
                if not next_state_set:
                    continue
                
                next_state_frozen = frozenset(next_state_set)
                
                # Add transition from current_state_set to next_state_set with symbol
                dfa_transitions[(current_state_frozen, symbol)] = next_state_frozen
                
                # If this is a new state, add it to the list of states
                if next_state_frozen not in dfa_states:
                    dfa_states.append(next_state_frozen)
                    unmarked_states.append(next_state_set)
                    
                    # Check if this new state contains any final states
                    if any(state in self.F for state in next_state_set):
                        dfa_final_states.append(next_state_frozen)
            
            # Check if current state contains any final states
            if any(state in self.F for state in current_state_set):
                dfa_final_states.append(current_state_frozen)
        
        # Convert frozen sets back to strings for easier visualization
        state_mapping = {state: f"q{i}" for i, state in enumerate(dfa_states)}
        
        new_Q = list(state_mapping.values())
        new_delta = {}
        
        for (state_set, symbol), next_state_set in dfa_transitions.items():
            new_delta[(state_mapping[state_set], symbol)] = state_mapping[next_state_set]
        
        new_q0 = state_mapping[frozenset({self.q0})]
        new_F = [state_mapping[state] for state in dfa_final_states]
        
        return FiniteAutomaton(new_Q, self.Sigma, new_delta, new_q0, new_F)


# Implementation for Variant 25
def main():
    # Define the finite automaton based on Variant 25
    Q = {'q0', 'q1', 'q2', 'q3'}
    Sigma = {'a', 'b'}
    delta = {
        ('q0', 'a'): ['q0', 'q1'],  # Non-deterministic transition
        ('q1', 'a'): 'q2',
        ('q1', 'b'): 'q1',
        ('q2', 'a'): 'q3',
        ('q3', 'a'): 'q1'
    }
    q0 = 'q0'
    F = {'q2'}
    
    # Create the FA
    fa = FiniteAutomaton(Q, Sigma, delta, q0, F)
    
    # Check if the FA is deterministic
    is_det = fa.is_deterministic()
    print(f"Is the FA deterministic? {is_det}")
    
    # Convert FA to regular grammar
    grammar = fa.to_regular_grammar()
    print("\nRegular Grammar:")
    print(f"Non-terminals: {grammar.Vn}")
    print(f"Terminals: {grammar.Vt}")
    print("Productions:")
    for left, right_list in grammar.P.items():
        if right_list:
            print(f"{left} -> {' | '.join(right_list)}")
    print(f"Start symbol: {grammar.S}")
    
    # Classify the grammar based on Chomsky hierarchy
    print(f"\nGrammar classification: {grammar.classify_chomsky()}")
    
    # Convert NDFA to DFA
    dfa = fa.to_dfa()
    print("\nConverted DFA:")
    print(f"States: {dfa.Q}")
    print(f"Alphabet: {dfa.Sigma}")
    print("Transitions:")
    for (state, symbol), next_state in dfa.delta.items():
        print(f"δ({state}, {symbol}) = {next_state}")
    print(f"Initial state: {dfa.q0}")
    print(f"Final states: {dfa.F}")
    print(f"Is the new FA deterministic? {dfa.is_deterministic()}")

if __name__ == "__main__":
    main()
