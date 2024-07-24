from dataclasses import dataclass
from typing import Union


@dataclass
class Name:
    first: str
    last: str


@dataclass
class Person:
    name: Name
    age: int
    score: Union[int, float]


def main(person: Person):
    """a simple demo"""
    print(person)
    return person


if __name__ == "__main__":
    import typer

    from typerx import with_dataclass

    typer.run(with_dataclass(main))
