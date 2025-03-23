
from md_to_html import markdown_to_html_node

def main():
    md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
    node = markdown_to_html_node(md)
    print([node.to_html()])
    print(["<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"])



if __name__ == "__main__":
    main()