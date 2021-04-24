from run import run

if __name__ == "__main__":
    while True:
        text = input("> ")
        r, e = run("shell", text)

        if e:
            print(e.as_str())
        elif r:
            print(repr(r))
