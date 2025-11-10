from functions.get_files_info import get_files_info


def test():
    print("Result for current directory:")
    res = get_files_info("calculator", ".")
    print(res)

    print("Result for 'pkg':")
    res = get_files_info("calculator", "pkg")
    print(res)

    print("Result for '/bin':")
    res = get_files_info("calculator", "/bin")
    print(res)

    print("Result for '../':")
    res = get_files_info("calculator", "../")
    print(res)


if __name__ == "__main__":
    test()
