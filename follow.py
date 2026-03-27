from collections import defaultdict

# -------- INPUT --------
n = int(input("Enter number of productions: "))
grammar = defaultdict(list)
non_terminals = []
start_symbol = None
follow = defaultdict(set)

# ---------- FIND TERMINALS ----------
terminals = set()
for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol not in non_terminals and symbol != 'ε':
                terminals.add(symbol)

terminals.add('$')

# ---------- FIRST ----------
first = defaultdict(set)

def compute_first(symbol):
    if symbol not in non_terminals:
        return {symbol}

    if first[symbol]:
        return first[symbol]

    for production in grammar[symbol]:
        if production == ['ε']:
            first[symbol].add('ε')
            continue

        for sym in production:
            sym_first = compute_first(sym)
            first[symbol].update(sym_first - {'ε'})

            if 'ε' not in sym_first:
                break
        else:
            first[symbol].add('ε')

    return first[symbol]

for nt in non_terminals:
    compute_first(nt)

# ---------- FOLLOW ----------
follow = defaultdict(set)
follow[start_symbol].add('$')

def compute_follow():
    changed = True

    while changed:
        changed = False

        for left in grammar:
            for production in grammar[left]:

                for i in range(len(production)):
                    B = production[i]

                    if B in non_terminals:
                        before = len(follow[B])

                        j = i + 1
                        epsilon_flag = True

                        while j < len(production) and epsilon_flag:
                            beta = production[j]
                            first_beta = compute_first(beta)

                            follow[B].update(first_beta - {'ε'})

                            if 'ε' in first_beta:
                                j += 1
                            else:
                                epsilon_flag = False

                        if epsilon_flag:
                            follow[B].update(follow[left])

                        if len(follow[B]) > before:
                            changed = True

compute_follow()

# ---------- PARSING TABLE ----------
table = {nt: {} for nt in non_terminals}

for lhs in grammar:
    for production in grammar[lhs]:
        first_set = set()

        if production[0] == 'ε':
            first_set.add('ε')
        else:
            for sym in production:
                sym_first = compute_first(sym)
                first_set |= (sym_first - {'ε'})

                if 'ε' not in sym_first:
                    break
            else:
                first_set.add('ε')

        # Fill table using FIRST
        for t in first_set - {'ε'}:
            table[lhs][t] = production

        # Fill using FOLLOW if ε present
        if 'ε' in first_set:
            for t in follow[lhs]:
                table[lhs][t] = production

# ---------- OUTPUT ----------
print("\nFIRST sets:\n")
for nt in sorted(non_terminals):
    print(f"FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")

print("\nFOLLOW sets:\n")
for nt in sorted(non_terminals):
    print(f"FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")

print("\nLL(1) Parsing Table:\n")

terms = list(terminals)

# Header
print("{:<8}".format("NT"), end="")
for t in terms:
    print("{:<12}".format(t), end="")
print("\n")

# Table
for nt in non_terminals:
    print("{:<8}".format(nt), end="")
    for t in terms:
        if t in table[nt]:
            rule = nt + "→" + " ".join(table[nt][t])
        else:
            rule = ""
        print("{:<12}".format(rule), end="")
    print()