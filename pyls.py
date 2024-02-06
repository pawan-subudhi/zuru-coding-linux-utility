from docopt import docopt
import json
import datetime
import sys

def is_directory(permissions):
    """
    Check if the given permissions indicate a directory.

    :param permissions: String representing file permissions.
    :return: True if the permissions indicate a directory, False otherwise.
    """
    return permissions.startswith('d')


def convert_bytes_to_human_readable(size_in_bytes):
    """
    Convert a size in bytes to human-readable format with appropriate suffixes (B, KB, MB, GB, TB).

    :param size_in_bytes: Size in bytes to be converted.
    :return: Human-readable string representation of the size.
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size_in_bytes >= 1024 and index < len(suffixes) - 1:
        size_in_bytes /= 1024.0
        index += 1
    return f"{size_in_bytes:.1f}{suffixes[index]}"


def filter_assets(file_info, filter_option):
    """
    Filter the contents of a file_info dictionary based on the specified filter_option.

    :param file_info: Dictionary containing information about files and directories.
    :param filter_option: Filter option ('file' or 'dir').
    :return: Dictionary with filtered contents based on the filter option.
    """
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


def path_exists_recursive(path, current_info):
    path_parts = path.split("/")

    for part in path_parts:
        if not part:
            continue

        part_info = next((item for item in current_info.get("contents", []) if item['name'] == part), None)
        if not part_info:
            return False

        current_info = part_info

    return True


def print_file_info(item, options):
    """
    Print file information based on the specified options.

    :param item: Dictionary representing file or directory information.
    :param options: Namespace object containing command-line options.
    :return: None
    """
    name = item['name']
    if not options['--show-all'] and name.startswith('.'):
        return

    permissions = item.get("permissions", "")
    size = item.get("size", 0)
    time_modified = item.get("time_modified", 0)
    formatted_time = datetime.datetime.fromtimestamp(time_modified).strftime("%b %d %H:%M")

    if options['--long-format']:
        if options['--human-readable']:
            human_readable_size = convert_bytes_to_human_readable(size)
            print(f"{permissions} {human_readable_size} {formatted_time} {name}")
        else:
            print(f"{permissions} {size} {formatted_time} {name}")
    else:
        print(name, end=' ')


def ls_command(file_info, options):
    """
    Perform the ls command based on the provided data structure and options for the given JSON data.

    :param file_info: Dictionary representing the file structure with metadata.
    :param options: Namespace object containing command-line options (parsed arguments).

    This function processes the ls command with the specified options and prints the output.
    The file_info parameter should contain a dictionary with a "contents" key, representing the
    directory structure. The options parameter holds information about how the ls command should be executed.

    The function handles options such as showing all files and directories, printing in long format,
    reversing the order, sorting by time_modified, and filtering based on file or directory, printing sizes in human-readable format.

    If the input path is a file, it prints the details of that file. If it is a directory, it prints the contents of that directory.

    :return: None
    """
    file_info_to_print = []
    if "contents" not in file_info:
        raise ValueError("invalid file_info structure. 'contents' key not found.")

    filtered_file_info = file_info.copy()
    if options['--filter']:
        filtered_file_info.update(filter_assets(file_info, options['--filter']))

    path = options['<path>']
    if not path:
        file_info_to_print = filtered_file_info["contents"]
    else:
        path_parts = path.split("/")
        current_info = filtered_file_info

        for part in path_parts:
            if not part:
                continue

            part_info = next((item for item in current_info.get("contents", []) if item['name'] == part), None)
            if part_info and is_directory(part_info.get('permissions', '')):
                current_info = part_info
            else:
                if part == path_parts[-1]:
                    # Check if it's a file or directory
                    if is_directory(part_info.get('permissions', '')):
                        file_info_to_print = part_info.get("contents", [])
                    else:
                        file_info_to_print = [part_info]
                else:
                    print(f"error: {part} is not a valid directory or file in the path.")
                    sys.exit(1)

    if not file_info_to_print:
        file_info_to_print = current_info.get("contents", [])

    # Sort file_info_to_print after the loop
    file_key = "time_modified" if options['--time'] else "name"
    file_info_to_print = sorted(file_info_to_print, key=lambda x: x[file_key], reverse=options['--reverse'])

    for item in file_info_to_print:
        print_file_info(item, options)
    else:
        print("\n")


def main():
    # usage string for docopt
    usage = """
    Python linux utility ls command

    Usage:
      pyls.py [-A] [-l] [-r] [-t] [--filter=<option>] [-h] [<path>]

    Options:
      -A, --show-all          Show all files and directories
      -l, --long-format       Print in long format i.e <permission size last_modification file/folder>
      -r, --reverse           Print in reverse order with long format i.e <permission size last_modification file/folder>
      -t, --time              Sort by time_modified
      --filter=<option>       Filter output based on 'file' or 'dir'
      -h --human-readable     Show human-readable sizes
      --help                  Show this help message and exit
    """

    # parse arguments using docopt
    args = docopt(usage)

    # read the json data from the file
    with open('structure.json', 'r') as file:
        structure_data = json.load(file)

    # Check if the provided path exists recursively
    path = args['<path>']
    if path and not path_exists_recursive(path, structure_data):
        print(f"error: cannot access '{path}': No such file or directory")
        sys.exit(1)

    # execute ls command
    ls_command(structure_data, args)


if __name__ == "__main__":
    main()
