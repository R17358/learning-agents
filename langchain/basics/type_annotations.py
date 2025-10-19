def factorial(n: int)->int:
    if n==0 or n==1:
        return 1
    return n*factorial(n-1)


def total(numbers: list[int]) -> int:
    return sum(numbers)

def point()->tuple[int, int]:
    return (10, 20)

num = int(input("Enter number to find Factorial: "))
ans = factorial(num)

print(f"Factorial of {num} is {ans}")