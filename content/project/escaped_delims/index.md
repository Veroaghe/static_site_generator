$ stylesheet=project.css $

[<< Back to Project Page](/project)

# Escaped Delimiters

[<< Back to Project Development Overview](/project)

> Escaped delimiters are ignored by the `split_nodes_delimiters` function

## Implementation

My version of the `split_nodes_delimiters` function uses a `start_index` variable to tell `text.find` from which index to start looking for the next `opening` delimiter. However, if an escaped character has been found, then we shouldn't start looking for other delimiters from `start_index` but from the index at which we found the last escaped delimiter. To solve this, I've added an `override` variable:

```python
start_index = 0
override = 0
while True: 
    opening = text.find(delimiter, start_index + override)
    ...
```

An escaped delimiter is one that is preceded by a backslash `\`. So when the function found a potential _opening delimiter_, it needs to check the previous character to know if it's an escaped character.

If it found a `\` then I want the code to do the following:

- remove the `\` from the text
- update the `override` variable
- `continue` to the next loop, effectively starting to look for another `opening` delimiter

```python
if text[opening - 1] == "\\":
    text = text[:opening - 1] + text[opening:]
    node.text = text
    override = opening - start_index
    continue
```

The previous piece of code is essentially a gatekeeper: as long as no legit opening delimiter is found, the rest of the code won't play out. Before that piece of code is the section that `breaks` the loop if `text.find` returns `-1`; which tells us no opening delimiter was found by the end of the text.

If our code manages to pass our gatekeeper, then the first thing the code does is resetting the `override` to 0, because the code will either update the `start_index` later beyond this point or `raise` an exception because no closing delimiter was found.

```python
override = 0
```

That's all there is to the modification.