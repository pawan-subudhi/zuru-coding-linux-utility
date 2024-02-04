import argparse
import json

def ls_command(data, show_all=False):
    """
    Handles Subtask: 1, 2

    Implements the ls command for the given JSON data.
    :param data: JSON data representing the file structure
    :param show_all: Flag to include all files and directories (including hidden ones)
    """
    for item in data['contents']:
        name = item['name']
        if not show_all and name.startswith('.'):
            continue

        print(name, end=' ')
    else:
        print("\n")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Python linux utility ls command")
    parser.add_argument('-A', '--show-all', action='store_true', help="Show all files and directories")
    args = parser.parse_args()

    # Read the JSON data from the file
    with open('structure.json', 'r') as file:
        structure_data = json.load(file)

    # Execute ls command
    ls_command(structure_data, show_all=args.show_all)

if __name__ == "__main__":
    main()
