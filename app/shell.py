from run import run

if __name__ == "__main__":
    while True:
        text = input("> ")
        t, e = run("shell", text)

        if e:
            print(e.as_str())
        else:
            print(t)
