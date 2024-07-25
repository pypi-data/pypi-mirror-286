import logging
import pandas as pd
from sqlalchemy import types

def disable_logging(func):
    def wrapper(*args, **kwargs):
        logging.disable(logging.CRITICAL)
        try:
            return func(*args, **kwargs)
        finally:
            logging.disable(logging.NOTSET)
    return wrapper

def map_types(dtype: pd.api.types) -> types.TypeEngine:
    if pd.api.types.is_integer_dtype(dtype):
        return types.Integer()
    elif pd.api.types.is_float_dtype(dtype):
        return types.Float()
    elif pd.api.types.is_bool_dtype(dtype):
        return types.Boolean()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return types.DateTime()
    else:
        return types.String()