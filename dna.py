import random
import copy

class DNA:
    def __init__(self):
        self.genes = {}
        self.precision = 7 # radar will have int outputs from 0 to precision (inclusive)
        self.dna_len = (self.precision+1)**3 # how many genes

        self.max_steer = 4

        for a in range(self.precision+1):
            for b in range(self.precision+1):
                for c in range(self.precision+1):
                    self.genes[self.key_repr([a, b, c])] = self.random_steer()

    def random_steer(self):
        return round(random.uniform(-self.max_steer, self.max_steer), 1)

    def key_repr(self, inp):
        return ",".join(str(x) for x in inp)

    def crossover_with(self, other_parent, len_divisor):
        new_dna = copy.deepcopy(self)

        crossover_len = random.randint(0, int(round(self.dna_len / len_divisor, 0)))
        for i in range(crossover_len):
            a = random.randint(0, self.precision)
            b = random.randint(0, self.precision)
            c = random.randint(0, self.precision)
            inp = [a, b, c]

            new_dna.genes[self.key_repr(inp)] = other_parent.genes[self.key_repr(inp)]
 
        return new_dna

    def mutation(self, prob):
        for i in range(self.dna_len):
            r = random.randint(1, int(round(1/prob, 0)))
            if r == 1:
                a = random.randint(0, self.precision)
                b = random.randint(0, self.precision)
                c = random.randint(0, self.precision)
                inp = [a, b, c]

                self.genes[self.key_repr(inp)] = self.random_steer()
