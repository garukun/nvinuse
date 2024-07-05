import os
import json
import argparse

def find_node_versions(directory):
    node_versions = set()

    for root, dirs, files in os.walk(directory):
        # Skip node_modules folders
        if 'node_modules' in dirs:
            dirs.remove('node_modules')

        for file in files:
            if file == 'package.json':
                package_json_path = os.path.join(root, file)
                try:
                    with open(package_json_path, 'r') as f:
                        package_data = json.load(f)
                        engines = package_data.get('engines', {})
                        if isinstance(engines, dict):
                            node_version = engines.get('node')
                            if node_version:
                                node_versions.add(node_version)
                        elif isinstance(engines, list):
                            for engine in engines:
                                if isinstance(engine, dict) and 'node' in engine:
                                    node_versions.add(engine['node'])
                except json.JSONDecodeError:
                    print(f"Error parsing {package_json_path}")

            elif file == '.nvmrc':
                nvmrc_path = os.path.join(root, file)
                try:
                    with open(nvmrc_path, 'r') as f:
                        node_version = f.read().strip()
                        if node_version:
                            node_versions.add(node_version)
                except IOError:
                    print(f"Error reading {nvmrc_path}")

    return list(node_versions)

def main():
    parser = argparse.ArgumentParser(description="Scan directory for Node.js versions in package.json and .nvmrc files.")
    parser.add_argument("-d", "--directory", required=True, help="Directory path to scan")
    args = parser.parse_args()

    directory = args.directory

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    node_versions = find_node_versions(directory)

    if node_versions:
        for version in node_versions:
            print(f"{version}")
    else:
        print("No Node.js versions found.")

if __name__ == "__main__":
    main()