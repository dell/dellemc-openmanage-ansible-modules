
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.powersupply import IDRACPowerSupplyInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils

powersupply_link =\
    ["/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/PowerSupplies/1"]
NA = "Not Available"


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
        result = idrac_memory_info.get_power_supply_details(powersupply_link[0])
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
        links_response = {
            "Members": [
                {
                    "@odata.id": powersupply_link[0]
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = links_response
        idrac_memory_info = IDRACPowerSupplyInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_links()
        expected_result = [
            powersupply_link[0]
        ]
        assert result == expected_result

    def test_get_power_supply_info_empty(self, idrac_mock):
        links_response = {
            "Members": [
                {
                    "@odata.id": powersupply_link[0]
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = links_response
        idrac_memory_info = IDRACPowerSupplyInfo(idrac_mock)
        result = idrac_memory_info.get_power_supply_details(links_response)
        expected_result = expected_result = {
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
            'InputVoltage': NA,
        }
        assert result == expected_result
