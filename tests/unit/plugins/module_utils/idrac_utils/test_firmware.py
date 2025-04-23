from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.firmware import IDRACFirmwareInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from ansible.module_utils.six.moves.urllib.error import HTTPError


class TestIDRACFirmwareInfo(TestUtils):
    def test_is_omsdk_required(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_firmware_info = IDRACFirmwareInfo(idrac_mock)
        result = idrac_firmware_info.is_omsdk_required()
        assert result is False

    def test_is_omsdk_required_other_statuscode(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 204
        idrac_firmware_info = IDRACFirmwareInfo(idrac_mock)
        result = idrac_firmware_info.is_omsdk_required()
        assert not result

    def test_is_omsdk_required_error_handling(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.side_effect = HTTPError(
            'https://testhost.com/',
            400,
            'Bad Request Error',
            {},
            None)
        idrac_firmware_info = IDRACFirmwareInfo(idrac_mock)
        result = idrac_firmware_info.is_omsdk_required()
        assert result is True
