import argparse
import json
import datetime

def ls_command(file_info, options):
    """
    Perform the ls command based on the provided data structure and options for the given JSON data.

    :param data: JSON data representing the file structure
    :param show_all: Flag to include all files and directories (including hidden ones)
    :param long_format: Flag to print in long format i.e <permission size last_modification file/folder>"
    :param reverse_order: Flag to include all files and directories (including hidden ones)
    """
    file_key = "time_modified" if options.sort_by_time else "name"
    file_info_to_print = sorted(file_info["contents"], key=lambda x: x[file_key], reverse=options.reverse)

    for item in file_info_to_print:
        name = item['name']
        if not options.show_all and name.startswith('.'):
            continue

        permissions = item.get("permissions", "")
        size = item.get("size", 0)
        time_modified = item.get("time_modified", 0)
        name = item.get("name", "")

        formatted_time = datetime.datetime.fromtimestamp(time_modified).strftime("%b %d %H:%M")

        if options.long_format:
            print(f"{permissions} {size} {formatted_time} {name}")
        else:
            print(name, end=' ')
    else:
        print("\n")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Python linux utility ls command")
    parser.add_argument('-A', '--show-all', action='store_true', help="Show all files and directories")
    parser.add_argument('-l', '--long-format', action='store_true', help="Print in long format i.e <permission size last_modification file/folder>")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true", help="Print in revserse order with long format i.e <permission size last_modification file/folder>")
    parser.add_argument("-t", "--time", dest="sort_by_time", action="store_true", help="sort by time_modified")

    args = parser.parse_args()

    # Read the JSON data from the file
    with open('structure.json', 'r') as file:
        structure_data = json.load(file)

    # Execute ls command
    ls_command(structure_data, args)

if __name__ == "__main__":
    main()
