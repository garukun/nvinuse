# Node Version Scanner

Node Version Scanner scans a directory and its subdirectories for `package.json` and `.nvmrc` files
to identify Node.js versions used in various projects.

## Features

- Scans for Node.js versions specified in `package.json` and `.nvmrc` files
- Ignores `node_modules` directories to avoid scanning dependencies
- Sorts versions in ascending order
- Option to describe the container diretory for each Node version detected,
  in "- <version>: <directory>" format.

## Requirements

- Python 3.6 or higher

## Usage

Run the script from the command line with the following syntax:

```shell
python script_name.py -d <directory_path> [--description]
```

### Arguments

- `-d, --directory`: (Required) The path to the directory you want to scan.
- `--description`: (Optional) Include this flag to show detailed output with file paths.

### Basic Output
```
lts/erbium
>=0.12.0
v8
>=10
v10.15.3
v12
```

### Output with Description
```
- lts/erbium: /path/to/parent/directory
- >=0.12.0: /path/to/parent/directory
- v8: /path/to/parent/directory
- >=10: /path/to/parent/directory
- v10.15.3: /path/to/parent/directory
- v12: /path/to/parent/directory
```