import sys
import solutions.day1

try:
    day = int(sys.argv[1])
    part = int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else ""
except:
    print(f'Usage: "py advent.py <day_integer> <part_integer> <mode_string>"\nReceived args: {sys.argv[1:]}')

def main():
    s = solutions
    solution = None
    if not day:
        return
    match day:
        case 1:
            s.day1.main(part, mode)
        case _:
            print(f'No matching day configured for day {day}')

if __name__ == "__main__":
    main()