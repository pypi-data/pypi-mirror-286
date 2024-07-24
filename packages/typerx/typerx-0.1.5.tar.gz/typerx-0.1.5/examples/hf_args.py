import typer
from transformers.trainer import TrainingArguments


def main(args: TrainingArguments):
    return args


if __name__ == "__main__":
    from typerx import with_dataclass

    typer.run(with_dataclass(main))
