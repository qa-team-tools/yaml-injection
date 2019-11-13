import os

import pytest
import yaml

from yaml_injection import InjectionLoader


@pytest.fixture
def in_current_dir():
    cwd_backup = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    yield
    os.chdir(cwd_backup)


@pytest.mark.usefixtures('in_current_dir')
def test_local_file():
    with open('main.yml') as in_:
        data = yaml.load(in_, InjectionLoader)

    with open('expected.yml') as in_:
        expected_data = yaml.safe_load(in_)

    assert expected_data == data
