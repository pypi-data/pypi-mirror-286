import inspect
from dataclasses import MISSING, Field, is_dataclass
from typing import Annotated, List, Union

import typer

FLATTENED_PARAM_NAME_BUILDER = lambda prefixs: "_".join(prefixs)
CLI_PARAM_NAME_BUILDER = lambda prefixs: "--" + ".".join(prefixs)


def get_union_parser(typ):
    # wrap as pydantic model
    from pydantic import create_model

    model = create_model("UnionModel", value=(typ, ...))

    def parse_union(value: str):
        return model.model_validate({"value": value}).value

    parse_union.__name__ = f"{typ}]"[7:]

    return parse_union, model


def flatten_dataclass(dataclass_type, prefixs: List[str]):
    flattened_params = []
    field_name_to_flattened_name = {}

    fields: List[Field] = dataclass_type.__dataclass_fields__.values()
    for field in fields:
        # init=False means the field should not be passed when creating the object
        # it is used for internal use
        if field.init is False:
            continue

        field_prefixs = prefixs + [field.name]
        if is_dataclass(field.type):
            sub_flattened_params, sub_field_name_to_flattened_name = flatten_dataclass(field.type, field_prefixs)
            flattened_params.extend(sub_flattened_params)
            field_name_to_flattened_name[field.name] = (field.type, sub_field_name_to_flattened_name)
            continue

        flattened_param_name = FLATTENED_PARAM_NAME_BUILDER(field_prefixs)
        cli_param_name = CLI_PARAM_NAME_BUILDER(field_prefixs)

        annotation_type = field.type
        parser = None
        default_factory = None
        default = inspect.Parameter.empty
        help = field.metadata.get("help", "")

        # hook union type
        if hasattr(field.type, "__origin__") and field.type.__origin__ == Union:
            types = []
            for type_ in field.type.__args__:
                if type_ is type(None):
                    continue
                types.append(type_)
            if len(types) > 1:
                parser, model = get_union_parser(field.type)
                annotation_type = model

        if field.default is not MISSING:
            default = field.default
        if field.default_factory is not MISSING:
            default_factory = field.default_factory
        flattened_param = inspect.Parameter(
            name=flattened_param_name,
            kind=inspect.Parameter.KEYWORD_ONLY,
            default=default,
            annotation=Annotated[
                annotation_type,
                typer.Option(
                    cli_param_name,
                    parser=parser,
                    help=help,
                    default_factory=default_factory,
                ),
            ],
        )
        flattened_params.append(flattened_param)
        field_name_to_flattened_name[field.name] = flattened_param_name

    return flattened_params, field_name_to_flattened_name


def fold_dataclass(kwargs: dict, field_name_to_flattened_name: dict):
    folded_kwargs = {}
    for field_name, flattened_name in field_name_to_flattened_name.items():
        if isinstance(flattened_name, tuple):
            sub_type, sub_field_name_to_flattened_name = flattened_name
            sub_kwargs = fold_dataclass(kwargs, sub_field_name_to_flattened_name)
            folded_kwargs[field_name] = sub_type(**sub_kwargs)
        else:
            folded_kwargs[field_name] = kwargs[flattened_name]
    return folded_kwargs


def with_dataclass(func):
    flattened_params = []
    field_name_to_flattened_name = {}
    for param in inspect.signature(func).parameters.values():
        if is_dataclass(param.annotation):
            sub_flattened_params, sub_field_name_to_flattened_name = flatten_dataclass(param.annotation, [param.name])
            flattened_params.extend(sub_flattened_params)
            field_name_to_flattened_name[param.name] = (param.annotation, sub_field_name_to_flattened_name)
        else:
            param = inspect.Parameter(
                name=param.name,
                kind=param.kind,
                default=param.default,
                annotation=Annotated[
                    param.annotation,
                    typer.Option(
                        f"--{param.name}",
                        help=param.annotation.__name__,
                    ),
                ],
            )
            flattened_params.append(param)
            field_name_to_flattened_name[param.name] = param.name

    def wrapped_func(**kwargs):
        invoke_kwargs = fold_dataclass(kwargs, field_name_to_flattened_name)
        return func(**invoke_kwargs)

    flattened_params = sorted(
        flattened_params,
        key=lambda p: p.default is inspect.Parameter.empty,
        reverse=True,
    )

    wrapped_func.__signature__ = inspect.Signature(parameters=flattened_params)
    if func.__doc__:
        wrapped_func.__doc__ = func.__doc__ + "\n" + ""

    return wrapped_func


__all__ = ["with_dataclass"]
