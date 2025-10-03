#!/usr/bin/env python3
"""
Lexp Scanner (Phase 1.1) - Vanessa
Reads an input file and writes tokens to an output file per spec.
Usage:
    python scanner.py <input_file> <output_file>
"""
from dataclasses import dataclass
from typing import List

SYMBOLS = {"+", "-", "*", "/", "(", ")"}

@dataclass
class Token:
    typ: str
    val: str

class ScannerError(Exception):
    def __init__(self, bad_char: str, position: int, tokens_so_far: List[Token]):
        super().__init__(f'Bad character {bad_char!r} at position {position}')
        self.bad_char = bad_char
        self.position = position
        self.tokens_so_far = tokens_so_far

def scan_line(line: str) -> List[Token]:
    """Scan a single input line and return a list of tokens.
    On encountering an invalid character, raise ScannerError containing tokens scanned so far.
    """
    tokens: List[Token] = []
    i = 0
    n = len(line)

    def is_alpha(c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z")

    def is_digit(c: str) -> bool:
        return "0" <= c <= "9"

    def is_alnum(c: str) -> bool:
        return is_alpha(c) or is_digit(c)

    while i < n:
        c = line[i]

        # Skip whitespace (spaces, tabs, etc.)
        if c.isspace():
            i += 1
            continue

        # SYMBOL (single character)
        if c in SYMBOLS:
            tokens.append(Token("SYMBOL", c))
            i += 1
            continue

        # IDENTIFIER
        if is_alpha(c):
            start = i
            i += 1
            while i < n and is_alnum(line[i]):
                i += 1
            tokens.append(Token("IDENTIFIER", line[start:i]))
            continue

        # NUMBER
        if is_digit(c):
            start = i
            i += 1
            while i < n and is_digit(line[i]):
                i += 1
            tokens.append(Token("NUMBER", line[start:i]))
            continue

        # Invalid character
        raise ScannerError(c, i, tokens)

    return tokens

def format_token(t: Token) -> str:
    # Output format: "<lexeme> : <TYPE>"
    return f"{t.val} : {t.typ}"

def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python scanner.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2]

    try:
        with open(in_path, "r", encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
            for raw_line in fin:
                # Preserve original line without trailing newline for printing
                line = raw_line.rstrip("\\n")
                fout.write(f"Line: {line}\\n")
                try:
                    tokens = scan_line(line)
                    for t in tokens:
                        fout.write(format_token(t) + "\\n")
                except ScannerError as e:
                    # Print tokens scanned before the error, then the error message
                    for t in e.tokens_so_far:
                        fout.write(format_token(t) + "\\n")
                    fout.write(f'ERROR READING "{e.bad_char}"\\n')
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
