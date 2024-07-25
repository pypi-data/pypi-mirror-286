from __future__ import annotations

from pydantic import BaseModel, Field, BeforeValidator, ValidationError
from typing import Any, Type, Callable
from pydantic_core import core_schema
from pydantic.dataclasses import *

def strictdataclass(arg=None, /, **kwargs):

    DEFAULTS = dict(
        frozen=True,
        kw_only=True,
    )
    CONFIG_DEFAULTS = dict( 
        validate_default=True, 
        validate_assignment=True,
        validate_return=True,
        extra='forbid',
    )

    if arg is None: 

        for key, val in DEFAULTS.items():
            if kwargs.get(key, None) is None:
                kwargs[key] = val

        config = kwargs.get('config', {})
        config = {**CONFIG_DEFAULTS, **config}
        kwargs['config'] = config
        return dataclass(**kwargs)

    else:

        return dataclass(config=CONFIG_DEFAULTS,**DEFAULTS)(arg)

def autoconverted(
        type_: Type[Any], 
        converter_function: Callable[[Any], Type[Any]] | None = None
):

    convert = type_ if converter_function is None else converter_function

    def get_schema(cls, source_type: Type[Any], handler: Any) -> Any:
        def validator(v: Any, info: core_schema.ValidationInfo) -> type_:
            return v if isinstance(v, type_) else convert(v)
        return core_schema.with_info_plain_validator_function(validator)

    cls = type(
        type_.__name__ + '_pydantic',
        (),
        {'__get_pydantic_core_schema__': classmethod(get_schema)}
    )
    return cls

