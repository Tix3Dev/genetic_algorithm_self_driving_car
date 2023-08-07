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
