import sys
from files_flattener import list_files, write_files_to_output

USAGE = """
Usage: flt <directory> [<ignore_file>] [> <output_file>]

Parameters:
  <directory>    : The path of the directory containing the files to be flattened.
  [<ignore_file>]: (Optional) The path to a file containing patterns of files to ignore.
                   If not provided, the script will look for a '.ignore' file in the specified directory.
                   If the '.ignore' file is not found, no files will be ignored.
  [> <output_file>]: The path of the output file where the contents of the files will be written.
"""


def main():
    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    directory = sys.argv[1]
    ignore_file = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.stdout if len(sys.argv) <= 3 else sys.argv[3]

    files_list = list_files(directory, ignore_file)

    if output_file == sys.stdout:
        for file in files_list:
            print(file)
    else:
        write_files_to_output(directory, output_file, files_list)
        print(f"All files have been successfully written to {output_file}")


if __name__ == "__main__":
    main()
