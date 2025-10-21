import sys

# Check if exactly 2 numbers are given
if len(sys.argv) != 3:
    print("Usage: python multiply_args.py <num1> <num2>")
    sys.exit(1)

num1 = float(sys.argv[1])
num2 = float(sys.argv[2])
print(f"The result of {num1} x {num2} = {num1 * num2}")
