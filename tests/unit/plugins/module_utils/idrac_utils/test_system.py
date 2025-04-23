import pytest
from unittest.mock import MagicMock
from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.system import (
    IDRACSystemInfo,
    GET_IDRAC_MANAGER_URI,
    GET_IDRAC_BIOS_URI,
    GET_IDRAC_MANAGER_SYSTEM_ATTRIBUTES,
    GET_IDRAC_MANAGER_IDRAC_ATTRIBUTES,
    GET_IDRAC_SYSTEM_DETAILS_URI_10,
)

NA = "Not Available"


@pytest.fixture
def idrac_mock():
    mock_idrac = MagicMock()

    uri_response_map = {
        GET_IDRAC_MANAGER_URI: {
            "FirmwareVersion": "x.x.x.x",
            "Oem": {
                "Dell": {
                    "DelliDRACCard": {
                        "URLString": "xx.xx.xx.xx"
                    }
                }
            },
            "PowerState": "On"
        },
        GET_IDRAC_BIOS_URI: {
            "Attributes": {
                "SysMemSize": "128 GB",
                "SystemManufacturer": "Dell Inc."
            }
        },
        GET_IDRAC_MANAGER_SYSTEM_ATTRIBUTES: {
            "Attributes": {
                "ServerOS.1.OSName": "VMware ESXi",
                "ServerOS.1.OSVersion": "7.0.3"
            }
        },
        GET_IDRAC_MANAGER_IDRAC_ATTRIBUTES: {
            "Attributes": {
                "Lockdown.1.SystemLockdown": "Enabled"
            }
        },
        GET_IDRAC_SYSTEM_DETAILS_URI_10: {
            "AssetTag": "ABC123",
            "BiosVersion": "1.0.0",
            "DeviceType": "Rack Server",
            "HostName": "idrac-host",
            "SKU": "SKU123",
            "Status": {"HealthRollup": "OK"},
            "Name": "PowerEdge R740",
            "Oem": {
                "Dell": {
                    "DellSystem": {
                        "BIOSReleaseDate": "2023-01-01",
                        "BaseBoardChassisSlot": "Slot 1",
                        "BladeGeometry": "2U",
                        "BoardPartNumber": "PN1234",
                        "BoardSerialNumber": "BSN1234",
                        "CMCIP": "192",
                        "ChassisModel": "Model X",
                        "ChassisName": "Chassis A",
                        "ChassisServiceTag": "CHST123",
                        "ChassisSystemHeightUnit": "2U",
                        "CurrentRollupStatus": "OK",
                        "ExpressServiceCode": "1234567890",
                        "MachineName": "Machine-A",
                        "MaxCPUSockets": 2,
                        "MaxDIMMSlots": 16,
                        "MaxPCIeSlots": 8,
                        "MemoryOperationMode": "Optimized",
                        "SystemGeneration": "15G",
                        "NodeID": "Node123",
                        "PlatformGUID": "GUID-1234",
                        "PowerCap": "Enabled",
                        "PowerCapEnabledState": "Enabled",
                        "RACType": "iDRAC9",
                        "ServerAllocation": "Allocated",
                        "Name": "PowerEdge",
                        "SystemRevision": "Rev1",
                        "SystemID": "System123",
                        "UUID": "UUID-1234",
                        "smbiosGUID": "SMBIOS-GUID-1234"
                    }
                }
            }
        }
    }

    def invoke_request_side_effect(method, uri):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json_data = uri_response_map.get(uri, {})
        return mock_response

    mock_idrac.invoke_request.side_effect = invoke_request_side_effect
    return mock_idrac


class TestIDRACSystemInfo:

    def test_get_firmware_ver_idrac_url(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)
        version, idrac_url, power_state = idrac_system_info.get_firmware_ver_idrac_url()

        assert version == "x.x.x.x"
        assert idrac_url == "xx.xx.xx.xx"
        assert power_state == "On"

    def test_get_system_cpldversion_and_memsize_and_manufacturer(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)
        cpld_version, memsize, manufacturer = idrac_system_info.get_system_cpldversion_and_memsize_and_manufacturer()

        assert cpld_version == ""
        assert memsize == "128 GB"
        assert manufacturer == "Dell Inc."

    def test_get_system_os_name_and_os_version(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)
        os_name, os_version = idrac_system_info.get_system_os_name_and_os_version()

        assert os_name == "VMware ESXi"
        assert os_version == "7.0.3"

    def test_get_system_lockdownmode(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)
        system_lockdown_mode = idrac_system_info.get_system_lockdownmode()

        assert system_lockdown_mode == "Enabled"

    def test_system_mapped_data(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)

        response_data = idrac_mock.invoke_request("GET", GET_IDRAC_SYSTEM_DETAILS_URI_10).json_data
        result = idrac_system_info.system_mapped_data(response_data)

        expected_result = {
            "AssetTag": "ABC123",
            "BIOSReleaseDate": "2023-01-01",
            "BIOSVersionString": "1.0.0",
            "BaseBoardChassisSlot": "Slot 1",
            "BladeGeometry": "2U",
            "BoardPartNumber": "PN1234",
            "BoardSerialNumber": "BSN1234",
            "CMCIP": "192",
            "CPLDVersion": NA,
            "ChassisModel": "Model X",
            "ChassisName": "Chassis A",
            "ChassisServiceTag": "CHST123",
            "ChassisSystemHeight": "2U",
            "CurrentRollupStatus": "OK",
            "DeviceDescription": "PowerEdge R740",
            "DeviceType": "Rack Server",
            "ExpressServiceCode": "1234567890",
            "HostName": "idrac-host",
            "Key": "SKU123",
            "LifecycleControllerVersion": "x.x.x.x",
            "MachineName": "Machine-A",
            "Manufacturer": "Dell Inc.",
            "MaxCPUSockets": 2,
            "MaxDIMMSlots": 16,
            "MaxPCIeSlots": 8,
            "MemoryOperationMode": "Optimized",
            "Model": "15G",
            "NodeID": "Node123",
            "OSName": "VMware ESXi",
            "OSVersion": "7.0.3",
            "PlatformGUID": "GUID-1234",
            "PowerCap": "Enabled",
            "PowerCapEnabledState": "Enabled",
            "PowerState": "On",
            "PrimaryStatus": "Healthy",
            "RACType": "iDRAC9",
            "ServerAllocation": "Allocated",
            "ServiceTag": "Node123",
            "SysMemTotalSize": "128 GB",
            "SysName": "PowerEdge",
            "SystemGeneration": "15G",
            "SystemID": "System123",
            "SystemLockDown": "Enabled",
            "SystemRevision": "Rev1",
            "UUID": "UUID-1234",
            "_Type": "Server",
            "iDRACURL": "xx.xx.xx.xx",
            "smbiosGUID": "SMBIOS-GUID-1234"
        }

        assert result == expected_result

    def test_system_mapped_data_missing_dell_block(self, idrac_mock):
        original_data = idrac_mock.invoke_request("GET", GET_IDRAC_SYSTEM_DETAILS_URI_10).json_data
        modified_data = original_data.copy()
        modified_data["Oem"]["Dell"].pop("DellSystem", None)

        idrac_system_info = IDRACSystemInfo(idrac_mock)
        result = idrac_system_info.system_mapped_data(modified_data)

        assert result["BIOSReleaseDate"] == NA
        assert result["BaseBoardChassisSlot"] == NA
        assert result["CMCIP"] == NA

    def test_system_mapped_data_with_empty_response(self, idrac_mock):
        idrac_system_info = IDRACSystemInfo(idrac_mock)
        result = idrac_system_info.system_mapped_data({})

        assert isinstance(result, dict)
        assert result["CPLDVersion"] == NA
        assert result["SystemLockDown"] == "Enabled"
        assert result["LifecycleControllerVersion"] == "x.x.x.x"
        assert result["SysMemTotalSize"] == "128 GB"

    def test_system_mapped_data_missing_oem_block(self, idrac_mock):
        original_data = idrac_mock.invoke_request("GET", GET_IDRAC_SYSTEM_DETAILS_URI_10).json_data
        modified_data = original_data.copy()
        modified_data.pop("Oem", None)

        idrac_system_info = IDRACSystemInfo(idrac_mock)
        result = idrac_system_info.system_mapped_data(modified_data)

        assert result["BIOSReleaseDate"] == NA
        assert result["RACType"] == NA

    def test_invoke_request_with_non_200_status(self):
        mock_idrac = MagicMock()

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json_data = {}

        mock_idrac.invoke_request.return_value = mock_response
        idrac_system_info = IDRACSystemInfo(mock_idrac)

        version, idrac_url, power_state = idrac_system_info.get_firmware_ver_idrac_url()
        assert version == ""
        assert idrac_url == ""
        assert power_state == ""

    def test_get_system_memsize_and_manufacturer_missing_attributes(self):
        mock_idrac = MagicMock()

        mock_idrac.invoke_request.return_value.status_code = 200
        mock_idrac.invoke_request.return_value.json_data = {}

        idrac_system_info = IDRACSystemInfo(mock_idrac)
        cpld_version, memsize, manufacturer = idrac_system_info.get_system_cpldversion_and_memsize_and_manufacturer()

        assert cpld_version == ""
        assert memsize == ""
        assert manufacturer == ""

    def test_get_system_info_success(self):
        mock_idrac = MagicMock()

        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_json = {
            "Oem": {
                "Dell": {
                    "DellSystem": {
                        "RACType": "iDRAC",
                        "SystemGeneration": "14G",
                        "Name": "TestSystem",
                        "NodeID": "ABC123",
                        "UUID": "uuid-123",
                    }
                }
            },
            "SKU": "SKU1234",
            "Name": "System",
            "Status": {"HealthRollup": "OK"},
            "BiosVersion": "2.4.8"
        }

        mock_response.json_data = mock_json
        mock_response.json.return_value = mock_json
        mock_idrac.invoke_request.return_value = mock_response

        idrac_system_info = IDRACSystemInfo(mock_idrac)

        idrac_system_info.get_firmware_ver_idrac_url = MagicMock(return_value=("x.x.x", "https://idrac-url", "On"))
        idrac_system_info.get_system_cpldversion_and_memsize_and_manufacturer = MagicMock(return_value=("1.x.x", "64 GB", "Dell Inc."))
        idrac_system_info.get_system_os_name_and_os_version = MagicMock(return_value=("Ubuntu", "x.x"))
        idrac_system_info.get_system_lockdownmode = MagicMock(return_value="Enabled")

        output = idrac_system_info.get_system_info()

        assert isinstance(output, list)
        assert output[0]["DeviceDescription"] == "System"
        assert output[0]["RACType"] == "iDRAC"
        assert output[0]["LifecycleControllerVersion"] == "x.x.x"
        assert output[0]["SysMemTotalSize"] == "64 GB"
        assert output[0]["Manufacturer"] == "Dell Inc."
        assert output[0]["OSName"] == "Ubuntu"
        assert output[0]["OSVersion"] == "x.x"
        assert output[0]["SystemLockDown"] == "Enabled"
        assert output[0]["PowerState"] == "On"
        assert output[0]["iDRACURL"] == "https://idrac-url"

    def test_get_system_info_non_200(self):
        mock_idrac = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_idrac.invoke_request.return_value = mock_response

        idrac_system_info = IDRACSystemInfo(mock_idrac)
        output = idrac_system_info.get_system_info()
        assert output == []
