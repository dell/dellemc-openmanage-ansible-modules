from ansible_collections.dellemc.openmanage.plugins.module_utils.idrac_utils.info.controller_battery import IDRACControllerBatteryInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils


class TestIDRACControllerBatteryInfo(TestUtils):
    def test_get_controller_battery_info(self, idrac_mock):
        response = {
            "Members": [
                {
                    "@odata.context": "/redfish/v1/$metadata#DellControllerBattery.DellControllerBattery",
                    "@odata.id": "/redfish/v1/Chassis/System.Embedded.1/PowerSubsystem/Oem/Dell/DellControllerBattery/Energypack.Integrated.1:RAID.Slot.7-1",
                    "@odata.type": "#DellControllerBattery.v1_0_0.DellControllerBattery",
                    "Description": "An instance of DellController will have RAID Controller specific data.",
                    "FQDD": "Energypack.Integrated.1:RAID.Slot.7-1",
                    "Id": "Energypack.Integrated.1:RAID.Slot.7-1",
                    "Name": "Energy pack on RAID Controller in Slot 7",
                    "PrimaryStatus": "OK",
                    "RAIDState": "Ready"
                }
            ],
        }
        idrac_mock.invoke_request.return_value.json_data = response
        idrac_controller_battery_info = IDRACControllerBatteryInfo(idrac_mock)
        result = idrac_controller_battery_info.get_controller_battery_info()
        expected_result = [
            {
                "DeviceDescription": "Energy pack on RAID Controller in Slot 7",
                "FQDD": "Energypack.Integrated.1:RAID.Slot.7-1",
                "InstanceID": "Energypack.Integrated.1:RAID.Slot.7-1",
                "Key": "Energypack.Integrated.1:RAID.Slot.7-1",
                "PrimaryStatus": "Healthy",
                "RAIDState": "Ready"
            }
        ]
        assert result == expected_result
