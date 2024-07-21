import pytest
from ruff_pyspark_filter_linter.linter import check_file
import tempfile
import os
import logging

from ruff_pyspark_filter_linter.log_utils import get_console_handler

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(get_console_handler())
LOGGER.setLevel(logging.DEBUG)


def test_account_id_filter():
    code_with_filter = """
df = spark.createDataFrame(data)
df = df.filter(df.account_id == '123')
"""
    code_without_filter = """
df = spark.createDataFrame(data)
"""
    config = ["account_id"]

    # Test with filter
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as tmpfile_with_filter:
        tmpfile_with_filter.write(code_with_filter)
        tmpfile_with_filter.flush()
        LOGGER.info(f"tmpfile_with_filter.name {tmpfile_with_filter.name}\n")
        result = check_file(tmpfile_with_filter.name, config)
        LOGGER.info(f"result {result}\n")
        os.remove(tmpfile_with_filter.name)
        assert not result

    # Test without filter
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as tmpfile_without_filter:
        tmpfile_without_filter.write(code_without_filter)
        tmpfile_without_filter.flush()
        LOGGER.info(f"tmpfile_without_filter.name {tmpfile_without_filter.name}\n")
        result = check_file(tmpfile_without_filter.name, config)
        LOGGER.info(f"result {result}\n")
        os.remove(tmpfile_without_filter.name)
        assert result
