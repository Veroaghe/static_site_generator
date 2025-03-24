from md_to_html import markdown_to_html_node
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception(f"No title header found. Input:\n{markdown}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()
    
    html_node = markdown_to_html_node(from_contents)
    html_text = html_node.to_html()

    page_title = extract_title(from_contents)

    template_contents = template_contents.replace(r"{{ Title }}", page_title)
    template_contents = template_contents.replace(r"{{ Content }}", html_text)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    
    with open(dest_path, "w") as f:
        f.write(template_contents)