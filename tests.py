from functions.get_file_content import get_file_content


def test():
    print("Test 1:", get_file_content("calculator", "main.py"))
    print("Test 2:", get_file_content("calculator", "pkg/calculator.py"))
    print("Test 3:", get_file_content("calculator", "/bin/cat"))
    print("Test 4:", get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    test()
