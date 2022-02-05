def full_name_and_print(fname: str, mname: str, lname: str) -> None:
    """Concatenates the names together and prints them

    Arguments:
        fname {str} -- first name
        mname {str} -- middle name
        lname {str} -- last name
    """
    full_name = " ".join([fname, mname, lname])
    full_name = " ".join(full_name.split())
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
    full_name = " ".join([fname, mname, lname])
    return " ".join(full_name.split())


def main():
    full_name_and_print("John", "", "Smith")

    the_full_name = full_name("John", "", "Smith")
    print(the_full_name)


if __name__ == "__main__":
    main()
