from unittest import TestCase


class SafeDict(dict):
    def __missing__(self, key):
        """Make sure to keep the original placeholder if the key is missing."""
        return f"{{{key}}}"


class BaseTest(TestCase): ...
