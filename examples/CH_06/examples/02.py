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
    successful = False
    while not successful:
        try:
            func_a()
        except ZeroDivisionError as e:
            print(f"The divisor can't be a zero value, error: {e}")
        except ValueError as e:
            print(
                f"The dividend and divisor must be a string that represents a number, error: {e}"
            )
        else:
            successful = True
        finally:
            if successful:
                print("Thanks for running the program")
            else:
                print("Try entering a dividend and divisor again")


if __name__ == "__main__":
    main()
