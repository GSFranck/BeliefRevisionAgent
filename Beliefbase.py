from sympy import symbols, Not, And, Or
from sympy.logic import to_cnf, simplify_logic
from sympy.logic.inference import satisfiable

class BeliefRevisionAgent:
    def __init__(self):
        self.belief_base = []

    def add_belief(self, belief):
        self.belief_base.append(belief)

    def remove_belief(self, belief):
        self.belief_base.remove(belief)

    def check_entailment(self, belief):
        cnf = And(*self.belief_base)
        neg_belief = Not(belief)
        combined_cnf = And(cnf, neg_belief)
        return not satisfiable(combined_cnf)



    def resolve(self, c1, c2):
        resolvents = set()
        for l1 in c1:
            for l2 in c2:
                if l1 == ~l2:
                    resolvents.add(frozenset(c1 | c2) - {l1, l2})
        return resolvents

    def contract(self, belief):
        if not self.check_entailment(belief):
            return

        remaining_beliefs = [b for b in self.belief_base if b != belief]
        belief_powerset = self.get_powerset(remaining_beliefs)
        belief_powerset.sort(key=lambda x: len(x), reverse=True)

        for subset in belief_powerset:
            if not self.check_entailment(And(*subset, belief)):
                self.belief_base = subset
                return

    def expand(self, belief):
        cnf_belief = to_cnf(belief)
        if not self.check_entailment(cnf_belief):
            self.add_belief(cnf_belief)



    def get_powerset(self, s):
        powerset = [[]]
        for elem in s:
            powerset += [subset + [elem] for subset in powerset]
        return powerset
    def agm_postulates(self):
        # Test the Success postulate
        print("Success postulate:")
        belief = symbols("p")
        self.expand(belief)
        if self.check_entailment(belief):
            print("Passed")
        else:
            print("Failed")

        # Test the Inclusion postulate
        print("Inclusion postulate:")
        belief = symbols("q")
        self.expand(belief)
        if all([self.check_entailment(b) for b in self.belief_base]):
            print("Passed")
        else:
            print("Failed")

        # Test the Vacuity postulate
        print("Vacuity postulate:")
        belief = symbols("r")
        self.contract(belief)
        if not self.check_entailment(belief):
            print("Passed")
        else:
            print("Failed")

        # Test the Consistency postulate
        print("Consistency postulate:")
        self.contract(symbols("p"))
        self.contract(symbols("q"))
        if not self.check_entailment(And(symbols("p"), symbols("q"))):
            print("Passed")
        else:
            print("Failed")

        # Test the Extensionality postulate
        print("Extensionality postulate:")
        belief_base_copy = self.belief_base.copy()
        belief_base_copy.sort()
        for belief in belief_base_copy:
            self.contract(belief)
        if len(self.belief_base) == 0:
            print("Passed")
        else:
            print("Failed")
