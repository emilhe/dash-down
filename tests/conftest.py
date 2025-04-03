import os

import pytest


@pytest.fixture(autouse=True)
def change_test_dir(request, monkeypatch):
    monkeypatch.chdir(os.path.join(request.fspath.dirname, ".."))
