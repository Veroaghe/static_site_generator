$ stylesheet=project.css $

[<< Back to Project Page](/project)

# List indentation

> Add indentation to lists with alternating list style-types for each level of indentation

## Work In Progress

### 15-04-2025

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