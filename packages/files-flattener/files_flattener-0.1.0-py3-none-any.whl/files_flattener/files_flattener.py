import os
import pathspec
from concurrent.futures import ThreadPoolExecutor


def get_spec(ignore_file):
    with open(ignore_file, "r", encoding="utf-8") as f:
        ignore_patterns = f.read().splitlines()
    return pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern, ignore_patterns
    )


def list_files(directory, ignore_file=None):
    files_list = []
    spec = None

    if ignore_file:
        if not os.path.exists(ignore_file):
            raise FileNotFoundError(f"Ignore file {ignore_file} does not exist.")
        spec = get_spec(ignore_file)
    elif os.path.exists(os.path.join(directory, ".ignore")):
        spec = get_spec(os.path.join(directory, ".ignore"))

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            if spec and spec.match_file(relative_path):
                continue
            files_list.append(relative_path)

    return files_list


def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as infile:
        return infile.read()


def write_files_to_output(directory, output_file, files_list):
    with open(output_file, "w", encoding="utf-8") as outfile:
        with ThreadPoolExecutor() as executor:
            future_to_file = {
                executor.submit(
                    read_file_content, os.path.join(directory, relative_path)
                ): relative_path
                for relative_path in files_list
            }

            for future in future_to_file:
                relative_path = future_to_file[future]
                try:
                    content = future.result()
                    outfile.write(f"**{relative_path}:**\n\n")
                    outfile.write(content)
                    outfile.write("\n\n")
                except Exception as exc:
                    print(f"Error reading file {relative_path}: {exc}")
