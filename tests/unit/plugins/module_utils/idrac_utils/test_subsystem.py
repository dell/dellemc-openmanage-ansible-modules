
from ansible_collections.dellemc.openmanage.plugins.\
    module_utils.idrac_utils.info.subsystem import IDRACSubsystemInfo
from ansible_collections.dellemc.openmanage.tests.unit.\
    plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

cpu_expected_result = {
    "Key": "CPU",
    "PrimaryStatus": "Healthy"
}
license_expected_result = {
    "Key": "License",
    "PrimaryStatus": "Healthy"
}
memory_expected_result = {
    "Key": "Memory",
    "PrimaryStatus": "Healthy"
}
power_supply_expected_result = {
    "Key": "PowerSupply",
    "PrimaryStatus": "Healthy"
}
sensor_voltage_expected_result = {
    "Key": "Sensors_Voltage",
    "PrimaryStatus": "Healthy"
}
sensor_battery_expected_result = {
    "Key": "Sensors_Battery",
    "PrimaryStatus": "Healthy"
}
sensor_fan_expected_result = {
    "Key": "Sensors_Fan",
    "PrimaryStatus": "Healthy"
}
sensor_intrusion_expected_result = {
    "Key": "Sensors_Intrusion",
    "PrimaryStatus": "Healthy"
}
sensor_temperature_expected_result = {
    "Key": "Sensors_Temperature",
    "PrimaryStatus": "Healthy"
}
system_expected_result = {
    "Key": "System",
    "PrimaryStatus": "Healthy"
}
vflash_expected_result = {
    "Key": "VFlash",
    "PrimaryStatus": "Unknown"
}
sensor_amperage_expected_result = {
    "Key": "Sensors_Amperage",
    "PrimaryStatus": "Healthy"
}
storage_expected_result = {
    "Key": "Storage",
    "PrimaryStatus": "Healthy"
}


class TestIDRACSubsystemInfo(TestUtils):
    def test_get_cpu_health_status(self, idrac_mock):
        cpu_mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = cpu_mock_response
        cpu_info = IDRACSubsystemInfo(idrac_mock)
        result = cpu_info.get_idrac_cpu_health_status()
        assert result == cpu_expected_result

    def test_get_cpu_health_status_empty(self, idrac_mock):
        cpu_mock_response = {
            "Members": []
        }
        idrac_mock.invoke_request.return_value.json_data = cpu_mock_response
        cpu_info = IDRACSubsystemInfo(idrac_mock)
        result = cpu_info.get_idrac_cpu_health_status()
        assert result == {
            "Key": "CPU",
            "PrimaryStatus": "Unknown"
        }

    def test_get_license_health_status(self, idrac_mock):
        license_mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = license_mock_response
        license_info = IDRACSubsystemInfo(idrac_mock)
        result = license_info.get_idrac_license_health_status()
        assert result == license_expected_result

    def test_get_memory_health_status(self, idrac_mock):
        memory_mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = memory_mock_response
        memory_info = IDRACSubsystemInfo(idrac_mock)
        result = memory_info.get_idrac_memory_health_status()
        assert result == memory_expected_result

    def test_get_power_supply_health_status(self, idrac_mock):
        power_supply_mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = power_supply_mock_response
        power_supply_info = IDRACSubsystemInfo(idrac_mock)
        result = power_supply_info.get_idrac_power_supply_health_status()
        assert result == power_supply_expected_result

    def test_get_sensor_voltage_health_status(self, idrac_mock):
        sensor_voltage_mock_response = {
            "Redundancy": [
                {
                    "Status": {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = sensor_voltage_mock_response
        sensor_voltage_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_voltage_info.get_idrac_sensor_voltage_health_status()
        assert result == sensor_voltage_expected_result

    def test_get_sensor_battery_health_status(self, idrac_mock):
        sensor_battery_mock_response = {
            "Members": [
                {
                    "ElementName": "System Board CMOS Battery",
                    "HealthState": "OK"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = sensor_battery_mock_response
        sensor_battery_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_battery_info.get_idrac_sensor_battery_health_status()
        assert result == sensor_battery_expected_result

    def test_get_sensor_battery_health_status_empty(self, idrac_mock):
        mock_response = {
            "Members": []
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        sensor_battery_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_battery_info.get_idrac_sensor_battery_health_status()
        expected_result = {
            "Key": "Sensors_Battery",
            "PrimaryStatus": "Unknown"
        }
        assert result == expected_result

    def test_get_sensor_fan_health_status(self, idrac_mock):
        sensor_fan_mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = sensor_fan_mock_response
        sensor_fan_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_fan_info.get_idrac_sensor_fan_health_status()
        assert result == sensor_fan_expected_result

    def test_get_sensor_intrusion_health_status(self, idrac_mock):
        mock_response = {
            "PhysicalSecurity": {
                "IntrusionSensor": "Normal"
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        sensor_intrusion_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_intrusion_info.get_idrac_sensor_intrusion_health_status()
        assert result == sensor_intrusion_expected_result

    def test_get_sensor_temperature_health_status(self, idrac_mock):
        mock_response = {
            "Members": [
                {
                    "Status":
                    {
                        "Health": "OK",
                        "State": "Enabled"
                    }
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        sensor_temperature_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_temperature_info.get_idrac_sensor_temperature_health_status()
        assert result == sensor_temperature_expected_result

    def test_get_system_health_status(self, idrac_mock):
        mock_response = {
            "Status": {
                "Health": "OK",
                "State": "Enabled"
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        system_info = IDRACSubsystemInfo(idrac_mock)
        result = system_info.get_idrac_system_health_status()
        assert result == system_expected_result

    def test_get_vflash_health_status(self, idrac_mock):
        vflash_info = IDRACSubsystemInfo(idrac_mock)
        result = vflash_info.get_idrac_vflash_health_status()
        assert result == vflash_expected_result

    def test_get_sensor_amperage_health_status(self, idrac_mock):
        mock_response = {
            "Status": {
                "Health": "OK",
                "State": "Enabled"
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        sensor_amperage_info = IDRACSubsystemInfo(idrac_mock)
        result = sensor_amperage_info.get_idrac_sensor_amperage_health_status()
        assert result == sensor_amperage_expected_result

    def test_get_subsystem_info(self, idrac_mock):
        subsystem_info = IDRACSubsystemInfo(idrac_mock)
        subsystem_info.get_idrac_system_health_status = MagicMock(
            return_value=system_expected_result)
        subsystem_info.get_idrac_memory_health_status = MagicMock(
            return_value=memory_expected_result)
        subsystem_info.get_idrac_cpu_health_status = MagicMock(
            return_value=cpu_expected_result)
        subsystem_info.get_idrac_sensor_fan_health_status = MagicMock(
            return_value=sensor_fan_expected_result)
        subsystem_info.get_idrac_power_supply_health_status = MagicMock(
            return_value=power_supply_expected_result)
        subsystem_info.get_idrac_storage_health_status = MagicMock(
            return_value=storage_expected_result)
        subsystem_info.get_idrac_license_health_status = MagicMock(
            return_value=license_expected_result)
        subsystem_info.get_idrac_sensor_voltage_health_status = MagicMock(
            return_value=sensor_voltage_expected_result)
        subsystem_info.get_idrac_sensor_temperature_health_status = MagicMock(
            return_value=sensor_temperature_expected_result)
        subsystem_info.get_idrac_sensor_battery_health_status = MagicMock(
            return_value=sensor_battery_expected_result)
        subsystem_info.get_idrac_vflash_health_status = MagicMock(
            return_value=vflash_expected_result)
        subsystem_info.get_idrac_sensor_intrusion_health_status = MagicMock(
            return_value=sensor_intrusion_expected_result)
        subsystem_info.get_idrac_sensor_amperage_health_status = MagicMock(
            return_value=sensor_amperage_expected_result)
        result = subsystem_info.get_subsystem_info()
        expected_result = [
            {
                "Key": "System",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Memory",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "CPU",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Sensors_Fan",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "PowerSupply",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Storage",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "License",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Sensors_Voltage",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Sensors_Temperature",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Sensors_Battery",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "VFlash",
                "PrimaryStatus": "Unknown"
            },
            {
                "Key": "Sensors_Intrusion",
                "PrimaryStatus": "Healthy"
            },
            {
                "Key": "Sensors_Amperage",
                "PrimaryStatus": "Healthy"
            }
        ]
        assert result == expected_result

    def test_get_idrac_storage_health_status(self, idrac_mock):
        mock_response = {
            "Members": [
                {
                    "@odata.id": "abcd"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        storage_info = IDRACSubsystemInfo(idrac_mock)
        storage_info.get_storage_health_status_data = MagicMock(
            return_value="OK"
        )
        result = storage_info.get_idrac_storage_health_status()
        expected_result = {
            "Key": "Storage",
            "PrimaryStatus": "Healthy"
        }
        assert result == expected_result

    def test_get_storage_health_status(self, idrac_mock):
        mock_response = {
            "Status": {
                "Health": "OK",
                "State": "Enabled"
            }
        }
        idrac_mock.invoke_request.return_value.json_data = mock_response
        storage_info = IDRACSubsystemInfo(idrac_mock)
        result = storage_info.get_storage_health_status_data(uri="abcd")
        assert result == "OK"
