import random

def playground(block):
    lines = block.split()
    if block.startswith("- ") or block.startswith("* ") or block.startswith("1. "):
        i = 1
        last_type = None
        for line in lines:
            line_copy = line
            line = line.lstrip()
            # Checking if line is a correct unordered list_item
            if line.startswith("- ") or line.startswith("* "):
                last_type = "ul"
                continue
            # Checking if line is a correct numbered list_item
            if line.startswith("1. "):
                if last_type and last_type == "ol" and i != 2:
                    return "PARAGRAPH" #BlockType.PARAGRAPH
                last_type = "ol"
                i = 2
                continue
            # Checking if line is a correct numbered list_item
            if line.startswith(f"{i}. "):
                last_type = "ol"
                i += 1
                continue
            # No correct ordered or unordered list_items were found
            return "PARAGRAPH" #BlockType.PARAGRAPH
        # Looped through all lines without a problem
        return "LIST" #BlockType.LIST

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
        