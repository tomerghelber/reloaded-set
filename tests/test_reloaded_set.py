import unittest
from unittest import mock

from reloaded_set import ReloadedSet, DEFAULT_FUNCTION_NAME, DEFAULT_FLAG_NAME


NOT_DEFAULT_FLAG_NAME = 'bla'
NOT_DEFAULT_FUNCTION_NAME = 'bla_flag'


class ReloadedSetTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.reloaded_set = ReloadedSet()
        cls.reloaded_set._reload = mock.MagicMock()

    def test_inner_reload_is_called(self):
        getattr(self.reloaded_set, DEFAULT_FUNCTION_NAME)()
        self.reloaded_set._reload.assert_called_once_with()

    def test_init_default_flag_to_false(self):
        self.assertFalse(getattr(self.reloaded_set, DEFAULT_FLAG_NAME))

    def test_default_flag_turned_true(self):
        getattr(self.reloaded_set, DEFAULT_FUNCTION_NAME)()
        self.assertTrue(getattr(self.reloaded_set, DEFAULT_FLAG_NAME))


class ReloadedSetOtherNamingTestCase(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.reloaded_set = ReloadedSet(flag_name=NOT_DEFAULT_FLAG_NAME, function_name=NOT_DEFAULT_FUNCTION_NAME)
        setattr(cls.reloaded_set, '_' + NOT_DEFAULT_FUNCTION_NAME, mock.MagicMock())

    def test_check_flag_exists(self):
        getattr(self.reloaded_set, NOT_DEFAULT_FLAG_NAME)

    def test_check_function_exists(self):
        getattr(self.reloaded_set, NOT_DEFAULT_FLAG_NAME)

    def test_check_flag_false(self):
        self.assertFalse(getattr(self.reloaded_set, NOT_DEFAULT_FLAG_NAME))

    def test_check_function_called(self):
        getattr(self.reloaded_set, NOT_DEFAULT_FUNCTION_NAME)()
        getattr(self.reloaded_set, '_' + NOT_DEFAULT_FUNCTION_NAME).assert_called_once_with()

    def test_check_flag_changed_true(self):
        getattr(self.reloaded_set, NOT_DEFAULT_FUNCTION_NAME)()
        self.assertTrue(getattr(self.reloaded_set, NOT_DEFAULT_FLAG_NAME))


def main():
    unittest.main()


if '__main__' == __name__:
    main()
