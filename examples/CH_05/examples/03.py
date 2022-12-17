"""Exception example
"""

import math
import logging


logger = logging.getLogger(__file__)


class OutsideRangeException(Exception):
    pass


def range_check_user_input(parameter: int) -> float:
    """This funtions performs a range check on the user input

    Arguments:
        parameter {int} -- The parameter to range check

    Returns:
        float -- The parameter if it is within the range

    Exception:
        Raises OutsideRangeException if parameter violates range
    """
    if not 0 < parameter <= 100:
        raise OutsideRangeException("range exceeded", parameter)

    return parameter


def get_data_from_user():
    """This function gathers input from the user and
    passes it to range check function
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
            result = range_check_user_input(parameter)
        except OutsideRangeException as e:
            logger.exception("Parameter outside of range", e)
            print(
                "Entered value outside of acceptable range,"
                " please re-enter a valid number"
            )
            continue

        print(f"Parameter within range = {result}")
        successful = True


def main():
    get_data_from_user()


if __name__ == "__main__":
    main()
