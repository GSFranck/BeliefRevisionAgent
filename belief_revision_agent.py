from sympy import And, Or
from sympy.logic import to_cnf

class BeliefRevisonAgent:
    """
        This is an implementation of a belief revision agent. It holds a belief base (list) of propositional logic sentences and has
        methods like pl_resolution, contract, expand and revise to alter the belief base. 
    """

    def __init__(self):
        # Belief base
        self.belif_base = []

    def add(self, sentence):
        sentence = to_cnf(sentence)
        self.belif_base.append(sentence)

    def pl_resolution(self, sentence, base=None):
        """
        Resolution based entailment check implemented based on figure 7.12 in the book "AI - A Modern Aproach". 
        Takes a sentence in propositional logic and returns boolean value True if the set clauses BB & not(sentence) is unsatisfiable; 
        and returns False otherwise. 
        """
        if base == None:
            base = self.belif_base
        
        clauses = []
        for s in base:
            clauses.extend(self._make_clauses(s))
        
        # Add contradiction
        not_sentence = to_cnf(~sentence)
        clauses.extend(self._make_clauses(not_sentence))
        
        # Create list of unique pairs of clauses in clauses
        new = set()
        while True:
            n = len(clauses)
            for ci, cj in [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]:
                resolvents = self._pl_resolve(ci, cj)
                if False in resolvents:
                    return True
                
                new = new.union(set(resolvents))
            
            if new.issubset(set(clauses)):
                return False
                
            clauses = list(set(clauses).union(new))
        
        
    def _pl_resolve(self, Ci, Cj):
        resolvents = []
        for li in self._make_literals(Ci):
            for lj in self._make_literals(Cj):
                if li == ~lj or ~li == lj:
                    resolved = [l for l in self._make_literals(Ci) if l != li] + [l for l in self._make_literals(Cj) if l != lj]
                    resolved = list(set(resolved)) # remove duplicates
                    
                    if len(resolved) == 0:
                        resolvents.append(False)
                    elif len(resolved) == 1:
                        resolvents.extend(resolved)
                    else:
                        resolvents.append(Or(*resolved))
        return resolvents

    # Function that splits a sentence on CNF form into clauses
    def _make_clauses(self, expr) -> tuple:
        if not isinstance(expr, And):
            return expr,
        return expr.args
    
    # Function that splits a clause into literals
    def _make_literals(self, expr) -> tuple:
        if not isinstance(expr, Or):
            return expr,
        return expr.args

    def contract(self, sentence):
        sentence = to_cnf(sentence)
        # check if sentence is a tautology
        if not self.pl_resolution(sentence, base=[]):
            for s in self.belif_base:
                base=[to_cnf(Or(sentence, s))]
                if self.pl_resolution(sentence, base):
                    continue
                else:
                    self._remove(s)
    
    def expand(self, sentence):
        # check for logical closure (if sentence is entailed it is already implicit understood in BB)
        if not self.pl_resolution(sentence):
            self.add(sentence)

    def revise(self, sentence):
        self._remove(~sentence)
        self.expand(sentence)

    def _remove(self, sentence):
        sentence = to_cnf(sentence)
        if sentence in self.belif_base:
            self.belif_base.remove(sentence)

    def clear(self):
        self.belif_base.clear()

        