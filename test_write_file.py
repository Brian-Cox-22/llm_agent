from functions.write_file import write_file
from functions.get_file_content import get_file_content

def main():
    results = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(results)

    print('Check file contents')
    print(get_file_content("calculator", "lorem.txt"))
    

    results = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(results)

    results = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(results) # this should be an Error message



if __name__ == '__main__':
    main()