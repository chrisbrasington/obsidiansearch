#!/usr/bin/env python3
import os, sys
import argparse
import configparser

def find_in_file(file_path, search_term):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines):
                if search_term in line:
                    start_line = max(0, line_number - 1)
                    end_line = min(len(lines), line_number + 4)
                    context = lines[start_line:end_line]
                    return line_number + 1, context
    except (UnicodeDecodeError, FileNotFoundError):
        pass
    return None, None

def print_file_link(file_path, line_number):
    abs_file_path = os.path.abspath(file_path)
    term_program = os.environ.get('TERM_PROGRAM', '')

    if term_program == 'vscode':
        print_blue (abs_file_path)
    else:
        vault = get_vault_path()
        title = abs_file_path.replace(vault, '').replace('.md', '')

        print_blue(f"\u001b]8;;file://{abs_file_path}\u001b\\{title} - Line {line_number}\u001b]8;;\u001b\\")

def print_contents(context, line_number, search_term):
    print(f"Line {line_number}")
    for line in context:

        if search_term in line:
            print_green(line, end='')
        else:
            print(line.strip())

def print_seperator():
    print('-' * 80)

def print_green(text, end='\n'):
    # bold only -  text = f"\033[1m{text}\033[0m"
    text = f"\033[1;32m{text}\033[0m"
    print(text, end=end)

def print_blue(text):
    print(f"\033[94m{text}\033[0m")   

def get_vault_path():
    obsidian_vault = None
    config_file = os.path.expanduser('~/.config/obsidiansearch/config.ini')
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        obsidian_vault = config.get('DEFAULT', 'obsidian_vault')
    return obsidian_vault

class Results:
    def __init__(self, line_number, file_path, context):
        self.line_number = line_number
        self.file_path = file_path
        self.context = context
        

def search_directory(directory, search_term):

    results = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.md'):
                file_path = os.path.join(root, file_name)
                line_number, context = find_in_file(file_path, search_term)
                if line_number is not None:

                    results.append(Results(line_number, file_path, context))

                    # print_file_link(file_path, line_number)

                    # print_contents(context, line_number, search_term)

                    # print_seperator()

    foundInTitle = False

    # if search term is in title, only print those
    for result in results:
        if search_term in result.file_path:
            print_file_link(result.file_path, result.line_number)
            print_contents(result.context, result.line_number, search_term)
            print_seperator()
            foundInTitle = True

    # if search term is not in title, print all
    if not foundInTitle:
        for result in results:
            print_file_link(result.file_path, result.line_number)
            print_contents(result.context, result.line_number, search_term)
            print_seperator()

def main():
    parser = argparse.ArgumentParser(description='Search for a string in markdown files.')
    parser.add_argument('search_term', nargs='?', help='The string to search for in markdown files.')
    parser.add_argument('--directory', default='.', help='The directory to start the search (default: current directory)')
    args = parser.parse_args()

    obsidian_vault = get_vault_path()

    if not args.search_term:

        if obsidian_vault == None:
            print('No obsidian vault config, run create_settings.sh')
        else:
            print(f'Using obsidian vault: {obsidian_vault}', end='\n')
            if os.path.exists(obsidian_vault):
                print('Vault exists')
            else: 
                print('Vault does not exist')

        parser.print_help()
    else:
        
        args.directory = obsidian_vault

        search_directory(args.directory, args.search_term)

if __name__ == '__main__':
    main()
