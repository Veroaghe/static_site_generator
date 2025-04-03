$ stylesheet=project.css $

[<< Back to Project Page](/project)

# Setup Override

> Lines starting with $ at the start of a text can be used to deliver key/value pairs for a page specific setup

## Implementation

Lines starting with a `$` dollar sign (can) contain instructions to override the default setup with. I'm not sure if I've implemented this feature in a robust way, but at the moment it does what I want it to do. Here's how it works:

- The text is split into lines.
- Each line is checked of it starts with a `$`. If not, then the `for loop` breaks, meaning that these lines need to be at te very top to be detected.
- If a `$` line is found, then a counter gets an uptick. This counter will be used at the end to return the text without the `$` lines with.
- Then the code tries to split the line at an `=` equal sign, to extract a `key/value pair` from it, to be added to `setup_dict`.
- When the `for loop` ends, 2 items are returned: `setup_dict` and the text starting from the line at the counter.

For now, I'm using this feature to [assign a specific stylesheet to a page](/project/stylesheet_override) because the default stylesheet is centered around the [Tolkien Fan Page](/), which isn't very interesting for these documentation pages.

```python
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
```