"""
@author: jldupont
"""

import re
import logging
from typing import Dict, Tuple, List, Callable
from functools import cache
from importlib.metadata import entry_points, EntryPoint


REGEX_VALIDATE_NAME = re.compile(r"^[a-zA-Z][0-9a-zA-Z\_\-]{0,62}$")


def validate_name(name: str) -> bool:
    if not isinstance(name, str):
        return False

    return REGEX_VALIDATE_NAME.match(name) is not None


def remove_parenthesis(name: str) -> str:
    assert isinstance(name, str)

    return name.replace("(", "").replace(")", "")


@cache
def get_points() -> Dict[str, List[EntryPoint]]:

    _entry_points: Tuple[EntryPoint]
    _map: Dict[str, List[EntryPoint]] = dict()

    processed_names = []
    _entry_points = entry_points().get("pygcloud.events", None)  # type: ignore

    if _entry_points is None:
        raise Exception("Is the package installed locally ?")

    point: EntryPoint

    for point in _entry_points:
        name: str = point.name

        liste: List[EntryPoint] = _map.get(name, [])
        if name in processed_names:
            continue

        liste.append(point)
        _map[name] = liste
        processed_names.append(name)

    return _map


@cache
def get_hooks(name: str) -> List[EntryPoint]:
    return get_points().get(name, [])


@cache
def get_hook_callable(entry: EntryPoint) -> Callable:
    return entry.load()


def execute_hooks(name: str, deployer, *p, **kw):
    """
    Go through the list of hooks and
    execute their callable
    """
    from .deployer import Deployer

    assert isinstance(name, str)
    assert isinstance(deployer, Deployer)

    hooks = get_hooks(name)

    for hook in hooks:
        try:
            func = get_hook_callable(hook)
            func(deployer, *p, **kw)
        except Exception as e:
            print(e)
            logging.debug(f"Failed to call entry-point: {hook}: {e}")
