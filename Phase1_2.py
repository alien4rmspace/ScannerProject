from dataclasses import dataclass

SYMBOLS = {'+', '-', '*', '/', '(', ')', ':=', ';'}
KEYWORDS = {"if", "then", "else", "endif", "while", "do", "endwhile", "skip"}

@dataclass
class Token:
    type: str
    value: str

def scan_line(line: str) -> list[Token]:
    tokens: list[Token] = []

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
                fout.write(line +"\n")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}", file=sys.stderr)
        sys.exit(1)



if __name__ == "__main__":
    main()