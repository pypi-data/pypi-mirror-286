import pytest

from pureml import storage


def test_get_storage_provider():
    # S3
    # provider = storage.get_storage_provider('s3')
    pass


def test_get_storage_provider_invalid():
    with pytest.raises(ValueError):
        storage.get_storage_provider("invalid", base_path=".")
