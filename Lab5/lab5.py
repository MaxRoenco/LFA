
"""
Chomsky Normal Form (CNF) Conversion Script

This script implements the steps to convert a given context-free grammar
into Chomsky Normal Form.

It can process any context-free grammar provided in the expected Python data structure format.
"""

import copy

class CFG:
    def __init__(self, vn, vt, p, s, grammar_name="UnnamedGrammar"):
        self.original_vn = set(vn) # Store original non-terminals for reference
        self.original_vt = set(vt)
        self.original_p = self._parse_productions(copy.deepcopy(p)) # Deepcopy for safety
        self.original_s = s

        self.vn = set(vn)
        self.vt = set(vt)
        self.p = self._parse_productions(p) # p is already parsed by the time it gets here if called from main
        self.s = s
        self.grammar_name = grammar_name
        self.new_nt_counters = {"T": 1, "Z": 1} # Counters for new non-terminal generation

    def _parse_productions(self, productions_dict):
        parsed_p = {}
        for lhs, rhss in productions_dict.items():
            parsed_p[lhs] = []
            for rhs_tuple in rhss:
                if rhs_tuple == ["ε"] or rhs_tuple == ["epsilon"]:
                    parsed_p[lhs].append([]) 
                else:
                    parsed_p[lhs].append(list(rhs_tuple))
        return parsed_p

    def __str__(self):
        p_str = []
        # Sort productions for consistent output: by LHS, then by RHS representation
        sorted_p_items = sorted(self.p.items())
        
        for lhs, rhss in sorted_p_items:
            try:
                sorted_rhss = sorted(rhss, key=lambda r: " ".join(map(str, r)))
            except TypeError: 
                sorted_rhss = rhss 

            for rhs in sorted_rhss:
                rhs_representation = " ".join(rhs) if rhs else "ε"
                p_str.append(f"  {lhs} -> {rhs_representation}")
        
        vn_str = ", ".join(sorted(list(self.vn)))
        vt_str = ", ".join(sorted(list(self.vt)))
        productions_str = "\n".join(p_str)

        return (
            f"VN = {{ {vn_str} }}\n"
            f"VT = {{ {vt_str} }}\n"
            f"S = {self.s}\n"
            f"P = {{\n{productions_str}\n}}"
        )

    def _add_production(self, lhs, rhs_list, target_p=None):
        current_p_ref = target_p if target_p is not None else self.p
        if lhs not in current_p_ref:
            current_p_ref[lhs] = []
        processed_rhs = list(rhs_list) 
        if processed_rhs == ["ε"] or processed_rhs == ["epsilon"]:
            processed_rhs = [] 
        if processed_rhs not in current_p_ref[lhs]:
            current_p_ref[lhs].append(processed_rhs)
            return True 
        return False

    def eliminate_epsilon_productions(self):
        print("\n--- Step 1: Eliminating ε-productions ---")
        nullable = set()
        for lhs, rhss in self.p.items():
            for rhs in rhss:
                if not rhs: 
                    nullable.add(lhs)
        
        changed_in_nullable_set = True
        while changed_in_nullable_set:
            changed_in_nullable_set = False
            for lhs, rhss in self.p.items():
                if lhs in nullable: continue
                for rhs in rhss:
                    if rhs and all(s in nullable for s in rhs if s in self.vn):
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed_in_nullable_set = True
        print(f"Nullable variables: {nullable}")

        new_p_after_eps_elim = {}
        for lhs_orig, rhss_orig_list in self.p.items():
            for rhs_orig in rhss_orig_list:
                if not rhs_orig: continue 
                nullable_indices_in_rhs = [i for i, symbol in enumerate(rhs_orig) if symbol in nullable]
                num_nullable_in_this_rhs = len(nullable_indices_in_rhs)
                for i in range(1 << num_nullable_in_this_rhs):
                    current_new_rhs = []
                    omitted_this_round_indices = set()
                    for k_idx in range(num_nullable_in_this_rhs):
                        if (i >> k_idx) & 1:
                            omitted_this_round_indices.add(nullable_indices_in_rhs[k_idx])
                    for symbol_idx, symbol_val in enumerate(rhs_orig):
                        if symbol_idx in nullable_indices_in_rhs:
                            if symbol_idx not in omitted_this_round_indices:
                                current_new_rhs.append(symbol_val)
                        else: current_new_rhs.append(symbol_val)
                    if current_new_rhs: 
                        self._add_production(lhs_orig, current_new_rhs, target_p=new_p_after_eps_elim)
        self.p = {k: v for k, v in new_p_after_eps_elim.items() if v}
        print("Grammar after eliminating ε-productions:")
        print(self)

    def eliminate_renaming(self):
        print("\n--- Step 2: Eliminating renaming (unit productions) ---")
        while True:
            p_snapshot_before_pass = copy.deepcopy(self.p)
            p_after_unit_elim_pass = {}
            any_unit_rule_processed_this_pass = False

            for lhs, rhss_list in p_snapshot_before_pass.items():
                rules_for_lhs_after_pass = []
                for rhs in rhss_list:
                    if len(rhs) == 1 and rhs[0] in self.vn:
                        b_symbol = rhs[0]
                        any_unit_rule_processed_this_pass = True # A unit rule A->B was encountered
                        if lhs == b_symbol: # A -> A, remove
                            continue # Don't add to rules_for_lhs_after_pass
                        # For A -> B, add A -> alpha for all B -> alpha (from snapshot)
                        if b_symbol in p_snapshot_before_pass:
                            for b_rhs_rule in p_snapshot_before_pass[b_symbol]:
                                if b_rhs_rule not in rules_for_lhs_after_pass:
                                    rules_for_lhs_after_pass.append(b_rhs_rule)
                    else: # Not a unit rule, keep it
                        if rhs not in rules_for_lhs_after_pass:
                            rules_for_lhs_after_pass.append(rhs)
                
                if rules_for_lhs_after_pass:
                    p_after_unit_elim_pass[lhs] = rules_for_lhs_after_pass
            
            if self.p == p_after_unit_elim_pass and not any_unit_rule_processed_this_pass:
                # If no unit rules were found to process, and P is same, then stable.
                # Or if unit rules were processed but resulted in the same grammar (e.g. A->B, B->A resolved to A->A then removed)
                break
            self.p = {k:v for k,v in p_after_unit_elim_pass.items() if v} # Update and clean
            if not any_unit_rule_processed_this_pass and p_snapshot_before_pass == self.p:
                 # This condition means no unit rules were found AND the grammar didn't change due to other cleanups.
                 break

        print("Grammar after eliminating renaming:")
        print(self)

    def eliminate_inaccessible_symbols(self):
        print("\n--- Step 3: Eliminating inaccessible symbols ---")
        if not self.s or self.s not in self.vn:
            print(f"Warning: Start symbol \'{self.s}\' is not defined or not in current non-terminals. Grammar might be empty or invalid.")
            self.p = {}
            self.vn = set() if not self.s else {self.s}.intersection(self.original_vn) # Keep S if it was original
            self.vt = set()
            print(self); return

        reachable_non_terminals = {self.s}
        worklist = [self.s]
        while worklist:
            current_nt = worklist.pop(0)
            if current_nt in self.p:
                for rhs in self.p[current_nt]:
                    for symbol in rhs:
                        if symbol in self.vn and symbol not in reachable_non_terminals:
                            reachable_non_terminals.add(symbol); worklist.append(symbol)
        
        self.vn = reachable_non_terminals
        p_after_inacc_elim = {}
        active_terminals = set()
        for lhs, rhss_list in self.p.items():
            if lhs in self.vn:
                current_lhs_rules = []
                for rhs in rhss_list:
                    if all((s in self.vn or s in self.vt) for s in rhs):
                        current_lhs_rules.append(rhs)
                        for symbol_in_rhs in rhs:
                            if symbol_in_rhs in self.vt: active_terminals.add(symbol_in_rhs)
                if current_lhs_rules: p_after_inacc_elim[lhs] = current_lhs_rules
        self.p = p_after_inacc_elim
        self.vt = active_terminals
        print("Grammar after eliminating inaccessible symbols:")
        print(self)

    def eliminate_non_productive_symbols(self):
        print("\n--- Step 4: Eliminating non-productive symbols ---")
        if not self.p:
            print("Grammar has no productions. Language is empty.")
            if self.s in self.original_vn: self.vn = {self.s} # Keep S if it was original, though non-productive
            else: self.vn = set()
            self.p = {}; self.vt = set()
            print(self); return

        productive_nts = set()
        non_prod_changed_iteration = True
        while non_prod_changed_iteration:
            non_prod_changed_iteration = False
            for lhs, rhss_list in self.p.items():
                if lhs not in productive_nts:
                    for rhs in rhss_list:
                        is_rhs_currently_productive = True
                        if not rhs: is_rhs_currently_productive = False # ε is not productive here
                        else:
                            for symbol_in_rhs in rhs:
                                if symbol_in_rhs in self.vn and symbol_in_rhs not in productive_nts:
                                    is_rhs_currently_productive = False; break
                                elif symbol_in_rhs not in self.vt and symbol_in_rhs not in self.vn:
                                    is_rhs_currently_productive = False; break
                        if is_rhs_currently_productive:
                            if lhs not in productive_nts:
                                productive_nts.add(lhs); non_prod_changed_iteration = True; break
        self.vn = productive_nts
        p_after_non_prod_elim = {}
        active_terminals_after_nonprod = set()
        for lhs, rhss_list in self.p.items():
            if lhs in self.vn:
                current_lhs_productive_rules = []
                for rhs in rhss_list:
                    if all((s_in_rhs in self.vn and s_in_rhs in productive_nts) or s_in_rhs in self.vt for s_in_rhs in rhs):
                        current_lhs_productive_rules.append(rhs)
                        for s_final_check in rhs:
                            if s_final_check in self.vt: active_terminals_after_nonprod.add(s_final_check)
                if current_lhs_productive_rules: p_after_non_prod_elim[lhs] = current_lhs_productive_rules
        self.p = p_after_non_prod_elim
        self.vt = active_terminals_after_nonprod
        if self.s in self.original_vn and self.s not in self.vn:
            print(f"Warning: Start symbol \'{self.s}\' became non-productive. Language is empty.")
            self.p = {}; self.vt = set() # Clear productions and terminals
        print("Grammar after eliminating non-productive symbols:")
        print(self)

    def _get_new_non_terminal(self, base_prefix="X"):
        # Use class-level counters for T_ and Z_ type new non-terminals
        # Ensure base_prefix is either 'T' or 'Z' or default to 'X'
        prefix_key = base_prefix if base_prefix in self.new_nt_counters else "X"
        if prefix_key == "X" and prefix_key not in self.new_nt_counters: # Generic X counter
            self.new_nt_counters["X"] = 1
        
        idx = self.new_nt_counters[prefix_key]
        all_known_symbols = self.vn.union(self.vt).union(set(self.p.keys()))
        # Also consider symbols that might be generated and added to VN later in the same step
        # This is tricky. For now, check against current state.
        while True:
            new_nt = f"{base_prefix.upper()}{idx}"
            if new_nt not in all_known_symbols:
                self.new_nt_counters[prefix_key] += 1
                return new_nt
            idx += 1
            if idx > 1000: # Safety break for runaway counter
                 # Fallback to more generic naming if many clashes
                 base_prefix = "NT"
                 if "NT" not in self.new_nt_counters: self.new_nt_counters["NT"] =1
                 prefix_key = "NT"
                 idx = self.new_nt_counters["NT"]
                 print(f"Warning: High new NT index for {base_prefix}, switching to NT{idx}")

    def obtain_chomsky_normal_form(self):
        print("\n--- Step 5: Obtaining Chomsky Normal Form ---")
        # Reset counters for each CNF conversion if the object is reused, or ensure they are instance specific.
        # They are instance specific (self.new_nt_counters) initialized in __init__.
        self.new_nt_counters = {"T": 1, "Z": 1} # Fresh counters for this specific CNF pass

        # Phase 1 (TERM): A -> a or A -> X Y Z... (all X,Y,Z are NTs)
        p_after_term_step = {}
        terminal_to_nt_map = {}
        for lhs, rhss_list in self.p.items():
            for rhs in rhss_list:
                if len(rhs) == 1 and rhs[0] in self.vt: # A -> a
                    self._add_production(lhs, rhs, target_p=p_after_term_step); continue
                new_rhs_for_term_step = []
                modified_rhs = False
                if len(rhs) > 1: # Only for rules with length > 1, e.g. A -> aB, A -> BC
                    for symbol in rhs:
                        if symbol in self.vt:
                            modified_rhs = True
                            if symbol not in terminal_to_nt_map:
                                new_t_nt = self._get_new_non_terminal(f"T_{symbol.upper()}")
                                terminal_to_nt_map[symbol] = new_t_nt
                                self.vn.add(new_t_nt)
                                self._add_production(new_t_nt, [symbol], target_p=p_after_term_step)
                            new_rhs_for_term_step.append(terminal_to_nt_map[symbol])
                        else: new_rhs_for_term_step.append(symbol)
                    self._add_production(lhs, new_rhs_for_term_step, target_p=p_after_term_step)
                else: # A -> B (single NT) or A -> a (already handled)
                    self._add_production(lhs, rhs, target_p=p_after_term_step)
        self.p = {k:v for k,v in p_after_term_step.items() if v}
        print("Grammar after TERM Chomsky step (A->a or A->X Y...):"); print(self)

        # Phase 2 (BIN): A -> B C
        bin_outer_loop_changed = True
        while bin_outer_loop_changed:
            bin_outer_loop_changed = False
            p_after_bin_pass = {}
            for lhs, rhss_list in self.p.items():
                for rhs in rhss_list:
                    if len(rhs) <= 2: # A->a, A->X (if X is NT, should be unit-eliminated), A->XY
                        self._add_production(lhs, rhs, target_p=p_after_bin_pass); continue
                    bin_outer_loop_changed = True
                    current_lhs_for_bin = lhs
                    symbols_to_binarize = list(rhs)
                    for i in range(len(symbols_to_binarize) - 2):
                        n_i = symbols_to_binarize[i]
                        new_intermediate_nt = self._get_new_non_terminal(f"Z")
                        self.vn.add(new_intermediate_nt)
                        self._add_production(current_lhs_for_bin, [n_i, new_intermediate_nt], target_p=p_after_bin_pass)
                        current_lhs_for_bin = new_intermediate_nt
                    self._add_production(current_lhs_for_bin, [symbols_to_binarize[-2], symbols_to_binarize[-1]], target_p=p_after_bin_pass)
            if bin_outer_loop_changed: self.p = {k:v for k,v in p_after_bin_pass.items() if v}
        print("Grammar after BIN Chomsky step (A->a or A->BC):"); print(self)

    def convert_to_cnf(self, grammar_variant_steps=True):
        print(f"\n=== Processing Grammar: {self.grammar_name} ===")
        # Store original S nullability before any transformations
        s_was_originally_nullable = self.check_original_s_nullable()
        print("Original Grammar:"); print(self)

        if grammar_variant_steps:
            self.eliminate_epsilon_productions()
            self.eliminate_renaming()
            self.eliminate_inaccessible_symbols()
            self.eliminate_non_productive_symbols()
            self.obtain_chomsky_normal_form()
        else: # Standard textbook order (example)
            self.eliminate_epsilon_productions()
            self.eliminate_renaming()
            self.eliminate_non_productive_symbols()
            self.eliminate_inaccessible_symbols()
            self.obtain_chomsky_normal_form()

        if s_was_originally_nullable and self.s in self.vn and self.s == self.original_s:
            # If original S was nullable, and current S is the same start symbol and is productive,
            # CNF allows adding S -> ε.
            # The 5 steps eliminate all ε. This is an optional re-addition for strict CNF compliance if L(G) includes ε.
            # For this assignment, we stick to the 5 steps. This is a note.
            print(f"Note: Original start symbol \'{self.s}\' was nullable. Standard CNF might add {self.s} -> ε.")
            print("Adhering to the 5 transformation steps which eliminate all ε-productions first.")

        print("\n--- Final CNF Grammar (after specified steps) ---"); print(self)
        return self.p, self.vn, self.vt, self.s

    def check_original_s_nullable(self):
        # Check nullability on a temporary copy of the original grammar state
        temp_cfg = CFG(self.original_vn, self.original_vt, self.original_p, self.original_s, "temp_check")
        nullable_s_check = set()
        for l, r_list in temp_cfg.p.items():
            for r_val in r_list: 
                if not r_val: nullable_s_check.add(l)
        changed_s_check = True
        while changed_s_check:
            changed_s_check = False
            for l, r_list in temp_cfg.p.items():
                if l in nullable_s_check: continue
                for r_val in r_list:
                    if r_val and all(s_val in nullable_s_check for s_val in r_val if s_val in temp_cfg.vn):
                        if l not in nullable_s_check: nullable_s_check.add(l); changed_s_check = True
        return self.original_s in nullable_s_check

# Main execution for testing
if __name__ == "__main__":
    # Variant 22 Grammar
    vn_v22 = {"S", "A", "B", "C", "E"}
    vt_v22 = {"a", "b"}
    p_v22 = {
        "S": [["a", "B"], ["A", "C"]],
        "A": [["a"], ["A", "C", "S", "C"], ["B", "C"]],
        "B": [["b"], ["a", "A"]],
        "C": [["ε"]]
    }
    s_v22 = "S"
    grammar_v22 = CFG(vn_v22, vt_v22, p_v22, s_v22, grammar_name="Variant 22")
    # Output will be redirected by shell command
    grammar_v22.convert_to_cnf(grammar_variant_steps=True)

    # Wikipedia Example Grammar (for testing generalization)
    # S -> ASA | aB, A -> B | S, B -> b | ε
    vn_wiki = {"S", "A", "B"}
    vt_wiki = {"a", "b"}
    p_wiki = {
        "S": [["A", "S", "A"], ["a", "B"]],
        "A": [["B"], ["S"]],
        "B": [["b"], ["ε"]]
    }
    s_wiki = "S"
    grammar_wiki = CFG(vn_wiki, vt_wiki, p_wiki, s_wiki, grammar_name="Wikipedia Example")
    grammar_wiki.convert_to_cnf(grammar_variant_steps=True) # Using same 5 steps for consistency

    # Another example: Simple grammar already in CNF (or close)
    vn_simple = {"S", "A", "B"}
    vt_simple = {"a", "b"}
    p_simple = {
        "S": [["A", "B"]],
        "A": [["a"]],
        "B": [["b"]]
    }
    s_simple = "S"
    grammar_simple = CFG(vn_simple, vt_simple, p_simple, s_simple, grammar_name="Simple CNF-like")
    grammar_simple.convert_to_cnf(grammar_variant_steps=True)

    # Example with more complex epsilon elimination and unit rules
    vn_complex_eps = {"S", "A", "B", "C", "D"}
    vt_complex_eps = {"a", "b"}
    p_complex_eps = {
        "S": [["A", "B", "C"]],
        "A": [["a"], ["ε"]],
        "B": [["A"], ["D"], ["b"]],
        "C": [["A"], ["ε"]],
        "D": [["B"], ["ε"]]
    }
    s_complex_eps = "S"
    grammar_complex_eps = CFG(vn_complex_eps, vt_complex_eps, p_complex_eps, s_complex_eps, grammar_name="Complex Epsilon/Unit")
    grammar_complex_eps.convert_to_cnf(grammar_variant_steps=True)


