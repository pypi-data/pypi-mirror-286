"""
json utilities for debugging serializability and attempting to ensure it in
some cases.
"""
import copy
import decimal
import fractions
import pathlib
import ubelt as ub
from collections import OrderedDict

try:
    import numpy as np
except ImportError:
    np = None


def debug_json_unserializable(data, msg=''):
    """
    Raises an exception if the data is not serializable and prints information
    about it. This is a thin wrapper around :func:`find_json_unserializable`.
    """
    unserializable = list(find_json_unserializable(data))
    if unserializable:
        raise Exception(msg + ub.urepr(unserializable))


def ensure_json_serializable(dict_, normalize_containers=False, verbose=0):
    """
    Attempt to convert common types (e.g. numpy) into something json complient

    Convert numpy and tuples into lists

    Args:
        dict_ (List | Dict):
            A data structure nearly compatabile with json. (todo: rename arg)

        normalize_containers (bool):
            if True, normalizes dict containers to be standard python
            structures. Defaults to False.

    Returns:
        Dict | List:
            normalized data structure that should be entirely json
            serializable.

    Note:
        This was ported from kwcoco.util

    Example:
        >>> from kwutil.util_json import *  # NOQA
        >>> assert ensure_json_serializable([]) == []
        >>> assert ensure_json_serializable({}) == {}
        >>> data = [pathlib.Path('.')]
        >>> assert ensure_json_serializable(data) == ['.']
        >>> assert ensure_json_serializable(data) != data

    Example:
        >>> # xdoctest: +REQUIRES(module:numpy)
        >>> from kwutil.util_json import *  # NOQA
        >>> data = ub.ddict(lambda: int)
        >>> data['foo'] = ub.ddict(lambda: int)
        >>> data['bar'] = np.array([1, 2, 3])
        >>> data['foo']['a'] = 1
        >>> data['foo']['b'] = (1, np.array([1, 2, 3]), {3: np.int32(3), 4: np.float16(1.0)})
        >>> dict_ = data
        >>> print(ub.urepr(data, nl=-1))
        >>> assert list(find_json_unserializable(data))
        >>> result = ensure_json_serializable(data, normalize_containers=True)
        >>> print(ub.urepr(result, nl=-1))
        >>> assert not list(find_json_unserializable(result))
        >>> assert type(result) is dict
    """
    dict_ = copy.deepcopy(dict_)

    def _norm_container(c):
        if isinstance(c, dict):
            # Cast to a normal dictionary
            if isinstance(c, OrderedDict):
                if type(c) is not OrderedDict:
                    c = OrderedDict(c)
            else:
                if type(c) is not dict:
                    c = dict(c)
        return c

    walker = ub.IndexableWalker(dict_)
    for prefix, value in walker:
        if isinstance(value, tuple):
            new_value = list(value)
            walker[prefix] = new_value
        elif np is not None and isinstance(value, np.ndarray):
            new_value = value.tolist()
            walker[prefix] = new_value
        elif np is not None and isinstance(value, (np.integer)):
            new_value = int(value)
            walker[prefix] = new_value
        elif np is not None and isinstance(value, (np.floating)):
            new_value = float(value)
            walker[prefix] = new_value
        elif np is not None and isinstance(value, (np.complexfloating)):
            new_value = complex(value)
            walker[prefix] = new_value
        elif isinstance(value, decimal.Decimal):
            new_value = float(value)
            walker[prefix] = new_value
        elif isinstance(value, fractions.Fraction):
            new_value = float(value)
            walker[prefix] = new_value
        elif isinstance(value, pathlib.Path):
            new_value = str(value)
            walker[prefix] = new_value
        elif hasattr(value, '__json__'):
            new_value = value.__json__()
            walker[prefix] = new_value
        elif normalize_containers:
            if isinstance(value, dict):
                new_value = _norm_container(value)
                walker[prefix] = new_value

    if normalize_containers:
        # normalize the outer layer
        dict_ = _norm_container(dict_)
    return dict_


def find_json_unserializable(data, quickcheck=False):
    """
    Recurse through json datastructure and find any component that
    causes a serialization error. Record the location of these errors
    in the datastructure as we recurse through the call tree.

    Args:
        data (object): data that should be json serializable
        quickcheck (bool): if True, check the entire datastructure assuming
            its ok before doing the python-based recursive logic.

    Returns:
        List[Dict]: list of "bad part" dictionaries containing items

            'value' - the value that caused the serialization error

            'loc' - which contains a list of key/indexes that can be used
            to lookup the location of the unserializable value.
            If the "loc" is a list, then it indicates a rare case where
            a key in a dictionary is causing the serialization error.

    Note:
        This was ported from kwcoco.util

    Example:
        >>> # xdoctest: +REQUIRES(module:numpy)
        >>> from kwutil.util_json import *  # NOQA
        >>> part = ub.ddict(lambda: int)
        >>> part['foo'] = ub.ddict(lambda: int)
        >>> part['bar'] = np.array([1, 2, 3])
        >>> part['foo']['a'] = 1
        >>> # Create a dictionary with two unserializable parts
        >>> data = [1, 2, {'nest1': [2, part]}, {frozenset({'badkey'}): 3, 2: 4}]
        >>> parts = list(find_json_unserializable(data))
        >>> print('parts = {}'.format(ub.urepr(parts, nl=1)))
        >>> # Check expected structure of bad parts
        >>> assert len(parts) == 2
        >>> part = parts[1]
        >>> assert list(part['loc']) == [2, 'nest1', 1, 'bar']
        >>> # We can use the "loc" to find the bad value
        >>> for part in parts:
        >>>     # "loc" is a list of directions containing which keys/indexes
        >>>     # to traverse at each descent into the data structure.
        >>>     directions = part['loc']
        >>>     curr = data
        >>>     special_flag = False
        >>>     for key in directions:
        >>>         if isinstance(key, list):
        >>>             # special case for bad keys
        >>>             special_flag = True
        >>>             break
        >>>         else:
        >>>             # normal case for bad values
        >>>             curr = curr[key]
        >>>     if special_flag:
        >>>         assert part['data'] in curr.keys()
        >>>         assert part['data'] is key[1]
        >>>     else:
        >>>         assert part['data'] is curr

    Example:
        >>> # xdoctest: +SKIP("TODO: circular ref detect algo is wrong, fix it")
        >>> from kwutil.util_json import *  # NOQA
        >>> import pytest
        >>> # Test circular reference
        >>> data = [[], {'a': []}]
        >>> data[1]['a'].append(data)
        >>> with pytest.raises(ValueError, match="Circular reference detected at.*1, 'a', 1*"):
        ...     parts = list(find_json_unserializable(data))
        >>> # Should be ok here
        >>> shared_data = {'shared': 1}
        >>> data = [[shared_data], shared_data]
        >>> parts = list(find_json_unserializable(data))
    """
    import json
    needs_check = True

    if quickcheck:
        try:
            # Might be a more efficient way to do this check. We duplicate a lot of
            # work by doing the check for unserializable data this way.
            json.dumps(data)
        except Exception:
            # if 'Circular reference detected' in str(ex):
            #     has_circular_reference = True
            # If there is unserializable data, find out where it is.
            # is_serializable = False
            pass
        else:
            # is_serializable = True
            needs_check = False

    # FIXME: the algo is wrong, fails when
    CHECK_FOR_CIRCULAR_REFERENCES = 0

    if needs_check:
        # mode = 'new'
        # if mode == 'new':
        scalar_types = (int, float, str, type(None))
        container_types = (tuple, list, dict)
        serializable_types = scalar_types + container_types
        walker = ub.IndexableWalker(data)

        if CHECK_FOR_CIRCULAR_REFERENCES:
            seen_ids = set()

        for prefix, value in walker:

            if CHECK_FOR_CIRCULAR_REFERENCES:
                # FIXME: We need to know if this container id is in this paths
                # ancestors. It is allowed to be elsewhere in the data
                # structure (i.e. the pointer graph must be a DAG)
                if isinstance(value, container_types):
                    container_id = id(value)
                    if container_id in seen_ids:
                        circ_loc = {'loc': prefix, 'data': value}
                        raise ValueError(f'Circular reference detected at {circ_loc}')
                    seen_ids.add(container_id)

            *root, key = prefix
            if not isinstance(key, scalar_types):
                # Special case where a dict key is the error value
                # Purposely make loc non-hashable so its not confused with
                # an address. All we can know in this case is that they key
                # is at this level, there is no concept of where.
                yield {'loc': root + [['.keys', key]], 'data': key}
            elif not isinstance(value, serializable_types):
                yield {'loc': prefix, 'data': value}
