def full_name_and_print(fname: str, mname: str, lname: str) -> None:
    """Concatenates the names together and prints them

    Arguments:
        fname {str} -- first name
        mname {str} -- middle name
        lname {str} -- last name
    """
    full_name = " ".join(name for name in [fname, mname, lname] if name)
    print(full_name)


def full_name(fname: str, mname: str, lname: str) -> str:
    """Concatenates the names together and returns the full name

    Arguments:
        fname {str} -- first name
        mname {str} -- middle name
        lname {str} -- last name

    Returns:
        str -- the full name with only a single space between names
    """
    full_name = " ".join(name for name in [fname, mname, lname] if name)
    return full_name


def main():
    full_name_and_print("John", "", "Smith")

    the_full_name = full_name("John", "", "Smith")
    print(the_full_name)


if __name__ == "__main__":
    main()
