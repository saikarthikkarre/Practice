# ---------- INPUT GRAMMAR ----------
grammar = {}

n = int(input("Number of productions: "))
for _ in range(n):
    line = input()
    left, right = line.split("->")
    left = left.strip()

    if left not in grammar:
        grammar[left] = []

    for prod in right.split("|"):
        grammar[left].append(prod.strip().split())

non_terminals = list(grammar.keys())

# ---------- FIND TERMINALS ----------
terminals = set()
for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol not in grammar and symbol != "#":
                terminals.add(symbol)

terminals.add("$")

# ---------- FIRST ----------
FIRST = {}

def find_first(symbol):
    if symbol not in grammar:
        return {symbol}

    if symbol in FIRST:
        return FIRST[symbol]

    FIRST[symbol] = set()

    for production in grammar[symbol]:
        if production[0] == "#":
            FIRST[symbol].add("#")
        else:
            for sym in production:
                sym_first = find_first(sym)
                FIRST[symbol] |= (sym_first - {"#"})

                if "#" not in sym_first:
                    break
            else:
                FIRST[symbol].add("#")

    return FIRST[symbol]


for nt in non_terminals:
    find_first(nt)

# ---------- FOLLOW ----------
FOLLOW = {nt: set() for nt in non_terminals}

start_symbol = non_terminals[0]
FOLLOW[start_symbol].add("$")

changed = True
while changed:
    changed = False

    for lhs in grammar:
        for production in grammar[lhs]:
            for i in range(len(production)):
                symbol = production[i]

                if symbol in grammar:
                    before = FOLLOW[symbol].copy()

                    if i + 1 < len(production):
                        next_sym = production[i + 1]
                        first_next = find_first(next_sym)

                        FOLLOW[symbol] |= (first_next - {"#"})

                        if "#" in first_next:
                            FOLLOW[symbol] |= FOLLOW[lhs]
                    else:
                        FOLLOW[symbol] |= FOLLOW[lhs]

                    if before != FOLLOW[symbol]:
                        changed = True

# ---------- PARSING TABLE ----------
table = {nt: {} for nt in non_terminals}

for lhs in grammar:
    for production in grammar[lhs]:
        first_set = set()

        if production[0] == "#":
            first_set.add("#")
        else:
            for sym in production:
                sym_first = find_first(sym)
                first_set |= (sym_first - {"#"})

                if "#" not in sym_first:
                    break
            else:
                first_set.add("#")

        for t in first_set - {"#"}:
            table[lhs][t] = production

        if "#" in first_set:
            for t in FOLLOW[lhs]:
                table[lhs][t] = production

# ---------- OUTPUT ----------
print("\nFIRST Sets")
for nt in non_terminals:
    print(nt, ":", FIRST[nt])

print("\nFOLLOW Sets")
for nt in non_terminals:
    print(nt, ":", FOLLOW[nt])

print("\nLL(1) Parsing Table\n")

terms = list(terminals)

# Header
print("{:<8}".format("NT"), end="")
for t in terms:
    print("{:<15}".format(t), end="")
print("\n")

# Table
for nt in non_terminals:
    print("{:<8}".format(nt), end="")
    for t in terms:
        if t in table[nt]:
            rule = nt + "→" + " ".join(table[nt][t])
        else:
            rule = ""
        print("{:<15}".format(rule), end="")
    print()