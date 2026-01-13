from functions.get_files_info import get_files_info

def main():
    # 1. Current calculator directory
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()

    # 2. 'pkg' directory inside calculator
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()

    # 3. Absolute path outside working dir
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()

    # 4. Parent directory outside working dir
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    print()

if __name__ == "__main__":
    main()