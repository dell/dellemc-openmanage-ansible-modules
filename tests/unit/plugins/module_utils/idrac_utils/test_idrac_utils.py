import pytest
from unittest.mock import MagicMock


class TestUtils:
    @pytest.fixture
    def idrac_mock(self):
        idrac_mock = MagicMock()
        idrac_mock.invoke_request.return_value.status_code = 200
        return idrac_mock
