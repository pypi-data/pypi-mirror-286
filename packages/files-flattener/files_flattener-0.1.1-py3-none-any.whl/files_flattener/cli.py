import sys
from .core import list_files, write_files_to_output, USAGE


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)

    directory = sys.argv[1]
    output_file = sys.argv[2]
    ignore_file = sys.argv[3] if len(sys.argv) > 3 else None  # Optional

    files_list = list_files(directory, ignore_file)

    for file in files_list:
        print(file)

    write_files_to_output(directory, output_file, files_list)
    print(f"All files have been successfully written to {output_file}")


if __name__ == "__main__":
    main()
