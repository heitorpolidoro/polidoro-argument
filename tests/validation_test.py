import pytest

from polidoro_argument import Argument


class NoNameClass:
    def __call__(self, *args, **kwargs):
        pass


def test_no_name():
    with pytest.raises(RuntimeError) as exit_info:
        Argument(NoNameClass())
    assert str(exit_info.value) == 'The "method" must have the attribute "__name__"!'
