from typing import Union

from pydantic import BaseModel, create_model


def get_union_parser(typ):
    # wrap as pydantic model
    model = create_model("UnionModel", value=(typ, ...))

    def parse_union(value: str):
        return model.model_validate({"value": value}).value

    parse_union.__name__ = f"{typ}]"[7:]

    return parse_union, model
