# abs, max, min
def abs(x: int | float) -> int | float:
    return x if x >= 0 else -x


def max(x: int | float, y: int | float) -> int | float:
    greater = x if x > y else y
    if isinstance(x, int) and isinstance(y, int):
        return greater
    return float(greater)


def min(x: int | float, y: int | float) -> int | float:
    lesser = x if x < y else y
    if isinstance(x, int) and isinstance(y, int):
        return lesser
    return float(lesser)