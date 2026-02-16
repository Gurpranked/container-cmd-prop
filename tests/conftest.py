### conftest.py is implicitly imported into all pytest test files. This file is
### a collection of globally available pytest fixtures.

import pytest

@pytest.fixture
def dockerfile_alpine_latest(tmp_path):
    """Fixture that provides a hardcoded Dockerfile for alpine:latest.
    The CMD used simply prints out the standard /etc/os-release file.
    """
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM alpine:latest\nCMD [\"cat\",\"/etc/os-release\"]\n")
    return dockerfile

@pytest.fixture
def containerfile_alpine_latest(dockerfile):
    """Fixture that provides a hardcoded Containerfile for alpine:latest.
    This fixture is equivalent to the `dockerfile_alpine_latest` fixture, except
    that the Path it gives back has basename Containerfile.
    """
    containerfile = dockerfile.replace(dockerfile.parent / "Containerfile")
    return containerfile
