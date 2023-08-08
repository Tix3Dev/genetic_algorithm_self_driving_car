import random

class DNA:
    def __init__(self):
        self.genes = {}
        self.precision = 7 # radar will have int outputs from 0 to precision (inclusive)
        self.dna_len = (self.precision+1)**3 # how many genes

        self.max_steer = 3

        for a in range(self.precision+1):
            for b in range(self.precision+1):
                for c in range(self.precision+1):
                    self.genes[self.key_repr([a, b, c])] = round(random.uniform(-self.max_steer, self.max_steer), 1)
        
    def key_repr(self, inp):
        return ",".join(str(x) for x in inp)
