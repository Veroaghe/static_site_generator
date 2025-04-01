# Static Site Generator Project

The [Static Site Generator Project](https://www.boot.dev/courses/build-static-site-generator-python) gave me the basic building blocks to create websites like this [Tolkien Fan Page](/). I would like to **take it a few steps further** and, while doing so, I want to **document any features I've added** to it here. You'll also find a **To Do list** with features I might add later.

## Done

- [Escaped delimiters are ignored by the `split_nodes_delimiters` function](/project/escaped_delims)

## To Do

- Make it possible to use different stylesheets
- Maybe use a special opening symbol inside a `.md` file to tell the code a line contains specific instructions on how to process this page. That way I could simply write such an instruction at the top the file, above the title header (e.g. an instruction to use a different stylesheet).
- Add indentation to lists.
- Make nested formatting possible.
- Add ability to format the text of a link
- Add `*` as a delimiter for italic text
- Make it so indentation of `code` blocks is maintained, even when the code blocks contain empty newlines
- Find a way to format code blocks to its programming language

## Fixes

- _2025-04-01_ : Inside `text_to_textnodes`, delimiters were processed before images and links, which gave errors when a URL contained a delimiter like an underscore. Fixed by running `split_nodes_image` and `split_nodes_link` before the loop of `split_nodes_delimiter`.