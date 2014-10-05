import unittest
import mock

from reloaded_set import ReloadedSet, DEFAULT_FUNCTION_NAME, DEFAULT_FLAG_NAME


NOT_DEFAULT_FLAG_NAME = 'bla'
NOT_DEFAULT_FUNCTION_NAME = 'bla_flag'


class InheritanceReloadedSet(ReloadedSet):
    def _reload(self):
        pass

    @property
    def _values(self):
        return list()


class InheritanceReloadedSetB(ReloadedSet):
    def _bla(self):
        pass

    @property
    def _values(self):
        return list()


class ReloadedSetTestCase(unittest.TestCase):
    def setUp(self):
        self.reloaded_set = InheritanceReloadedSet()
        self.reloaded_set._reload = mock.Mock()

    def test_inner_reload_is_called(self):
        getattr(self.reloaded_set, DEFAULT_FUNCTION_NAME)()
        self.reloaded_set._reload.assert_called_once_with()

    def test_init_default_flag_to_false(self):
        self.assertFalse(getattr(self.reloaded_set, DEFAULT_FLAG_NAME))

    def test_default_flag_turned_true(self):
        getattr(self.reloaded_set, DEFAULT_FUNCTION_NAME)()
        self.assertTrue(getattr(self.reloaded_set, DEFAULT_FLAG_NAME))


class ReloadedSetOtherNamingTestCase(unittest.TestCase):
    def setUp(self):
        self.reloaded_set = InheritanceReloadedSetB(flag_name=NOT_DEFAULT_FLAG_NAME, function_name=NOT_DEFAULT_FUNCTION_NAME)
        setattr(self.reloaded_set, '_' + NOT_DEFAULT_FUNCTION_NAME, mock.Mock())

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

VALUES = [1, 2, 3, 4, 5, ]


class CReloadedSet(ReloadedSet):
    def _reload(self):
        pass

    @property
    def _values(self):
        return VALUES


class ReloadedSetFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.reloaded_set = CReloadedSet()

    def test_in(self):
        return VALUES[0] in self.reloaded_set

    def test_not_in(self):
        return sum(VALUES) not in self.reloaded_set

    def test___iter__(self):
        self.assertListEqual(VALUES, list(self.reloaded_set))

    def test_len(self):
        self.assertEqual(len(VALUES), len(self.reloaded_set))

    def test_issubset(self):
        self.assertTrue(self.reloaded_set.issubset(VALUES))

    def test_not_issubset(self):
        self.assertFalse(self.reloaded_set.issubset(VALUES[:-1]))

    def test_issuperset(self):
        self.assertTrue(self.reloaded_set.issuperset(VALUES))

    def test_not_issuperset(self):
        self.assertFalse(self.reloaded_set.issuperset(VALUES + [sum(VALUES)]))

    def test_union(self):
        unioned1 = [sum(VALUES)]
        unioned2 = [sum(VALUES) * 2]
        wanted = sorted(VALUES + unioned1 + unioned2)
        result = sorted(self.reloaded_set.union(unioned1, unioned2))
        self.assertListEqual(wanted, result)

    def test___or__(self):
        unioned1 = [sum(VALUES)]
        unioned2 = [sum(VALUES) * 2]
        wanted = sorted(VALUES + unioned1 + unioned2)
        result = sorted(self.reloaded_set | set(unioned1) | set(unioned2))
        self.assertListEqual(wanted, result)

    def test_intersection(self):
        wanted = VALUES[0]
        result = sorted(self.reloaded_set.intersection([wanted]))
        self.assertListEqual([wanted], result)

    def test___and__(self):
        wanted = [VALUES[0]]
        result = sorted(self.reloaded_set & set([VALUES[0]]))
        self.assertListEqual(wanted, result)

    def test_difference(self):
        other = [VALUES[0]]
        wanted = VALUES[1:]
        result = sorted(self.reloaded_set.difference(other))
        self.assertListEqual(wanted, result)

    def test___sub__(self):
        other = set([VALUES[0]])
        wanted = VALUES[1:]
        result = sorted(self.reloaded_set - other)
        self.assertListEqual(wanted, result)

    def test_symmetric_difference(self):
        wanted = [VALUES[0], sum(VALUES)]
        other = VALUES[1:] + [sum(VALUES)]
        result = sorted(self.reloaded_set.symmetric_difference(other))
        self.assertListEqual(wanted, result)

    def test___xor__(self):
        wanted = [VALUES[0], sum(VALUES)]
        other = VALUES[1:] + [sum(VALUES)]
        result = sorted(self.reloaded_set ^other)
        self.assertListEqual(wanted, result)


def main():
    unittest.main()


if '__main__' == __name__:
    main()
