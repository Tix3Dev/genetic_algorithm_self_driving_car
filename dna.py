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
                    self.genes[self.key_repr([a, b, c])] = self.random_steer()

    def random_steer(self):
        return round(random.uniform(-self.max_steer, self.max_steer), 1)

    def key_repr(self, inp):
        return ",".join(str(x) for x in inp)

    def crossover_with(self, other_parent):
        swapped_already = []
        

        crossover_len = random.randint(0, self.dna_len)
        for i in range(crossover_len):
            a = random.randint(0, self.precision)
            b = random.randint(0, self.precision)
            c = random.randint(0, self.precision)
            inp = [a, b, c]

            if inp in swapped_already:
                # NOTE: this will most likely be called at some point,
                # decreasing the total number of swapped genes at the end,
                # since it will already skip to another iteration (and won't retry)
                continue
            swapped_already.append(inp)

            self.genes[self.key_repr(inp)] = other_parent.genes[self.key_repr(inp)]
 
        return self

    def mutation(self, prob):
        for i in range(self.dna_len):
            r = random.randint(1, 1/prob)
            if r == 1:
                a = random.randint(0, self.precision)
                b = random.randint(0, self.precision)
                c = random.randint(0, self.precision)
                inp = [a, b, c]

                self.genes[self.key_repr(inp)] = self.random_steer()
                print("genes mutated:", i)
