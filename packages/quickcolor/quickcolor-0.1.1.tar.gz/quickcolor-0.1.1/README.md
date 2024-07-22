# QuickColor

**QuickColor** is a Python library providing tags for color formatting sections of printable content. The tags can be flexibly used as part of any string as they simply resolve to the ASCII color codes interpreted by your terminal or terminal emulator.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **quickcolor**.

```bash
pip install quickcolor
```


## Library Usage
```python
from quickcolor.color_def import color

# colorize printable content
print(f"{color.CGREEN2}This text is bold green{color.CEND}")
```
```python
from quickcolor.color_def import colors

# alternate method to colorize printable content
print(f"Formatting this phrase part to {colors.fg.yellow}display yellow{colors.off}")
```


## CLI Utility

The following CLI is included with this package for visualizing available color fields and code combinations.

```bash
# qc -h
usage: qc [-h] {shell.colors,color.fields} ...

-.-.-. Color attributes for python scripts

positional arguments:
  {shell.colors,color.fields}
    shell.colors   display a color chart for current shell
    color.fields   display class color fields

options:
  -h, --help            show this help message and exit

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements
Inspiration for the color names came from [this StackOverflow reply](https://stackoverflow.com/a/39452138).
