from functions.get_file_content import get_file_content

def main():
    results = get_file_content("calculator", "lorem.txt")
    print("Results for Calculator and lorem.txt")
    print(len(results))
    print('')

    results = get_file_content("calculator", "main.py")
    print("Calc and main")
    # print(len(results))
    print(results)
    print('')

    results = get_file_content("calculator", "pkg/calculator.py")
    print("Calc and calculator.py")
    print(results)
    print('')

    results = get_file_content("calculator", "/bin/cat") # (this should return an error string)
    print('Calculator and .bin')
    print(results)
    print('')

    results = get_file_content("calculator", "pkg/does_not_exist.py") # should return an error string
    print('calculator and does not exist')
    print(results)
    print('')





if __name__ == "__main__":
    main()