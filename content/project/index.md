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
- _2025-04-16_ : `markdown_to_blocks` handles a **code_block**, i.e. a block that starts and ends with 3 backticks **\`\`\`**, uniquely, allowing code\_blocks to have code separated by double newline characters `\n\n`. However, each section was first stripped of trailing spaces, which meant that the first line's indentation of a code\_block section could become lost. This has now been fixed.
- _2025-04-16_ : Added an exception inside `markdown_to_blocks` that would raise whenever the `open_code_block` variable would be `True`, meaning that we found a block starting with 3 backticks **\`\`\`** but not a block ending with 3 backticks, after the loop through all the blocks had ended.
- - _2025-04-18_ : a bug was found in `markdown_to_blocks` with the way it handles **code_blocks**. While no ending 3 backticks are found for a code\_block, all the blocks that follow are stored in a list with the name **stalled_blocks**. Once the ending 3 backticks are found, the blocks in the list are rejoined with `\n\n` in between them. The bug was that this **stalled_blocks** list wasn't emptied after rejoining the blocks, meaning its contents would persist if there ever was another code\_block with multiple sections.