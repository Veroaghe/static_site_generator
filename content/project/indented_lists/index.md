$ stylesheet=project.css $

[<< Back to Project Page](/project)

# List indentation

> Add indentation to lists with alternating list style-types for each level of indentation

## Work In Progress

### **2025-04-15**

**Stack Overflow** [Indenting lists in HTML](https://stackoverflow.com/questions/29464815/indenting-lists-in-html)

To indent a list, we need to add the whole `ol` or `ul` parent node of the indented section to the list of children of the previous `li` node of the list that is less indented.

As a reminder, here's how the HTML nodes are currently structured. Curly brackets represent the list of children for a Parent Node. The following example is for an Ordered List:

```
Parent Node OL {
    Parent Node LI {
        Leaf Nodes, each containing text as a value and the possibility of formatting (like bold or italic)
    }
    Parent Node LI {
        Leaf Nodes, each containing text as a value and the possibility of formatting (like bold or italic)
    }
    ...
}
```

Here's how the above example would look if we wanted to add an Unordered List `ul` between the first and second `li` item of the Ordered List `ol`:

```
Parent Node OL {
    Parent Node LI {
        Leaf Nodes...
        Parent Node UL {
            Parent Node LI {
                Leaf Nodes...
            }
            Parent Node LI {
                Leaf Nodes...
            }
            ...
        }
    }
    Parent Node LI {
        Leaf Nodes...
    }
    ...
}
```

## **2025-04-16** How are list blocks handled currently?

1. `markdown_to_html_node` is called with the markdown text as its input argument. 
2. Inside `markdown_to_html_node`, `markdown_to_blocks` splits the markdown text into blocks by splitting the text at every 2 newline characters `\n\n`. It also strips each block, which shouldn't be a problem as the first list item shouldn't be indented at all.
3. Each block is fed to `block_to_html_node` which first uses `block_to_block_type` to determine the type of each block; once type is determined, it parses the text of a block into its HTML ParentNode with children.

### How does `block_to_block_type` handle list type checking currently?

```
def block_to_block_type(block):
    ...
    lines = block.split("\n")
    ...

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
```

Looking at the code, whenever a line doesn't start with a bullet or number (+ following space), the block is immediately shipped off as a Paragraph. This means trouble for lists with indented sections.

We might be able to bypass this by `.lstrip` each line, to determine if it is still a list item. The actual parsing of the text is done by another function, `block_to_html_node`, so we don't need to worry about it right now. As long as each line is by definition a list item, we can give it its first determined list type as its block\_type.

That being written out now, I'm starting to think it might be beneficial to change the way list\_blocks are handled entirely: instead of determining wether a list\_block is an _unordered_ or an _ordered_ list at this stage, we might want to use a more general `BlockType.LIST`.

## **2025-04-18** Indented list builder

Yesterday I already tried making a modified version of `block_to_block_type` and while doing so I thought "How will I be able to test this thorougly?". It would be a hassle to write different types of indented lists in all sorts of variations. That's how I then spent the next day and a half building a function that builds indented lists. Well, maybe it took me about an hour or 2 in total.

```
def indented_list_builder(indent_spaces=2, max_indent_level = 4):
    output = []
    indent_level = None
    previous_level = None
    list_type = random.choice(["ul", "ol"])

    list_num = 0
    if list_type == "ul":
        bullet = random.choice(["-", "*"])
    else:
        list_num += 1
        bullet = f"{list_num}."

    for _ in range(random.randint(5, 20)):
        if indent_level is None:
            indent_level = 0
            output.append(f"{' ' * indent_level * indent_spaces}{bullet} {list_type.upper()} Level {indent_level}")
            continue

        # Randomizing indent_level of the next line
        #  Indent_level may increase by 1
        #  Indent_level may decrease to a level from 0 to current_level - 1
        previous_level = indent_level
        level_influencer = random.random()
        if indent_level == 0:
            if level_influencer > 0.5:
                indent_level += 1
        elif indent_level == max_indent_level:
            if level_influencer < 0.5:
                indent_level -= random.randint(0, indent_level)
        else:
            if level_influencer > 0.750:
                indent_level += 1
            elif level_influencer < 0.250:
                indent_level -= random.randint(0, indent_level)
        
        # When going up a level, we can pick a random list_type
        if previous_level < indent_level:
            list_type = random.choice(["ul", "ol"])
            # The following if clause is to ensure the bullets of a new unordered list
            # aren't the same as the one from the previous unordered list, if they only
            # differ in one indent_level
            if list_type == "ul" and indent_level != 0:
                # for i in range(len(output) - 1, -1, -1):
                #     if f"UL Level {indent_level - 1}" in output[i]:
                previous_bullet = output[-1].lstrip()[0]
                if previous_bullet == "-":
                    bullet = "*"
                    # break
                elif previous_bullet == "*":
                    bullet = "-"
                    # break
                else:
                    bullet = random.choice(["-", "*"])
                    # break
            # A new ordered list should always start at 1.
            if list_type == "ol":
                list_num = 0

        # When going down a level, we should maintain the same list_type
        # that was used last at this level
        if previous_level > indent_level:
            # Go through the output list backwards
            for i in range(len(output) - 1, -1, -1):
                # if previous output at this level was an ordered list_type
                # continue its numbering
                if f"OL Level {indent_level}" in output[i]:
                    list_type = "ol"
                    list_num = int(output[i].lstrip().split(".")[0])
                    break
                # if previous output at this level was an unordered list_type
                # use its bullet
                if f"UL Level {indent_level}" in output[i]:
                    list_type = "ul"
                    bullet = output[i].lstrip()[0]
                    break
        
        if list_type == "ol":
            list_num += 1
            bullet = f"{list_num}."

        output.append(f"{' ' * indent_level * indent_spaces}{bullet} {list_type.upper()} Level {indent_level}")

    return "\n".join(output)
        
print(indented_list_builder())
```

Here are a few examples it produced:

```
1. OL Level 0
  - UL Level 1
  - UL Level 1
    * UL Level 2
    * UL Level 2
    * UL Level 2
      - UL Level 3
      - UL Level 3
      - UL Level 3
        1. OL Level 4
        2. OL Level 4
      - UL Level 3
      - UL Level 3
      - UL Level 3
2. OL Level 0
  1. OL Level 1
  2. OL Level 1
```

```
1. OL Level 0
  - UL Level 1
  - UL Level 1
2. OL Level 0
  - UL Level 1
3. OL Level 0
4. OL Level 0
5. OL Level 0
  1. OL Level 1
  2. OL Level 1
    1. OL Level 2
    2. OL Level 2
6. OL Level 0
7. OL Level 0
  1. OL Level 1
```

```
* UL Level 0
  - UL Level 1
    1. OL Level 2
* UL Level 0
* UL Level 0
  - UL Level 1
    * UL Level 2
    * UL Level 2
    * UL Level 2
    * UL Level 2
      1. OL Level 3
      2. OL Level 3
      3. OL Level 3
        1. OL Level 4
        2. OL Level 4
        3. OL Level 4
```