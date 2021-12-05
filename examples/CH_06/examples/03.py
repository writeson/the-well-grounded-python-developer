"""Exception example
"""

import math
import logging


logger = logging.getLogger(__file__)


class OutsideRangeException(ValueError):
    pass


def calculate(parameter: int) -> float:
    """This funtions performs a calculation on the passed parameter
    and returns the results to the caller

    Arguments:
        parameter {int} -- The parameter to use for the calculation

    Returns:
        float -- The results of the calculation
    """
    if not 0 < parameter <= 100:
        raise OutsideRangeException("range exceeded", parameter)

    return parameter * math.pi


def prompt_user_for_data():
    """This function gathers input from the user and
    passes it to calculate to perform a calculation
    """
    successful = False
    while not successful:
        parameter = input(
            "Please enter a integer greater than 0 and less than or equal to 100: ")

        try:
            parameter = int(parameter)
        except ValueError as e:
            logger.exception("Something happened", e)
            print(e)
            continue

        try:
            result = calculate(parameter)
        except OutsideRangeException as e:
            logger.exception("Parameter outside of range", e)
            print(
                "Entered value outside of acceptable range,"
                " please re-enter a valid number"
            )
            continue

        print(f"Calculated result = {result}")
        successful = True


def main():
    prompt_user_for_data()


if __name__ == "__main__":
    main()
