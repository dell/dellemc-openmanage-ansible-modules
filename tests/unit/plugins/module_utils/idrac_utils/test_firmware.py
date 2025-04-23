from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.firmware import IDRACFirmwareInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACFirmwareInfo(TestUtils):
    def test_get_firmware_version(self, idrac_mock):
        fimrware_version = "xx.xx"
        response = {
            "Members":
                {
                    "Version": fimrware_version
                }
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_license_info = IDRACFirmwareInfo(idrac_mock)
        result = idrac_license_info.get_firmware_version()
        assert result == fimrware_version

    def test_is_omsdk_required(self, idrac_mock):
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_license_info = IDRACFirmwareInfo(idrac_mock)
        result = idrac_license_info.is_omsdk_required()
        assert result is False

    # def test_get_license_info_empty(self, idrac_mock):
    #     response = {}
    #     idrac_mock.invoke_request.return_value.status_code = 400
    #     idrac_mock.invoke_request.return_value.json_data = response
    #     idrac_license_info = IDRACFirmwareInfo(idrac_mock)
    #     result = idrac_license_info.get_license_info()
    #     assert result == []
