import argparse
import json
import datetime
import sys

def is_directory(permissions):
    return permissions.startswith('d')

def filter_assets(file_info, filter_option):
    contents = file_info["contents"]
    filtered_contents = None

    if filter_option == 'file':
        filtered_contents = [item for item in contents if not is_directory(item.get('permissions', ''))]
    elif filter_option == 'dir':
        filtered_contents = [item for item in contents if is_directory(item.get('permissions', ''))]
    else:
        print(f"error: '{filter_option}' is not a valid filter criteria. Available filters are 'dir' and 'file'")
        sys.exit(1)

    return {"contents": filtered_contents}

def ls_command(file_info, options):
    """
    perform the ls command based on the provided data structure and options for the given json data.
    """
    if "contents" not in file_info:
        raise ValueError("invalid file_info structure. 'contents' key not found.")

    filtered_file_info = file_info.copy()
    if options.filter_option:
        filtered_file_info.update(filter_assets(file_info, options.filter_option))

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
    # argument parser setup
    parser = argparse.ArgumentParser(description="Python linux utility ls command")

    parser.add_argument('-a', '--show-all', action='store_true', help="show all files and directories")
    parser.add_argument('-l', '--long-format', action='store_true', help="print in long format i.e <permission size last_modification file/folder>")
    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true", help="print in revserse order with long format i.e <permission size last_modification file/folder>")
    parser.add_argument("-t", "--time", dest="sort_by_time", action="store_true", help="sort by time_modified")
    # With choices we can bound the choices but we have handled explicitly
    parser.add_argument("--filter", dest="filter_option",
                        # choices=['file', 'dir'],
                        help="filter output based on 'file' or 'dir'")

    args = parser.parse_args()

    # read the json data from the file
    with open('structure.json', 'r') as file:
        structure_data = json.load(file)

    # execute ls command
    ls_command(structure_data, args)

if __name__ == "__main__":
    main()
