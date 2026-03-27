import re

code = "a+b"

patterns = [
    ("keyword", r"\b(if|else|while|for)\b"),
    ("identifier", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("number", r"\b\d+\b"),
    ("operator", r"[+\-*/]")
]

for token, pattern in patterns:
    for match in re.finditer(pattern, code):
        print(f"{token}: {match.group()}")