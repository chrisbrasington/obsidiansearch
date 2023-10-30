import os
import argparse

def find_in_file(file_path, search_term):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if search_term in content:
                return True
    except (UnicodeDecodeError, FileNotFoundError):
        pass
    return False

def search_directory(directory, search_term):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.md'):
                file_path = os.path.join(root, file_name)
                if find_in_file(file_path, search_term):
                    print(f"Found '{search_term}' in Markdown file: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Search for a string in markdown files.')
    parser.add_argument('search_term', help='The string to search for in markdown files.')
    parser.add_argument('--directory', default='.', help='The directory to start the search (default: current directory)')
    args = parser.parse_args()

    search_directory(args.directory, args.search_term)

if __name__ == '__main__':
    main()
