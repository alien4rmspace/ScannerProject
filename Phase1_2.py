
#!/usr/bin/env python3
"""
Limp Scanner (Phase 1.2) - Damian S.
Reads an input file and writes tokens to an output file per spec.
Usage:
    python scanner.py <input_file> <output_file>
"""

from dataclasses import dataclass


SYMBOLS = {'+', '-', '*', '/', '(', ')', ':', '=', ';'}
KEYWORDS = {"if", "then", "else", "endif", "while", "do", "endwhile", "skip"}

@dataclass
class Token:
    type: str
    value: str

def scan_line(line: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(line)

    while i < n:
        c = line[i]

        if c.isspace():
            i += 1
            continue

        if c.isalpha():
            start = i
            while i < n and line[i].isalnum():
                i += 1
            if line[start:i] in KEYWORDS:
                tokens.append(Token("KEYWORD", line[start:i]))
            else:
                tokens.append(Token("IDENTIFIER", line[start:i]))
            continue

        if c.isdigit():
            start = i
            while i < n and line[i].isdigit():
                i +=1
            tokens.append(Token("NUMBER", line[start:i]))
            continue

        if c in SYMBOLS:
            start = i
            if c != ':':
                i += 1
                tokens.append(Token("SYMBOL", line[start:i]))
                continue
            if  c == ':' and line[start + 1] == '=':
                i += 2
                tokens.append(Token("SYMBOL", line[start:i]))
                continue

        tokens.append(Token("ERROR READING", c))
        i += 1

    return tokens



def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scanner.py test_input.txt test_output.txt", file=sys.stderr)
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    try:
        with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
            for raw_line in fin:
                line = raw_line.rstrip("\n")
                fout.write("Line: " + line +"\n")

                token = scan_line(line)
                for token in token:
                    fout.write(token.value + " : " + token.type + "\n")
                fout.write("\n")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()