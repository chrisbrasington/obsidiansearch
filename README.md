# Obsidian Search

**Obsidian Search** is a Python command-line utility for searching for a string within Markdown files. This tool is designed to work with Obsidian vaults, making it easier to find content within your knowledge base. It provides search results with context and supports searching both in titles and content.

## Prerequisites

- Python 3
- [Obsidian](https://obsidian.md/)
    - (or any directory of markdown files really)

## Usage

To use **Obsidian Search**, run the following command in your terminal:

```bash
python obsidiansearch.py [OPTIONS] SEARCH_TERM [ALL]
```

- `SEARCH_TERM`: The string you want to search for in Markdown files.
- `all` (optional): If specified, all matches will be shown regardless of title match.
- `full` (optional): If specified, full file will output, prompting between each file

### Options

- `--directory`: The directory to start the search (default: current directory).

## Example Usage

> Note to use `obsearch` system wide instead of `python obsidiansearch.py` see [Running obsearch directly](#running-obsearch-directly) below.


- To search for the string "example" in all Markdown files within the Obsidian vault:

```bash
python obsidiansearch.py example
```

- To search for the string "example" in all Markdown files within a specific directory:

```bash
python obsidiansearch.py --directory /path/to/directory example
```

- To search for the string "example" in all Markdown files, including content-only matches:

```bash
python obsidiansearch.py example all
```

## Configuration

Config file can be created with:

```bash
create_settings.sh ~/obsidian_directory
```

**Obsidian Search** uses a configuration file to store settings. You can configure the tool by editing the `~/.config/obsidiansearch/config.ini` file. The available configuration options are:

- `obsidian_vault`: Path to your Obsidian vault directory.
- `hide_tips`: Set to "true" to hide search tips when there are title matches. 

## Tips

- When searching for a string in the title, only results with title matches will be shown by default. Use the `all` option to display all results, including content-only matches.
- If you don't have the Obsidian vault configuration set, you can run `create_settings.sh` to configure it.

## Output

**Obsidian Search** will display search results, showing the file paths, line numbers, and context of the matches. The output includes syntax highlighting for matched text.

### Output Example 1:

> obsearch tar.gz
```bash
Found 1 results with title match (only showing)
--------------------------------------------------------------------------------
brain/03 - Resources/Linux/tar.gz - Line 1
~Line 1~

# How to unzip tar.gz
tar -xzvf yourfile.tar.gz
--------------------------------------------------------------------------------
```

### Output Example 2:

> obsearch coffee all

```bash
obsearch coffee all
Found 1 results with title match
Found 2 results content match
--------------------------------------------------------------------------------
brain/03 - Resources/Recipes/Coffee - Line -1
~Match only in title~
I f-ing love Ethiopian beans.
--------------------------------------------------------------------------------
brain/03 - Resources/Notetaking/The PARA Method The Simple System for Organizing Your Digital Life in Seconds - Line 48
~Line 48~
-   Organic gardening
-   Coffee
-   Modern architecture
-   Web design
-   Japanese language
--------------------------------------------------------------------------------
Press enter to continue... (q to quit)
highlights/Corey, James S. A - Line 3
~Line 3~
##### Holden pulled himself a cup of coffee from the galley coffeepot, and the strong smell filled the room.
**Location**: Page (043) Point (/1/4/3:1)
**Date**: 2023-10-29T18:26:01Z
--------------------------------------------------------------------------------
```

## Compatibility

- **Obsidian Search** works with Obsidian vaults and is designed for use with any Markdown files.
    - Theoretically it could be used for any file typo

## Limitations (there be dragons)

- I did not focus on any sort of performance on large directories or files. 
    - Consider enhancing my code to use specific directory parameters or parallel process crawl multiple directories.

## Running `obsearch` Directly

To make it more convenient to run the `obsidiansearch.py` script as `obsearch`, you can create an executable script or symbolic link. This will allow you to use the simplified command `obsearch` instead of `python obsidiansearch.py`.

### Option 1: Using `create_exec.sh`

We provide a shell script named `create_exec.sh` that automates the process of creating an executable script for `obsearch`. Follow these steps to use it:

1. Open your terminal and navigate to the directory where the `obsidiansearch.py` script is located.

2. Run the `create_exec.sh` script:

    ```bash
    ./create_exec.sh
    ```

3. The script will create a new file named `obsearch` in the same directory. This file will be marked as executable.

4. Now, you can run `obsearch` directly in your terminal:

    ```bash
    obsearch [OPTIONS] SEARCH_TERM [ALL]
    ```

### Option 2: Creating a Symbolic Link

Alternatively, you can create a symbolic link manually to achieve the same result. Here are the steps:

Open your terminal and navigate to the directory where the obsidiansearch.py script is located.

Run the create_exec.sh script:

./create_symbolic_link.sh

With either of these options, you can easily run `obsearch` without needing to specify `python obsidiansearch.py` each time you want to use the tool. This makes searching your Obsidian vault more convenient and user-friendly.


## License

This tool is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

This tool is created by [chrisbrasington](github.com/chrisbrasington).

## Disclaimer

This tool is not officially affiliated with Obsidian or its creators.

Feel free to contribute or report issues on the [GitHub repository](hhttps://github.com/chrisbrasington/obsidiansearch).
