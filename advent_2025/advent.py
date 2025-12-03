import sys
import importlib

try:
    day = int(sys.argv[1])
    part = int(sys.argv[2])
    mode = sys.argv[3] if len(sys.argv) > 3 else ""
except:
    print(f'Usage: "py advent.py <day_integer> <part_integer> <mode_string>"\nReceived args: {sys.argv[1:]}')

def main():
    if not day:
        return
    try:
        solution_module = importlib.import_module(f'solutions.day{day}')
        solution_module.main(part, mode)
    except ModuleNotFoundError:
        print(f'No solution module found for day {day}')
        return
    except AttributeError:
        print(f'Solution module for day {day} does not have a main() function')
        return

if __name__ == "__main__":
    main()