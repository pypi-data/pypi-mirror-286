import copy


def delete(obj: dict, key: str) -> dict:
    obj_copy = copy.deepcopy(obj)
    obj_copy.pop(key, None)
    return obj_copy


def get(obj: dict, keys: str | list) -> any:
    if len(keys) == 1:
        keys = keys[0]
    if isinstance(keys, str) or isinstance(keys, int):
        return obj[keys]
    else:
        return get(obj[keys[0]], keys[1:])


def merge(first: dict, second: dict) -> dict:
    return {**first, **second}


def merge_nested(first: dict, second: dict):
    copy_first = copy.deepcopy(first)
    copy_second = copy.deepcopy(second)
    _merge_nested(copy_first, copy_second)
    return copy_first


def _merge_nested(first: dict, second: dict):
    for k, v in second.items():
        # @formatter:off
        if k in first and isinstance(first[k], dict) and isinstance(second[k], dict):
            merge_nested(first[k], second[k])
        else:
            first[k] = second[k]