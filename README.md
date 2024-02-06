# zuru-coding-linux-utility

Python program, that takes a json file (which contains the information of a directory in nested structure) and prints out its content in the console in the style of ls (linux utility).

# pyls.py - Python LS Command

pyls.py is a Python implementation of the ls command, providing a simple and customizable way to list files and directories in a specified path.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/pawan-subudhi/zuru-coding-linux-utility.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pyls
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python pyls.py [OPTIONS] [PATH]
```

- `[OPTIONS]`: Optional command-line options. See available options below.
- `[PATH]`: Optional path to the directory or file. If not provided, the current directory is used.

### Command-line Options

- `-A, --show-all`: Show all files and directories, including hidden ones.
- `-l, --long-format`: Print in long format, displaying permissions, size, last modification, and file/folder names.
- `-r, --reverse`: Print in reverse order with long format.
- `-t, --time`: Sort by time_modified.
- `--filter=<option>`: Filter output based on 'file' or 'dir'.
- `-h --human-readable`: Show human-readable sizes.
- `--help`: Show help message and exit.

### Examples

1. List files and directories in the current directory:

   ```bash
   python -m pyls
   ```

2. List files and directories including hiddens in the current directory:

   ```bash
   python -m pyls -A
   ```

3. List files and directories in long format:

   ```bash
   python -m pyls -l
   ```

4. List files and directories in long format but in reverse format:

   ```bash
   python -m pyls -l -r
   ```

5. List files and directories in long format but in reverse format and the results sorted by time_modified(oldest first):

   ```bash
   python -m pyls -l -r -t
   ```

6. Filter and list only files/dir:

   ```bash
   # for files
   python -m pyls -l -r -t --filter=file

   # for directories
   python -m pyls -l -r -t --filter=dir
   ```

7. List files and directories in a specific path:

- The output will be the contents of the parser subdirectory under interpreter directory.
  ```bash
  python -m pyls -l parser
  ```
- If the path is a file, it should list the file itself

  ```bash
  python -m pyls -l parser/parser.go
  ```

8. Show human readable size:

```bash
 python -m pyls -l parser -h
```

9. For additional information and options, run:
   ```bash
   python -m pyls --help
   ```
