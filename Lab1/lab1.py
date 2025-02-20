class FiniteAutomaton:
    def __init__(self, Q, Sigma, Delta, Q0, QF):
        self.Q = Q  # States
        self.Sigma = Sigma  # Alphabet
        self.Delta = Delta  # Transitions
        self.Q0 = Q0  # Initial state
        self.QF = QF  # Final states
    
    def does_string_belong_to_language(self, input_string):
        current_states = {self.Q0}
        print(f"\nChecking string: \"{input_string}\"")
        
        for letter in input_string:
            print(f"Processing letter: \"{letter}\"")
            if letter not in self.Sigma:
                print(f"Invalid character \"{letter}\".")
                return False
            
            next_states = set()
            for state in current_states:
                if state in self.Delta and letter in self.Delta[state]:
                    next_states.update(self.Delta[state][letter])
            
            if not next_states:
                print(f"No valid transitions found. \"{input_string}\" is INVALID.")
                return False
            
            current_states = next_states
            print(f"Possible next states: {', '.join(current_states)}")
        
        is_valid = any(state in self.QF for state in current_states)
        print(f"Final states: {', '.join(current_states)}")
        print(f"Result: \"{input_string}\" is {'VALID ✓' if is_valid else 'INVALID ✗'}")
        return is_valid
    
    def generate_valid_string(self, max_length=10):
        import random
        
        current_state = self.Q0
        result = ''
        steps = 0
        
        while steps < max_length:
            if current_state not in self.Delta:
                break
            
            possible_transitions = self.Delta[current_state]
            if not possible_transitions:
                break
            
            transitions = list(possible_transitions.items())
            letter, next_states = random.choice(transitions)
            next_state = random.choice(list(next_states))
            
            result += letter
            current_state = next_state
            steps += 1
            
            if current_state in self.QF:
                return result
        
        return None
    
    def show_valid_transitions(self):
        print("\nValid State Transitions:")
        print("------------------------")
        for state, transitions in self.Delta.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    print(f"State {state} --{symbol}--> State {next_state}")


class Grammar:
    def __init__(self, vN, vT, p, s):
        self.VN = vN  # Non-terminals
        self.VT = vT  # Terminals
        self.P = p    # Production rules
        self.S = s    # Start symbol
    
    def create_word(self):
        import random
        
        word_in_progress = self.S
        print("\nGenerating word:", word_in_progress)
        
        while True:
            found_non_terminal = False
            for i, current_char in enumerate(word_in_progress):
                if current_char in self.VN:
                    found_non_terminal = True
                    rules = self.P.get(current_char, [])
                    if not rules:
                        continue
                    
                    used_replacement = random.choice(rules)
                    word_in_progress = word_in_progress[:i] + used_replacement + word_in_progress[i+1:]
                    print(" =>", word_in_progress)
                    break
            
            if not found_non_terminal:
                break
        
        return word_in_progress
    
    def to_finite_automaton(self):
        q_f = {"q_F"}
        q = self.VN.union(q_f)
        sigma = self.VT.copy()
        q0 = self.S
        delta = {}
        
        for key, products in self.P.items():
            for product in products:
                terminal = product[0]
                non_terminal = product[1] if len(product) > 1 else "q_F"
                
                if terminal not in self.VT:
                    continue
                
                state_transitions = delta.get(key, {})
                target_states = state_transitions.get(terminal, set())
                target_states.add(non_terminal)
                state_transitions[terminal] = target_states
                delta[key] = state_transitions
        
        return FiniteAutomaton(q, sigma, delta, q0, q_f)
    
    def __str__(self):
        output = f"V_N = {{ {', '.join(self.VN)} }}\n"
        output += f"V_T = {{ {', '.join(self.VT)} }}\n"
        output += "P = {\n"
        
        for key, values in self.P.items():
            output += f"    {key} ---> {' | '.join(values)}\n"
        
        output += "}\n"
        output += f"S = {{ {self.S} }}\n"
        return output


def generate_random_string(vT):
    import random
    
    some_string = ''
    alphabet_array = list(vT)
    length = random.randint(3, 10)
    
    for _ in range(length):
        some_string += random.choice(alphabet_array)
    
    return some_string


def main():
    import random
    
    print("Laboratory Work 1: Intro to formal languages. Regular grammars. Finite Automata.\n")
    print("Student: Roenco Maxim\nGroup: FAF-231\nVariant 25\n")
    
    vN = {"S", "A", "B"}
    vT = {"a", "b", "c", "d"}
    p = {
        "S": ["bS", "dA"],
        "A": ["aA", "dB", "b"],
        "B": ["cB", "a"]
    }
    s = "S"
    
    grammar = Grammar(vN, vT, p, s)
    print("Grammar:")
    print(grammar)
    
    print("\n5 valid strings by grammar:")
    for i in range(5):
        print(f"\nString {i + 1}:")
        generated_string = grammar.create_word()
        print("Final string:", generated_string)
    
    finite_automaton = grammar.to_finite_automaton()
    print("\nTesting random strings with the Finite Automaton:")
    for i in range(5):
        test_string = generate_random_string(vT)
        print(f"\nTest string {i + 1}: {test_string}")
        belongs = finite_automaton.does_string_belong_to_language(test_string)
        print(f"String belongs to language: {belongs}")
    
    print("\nEnter a string to check if it belongs to the language (type 'exit' to quit):")
    
    while True:
        input_string = input("> ")
        if input_string.lower() == "exit":
            print("Exiting...")
            break
        else:
            belongs = finite_automaton.does_string_belong_to_language(input_string)
            print(f"String belongs to language: {belongs}")


if __name__ == "__main__":
    main()

