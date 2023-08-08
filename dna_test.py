import random

poss_inp1 = [0, 3, 4]
poss_inp2 = [2, 4, 1]
poss_inp3 = [5, 0, 4]

out_val1 = 2
out_val2 = -1
out_val3 = 3

dna = {}

def key_repr_of_inp(inp):
    return ",".join(str(x) for x in inp)

dna[key_repr_of_inp(poss_inp1)] = out_val1
dna[key_repr_of_inp(poss_inp2)] = out_val2
dna[key_repr_of_inp(poss_inp3)] = out_val3

print(dna)

# given an input, find output
arb_inp = [2, 4, 1]
print("output:", dna[key_repr_of_inp(arb_inp)])

#########
print("----------")

n = 7 # n is inclusive!
dna_len = (n+1)**3

for a in range(n+1):
    for b in range(n+1):
        for c in range(n+1):
            dna[key_repr_of_inp([a, b, c])] = random.randint(-5, 5)


print(len(dna))
print(dna)

#########
print("----------")

print("crossover")
swapped_already = []

crossover_len = random.randint(0, dna_len)
for i in range(crossover_len):
    a = random.randint(0, n)
    b = random.randint(0, n)
    c = random.randint(0, n)
    
    inp = [a, b, c]
    if inp in swapped_already:
        # NOTE: this will most likely be called at some point,
        # decreasing the total number of swapped genes at the end,
        # since it will already skip to another iteration (and won't retry)
        continue

    dna[key_repr_of_inp(inp)] = 10000000000000

print(dna)
