import argparse
import json
import os
import re

def parse_version(version_str):
    clean_version = re.sub(r'^[^0-9]*', '', version_str.strip())
    parts = clean_version.split('.')
    return [int(p) if p.isdigit() else 0 for p in parts] + [0] * (3 - len(parts))

def version_key(version_str):
    return parse_version(version_str)

def find_node_versions(directory):
    node_versions = []

    for root, dirs, files in os.walk(directory):
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
                                node_versions.append((node_version, os.path.dirname(package_json_path)))
                        elif isinstance(engines, list):
                            for engine in engines:
                                if isinstance(engine, dict) and 'node' in engine:
                                    node_versions.append((engine['node'], os.path.dirname(package_json_path)))
                except json.JSONDecodeError:
                    print(f"Error parsing {package_json_path}")

            elif file == '.nvmrc':
                nvmrc_path = os.path.join(root, file)
                try:
                    with open(nvmrc_path, 'r') as f:
                        node_version = f.read().strip()
                        if node_version:
                            node_versions.append((node_version, os.path.dirname(nvmrc_path)))
                except IOError:
                    print(f"Error reading {nvmrc_path}")

    return node_versions

def sort_versions(node_versions):
    return sorted(node_versions, key=lambda x: version_key(x[0]))

def main():
    parser = argparse.ArgumentParser(description="Scan directory for Node.js versions in package.json and .nvmrc files.")
    parser.add_argument("-d", "--directory", required=True, help="Directory path to scan")
    parser.add_argument("--description", action="store_true", help="Print detailed desgit scription with parent directories")
    args = parser.parse_args()

    directory = args.directory

    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    node_versions = find_node_versions(directory)
    sorted_versions = sort_versions(node_versions)

    if sorted_versions:
        if args.description:
            for ver, path in sorted_versions:
                print(f"- {ver}: {path}")
        else:
            unique_versions = sorted(set(ver for ver, _ in sorted_versions), key=version_key)
            for ver in unique_versions:
                print(f"{ver}")
    else:
        print("No Node.js versions found.")

if __name__ == "__main__":
    main()