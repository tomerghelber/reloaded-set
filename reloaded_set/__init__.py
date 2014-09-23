import collections

__version__ = '0.1'

DEFAULT_FLAG_NAME = '_is_loaded'
DEFAULT_FUNCTION_NAME = 'reload'


class ReloadedSet(collections.Set):
    """
    A reloaded set - like frozenset but can fetch new data in the function reload.
    To inheritance you need to make:

    :ivar _values: The value the set will look when doing staff.
    :type _values: any things that can be iterable like list, tuple, set or frozen set.
    :ivar _is_loaded: The flag that will check that the object is first load or not.
    :type _is_loaded: bool
    """
    def __init__(self, flag_name: str=DEFAULT_FLAG_NAME, function_name: str=DEFAULT_FUNCTION_NAME):
        setattr(self, flag_name, False)

        inner_function_name = '_' + function_name

        def inner_function():
            raise NotImplemented()

        def function():
            getattr(self, inner_function_name)()
            setattr(self, flag_name, True)

        setattr(self, inner_function_name, inner_function)
        setattr(self, function_name, function)

    @property
    def _values(self):
        raise NotImplemented()

    def __contains__(self, item):
        return item in list(self._values)

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def issubset(self, other) -> frozenset:
        return self <= frozenset(other)

    def issuperset(self, other) -> frozenset:
        return self >= frozenset(other)

    def union(self, *others) -> frozenset:
        res = set(self)
        for other in others:
            res |= frozenset(other)
        return frozenset(res)

    def __or__(self, other) -> frozenset:
        return self.union(other)

    def intersection(self, *others) -> frozenset:
        other_lists = map(list, list(others) + [list(self)])
        def in_all(x):
            return all(map(lambda other_list: x in other_list, other_lists))

        import itertools
        other_union_lists = itertools.chain(other_lists)
        items_in_all = filter(in_all, other_union_lists)

        res = list()

        for item in items_in_all:
            if item not in res:
                res.append(item)

        return frozenset(res)

    def __and__(self, other) -> frozenset:
        return self.intersection(other)

    def difference(self, *others) -> frozenset:
        import itertools
        other_lists = map(list, others)
        other_union_lists = itertools.chain(other_lists)
        return frozenset(filter(lambda x: x not in other_union_lists, self))

    def __sub__(self, other) -> frozenset:
        return self.difference(other)

    def symmetric_difference(self, other) -> frozenset:
        self_list = list(self)
        other_not_in_self = frozenset(filter(lambda x: x not in self_list, other))

        other = list(other)
        self_not_in_other = frozenset(filter(lambda x: x not in other, self))

        return other_not_in_self | self_not_in_other

    def __xor__(self, other) -> frozenset:
        return self.symmetric_difference(other)


def load(flag_name: str=DEFAULT_FLAG_NAME, function_name: str=DEFAULT_FUNCTION_NAME):
    """
    This decorator checking of the class was loaded and load it if needed.
    For lazy.
    """
    def _decorator_wrapper(function):
        """
        The real decorator
        :param function: The function to wrap.
        :return: The wrapped function.
        """
        def _load_wrapper(self, *args):
            flag = getattr(self, flag_name)
            if not flag:
                reload_function = getattr(self, function_name)
                reload_function()
            return function(self, *args)

        return _load_wrapper

    return _decorator_wrapper