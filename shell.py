from run import run

if __name__ == "__main__":
    while True:
        text = input("> ")
        if text.strip() == "":
            continue
        r, e = run("shell", text)

        if e:
            print(e.as_str())
        elif r:
            if len(r.elements) == 1:
                print(repr(r.elements[0]))
            else:
                print(repr(r))
