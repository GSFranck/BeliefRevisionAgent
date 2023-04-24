from operator import neg

from sympy import And, Or
from sympy.logic import to_cnf

class BeliefRevisonAgent:
    """
    Belief base that implements epistemic entrenchment
    with finite partial entrenchment ranking.
    Each belief is assigned an order (a real number between 0 and 1)
    which determines its entrenchment, i.e. the level of commitment
    to maintain it when applying a change function (contraction,
    revision, etc).
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
                    result = [x for x in self._make_literals(Ci) if x != li] + [x for x in self._make_literals(Cj) if x != lj]
                    result = list(set(result)) # remove duplicates
                    
                    if len(result) == 0:
                        resolvents.append(False)
                    elif len(result) == 1:
                        resolvents.extend(result)
                    else:
                        resolvents.append(Or(*result))
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
                    self._retract(s)
    
    def expand(self, sentence):
        # check for logical closure (if sentence is entailed it is already implicit understood in BB)
        if not self.pl_resolution(sentence):
            self.add(sentence)

    def revise(self, sentence):
        self._retract(~sentence)
        self.expand(sentence)

    def _retract(self, sentence):
        sentence = to_cnf(sentence)
        if sentence in self.belif_base:
            self.belif_base.remove(sentence)

    def clear(self):
        self.belif_base.clear()

        