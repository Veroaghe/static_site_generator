
from gencontent import generate_pages_recursive
from copystatic import empty_docs_dir, copy_files_recursive, log_static_to_public_copy
import sys


def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"
    
    print(basepath)

    empty_docs_dir()
    log_items = copy_files_recursive("static")
    log_static_to_public_copy(log_items)
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()