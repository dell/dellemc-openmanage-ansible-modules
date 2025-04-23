
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.powersupply import IDRACPowerSupplyInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

LINK = "/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/PowerSupplies/1"
POWERSUPPLY_LINK = {
    "Members": [
        {
            "@odata.id": LINK
        }
    ]
}
NA = "Not Available"
POWERSUPPLYOUTPUT = {
    "DetailedState": NA,
    "DeviceDescription": NA,
    "FQDD": NA,
    "Key": NA,
    "Name": NA,
    "FirmwareVersion": NA,
    "Model": NA,
    "Manufacturer": NA,
    "PartNumber": NA,
    "SerialNumber": NA,
    'PowerSupplySensorState': NA,
    "PrimaryStatus": NA,
    "RAIDState": NA,
    "Range1MaxInputPower": NA,
    "RedMinNumberNeeded": NA,
    "TotalOutputPower": NA,
    "Type": NA,
    "powerSupplyStateCapabilitiesUnique": NA,
    "Redundancy": NA,
    "RedTypeOfSet": NA,
    'InputVoltage': NA
}


class TestIDRACPowerSupplyInfo(TestUtils):
    def test_get_power_supply_info(self, idrac_mock):
        response = {
            "Id": "1",
            "Name": "Power Supply 1",
            "FirmwareVersion": "1.0.0",
            "Model": "Power Supply Model",
            "Manufacturer": "Dell",
            "PartNumber": "Power Supply Part Number",
            "SerialNumber": "Power Supply Serial Number",
            "PowerCapacityWatts": 1000,
            "Status": {
                "State": "Enabled",
                "Health": "OK"
            },
            "PowerSupplyType": "ACorDC",
            "Oem": {
                "Dell": {
                    "DellPowerSupplyView": {
                        "DetailedState": "Detailed State",
                        "DeviceDescription": "Device Description",
                        "RedTypeOfSet": ["N+1"],
                        "Range1MaxInputPowerWatts": 1000,
                        "RedMinNumberNeeded": 1,
                        "TotalOutputPower": 1000,
                        "powerSupplyStateCapabilitiesUnique": "Power Supply State Capabilities Unique",
                        "RedundancyStatus": "NotRedundant"
                    }
                }
            }
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_memory_info = IDRACPowerSupplyInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_details(LINK)
        expected_result = {
            "DetailedState": "Detailed State",
            "DeviceDescription": "Device Description",
            "FQDD": "1",
            "Key": "1",
            "Name": "Power Supply 1",
            "FirmwareVersion": "1.0.0",
            "Model": "Power Supply Model",
            "Manufacturer": "Dell",
            "PartNumber": "Power Supply Part Number",
            "SerialNumber": "Power Supply Serial Number",
            'PowerSupplySensorState': NA,
            "PrimaryStatus": "Healthy",
            "RAIDState": NA,
            "Range1MaxInputPower": "1000 W",
            "RedMinNumberNeeded": 1,
            "TotalOutputPower": "1000 W",
            "Type": "ACorDC",
            "powerSupplyStateCapabilitiesUnique": "Power Supply State Capabilities Unique",
            "Redundancy": "NotRedundant",
            "RedTypeOfSet": '2',
            'InputVoltage': NA,

        }
        assert result == expected_result

    def test_get_power_supply_links(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = POWERSUPPLY_LINK
        idrac_memory_info = IDRACPowerSupplyInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_links()
        expected_result = [LINK]
        assert result == expected_result

    def test_get_power_supply_details_empty(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = POWERSUPPLY_LINK
        idrac_memory_info = IDRACPowerSupplyInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_details(POWERSUPPLY_LINK)
        assert result == POWERSUPPLYOUTPUT

    def test_get_power_supply_info_empty(self, idrac_mock):
        idrac_mock.invoke_request.return_value.json_data = LINK
        idrac_powersupply_info = IDRACPowerSupplyInfo(idrac_mock)
        idrac_powersupply_info.get_power_supply_links = MagicMock(
            return_value=[LINK])
        idrac_powersupply_info.get_power_supply_details = MagicMock(
            return_value={})
        result = idrac_powersupply_info.get_power_supply_info()
        assert result == [{}]
