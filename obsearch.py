#!/usr/bin/env python3
import os, sys
import argparse
import configparser

class Results:
    def __init__(self, line_number, file_path, context):
        self.line_number = line_number
        self.file_path = file_path

        # remove empty lines at the end of the context
        while context and not context[-1].strip():
            context.pop()

        self.context = context

def find_in_file(file_path, search_term, get_full_contents):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines):

                if 'data:image' in line:
                    continue

                if search_term in line.lower():
                    start_line = max(0, line_number - 1)
                    end_line = min(len(lines), line_number + 4)
                    if get_full_contents:
                        context = lines
                    else:
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

    if line_number == -1:
        print('~Match only in title~')
    else:
        print(f"~Line {line_number}~")
    for line in context:

        if search_term in line.lower():
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

def hide_tips():
    value = get_config_value('hide_tips')   
    # ughhh ini files
    if value is None:
        return False
    if value.lower() == 'true':
        return True
    return False

def get_vault_path():
    return get_config_value('obsidian_vault')   

def get_config_value(key):
    value = None
    config_file = os.path.expanduser('~/.config/obsidiansearch/config.ini')
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        value = config.get('DEFAULT', key)
    return value        

def print_result(result, search_term):
    print_file_link(result.file_path, result.line_number)
    print_contents(result.context, result.line_number, search_term)
    print_seperator()

def check_for_continue(displayed_count, total_count, get_full_contents):
    if(displayed_count == total_count):
        return

    # if display_count is divisible by number, ask the user to continue
    if displayed_count % 2 == 0 or get_full_contents:
        cont = input('Press enter to continue... (q to quit) ')
    
        if cont != '':
            sys.exit()

        if get_full_contents:
            # clear console
            os.system('cls' if os.name == 'nt' else 'clear')

def search_directory(directory, search_term, search_all):

    search_term = search_term.lower()

    full_contents = False

    if search_all is not None and search_all.lower() == 'full':
        full_contents = True

    results_with_title_match = []
    results = []

    for root, dirs, files in os.walk(directory, followlinks=True):
        dirs[:] = [d for d in dirs if not d.startswith('.')] # skip hidden folders
        for file_name in files:
            if file_name.lower().endswith('.md'):

                title_match = False
                if search_term in file_name.lower():
                    title_match = True

                file_path = os.path.join(root, file_name)
                line_number, context = find_in_file(file_path, search_term, full_contents)

                # found in content
                if line_number is not None:
                    # found in title and content
                    if title_match:
                        results_with_title_match.append(Results(line_number, file_path, context))
                    # found in content only
                    else:
                        results.append(Results(line_number, file_path, context))
                # found in title only, read some of the file from front
                else:
                    context = None
                    if title_match:
                        with open(file_path, 'r') as f:
                            lines = f.readlines()

                            if full_contents:
                                context = lines
                            else:
                                context = lines[:10] # get first 10 lines

                        results_with_title_match.append(Results(-1, file_path, context))

    displayed_count = 0
    if search_all is None:
        total_count = len(results_with_title_match)
    else:
        total_count = len(results_with_title_match) + len(results)

    if len(results_with_title_match) > 0:
        print(f'Found {len(results_with_title_match)} results with title match', end='')
        if search_all is None:
            print(' (only showing)')
        else:
            print()

    if len(results) > 0:
        print(f'Found {len(results)} results content match')

    if search_all is None and len(results_with_title_match) > 0:
        if not hide_tips():
            print(f'Use `all` after search_term to show all results')

    if len(results_with_title_match) > 0 or len(results) > 0:
        print_seperator()

    # if search term is in title, print those
    for result in results_with_title_match:
        print_result(result, search_term)
        displayed_count += 1
        check_for_continue(displayed_count, total_count, full_contents)

    # if search term is not in title, print all
    if search_all is not None or len(results_with_title_match) == 0 : 
        for result in results:
            print_result(result, search_term)
            displayed_count += 1
            check_for_continue(displayed_count, total_count, full_contents)

    if len(results_with_title_match) == 0 and len(results) == 0:
        print(f'No results found for {search_term}')

def main():
    parser = argparse.ArgumentParser(description='Search for a string in markdown files.')
    # parser.add_argument('--search', nargs='?', help='The string to search for in markdown files.')
    parser.add_argument('--directory', default='.', help='The directory to start the search (default: current directory)')
    parser.add_argument('search', nargs='?', help='The string to search for in markdown files.')
    parser.add_argument('all', nargs='?', help='If exists, show all matches regardless of title match.')
    args = parser.parse_args()

    # print(args)
    
    obsidian_vault = get_vault_path()

    if not args.search:

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

        search_directory(args.directory, args.search, args.all)

if __name__ == '__main__':
    main()
