import sys
import adventDays.advent10
import adventDays.advent11
import adventDays.advent12
import adventDays.advent13
import adventDays.advent14
import adventDays.advent15
import adventDays.advent16
import adventDays.advent17
import adventDays.advent18
import adventDays.advent19
import adventDays.advent20
import adventDays.advent21
import adventDays.advent22
import adventDays.advent23
import adventDays.advent24
import adventDays.advent25

try:
    day = int(sys.argv[1])
except:
    print(f'Usage: "py advent.py <day_integer>"\nReceived args: {sys.argv[1:]}')

def main():
    if not day:
        return
    match day:
        case 10:
            adventDays.advent10.main()
        case 11:
            adventDays.advent11.main()
        case 12:
            adventDays.advent12.main()
        case 13:
            adventDays.advent13.main()
        case 14:
            adventDays.advent14.main()
        case 15:
            adventDays.advent15.main()
        case 16:
            adventDays.advent16.main()
        case 17:
            adventDays.advent17.main()
        case 18:
            adventDays.advent18.main()
        case 19:
            adventDays.advent19.main()
        case 20:
            adventDays.advent20.main()
        case 21:
            adventDays.advent21.main()
        case 22:
            adventDays.advent22.main()
        case 23:
            adventDays.advent23.main()
        case 24:
            adventDays.advent24.main()
        case 25:
            adventDays.advent25.main()
        case _:
            print(f'No matching day configured for day {day}')

if __name__ == "__main__":
    main()