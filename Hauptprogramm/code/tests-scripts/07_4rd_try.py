import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("echo", help="echo the string you use here")
#parser.add_argument("square", help="display a square of a given number", type=int)

# optionale Argumente
#parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true") # by default is the value "None"
#parser.add_argument("square", type=int, help="display a square of a given number")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
parser.add_argument("-f", "--filename", type=str, required=True, help="file which should be executed")
parser.add_argument("-t", "--tlimit", type=str, required=False, help="time limit after the programm should break up (units: s = (second), min = (minute), h = (hour), d = (day), m = (month))")

args = parser.parse_args()

fileName = args.filename
timeLimit = args.tlimit

#answer = args.square**2
answer = 0 

if args.verbosity == 2:
    print(f"the square of {args.square} equals {answer}")
elif args.verbosity == 1:
    print(f"{args.square}^2 == {answer}")
else:
    print(answer)
    print(fileName)
    print(timeLimit)