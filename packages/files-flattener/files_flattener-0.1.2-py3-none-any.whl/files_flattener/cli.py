import sys
from .core import list_files, write_files_to_output, USAGE
from .common import logger


def main():
    if len(sys.argv) < 3:
        logger.info(USAGE)
        sys.exit(1)

    directory = sys.argv[1]
    output_file = sys.argv[2]
    ignore_file = sys.argv[3] if len(sys.argv) > 3 else None  # Optional

    files_list = list_files(directory, ignore_file)

    for file in files_list:
        logger.info(file)

    write_files_to_output(directory, output_file, files_list)
    logger.debug(f"All files have been successfully written to {output_file}")


if __name__ == "__main__":
    main()
