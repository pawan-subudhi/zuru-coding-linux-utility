import argparse
import json
import datetime

def format_date_time_from_timestamp(timestamp):
    """
    Format the date and time based on the timestamp.
    """
    date_object = datetime.datetime.fromtimestamp(timestamp)
    return date_object.strftime("%b %d %H:%M")

def ls_command(file_info, show_all=False, long_format=False, reverse_order=False):
    """
    Perform the ls command based on the provided data structure and options for the given JSON data.

    :param data: JSON data representing the file structure
    :param show_all: Flag to include all files and directories (including hidden ones)
    :param long_format: Flag to print in long format i.e <permission size last_modification file/folder>"
    :param reverse_order: Flag to include all files and directories (including hidden ones)
    """
    file_info_to_print = sorted(file_info['contents'], key=lambda x: x["name"], reverse=reverse_order)

    for item in file_info_to_print:
        name = item['name']
        if not show_all and name.startswith('.'):
            continue

        permissions = item['permissions']
        size = item['size']
        time_modified = item['time_modified']
        formatted_time = format_date_time_from_timestamp(time_modified)

        if long_format:
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

    args = parser.parse_args()

    # Read the JSON data from the file
    with open('structure.json', 'r') as file:
        structure_data = json.load(file)

    # Execute ls command
    ls_command(structure_data, show_all=args.show_all, long_format=args.long_format, reverse_order=args.reverse)

if __name__ == "__main__":
    main()
