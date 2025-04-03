$ stylesheet=project.css $

[<< Back to Project Page](/project)

# Stylesheet Override

> Using the setup override from point 2, it is now possible to assign a different stylesheet to a page 

## Implementation

- In the `generate_page` function, that is used to fabricate an HTML page from a Markdown page, the [extract_setup_override](/project/setup_override) function is called on the markdown text. It returns a `setup_override` dictionary and the text.
- If the dictionary contains a `stylesheet` key, its value will be used to replace the default stylesheet.

```python
setup_dict, from_contents = extract_setup_override(from_contents)
# ...
if "stylesheet" in setup_dict:
    template_contents = template_contents.replace("/index.css", f"/{setup_dict['stylesheet']}")
```

**Example** of how a setup\_override line looks in the markdown file

```
$ stylesheet=project.css $
```