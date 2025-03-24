
import os
import shutil
import time

def main():
    empty_public_dir()
    log_items = copy_from_static_to_public_dir("./static")
    log_static_to_public_copy(log_items)


def empty_public_dir():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")


def copy_from_static_to_public_dir(source):
    destination = "./public" + source[len("./static"):]
    if not os.path.exists(destination):
        os.mkdir(destination)

    log_items = []
    content = os.listdir(source)
    for item in content:
        item_path = os.path.join(source, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination)
        else:
            log_items += copy_from_static_to_public_dir(item_path)
    
    return [(source, content, destination)] + log_items


def log_static_to_public_copy(log_items):
    with open("./log.txt", "w") as f:
        f.write(time.ctime(time.time()))
        for source, content, destination in log_items:
            f.write(f"\nFollowing items were copied from \"{source}\" to \"{destination}\"")
            [f.write(f"\n  - {item}")for item in content]
            f.write("\n")



    

if __name__ == "__main__":
    main()