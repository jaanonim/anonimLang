import sys

from run import run


def main():
    try:
        file_name = sys.argv[1]
    except:
        file_name = None
    if file_name:
        file_name = file_name.replace("\\", "\\\\")
        execute_command(f'run("{file_name}")')
    else:
        shell()


def shell():
    while True:
        text = input("> ")
        if text.strip() == "":
            continue
        execute_command(text)


def execute_command(text):
    r, e = run("shell", text)

    if e:
        print(e.as_str())
    elif r:
        if len(r.elements) == 1:
            print(repr(r.elements[0]))
        else:
            print(repr(r))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
