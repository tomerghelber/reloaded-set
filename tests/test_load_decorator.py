import unittest
from unittest import mock

from reloaded_set import ReloadedSet, load


NOT_DEFAULT_FLAG_NAME = 'bla'
NOT_DEFAULT_FUNCTION_NAME = 'bla_flag'


class AReloadedSet(ReloadedSet):
    @load()
    def tested_function(self):
        pass

    @property
    def _values(self):
        return list()


class ReloadedSetDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.reloaded_set = AReloadedSet()
        self.reloaded_set._reload = mock.Mock()

    def test_load_decorator_working(self):
        self.reloaded_set.tested_function()
        self.reloaded_set._reload.assert_called_once_with()


class BReloadedSet(ReloadedSet):
    def __init__(self):
        super().__init__(flag_name=NOT_DEFAULT_FLAG_NAME, function_name=NOT_DEFAULT_FUNCTION_NAME)

    @load(flag_name=NOT_DEFAULT_FLAG_NAME, function_name=NOT_DEFAULT_FUNCTION_NAME)
    def tested_function(self):
        pass

    @property
    def _values(self):
        return list()

class ReloadedSetDecoratorOtherNamingTestCase(unittest.TestCase):
    def setUp(self):
        self.reloaded_set = BReloadedSet()
        setattr(self.reloaded_set, '_' + NOT_DEFAULT_FUNCTION_NAME, mock.Mock())

    def test_load_decorator_working(self):
        self.reloaded_set.tested_function()
        getattr(self.reloaded_set, '_' + NOT_DEFAULT_FUNCTION_NAME).assert_called_once_with()


def main():
    unittest.main()


if '__main__' == __name__:
    main()
