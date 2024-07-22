import dataclasses
import inspect
from typing import Annotated, Union

import typer

from ._union import get_union_parser

dataclasses.field


class _DataclassParameter:
    def __init__(self, param: dataclasses.dataclass):
        self._param = param
        self._wrapped_params = {}
        for p in param.annotation.__dataclass_fields__.values():
            # skip init=False fields
            if p.init is False:
                continue

            wrapped_param_name = f"{self._param.name}_{p.name}"
            typer_param_name = f"--{self._param.name}.{p.name}"

            # hook union type
            annotation_type = p.type
            parser = None
            if hasattr(p.type, "__origin__") and p.type.__origin__ == Union:
                types = []
                for type_ in p.type.__args__:
                    if type_ is type(None):
                        continue
                    types.append(type_)
                if len(types) > 1:
                    parser, model = get_union_parser(p.type)
                    annotation_type = model

            default_factory = None
            default = inspect.Parameter.empty
            if p.default is not dataclasses.MISSING:
                default = p.default
            if p.default_factory is not dataclasses.MISSING:
                default_factory = p.default_factory
            wrapped_param = inspect.Parameter(
                name=wrapped_param_name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=default,
                annotation=Annotated[
                    annotation_type,
                    typer.Option(
                        typer_param_name,
                        parser=parser,
                        help=p.metadata.get("help", ""),
                        default_factory=default_factory,
                    ),
                ],
            )
            self._wrapped_params[p.name] = wrapped_param

    def invoke(self, passed_kwargs: dict):
        kwargs = {}
        for wrapped_param_name, wrapped_param in self._wrapped_params.items():
            kwargs[wrapped_param_name] = passed_kwargs[wrapped_param.name]
        return self._param.annotation(**kwargs)

    def flattened_params(self):
        return list(self._wrapped_params.values())


class _BaseParameter:
    def __init__(self, param):
        self.param = param

    def invoke(self, passed_kwargs: dict):
        return passed_kwargs[self.param.name]

    def flattened_params(self):
        return [self.param]


def with_dataclass(func):
    wrapped_params = {}
    for param in inspect.signature(func).parameters.values():
        if dataclasses.is_dataclass(param.annotation):
            wrapped_params[param.name] = _DataclassParameter(param)
        else:
            wrapped_params[param.name] = _BaseParameter(param)

    def wrapped_func(**kwargs):
        invoke_kwargs = {}
        for name, param in wrapped_params.items():
            invoke_kwargs[name] = param.invoke(kwargs)
        return func(**invoke_kwargs)

    flattened_params = [
        param for wrapped_param in wrapped_params.values() for param in wrapped_param.flattened_params()
    ]

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
