from typing import Tuple


def split_fullname(full_name: str) -> Tuple[str, str, str]:
    """This function splits the full name passed in
    and returns the parts in a tuple as the fname,
    mname and lname as best it can

    Arguments:
        full_name {str} -- A space separated name string of up to three parts

    Returns:
        Tuple[str, str, str] -- A tuple containing the fname, mname, lname
                                from the passed in fullname parameter
    """
    fname = mname = lname = ""
    parts = full_name.split()
    if len(parts) >= 1:
        fname = parts[0]
    if len(parts) >= 2:
        mname = parts[1]
    if len(parts) == 3:
        lname = parts[2]
    if not lname:
        mname, lname = (lname, mname)
    return (fname, mname, lname)


def main():
    fname, mname, lname = split_fullname("John")
    print(fname, mname, lname)
    fname, mname, lname = split_fullname("John Smith")
    print(fname, mname, lname)
    fname, mname, lname = split_fullname("John James Smith")
    print(fname, mname, lname)


if __name__ == "__main__":
    main()
