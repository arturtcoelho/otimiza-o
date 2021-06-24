#!/usr/bin/env python3

from itertools import combinations

total_time = 540 #min

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
disp = 0
for i, v in enumerate(viable_dict2.keys()):
    # for each multiplier combination
    mod = 0
    for val in viable_dict2[v]:
        mod += 1
        eq = []
        for j, x in enumerate(val[0]):
            eq += [f"{f'{val[1][j]} x ' if val[1][j] > 1 else ''}{reqs[x][2]}"]

        eq = " + ".join(eq)
        combinations.append(eq)

        for j, k in enumerate(val[0]):
            equations[k] = equations[k] + [[i+disp, val[1][j]]]
    if mod > 1:
        disp += 1

# get formated bases
base = []
for i, b in enumerate(combinations):
    base.append(f"P{i}: {b}")
    
# get linear problem
borders = []
for k in equations.keys():
    p = []
    last = -1
    disp = 0
    for j in equations[k]:
        i = j[0]
        if (i == last): 
            disp = 1
        p.append(f"{j[1] if j[1] > 1 else ''}x{i+disp}")
        last = j[0]
        disp = 0
    eq = " + ".join(p)
    eq += f" >= {reqs[k][1]}"
    borders.append(eq)

# print lp solver entry to stdout
mins = [f"x{i}" for i in range(len(base))]
print(f"min: {' + '.join(mins)};")
print(f"")
for b in borders:
    print(f"{b};")

output = open("equations.out", "w")

for r in reqs:
    print(f"i: {r[0]} qtd: {r[1]} val: {r[2]}", file=output)
print(file=output)

for b in base:
    print(b, file=output)
print(file=output)

mins = [f"x{i}" for i in range(len(base))]
print(f"min: {' + '.join(mins)};", file=output)
print(f"", file=output)
for b in borders:
    print(f"{b};", file=output)
