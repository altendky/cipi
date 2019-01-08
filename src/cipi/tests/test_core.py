import pytest

import cipi.core


@pytest.mark.parametrize(
    'version, expected',
    (
        ('2.7.15', 'python2.7'),
        ('3.7.2', 'python3.7'),
        ('pypy2.7-6.0.0', 'pypy'),
        ('pypy3.5-6.0.0', 'pypy3'),
    ),
)
def test_python_name_from_version(version, expected):
    assert cipi.core.python_name_from_version(version) == expected
