

def outer():
    def inner():
        print(out_var)
    out_var = 10
    inner()


if "__main__" == __name__:
    outer()