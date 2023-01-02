import re


def is_valid(passwd):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    # compiling regex
    pat = re.compile(reg)

    # searching regex
    return re.search(pat, passwd)
