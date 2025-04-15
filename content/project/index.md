$ stylesheet=project.css $

# Static Site Generator Project

The [Static Site Generator Project](https://www.boot.dev/courses/build-static-site-generator-python) gave me the basic building blocks to create websites like this [Tolkien Fan Page](/). I would like to **take it a few steps further** and, while doing so, I want to **document any features I've added**. You'll also find a **To Do list** with features I might add later.

## Done

1. _2025-04-01_ [Escaped delimiters are ignored by the `split_nodes_delimiters` function](/project/escaped_delims)
2. _2025-04-03_ [Lines starting with $ at the start of a text can be used to deliver key/value pairs for a page specific setup](/project/setup_override)
3. _2025-04-03_ [Using the setup override from point 2, it is now possible to assign a different stylesheet to a page ](/project/stylesheet_override)

## To Do

- [Add indentation to lists with alternating list style-types for each level of indentation](/project/indented_lists)
- Make nested formatting possible.
- Add ability to format the text of a link
- Add `*` as a delimiter for italic text
- Make it so indentation of `code` blocks is maintained, even when the code blocks contain empty newlines
- Find a way to format code blocks to its programming language

## Fixes

- _2025-04-01_ : Inside `text_to_textnodes`, delimiters were processed before images and links, which gave errors when a URL contained a delimiter like an underscore. Fixed by running `split_nodes_image` and `split_nodes_link` before the loop of `split_nodes_delimiter`.