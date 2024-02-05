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

    :return: None
    """
    if "contents" not in file_info:
        raise ValueError("invalid file_info structure. 'contents' key not found.")

    filtered_file_info = file_info.copy()
    if options['--filter']:
        filtered_file_info.update(filter_assets(file_info, options['--filter']))

    file_key = "time_modified" if options['--time'] else "name"
    file_info_to_print = sorted(filtered_file_info["contents"], key=lambda x: x[file_key], reverse=options['--reverse'])

    for item in file_info_to_print:
        name = item['name']
        if not options['--show-all'] and name.startswith('.'):
            continue

        permissions = item.get("permissions", "")
        size = item.get("size", 0)
        time_modified = item.get("time_modified", 0)
        name = item.get("name", "")

        formatted_time = datetime.datetime.fromtimestamp(time_modified).strftime("%b %d %H:%M")

        if options['--long-format']:
            if options['--human-readable']:
                human_readable_size = convert_bytes_to_human_readable(size)
                print(f"{permissions} {human_readable_size} {formatted_time} {name}")
            else:
                print(f"{permissions} {size} {formatted_time} {name}")
        else:
            print(name, end=' ')
    else:
        print("\n")


def main():
    # usage string for docopt
    usage = """
    Python linux utility ls command

    Usage:
      pyls.py [-A] [-l] [-r] [-t] [--filter=<option>] [-h]

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

    # execute ls command
    ls_command(structure_data, args)


if __name__ == "__main__":
    main()
