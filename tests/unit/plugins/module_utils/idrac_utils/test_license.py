from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.license import IDRACLicenseInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACLicenseInfo(TestUtils):
    def test_get_license_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "Id": "1234",
                    "LicenseDescription": ["License Description"],
                    "LicenseInstallDate": "2023-02-20",
                    "LicenseSoldDate": "2023-02-20",
                    "LicenseType": "License Type",
                    "LicensePrimaryStatus": "OK"
                },
                {
                    "Id": "12",
                    "LicenseDescription": ["test license"],
                    "LicenseInstallDate": "2024-02-21",
                    "LicenseSoldDate": "2024-02-21",
                    "LicenseType": "Perpetual",
                    "LicensePrimaryStatus": "Warning"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_license_info = IDRACLicenseInfo(idrac_mock)
        result = idrac_license_info.get_license_info()
        expected_result = [
            {
                "InstanceID": "1234",
                "Key": "1234",
                "LicenseDescription": "License Description",
                "LicenseInstallDate": "2023-02-20",
                "LicenseSoldDate": "2023-02-20",
                "LicenseType": "License Type",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "12",
                "InstanceID": "12",
                "LicenseDescription": "test license",
                "LicenseInstallDate": "2024-02-21",
                "LicenseSoldDate": "2024-02-21",
                "LicenseType": "Perpetual",
                "PrimaryStatus": "Warning"
            }
        ]
        assert result == expected_result

    def test_get_license_info_empty(self, idrac_mock):
        response = {}
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_license_info = IDRACLicenseInfo(idrac_mock)
        result = idrac_license_info.get_license_info()
        assert result == []
