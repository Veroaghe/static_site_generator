
from gencontent import generate_pages_recursive
from copystatic import empty_public_dir, copy_files_recursive, log_static_to_public_copy


def main():
    empty_public_dir()
    log_items = copy_files_recursive("./static")
    log_static_to_public_copy(log_items)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()