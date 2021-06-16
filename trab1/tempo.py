#!/usr/bin/env python3

from itertools import combinations

total_time = 300 #min

# Read number of machines and number of request sizes and quantities
n_mach, n_req = input().split()
n_mach = int(n_mach)
n_req = int(n_req)

# read requirements
# [index, multiplier, value]
reqs = []
for i in range(n_req*2):
    try:
        n, m = input().split()
    except EOFError:
        break
    reqs.append([i, int(n), int(m)])

# add all possible multipliers
times = [[r[0], 1, r[2]] for r in reqs]

m = []
for t in times:
    i = 2
    while (t[2]*i <= total_time):
        m.append([t[0], i, t[2]])
        i+=1
times += m

# Generate all possible combination of single requests
combs = []
for i in range(1, len(reqs)):
    for c in list(combinations(times, i)):
        combs.append(c)

# filter viable ones
viable = [c for c in combs if sum([n[2]*n[1] for n in c]) <= total_time]

# filter repeated
viable = [list(v) for v in viable if len(set([k[2] for k in v])) == len(v)]
for v in viable:
    v.sort(key=lambda k: k[2])

# add keys to dict to filter all single value combinatios
# store their multipliers
viable_dict = {}
for v in viable:
    key = "+".join([f"{k[2]}" for k in v])
    try:
        viable_dict[key] += [([k[0] for k in v], [k[1] for k in v])]
    except:
        viable_dict[key] = [([k[0] for k in v], [k[1] for k in v])]

# Filter each multiplier combination to get the biggest one for each value
viable_dict2 = {}
for k, val in viable_dict.items():
    values = []
    biggest = []

    for mult in val:
        values.append(mult[1])
        
    for i in range(len(values[0])):
        biggest += [max(values, key=lambda k: k[i]*10+sum(k))]
    
    aux = []
    for b in biggest:
        if (b not in aux):
            aux.append(b)

    viable_dict2[k] = [(val[0][0], x) for x in aux]

# generate final equations from all viable combinations
combinations = []
equations = {v[0]:[] for v in reqs}
for i, v in enumerate(viable_dict2.keys()):
    # for each multiplier combination
    for val in viable_dict2[v]:
        eq = []
        for j, x in enumerate(val[0]):
            eq += [f"{val[1][j] if val[1][j] > 1 else ''}x{x}"]

        eq = " + ".join(eq)
        combinations.append(eq)

        for j, k in enumerate(val[0]):
            equations[k] = equations[k] + [[i, val[1][j]]]

# get formated bases
base = []
for i, b in enumerate(combinations):
    base.append(f"P{i}: {b}")
    
# get linear problem
borders = []
for k in equations.keys():
    p = [f"{k[1] if k[1] > 1 else ''}x{k[0]}" for k in equations[k]]
    eq = " + ".join(p)
    eq += f" >= {reqs[k][1]}"
    borders.append(eq)

# for r in reqs:
#     print(r)
# print()

for b in base:
    print(b)
print()

# print lp solver entry to stdout
mins = [f"x{i}" for i in range(len(base))]
print(f"min: {' + '.join(mins)};")
print(f"")
for b in borders:
    print(f"{b};")