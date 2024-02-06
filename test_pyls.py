import json
import pytest
from pyls import ls_command

def load_structure_data():
    with open('structure.json', 'r') as file:
        return json.load(file)

# Define a fixture to provide sample data for testing
@pytest.fixture
def structure_data():
    return load_structure_data()

# Test ls_command with specific options
def test_ls_command(structure_data, capsys):
    options = {
        "--long-format": True,
        "--reverse": True,
        "--time": True,
        "--filter": "file",
        "--show-all": False,
        "--human-readable": False,
        "<path>": None,
    }

    ls_command(structure_data, options)

    captured = capsys.readouterr()
    expected_output = (
        "-rw-r--r-- 74 Nov 14 13:57 main.go\n"
        "-rwxr-xr-x 60 Nov 14 13:51 go.mod\n"
        "-rwxr-xr-x 1071 Nov 14 11:27 LICENSE\n"
        "-rwxr-xr-x 83 Nov 14 11:27 README.md\n"
    )

    assert captured.out.strip() == expected_output.strip()

