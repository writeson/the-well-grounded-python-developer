"""Exception example
"""


def func_a():
    dividend = float(input("Enter a dividend value: "))
    divisor = float(input("Enter a divisor value: "))
    result = func_b(dividend, divisor)
    print(f"dividing {dividend} by {divisor} = {result}")


def func_b(dividend: float, divisor: float) -> float:
    return func_c(dividend, divisor)


def func_c(dividend: float, divisor: float) -> float:
    return dividend / divisor


def main():
    func_a()


if __name__ == "__main__":
    main()
