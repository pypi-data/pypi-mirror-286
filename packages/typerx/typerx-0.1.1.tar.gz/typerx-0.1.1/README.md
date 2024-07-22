# TyperX

TyperX is a library for extending Typer with features useful in Machine Learning applications, including:

- Basic dataclass type support [x]
- Basic union type support [x]
- Recursive dataclass type support [ ]
- pydantic model support [ ]

## Installation

Install TyperX using pip:

```bash
pip install agentx
```

## Usage Example

Create a file named `main.py`:

```python
from dataclasses import dataclass
from typing import Union

@dataclass
class Data:
    hi: int = 1
    ho: Union[int, str] = 1

def main(data: Data):
    print(data)

if __name__ == "__main__":
    import typer
    from typerx import with_dataclass

    typer.run(with_dataclass(main))
```

Run the script and check the help message:

```bash
python main.py --help
```

You should see output similar to this:

```
 Usage: main.py [OPTIONS]

 a simple demo

╭─ Options ───────────────────────────────────────────────────────────────────────╮
│ --data.hi        INTEGER           [default: 1]                                 │
│ --data.ho        UNION[INT, STR]   [default: 1]                                 │
│ --help                             Show this message and exit.                  │
╰─────────────────────────────────────────────────────────────────────────────────╯
```

Run the script without any options:

```bash
python main.py
```

This will output:

```
Data(hi=1, ho=1)
```
