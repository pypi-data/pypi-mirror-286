from dataclasses import dataclass
from typing import Union

from typerx import with_dataclass


@dataclass
class Data:
    hi: int = 1
    ho: Union[int, str] = 1


@with_dataclass
def main(data: Data):
    """a simple demo"""
    print(data)
    return data


if __name__ == "__main__":
    import typer

    typer.run(with_dataclass(main))
