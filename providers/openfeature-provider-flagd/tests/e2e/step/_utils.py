import json
import typing


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


type_cast = {
    "Integer": int,
    "Float": float,
    "String": str,
    "Boolean": str2bool,
    "Object": json.loads,
}


JsonObject = typing.Union[dict, list]
JsonPrimitive = typing.Union[str, bool, float, int, JsonObject]
