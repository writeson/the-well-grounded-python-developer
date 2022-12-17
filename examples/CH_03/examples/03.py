"""
This module contains the example_03 function demonstrating
the possible side effects of Python's pass by reference
of function arguments.
"""

from copy import copy


def total(values: list, new_value: int) -> int:
    """This function adds new_value to the values list,
    totals the contents and returns the total.

    Arguments:
        values {list} -- list of values to total
        new_value {int} -- value to include in total

    Returns:
        int -- total of values in list
    """
    values.append(new_value)
    return sum(values)


def better_total(values: list, new_value: int) -> int:
    """This function adds new_value to the values list,
    totals the contents and returns the total

    Arguments:
        values {list} -- list of values to total
        new_value {int} -- value to include in total

    Returns:
        int -- total of values in list
    """
    temp_list = copy(values)
    temp_list.append(new_value)
    return sum(temp_list)


def main():
    values_1 = [1, 2, 3]
    total_1 = total(values_1, 4)
    print(f"values_1 has been modified: {values_1}")
    print(f"total_2 is as expected: {total_1}")
    print()
    values_2 = [1, 2, 3]
    total_2 = better_total(values_2, 4)
    print(f"values_2 unchanged: {values_2}")
    print(f"total_2 is as expected: {total_2}")


if __name__ == "__main__":
    main()
