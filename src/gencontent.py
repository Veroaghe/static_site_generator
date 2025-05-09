from md_to_html import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception(f"No title header found. Input:\n{markdown}")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()
    
    setup_dict, from_contents = extract_setup_override(from_contents)

    html_node = markdown_to_html_node(from_contents)
    html_text = html_node.to_html()

    page_title = extract_title(from_contents)

    if "stylesheet" in setup_dict:
        template_contents = template_contents.replace("/index.css", f"/{setup_dict['stylesheet']}")

    template_contents = template_contents.replace(r"{{ Title }}", page_title)
    template_contents = template_contents.replace(r"{{ Content }}", html_text)
    template_contents = template_contents.replace("href=\"/", f"href=\"{basepath}")
    template_contents = template_contents.replace("src=\"/", f"src=\"{basepath}")

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as f:
        f.write(template_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        if os.path.isdir(item_path):
            destination = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, destination, basepath)

        if item.endswith(".md"):
            new_item = item.removesuffix(".md") + ".html"
            destination = os.path.join(dest_dir_path, new_item)
            generate_page(item_path, template_path, destination, basepath)


def extract_setup_override(text):
    '''
    Lines at the top of a .md file that start with dollar sign $
    are used to change certain parameters with during setup
    The line should contain a key/value pair, written as "key=value"
    '''
    lines = text.split("\n")
    setup_dict = {}
    count = 0
    for line in lines:
        if not line.startswith("$"):
            break

        count += 1

        try:
            key, value = line[1:-1].strip().split("=")
            setup_dict[key.strip()] = value.strip()
        except Exception:
            print(f"Unable to extract setup override from:\n  {line}")
        

    return setup_dict, "\n".join(lines[count:])