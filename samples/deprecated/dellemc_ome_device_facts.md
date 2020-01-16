Get Device List:

"ansible_facts": { {
"@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
"@odata.count": 3,
"value": [
	{
		"@odata.id": "/api/DeviceService/Devices(11111)",
		"@odata.type": "#DeviceService.Device",
		"Actions": null,
		"AssetTag": null,
		"BlinkStatus": {
			"@odata.id": "/api/DeviceService/Devices(11111)/BlinkStatus"
		},
		"ChassisServiceTag": "ST0004B",
		"ConnectionState": true,
		"DeployRequired": {
			"@odata.id": "/api/DeviceService/Devices(11111)/DeployRequired"
		},
		"DeviceBladeSlots@odata.navigationLink": "/api/DeviceService/Devices(11111)/DeviceBladeSlots",
		"DeviceCapabilities": [
			1,
			2,
			3,
			5,
			7,
			9
		],
		"DeviceManagement": [],
		"DeviceName": "IOM-A1",
		"DeviceServiceTag": null,
		"DeviceSubscription": null,
		"GraphicInfo": {
			"@odata.id": "/api/DeviceService/Devices(11111)/GraphicInfo"
		},
		"HardwareLogs@odata.navigationLink": "/api/DeviceService/Devices(11111)/HardwareLogs",
		"Id": 11111,
		"Identifier": "0W875HX30CNFCP007BI0035",
		"InventoryDetails@odata.navigationLink": "/api/DeviceService/Devices(11111)/InventoryDetails",
		"InventoryTypes": {
			"@odata.id": "/api/DeviceService/Devices(11111)/InventoryTypes"
		},
		"LastInventoryTime": null,
		"LastStatusTime": "2019-01-22 07:30:03.671",
		"LogSeverities": {
			"@odata.id": "/api/DeviceService/Devices(11111)/LogSeverities"
		},
		"ManagedState": 3000,
		"Model": "Dell EMC PowerEdge MX 10GbE PTM",
		"Power": {
			"@odata.id": "/api/DeviceService/Devices(11111)/Power"
		},
		"PowerState": 17,
		"PowerUsageByDevice@odata.navigationLink": "/api/DeviceService/Devices(11111)/PowerUsageByDevice",
		"RecentActivity@odata.navigationLink": "/api/DeviceService/Devices(11111)/RecentActivity",
		"Settings@odata.navigationLink": "/api/DeviceService/Devices(11111)/Settings",
		"SlotConfiguration": {
			"ChassisId": "22222",
			"ChassisName": "MX- ST0003I",
			"ChassisServiceTag": "ST0004B",
			"SledBlockPowerOn": "null",
			"SlotName": "IOM-A1",
			"SlotNumber": "1",
			"SlotType": "4000"
		},
		"Status": 1000,
		"SubSystemHealth@odata.navigationLink": "/api/DeviceService/Devices(11111)/SubSystemHealth",
		"SystemId": 2031,
		"SystemUpTime": {
			"@odata.id": "/api/DeviceService/Devices(11111)/SystemUpTime"
		},
		"Temperature": {
			"@odata.id": "/api/DeviceService/Devices(11111)/Temperature"
		},
		"Type": 4000
	},
	{
		"@odata.id": "/api/DeviceService/Devices(22222)",
		"@odata.type": "#DeviceService.Device",
		"Actions": null,
		"AssetTag": null,
		"BlinkStatus": {
			"@odata.id": "/api/DeviceService/Devices(22222)/BlinkStatus"
		},
		"ChassisServiceTag": null,
		"ConnectionState": true,
		"DeployRequired": {
			"@odata.id": "/api/DeviceService/Devices(22222)/DeployRequired"
		},
		"DeviceBladeSlots@odata.navigationLink": "/api/DeviceService/Devices(22222)/DeviceBladeSlots",
		"DeviceCapabilities": [
			18,
			8,
			201
		],
		"DeviceManagement": [
			{
				"DnsName": "XXXX.host.com",
				"InstrumentationName": "MX- XXXXX",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "https://192.168.0.1:443",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:08.584"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "192.168.0.1"
			}
		],
		"DeviceName": "MX- ST0003I",
		"DeviceServiceTag": "ST0004B",
		"DeviceSubscription": null,
		"GraphicInfo": {
			"@odata.id": "/api/DeviceService/Devices(22222)/GraphicInfo"
		},
		"HardwareLogs@odata.navigationLink": "/api/DeviceService/Devices(22222)/HardwareLogs",
		"Id": 22222,
		"Identifier": "ST0004B",
		"InventoryDetails@odata.navigationLink": "/api/DeviceService/Devices(22222)/InventoryDetails",
		"InventoryTypes": {
			"@odata.id": "/api/DeviceService/Devices(22222)/InventoryTypes"
		},
		"LastInventoryTime": "2019-01-22 07:30:08.583",
		"LastStatusTime": "2019-01-22 07:30:02.426",
		"LogSeverities": {
			"@odata.id": "/api/DeviceService/Devices(22222)/LogSeverities"
		},
		"ManagedState": 3000,
		"Model": "PowerEdge MX7000",
		"Power": {
			"@odata.id": "/api/DeviceService/Devices(22222)/Power"
		},
		"PowerState": 17,
		"PowerUsageByDevice@odata.navigationLink": "/api/DeviceService/Devices(22222)/PowerUsageByDevice",
		"RecentActivity@odata.navigationLink": "/api/DeviceService/Devices(22222)/RecentActivity",
		"Settings@odata.navigationLink": "/api/DeviceService/Devices(22222)/Settings",
		"SlotConfiguration": {},
		"Status": 4000,
		"SubSystemHealth@odata.navigationLink": "/api/DeviceService/Devices(22222)/SubSystemHealth",
		"SystemId": 2031,
		"SystemUpTime": {
			"@odata.id": "/api/DeviceService/Devices(22222)/SystemUpTime"
		},
		"Temperature": {
			"@odata.id": "/api/DeviceService/Devices(22222)/Temperature"
		},
		"Type": 2000
	},
	{
		"@odata.id": "/api/DeviceService/Devices(33333)",
		"@odata.type": "#DeviceService.Device",
		"Actions": null,
		"AssetTag": null,
		"BlinkStatus": {
			"@odata.id": "/api/DeviceService/Devices(33333)/BlinkStatus"
		},
		"ChassisServiceTag": "ST0004B",
		"ConnectionState": true,
		"DeployRequired": {
			"@odata.id": "/api/DeviceService/Devices(33333)/DeployRequired"
		},
		"DeviceBladeSlots@odata.navigationLink": "/api/DeviceService/Devices(33333)/DeviceBladeSlots",
		"DeviceCapabilities": [
			1,
			2,
			3,
			4,
			7,
			8,
			9,
			41,
			10,
			11,
			12,
			13,
			14,
			15,
			17,
			18,
			30,
			31
		],
		"DeviceManagement": [
			{
				"DnsName": "iDRAC-XXXXX",
				"InstrumentationName": "hostname.xxx.xxx.dell.com",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"AgentName": "iDRAC",
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "https://192.168.0.1:443",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:29.280",
						"Version": "3.20.20.20"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "100.96.45.142"
			},
			{
				"DnsName": "iDRAC-XXXXX",
				"InstrumentationName": "hostname.xxx.xxx.dell.com",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"AgentName": "iDRAC",
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "unknown",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:29.280",
						"Version": "3.20.20.20"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "[::]"
			}
		],
		"DeviceName": "Sled-3",
		"DeviceServiceTag": "KLBR840",
		"DeviceSubscription": null,
		"GraphicInfo": {
			"@odata.id": "/api/DeviceService/Devices(33333)/GraphicInfo"
		},
		"HardwareLogs@odata.navigationLink": "/api/DeviceService/Devices(33333)/HardwareLogs",
		"Id": 33333,
		"Identifier": "KLBR840",
		"InventoryDetails@odata.navigationLink": "/api/DeviceService/Devices(33333)/InventoryDetails",
		"InventoryTypes": {
			"@odata.id": "/api/DeviceService/Devices(33333)/InventoryTypes"
		},
		"LastInventoryTime": "2019-01-22 07:30:29.279",
		"LastStatusTime": "2019-01-22 07:30:03.597",
		"LogSeverities": {
			"@odata.id": "/api/DeviceService/Devices(33333)/LogSeverities"
		},
		"ManagedState": 3000,
		"Model": "PowerEdge MX840c",
		"Power": {
			"@odata.id": "/api/DeviceService/Devices(33333)/Power"
		},
		"PowerState": 17,
		"PowerUsageByDevice@odata.navigationLink": "/api/DeviceService/Devices(33333)/PowerUsageByDevice",
		"RecentActivity@odata.navigationLink": "/api/DeviceService/Devices(33333)/RecentActivity",
		"Settings@odata.navigationLink": "/api/DeviceService/Devices(33333)/Settings",
		"SlotConfiguration": {
			"ChassisId": "22222",
			"ChassisName": "MX- ST0003I",
			"ChassisServiceTag": "ST0004B",
			"SledBlockPowerOn": "None blocking",
			"SlotName": "Sled-3",
			"SlotNumber": "3",
			"SlotType": "2000"
		},
		"Status": 1000,
		"SubSystemHealth@odata.navigationLink": "/api/DeviceService/Devices(33333)/SubSystemHealth",
		"SystemId": 1894,
		"SystemUpTime": {
			"@odata.id": "/api/DeviceService/Devices(33333)/SystemUpTime"
		},
		"Temperature": {
			"@odata.id": "/api/DeviceService/Devices(33333)/Temperature"
		},
		"Type": 1000
	}
]
} }


Get devices using filtering:

"ansible_facts": { {
"@odata.context": "/api/$metadata#Collection(DeviceService.Device)",
"@odata.count": 2,
"value": [
	{
		"@odata.id": "/api/DeviceService/Devices(22222)",
		"@odata.type": "#DeviceService.Device",
		"Actions": null,
		"AssetTag": null,
		"BlinkStatus": {
			"@odata.id": "/api/DeviceService/Devices(22222)/BlinkStatus"
		},
		"ChassisServiceTag": null,
		"ConnectionState": true,
		"DeployRequired": {
			"@odata.id": "/api/DeviceService/Devices(22222)/DeployRequired"
		},
		"DeviceBladeSlots@odata.navigationLink": "/api/DeviceService/Devices(22222)/DeviceBladeSlots",
		"DeviceCapabilities": [
			18,
			8,
			201
		],
		"DeviceManagement": [
			{
				"DnsName": "XXXX.host.com",
				"InstrumentationName": "MX- XXXXX",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "https://192.168.0.1:443",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:08.584"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "192.168.0.1"
			}
		],
		"DeviceName": "MX- ST0003I",
		"DeviceServiceTag": "ST0004B",
		"DeviceSubscription": null,
		"GraphicInfo": {
			"@odata.id": "/api/DeviceService/Devices(22222)/GraphicInfo"
		},
		"HardwareLogs@odata.navigationLink": "/api/DeviceService/Devices(22222)/HardwareLogs",
		"Id": 22222,
		"Identifier": "ST0004B",
		"InventoryDetails@odata.navigationLink": "/api/DeviceService/Devices(22222)/InventoryDetails",
		"InventoryTypes": {
			"@odata.id": "/api/DeviceService/Devices(22222)/InventoryTypes"
		},
		"LastInventoryTime": "2019-01-22 07:30:08.583",
		"LastStatusTime": "2019-01-22 07:30:02.426",
		"LogSeverities": {
			"@odata.id": "/api/DeviceService/Devices(22222)/LogSeverities"
		},
		"ManagedState": 3000,
		"Model": "PowerEdge MX7000",
		"Power": {
			"@odata.id": "/api/DeviceService/Devices(22222)/Power"
		},
		"PowerState": 17,
		"PowerUsageByDevice@odata.navigationLink": "/api/DeviceService/Devices(22222)/PowerUsageByDevice",
		"RecentActivity@odata.navigationLink": "/api/DeviceService/Devices(22222)/RecentActivity",
		"Settings@odata.navigationLink": "/api/DeviceService/Devices(22222)/Settings",
		"SlotConfiguration": {},
		"Status": 4000,
		"SubSystemHealth@odata.navigationLink": "/api/DeviceService/Devices(22222)/SubSystemHealth",
		"SystemId": 2031,
		"SystemUpTime": {
			"@odata.id": "/api/DeviceService/Devices(22222)/SystemUpTime"
		},
		"Temperature": {
			"@odata.id": "/api/DeviceService/Devices(22222)/Temperature"
		},
		"Type": 2000
	},
	{
		"@odata.id": "/api/DeviceService/Devices(33333)",
		"@odata.type": "#DeviceService.Device",
		"Actions": null,
		"AssetTag": null,
		"BlinkStatus": {
			"@odata.id": "/api/DeviceService/Devices(33333)/BlinkStatus"
		},
		"ChassisServiceTag": "ST0004B",
		"ConnectionState": true,
		"DeployRequired": {
			"@odata.id": "/api/DeviceService/Devices(33333)/DeployRequired"
		},
		"DeviceBladeSlots@odata.navigationLink": "/api/DeviceService/Devices(33333)/DeviceBladeSlots",
		"DeviceCapabilities": [
			1,
			2,
			3,
			4,
			7,
			8,
			9,
			41,
			10,
			11,
			12,
			13,
			14,
			15,
			17,
			18,
			30,
			31
		],
		"DeviceManagement": [
			{
				"DnsName": "iDRAC-XXXXX",
				"InstrumentationName": "hostname.xxx.xxx.dell.com",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"AgentName": "iDRAC",
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "https://192.168.0.1:443",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:29.280",
						"Version": "3.20.20.20"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "100.96.45.142"
			},
			{
				"DnsName": "iDRAC-XXXXX",
				"InstrumentationName": "hostname.xxx.xxx.dell.com",
				"MacAddress": "XX:XX:XX:XX:XX:XX",
				"ManagementId": XXXXX,
				"ManagementProfile": [
					{
						"AgentName": "iDRAC",
						"HasCreds": 0,
						"ManagementId": XXXXX,
						"ManagementProfileId": XXXXX,
						"ManagementURL": "unknown",
						"Status": 1000,
						"StatusDateTime": "2019-01-22 07:30:29.280",
						"Version": "3.20.20.20"
					}
				],
				"ManagementType": 2,
				"NetworkAddress": "[::]"
			}
		],
		"DeviceName": "Sled-3",
		"DeviceServiceTag": "KLBR840",
		"DeviceSubscription": null,
		"GraphicInfo": {
			"@odata.id": "/api/DeviceService/Devices(33333)/GraphicInfo"
		},
		"HardwareLogs@odata.navigationLink": "/api/DeviceService/Devices(33333)/HardwareLogs",
		"Id": 33333,
		"Identifier": "KLBR840",
		"InventoryDetails@odata.navigationLink": "/api/DeviceService/Devices(33333)/InventoryDetails",
		"InventoryTypes": {
			"@odata.id": "/api/DeviceService/Devices(33333)/InventoryTypes"
		},
		"LastInventoryTime": "2019-01-22 07:30:29.279",
		"LastStatusTime": "2019-01-22 07:30:03.597",
		"LogSeverities": {
			"@odata.id": "/api/DeviceService/Devices(33333)/LogSeverities"
		},
		"ManagedState": 3000,
		"Model": "PowerEdge MX840c",
		"Power": {
			"@odata.id": "/api/DeviceService/Devices(33333)/Power"
		},
		"PowerState": 17,
		"PowerUsageByDevice@odata.navigationLink": "/api/DeviceService/Devices(33333)/PowerUsageByDevice",
		"RecentActivity@odata.navigationLink": "/api/DeviceService/Devices(33333)/RecentActivity",
		"Settings@odata.navigationLink": "/api/DeviceService/Devices(33333)/Settings",
		"SlotConfiguration": {
			"ChassisId": "22222",
			"ChassisName": "MX- ST0003I",
			"ChassisServiceTag": "ST0004B",
			"SledBlockPowerOn": "None blocking",
			"SlotName": "Sled-3",
			"SlotNumber": "3",
			"SlotType": "2000"
		},
		"Status": 1000,
		"SubSystemHealth@odata.navigationLink": "/api/DeviceService/Devices(33333)/SubSystemHealth",
		"SystemId": 1894,
		"SystemUpTime": {
			"@odata.id": "/api/DeviceService/Devices(33333)/SystemUpTime"
		},
		"Temperature": {
			"@odata.id": "/api/DeviceService/Devices(33333)/Temperature"
		},
		"Type": 1000
	}
]
} }



Get Inventory Details of specified devices:


"ansible_facts": { {
    "device_id": {
		"22222": {
			"@odata.context": "/api/$metadata#Collection(DeviceService.InventoryDetail)",
			"@odata.count": 14,
			"value": [
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisPowerSupplies')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"CapacityWatts": 0,
							"DeviceId": 22222,
							"EnableState": "Absent",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "Amps",
							"InputVoltage": 0,
							"MemberId": "PSU.Slot.1",
							"Name": "PSU.Slot.1",
							"PartNumber": "",
							"PowerStatus": "18",
							"PowerSupplyType": "AC",
							"StateStr": "Absent"
						},
						{
							"CapacityWatts": 3000,
							"DeviceId": 22222,
							"EnableState": "Present",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "Amps",
							"InputVoltage": 0,
							"MemberId": "PSU.Slot.2",
							"Name": "PSU.Slot.2",
							"PartNumber": "01W1TNX31",
							"PowerStatus": "18",
							"PowerSupplyType": "AC",
							"StateStr": "Present"
						},
						{
							"CapacityWatts": 0,
							"DeviceId": 22222,
							"EnableState": "Absent",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "Amps",
							"InputVoltage": 0,
							"MemberId": "PSU.Slot.3",
							"Name": "PSU.Slot.3",
							"PartNumber": "",
							"PowerStatus": "18",
							"PowerSupplyType": "AC",
							"StateStr": "Absent"
						},
						{
							"CapacityWatts": 0,
							"DeviceId": 22222,
							"EnableState": "Absent",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "Amps",
							"InputVoltage": 0,
							"MemberId": "PSU.Slot.4",
							"Name": "PSU.Slot.4",
							"PartNumber": "",
							"PowerStatus": "18",
							"PowerSupplyType": "AC",
							"StateStr": "Absent"
						},
						{
							"CapacityWatts": 3000,
							"DeviceId": 22222,
							"EnableState": "Present",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "0.61Amps",
							"InputVoltage": 229,
							"MemberId": "PSU.Slot.5",
							"Name": "PSU.Slot.5",
							"PartNumber": "01W1TNX31",
							"PowerStatus": "17",
							"PowerSupplyType": "AC",
							"StateStr": "Present"
						},
						{
							"CapacityWatts": 0,
							"DeviceId": 22222,
							"EnableState": "Absent",
							"HealthState": 1000,
							"Id": 0,
							"InputCurrent": "Amps",
							"InputVoltage": 0,
							"MemberId": "PSU.Slot.6",
							"Name": "PSU.Slot.6",
							"PartNumber": "",
							"PowerStatus": "18",
							"PowerSupplyType": "AC",
							"StateStr": "Absent"
						}
					],
					"InventoryType": "chassisPowerSupplies"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisSlotsList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25012,
							"IsPrimarySlot": "True",
							"Name": "Sled-1",
							"Number": "1",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25013,
							"IsPrimarySlot": "True",
							"Name": "Sled-2",
							"Number": "2",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 1000,
							"DnsName": "XXXX.host.com",
							"HealthStatus": 1000,
							"Id": 25014,
							"IsPrimarySlot": "True",
							"Model": "PowerEdge MX840c",
							"Name": "Sled-3",
							"Number": "3",
							"Occupied": "True",
							"PowerState": 17,
							"ServiceTag": "KLBR840",
							"SledBlockPowerOn": "None blocking",
							"SlotDeviceId": 33333,
							"SlotDeviceName": "Sled-3",
							"SlotIdentifier": "KLBR840",
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 1
						},
						{
							"DeviceId": 0,
							"DeviceType": 1000,
							"DnsName": "XXXX.host.com",
							"HealthStatus": 1000,
							"Id": 25015,
							"IsPrimarySlot": "False",
							"Model": "PowerEdge MX840c",
							"Name": "Sled-4",
							"Number": "4",
							"Occupied": "True",
							"PowerState": 17,
							"ServiceTag": "KLBR840",
							"SledBlockPowerOn": "None blocking",
							"SlotDeviceId": 33333,
							"SlotDeviceName": "Sled-4",
							"SlotIdentifier": "KLBR840",
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 1
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25017,
							"IsPrimarySlot": "True",
							"Name": "Sled-5",
							"Number": "5",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25019,
							"IsPrimarySlot": "True",
							"Name": "Sled-6",
							"Number": "6",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25020,
							"IsPrimarySlot": "True",
							"Name": "Sled-7",
							"Number": "7",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25021,
							"IsPrimarySlot": "True",
							"Name": "Sled-8",
							"Number": "8",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 2000,
							"VlanCapable": true,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 4000,
							"DnsName": "XXXX.host.com",
							"HealthStatus": 1000,
							"Id": 25022,
							"IsPrimarySlot": "True",
							"Model": "Dell EMC PowerEdge MX 10GbE PTM",
							"Name": "IOM-A1",
							"Number": "1",
							"Occupied": "True",
							"PowerState": 17,
							"ServiceTag": "",
							"SlotDeviceId": 11111,
							"SlotDeviceName": "IOM-A1",
							"SlotIdentifier": "0W875HX30CNFCP007BI0035",
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25023,
							"IsPrimarySlot": "True",
							"Name": "IOM-A2",
							"Number": "2",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25025,
							"IsPrimarySlot": "True",
							"Name": "IOM-B1",
							"Number": "3",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25026,
							"IsPrimarySlot": "True",
							"Name": "IOM-B2",
							"Number": "4",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25027,
							"IsPrimarySlot": "True",
							"Name": "IOM-C1",
							"Number": "5",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25028,
							"IsPrimarySlot": "True",
							"Name": "IOM-C2",
							"Number": "6",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"Type": 4000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25044,
							"IsPrimarySlot": "True",
							"Name": "",
							"Number": "1",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"SlotIdentifier": "unknown",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25045,
							"IsPrimarySlot": "True",
							"Name": "2",
							"Number": "2",
							"Occupied": "True",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"SlotIdentifier": "PSU.Slot.2",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25046,
							"IsPrimarySlot": "True",
							"Name": "",
							"Number": "3",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"SlotIdentifier": "unknown",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25047,
							"IsPrimarySlot": "True",
							"Name": "",
							"Number": "4",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"SlotIdentifier": "unknown",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25048,
							"IsPrimarySlot": "True",
							"Name": "5",
							"Number": "5",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "PSU.Slot.5",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 2000,
							"Id": 25049,
							"IsPrimarySlot": "True",
							"Name": "",
							"Number": "6",
							"Occupied": "False",
							"PowerState": 18,
							"SlotDeviceId": 0,
							"SlotIdentifier": "unknown",
							"Type": 6000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25050,
							"IsPrimarySlot": "True",
							"Name": "1",
							"Number": "1",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.1",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25051,
							"IsPrimarySlot": "True",
							"Name": "2",
							"Number": "2",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.2",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25052,
							"IsPrimarySlot": "True",
							"Name": "3",
							"Number": "3",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.3",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25053,
							"IsPrimarySlot": "True",
							"Name": "4",
							"Number": "4",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.4",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25054,
							"IsPrimarySlot": "True",
							"Name": "5",
							"Number": "5",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.5",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25055,
							"IsPrimarySlot": "True",
							"Name": "6",
							"Number": "6",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.6",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25056,
							"IsPrimarySlot": "True",
							"Name": "7",
							"Number": "7",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.7",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25057,
							"IsPrimarySlot": "True",
							"Name": "8",
							"Number": "8",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.8",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						},
						{
							"DeviceId": 0,
							"DeviceType": 0,
							"HealthStatus": 1000,
							"Id": 25058,
							"IsPrimarySlot": "True",
							"Name": "9",
							"Number": "9",
							"Occupied": "True",
							"PowerState": 17,
							"SlotDeviceId": 0,
							"SlotIdentifier": "Fan.Slot.9",
							"Type": 3000,
							"VlanCapable": false,
							"VlanId": 0
						}
					],
					"InventoryType": "chassisSlotsList"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisControllerList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"FirmwareVersion": "1.00.01",
							"Health": 1000,
							"Id": 0,
							"Name": "MM1",
							"SlotNumber": "1",
							"State": "Active"
						}
					],
					"InventoryType": "chassisControllerList"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisPciDeviceList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "chassisPciDeviceList"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisFansList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.1",
							"Name": "Front Fan 1",
							"Pwm": "15",
							"PwmUnits": "Percent",
							"Speed": 3001,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.2",
							"Name": "Front Fan 2",
							"Pwm": "15",
							"PwmUnits": "Percent",
							"Speed": 2989,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.3",
							"Name": "Front Fan 3",
							"Pwm": "15",
							"PwmUnits": "Percent",
							"Speed": 2903,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.4",
							"Name": "Front Fan 4",
							"Pwm": "15",
							"PwmUnits": "Percent",
							"Speed": 2956,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.5",
							"Name": "Rear Fan 1",
							"Pwm": "16",
							"PwmUnits": "Percent",
							"Speed": 2664,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.6",
							"Name": "Rear Fan 2",
							"Pwm": "16",
							"PwmUnits": "Percent",
							"Speed": 2675,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.7",
							"Name": "Rear Fan 3",
							"Pwm": "27",
							"PwmUnits": "Percent",
							"Speed": 4168,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.8",
							"Name": "Rear Fan 4",
							"Pwm": "27",
							"PwmUnits": "Percent",
							"Speed": 4170,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						},
						{
							"DeviceId": 22222,
							"FirmwareVersion": "01.00.00",
							"HardwareVersion": "1",
							"Id": 0,
							"MemberId": "Fan.Slot.9",
							"Name": "Rear Fan 5",
							"Pwm": "27",
							"PwmUnits": "Percent",
							"Speed": 4159,
							"SpeedUnits": "RPM",
							"State": "17",
							"Status": 1000
						}
					],
					"InventoryType": "chassisFansList"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisTemperatureList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 0,
							"LowerThresholdCritical": "-7",
							"LowerThresholdNoncritical": "3",
							"MemberId": "System.Chassis.1",
							"ReadingCelsius": "24",
							"SensorName": "Chassis Inlet Temperature",
							"Status": "1000",
							"UpperThresholdCritical": "47",
							"UpperThresholdNoncritical": "43"
						}
					],
					"InventoryType": "chassisTemperatureList"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceLicense')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "deviceLicense"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceCapabilities')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"CapabilityType": {
								"CapabilityId": 18,
								"Description": "Device capable of sending alerts.",
								"Name": "DEVICE_ALERT"
							},
							"Id": 319056
						},
						{
							"CapabilityType": {
								"CapabilityId": 201,
								"Description": "Ngm Chassis Capability bit",
								"Name": "NGM_CHASSIS"
							},
							"Id": 319057
						},
						{
							"CapabilityType": {
								"CapabilityId": 8,
								"Description": "Remote Firmware update capability. ",
								"Name": "FW_UPDATE"
							},
							"Id": 319058
						}
					],
					"InventoryType": "deviceCapabilities"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceFru')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 258502,
							"Manufacturer": "",
							"Name": "PSU.Slot.2",
							"PartNumber": "01W1TNX31",
							"SerialNumber": "PHARP007CQ004B"
						},
						{
							"Id": 258503,
							"Manufacturer": "",
							"Name": "PSU.Slot.5",
							"PartNumber": "01W1TNX31",
							"SerialNumber": "PHARP00812001H"
						},
						{
							"Id": 258499,
							"Manufacturer": "",
							"Name": "Front Fan 3",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR01FH"
						},
						{
							"Id": 258504,
							"Manufacturer": "",
							"Name": "Rear Fan 3",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR028M"
						},
						{
							"Id": 258509,
							"Manufacturer": "",
							"Name": "Front Fan 1",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR0271"
						},
						{
							"Id": 258500,
							"Manufacturer": "",
							"Name": "Rear Fan 4",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR02BH"
						},
						{
							"Id": 258508,
							"Manufacturer": "Dell Inc.",
							"Name": "MX- ST0003I",
							"PartNumber": "0XT50JX30",
							"SerialNumber": "CNFCP007B2009V"
						},
						{
							"Id": 258510,
							"Manufacturer": "",
							"Name": "Rear Fan 2",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR01YJ"
						},
						{
							"Id": 258498,
							"Manufacturer": "",
							"Name": "Front Fan 4",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR014H"
						},
						{
							"Id": 258507,
							"Manufacturer": "",
							"Name": "Rear Fan 5",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR020U"
						},
						{
							"Id": 258506,
							"Manufacturer": "",
							"Name": "Front Fan 2",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR01DT"
						},
						{
							"Id": 258505,
							"Manufacturer": "",
							"Name": "Rear Fan 1",
							"PartNumber": "0FHH0KX30",
							"SerialNumber": "CNFCP007AR02AB"
						},
						{
							"Id": 258501,
							"Manufacturer": "Dell Inc.",
							"Name": "MX- ST0003I",
							"PartNumber": "0VMNRCX05",
							"SerialNumber": "CNFCP007B300CW"
						}
					],
					"InventoryType": "deviceFru"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceLocation')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "deviceLocation"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceManagement')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Device": 0,
							"DnsName": "XXXX.host.com",
							"EndPointAgents": [
								{
									"HasCreds": 2,
									"ManagementProfileId": XXXXX,
									"ManagementURL": "https://192.168.0.1:443",
									"ProfileId": "MSM_BASE",
									"Status": 1000,
									"StatusDateTime": 1548142208584
								}
							],
							"InstrumentationName": "MX- XXXXX",
							"IpAddress": "192.168.0.1",
							"MacAddress": "XX:XX:XX:XX:XX:XX",
							"ManagementId": XXXXX,
							"ManagementType": {
								"Description": "Public Management Interface",
								"ManagementType": 2,
								"Name": "PUBLIC"
							}
						}
					],
					"InventoryType": "deviceManagement"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('deviceSoftware')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"ComponentId": "",
							"DeviceDescription": "unknown",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.6",
							"SoftwareType": "FRMW",
							"Status": "Available",
							"Version": "0.0.0"
						},
						{
							"ComponentId": "104850",
							"DeviceDescription": "PSU.Slot.2",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.2",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "00.31.63"
						},
						{
							"ComponentId": "106452",
							"DeviceDescription": "MM1",
							"InstallationDate": "2018-11-27T08:30:06Z",
							"InstanceId": "MM1",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "1.00.01"
						},
						{
							"ComponentId": "",
							"DeviceDescription": "unknown",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.3",
							"SoftwareType": "FRMW",
							"Status": "Available",
							"Version": "0.0.0"
						},
						{
							"ComponentId": "",
							"DeviceDescription": "unknown",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.4",
							"SoftwareType": "FRMW",
							"Status": "Available",
							"Version": "0.0.0"
						},
						{
							"ComponentId": "104850",
							"DeviceDescription": "PSU.Slot.5",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.5",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "00.31.63"
						},
						{
							"ComponentId": "",
							"DeviceDescription": "unknown",
							"InstallationDate": "",
							"InstanceId": "PSU.Slot.1",
							"SoftwareType": "FRMW",
							"Status": "Available",
							"Version": "0.0.0"
						}
					],
					"InventoryType": "deviceSoftware"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('subsystemRollupStatus')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "subsystemRollupStatus"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(22222)/InventoryDetails('chassisStackMemberList')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"ChassisId": 22222,
							"ChassisModel": "",
							"ChassisName": "",
							"LinkSpeed": "mbps10",
							"LinkState": "Up",
							"NeighborChassisId": "GBE.1",
							"NeighborChassisMAC": "",
							"NeighborChassisType": "Not EC",
							"NeighborMgmtIPv4": "",
							"NeighborMgmtIPv6": "",
							"NeighborPortName": "",
							"ServiceTag": "",
							"SystemID": ""
						},
						{
							"ChassisId": 22222,
							"ChassisModel": "",
							"ChassisName": "",
							"LinkSpeed": "mbps10",
							"LinkState": "Down",
							"NeighborChassisId": "GBE.2",
							"NeighborChassisMAC": "",
							"NeighborChassisType": "",
							"NeighborMgmtIPv4": "",
							"NeighborMgmtIPv6": "",
							"NeighborPortName": "",
							"ServiceTag": "",
							"SystemID": ""
						},
						{
							"ChassisId": 22222,
							"ChassisModel": "",
							"ChassisName": "",
							"LinkSpeed": "mbps10",
							"LinkState": "Down",
							"NeighborChassisId": "GBE.3",
							"NeighborChassisMAC": "",
							"NeighborChassisType": "",
							"NeighborMgmtIPv4": "",
							"NeighborMgmtIPv6": "",
							"NeighborPortName": "",
							"ServiceTag": "",
							"SystemID": ""
						},
						{
							"ChassisId": 22222,
							"ChassisModel": "",
							"ChassisName": "",
							"LinkSpeed": "mbps10",
							"LinkState": "Down",
							"NeighborChassisId": "GBE.4",
							"NeighborChassisMAC": "",
							"NeighborChassisType": "",
							"NeighborMgmtIPv4": "",
							"NeighborMgmtIPv6": "",
							"NeighborPortName": "",
							"ServiceTag": "",
							"SystemID": ""
						}
					],
					"InventoryType": "chassisStackMemberList"
				}
			]
		},
		"33333": {
			"@odata.context": "/api/$metadata#Collection(DeviceService.InventoryDetail)",
			"@odata.count": 19,
			"value": [
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverDeviceCards')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"DatabusWidth": "8x or x8",
							"Description": "Ethernet 25G 2P XXV710 Mezz",
							"Id": 150329,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Other",
							"SlotNumber": "NIC.Mezzanine.1A-1-1",
							"SlotType": "PCI Express Gen 3 x16"
						},
						{
							"DatabusWidth": "8x or x8",
							"Description": "Ethernet Controller XXV710 for 25GbE backplane",
							"Id": 150330,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Other",
							"SlotNumber": "NIC.Mezzanine.1A-2-1",
							"SlotType": "PCI Express Gen 3 x16"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg SMBus",
							"Id": 150331,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "SMBus.Embedded.3-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg SATA Controller [AHCI mode]",
							"Id": 150332,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "AHCI.Embedded.2-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg PCI Express Root Port #5",
							"Id": 150333,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "P2PBridge.Embedded.2-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg LPC Controller",
							"Id": 150334,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "ISABridge.Embedded.1-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Integrated Matrox G200eW3 Graphics Controller",
							"Id": 150335,
							"Manufacturer": "Matrox Electronics Systems Ltd.",
							"SlotLength": "Unknown",
							"SlotNumber": "Video.Embedded.1-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Sky Lake-E DMI3 Registers",
							"Id": 150336,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "HostBridge.Embedded.1-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg SSATA Controller [AHCI mode]",
							"Id": 150337,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "AHCI.Embedded.1-1",
							"SlotType": "Unknown"
						},
						{
							"DatabusWidth": "Unknown",
							"Description": "Lewisburg PCI Express Root Port #1",
							"Id": 150338,
							"Manufacturer": "Intel Corporation",
							"SlotLength": "Unknown",
							"SlotNumber": "P2PBridge.Embedded.1-1",
							"SlotType": "Unknown"
						}
					],
					"InventoryType": "serverDeviceCards"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverProcessors')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"BrandName": "Intel",
							"CurrentSpeed": 2400,
							"Family": "Intel(R) Xeon(TM)",
							"Id": 29519,
							"InstanceId": "CPU.Socket.1",
							"MaxSpeed": 4000,
							"ModelName": "Intel(R) Xeon(R) Gold 5115 CPU @ 2.40GHz",
							"NumberOfCores": 10,
							"NumberOfEnabledCores": 10,
							"SlotNumber": "CPU.Socket.1",
							"Status": 1000,
							"Voltage": "1.8"
						},
						{
							"BrandName": "Intel",
							"CurrentSpeed": 2400,
							"Family": "Intel(R) Xeon(TM)",
							"Id": 29520,
							"InstanceId": "CPU.Socket.2",
							"MaxSpeed": 4000,
							"ModelName": "Intel(R) Xeon(R) Gold 5115 CPU @ 2.40GHz",
							"NumberOfCores": 10,
							"NumberOfEnabledCores": 10,
							"SlotNumber": "CPU.Socket.2",
							"Status": 1000,
							"Voltage": "1.8"
						}
					],
					"InventoryType": "serverProcessors"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverNetworkInterfaces')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"NicId": "NIC.Mezzanine.1A",
							"Ports": [
								{
									"InitiatorGateway": "",
									"InitiatorIpAddress": "",
									"InitiatorName": "",
									"InitiatorPrimaryDns": "",
									"InitiatorSecondaryDns": "",
									"InitiatorSubnetMask": "",
									"LinkSpeed": 10000,
									"LinkStatus": "",
									"Partitions": [
										{
											"CurrentMacAddress": "XX:XX:XX:XX:XX:XX",
											"FcoeMode": "Disabled",
											"Fqdd": "NIC.Mezzanine.1A-1-1",
											"IscsiMode": "Disabled",
											"MaxBandwidth": 0,
											"MinBandwidth": 0,
											"NicMode": "Disabled",
											"PermanentMacAddress": "XX:XX:XX:XX:XX:XX",
											"VirtualFipMacAddress": "",
											"VirtualIscsiMacAddress": "",
											"VirtualMacAddress": ""
										}
									],
									"PortId": "NIC.Mezzanine.1A-1",
									"ProductName": "Intel(R) Ethernet 25G 2P XXV710 Mezz - 24:6E:96:9C:E6:70",
									"TargetFcoeWwpn": "",
									"TargetIpAddress": ""
								},
								{
									"InitiatorGateway": "",
									"InitiatorIpAddress": "",
									"InitiatorName": "",
									"InitiatorPrimaryDns": "",
									"InitiatorSecondaryDns": "",
									"InitiatorSubnetMask": "",
									"LinkSpeed": 0,
									"LinkStatus": "",
									"Partitions": [
										{
											"CurrentMacAddress": "XX:XX:XX:XX:XX:XX",
											"FcoeMode": "Disabled",
											"Fqdd": "NIC.Mezzanine.1A-2-1",
											"IscsiMode": "Disabled",
											"MaxBandwidth": 0,
											"MinBandwidth": 0,
											"NicMode": "Disabled",
											"PermanentMacAddress": "XX:XX:XX:XX:XX:XX",
											"VirtualFipMacAddress": "",
											"VirtualIscsiMacAddress": "",
											"VirtualMacAddress": ""
										}
									],
									"PortId": "NIC.Mezzanine.1A-2",
									"ProductName": "Intel(R) Ethernet Controller XXV710 for 25GbE backplane - 24:6E:96:9C:E6:71",
									"TargetFcoeWwpn": "",
									"TargetIpAddress": ""
								}
							],
							"VendorName": "Intel Corp"
						}
					],
					"InventoryType": "serverNetworkInterfaces"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverFcCards')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "serverFcCards"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverOperatingSystems')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Hostname": "localhost.blr.amer.dell.com",
							"Id": 14778,
							"OsName": "VMware ESXi 6.0.0 build-5050593"
						}
					],
					"InventoryType": "serverOperatingSystems"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverVirtualFlashes')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "serverVirtualFlashes"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverPowerSupplies')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "serverPowerSupplies"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverArrayDisks')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"BusType": "SATA",
							"Channel": 0,
							"DeviceId": 0,
							"DiskNumber": "Disk 0 on Embedded AHCI Controller 2",
							"EnclosureId": "Disk.Direct.0-0:AHCI.Embedded.2-1",
							"EncryptionAbility": false,
							"FreeSpace": "0 bytes",
							"Id": 14776,
							"ManufacturedDay": 15,
							"ManufacturedWeek": 14,
							"ManufacturedYear": 2007,
							"MediaType": "Hard Disk Drive",
							"ModelNumber": "ST1000NX0443",
							"PredictiveFailureState": "0",
							"RaidStatus": "Non-RAID",
							"RemainingReadWriteEndurance": "255",
							"Revision": "NB33",
							"SasAddress": "5000C500A99C65B1",
							"SecurityState": "Not Capable",
							"SerialNumber": "W470FE2J",
							"Size": "931.52 GB",
							"SlotNumber": 0,
							"Status": 2000,
							"StatusString": "Unknown",
							"UsedSpace": "0 bytes",
							"VendorName": "SEAGATE"
						}
					],
					"InventoryType": "serverArrayDisks"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverRaidControllers')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"CacheSizeInMb": 0,
							"DeviceDescription": "Embedded AHCI 2",
							"DeviceId": 0,
							"Fqdd": "AHCI.Embedded.2-1",
							"Id": 29550,
							"Name": "Lewisburg SATA Controller [AHCI mode]",
							"PciSlot": "Not Applicable",
							"RollupStatus": 2000,
							"RollupStatusString": "UNKNOWN",
							"Status": 2000,
							"StatusTypeString": "UNKNOWN",
							"StorageAssignmentAllowed": "0"
						},
						{
							"CacheSizeInMb": 0,
							"DeviceDescription": "Embedded AHCI 1",
							"DeviceId": 0,
							"Fqdd": "AHCI.Embedded.1-1",
							"Id": 29551,
							"Name": "Lewisburg SSATA Controller [AHCI mode]",
							"PciSlot": "Not Applicable",
							"RollupStatus": 2000,
							"RollupStatusString": "UNKNOWN",
							"Status": 2000,
							"StatusTypeString": "UNKNOWN",
							"StorageAssignmentAllowed": "0"
						}
					],
					"InventoryType": "serverRaidControllers"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverMemoryDevices')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"BankName": "A",
							"CurrentOperatingSpeed": 2400,
							"DeviceDescription": "DIMM A1",
							"Id": 14776,
							"InstanceId": "DIMM.Socket.A1",
							"Manufacturer": "Hynix Semiconductor",
							"ManufacturerDate": "Mon Jul 10 07:00:00 2017 UTC",
							"Name": "DIMM.Socket.A1",
							"PartNumber": "HMA81GR7AFR8N-VK",
							"Rank": "Single Rank",
							"SerialNumber": "325C8FC4",
							"Size": 8192,
							"Speed": 2666,
							"Status": 1000,
							"TypeDetails": "DDR4 DIMM"
						}
					],
					"InventoryType": "serverMemoryDevices"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverStorageEnclosures')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "serverStorageEnclosures"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('serverSupportedPowerStates')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 88645,
							"PowerState": 2
						},
						{
							"Id": 88646,
							"PowerState": 5
						},
						{
							"Id": 88647,
							"PowerState": 8
						},
						{
							"Id": 88648,
							"PowerState": 10
						},
						{
							"Id": 88649,
							"PowerState": 11
						},
						{
							"Id": 88650,
							"PowerState": 12
						}
					],
					"InventoryType": "serverSupportedPowerStates"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceLicense')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [],
					"InventoryType": "deviceLicense"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceCapabilities')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"CapabilityType": {
								"CapabilityId": 18,
								"Description": "Device capable of sending alerts.",
								"Name": "DEVICE_ALERT"
							},
							"Id": 319059
						},
						{
							"CapabilityType": {
								"CapabilityId": 17,
								"Description": "14G specific features",
								"Name": "FEATURES_14G"
							},
							"Id": 319060
						},
						{
							"CapabilityType": {
								"CapabilityId": 15,
								"Description": "Retrieve historical temperature data",
								"Name": "TEMP_HISTORY"
							},
							"Id": 319061
						},
						{
							"CapabilityType": {
								"CapabilityId": 14,
								"Description": "Retrieve historical power data",
								"Name": "POWER_HISTORY"
							},
							"Id": 319062
						},
						{
							"CapabilityType": {
								"CapabilityId": 13,
								"Description": "Tech Support Report",
								"Name": "TSR"
							},
							"Id": 319063
						},
						{
							"CapabilityType": {
								"CapabilityId": 12,
								"Description": "Diagnostics",
								"Name": "DIAGS"
							},
							"Id": 319064
						},
						{
							"CapabilityType": {
								"CapabilityId": 11,
								"Description": "System Hardware logs",
								"Name": "HW_LOGS "
							},
							"Id": 319065
						},
						{
							"CapabilityType": {
								"CapabilityId": 10,
								"Description": "Move sled and associate profile w sled location",
								"Name": "SLOT_ASSOCIATION"
							},
							"Id": 319066
						},
						{
							"CapabilityType": {
								"CapabilityId": 9,
								"Description": "Identify function on server",
								"Name": "BLINK"
							},
							"Id": 319067
						},
						{
							"CapabilityType": {
								"CapabilityId": 41,
								"Description": "Capability to share externally assigned Storage",
								"Name": "SHARED_STORAGE_ALLLOWED"
							},
							"Id": 319068
						},
						{
							"CapabilityType": {
								"CapabilityId": 8,
								"Description": "Remote Firmware update capability. ",
								"Name": "FW_UPDATE"
							},
							"Id": 319069
						},
						{
							"CapabilityType": {
								"CapabilityId": 7,
								"Description": "Set attributes on the system",
								"Name": "CONFIGURE"
							},
							"Id": 319070
						},
						{
							"CapabilityType": {
								"CapabilityId": 4,
								"Description": "Get Sensor Info, sub system health details",
								"Name": "SENSOR_DETAILS"
							},
							"Id": 319071
						},
						{
							"CapabilityType": {
								"CapabilityId": 3,
								"Description": "Power reset hard/graceful",
								"Name": "POWER_CONTROL_RESET"
							},
							"Id": 319072
						},
						{
							"CapabilityType": {
								"CapabilityId": 2,
								"Description": "Power Down hard/graceful",
								"Name": "POWER_CONTROL_OFF"
							},
							"Id": 319073
						},
						{
							"CapabilityType": {
								"CapabilityId": 1,
								"Description": "Power up",
								"Name": "POWER_CONTROL_ON"
							},
							"Id": 319074
						},
						{
							"CapabilityType": {
								"CapabilityId": 31,
								"Description": "Ability to execute IPMI tasks",
								"Name": "REMOTE_IPMI"
							},
							"Id": 319075
						},
						{
							"CapabilityType": {
								"CapabilityId": 30,
								"Description": "Ability to execute RACADM tasks",
								"Name": "REMOTE_RACADM"
							},
							"Id": 319076
						}
					],
					"InventoryType": "deviceCapabilities"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceFru')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 258511,
							"Manufacturer": "Hynix Semiconductor",
							"Name": "DDR4 DIMM",
							"PartNumber": "HMA81GR7AFR8N-VK",
							"SerialNumber": "325C8FC4"
						},
						{
							"Id": 258512,
							"Manufacturer": "Dell Inc.",
							"Name": "SystemPlanar",
							"PartNumber": "0740HW",
							"Revision": "X30",
							"SerialNumber": "CNFCP007BH005G"
						},
						{
							"Id": 258513,
							"Manufacturer": "Dell",
							"Name": "Intel(R) 25GbE 2P XXV710  Mezz",
							"PartNumber": "0H9NTY",
							"Revision": "X03",
							"SerialNumber": "MY124027CF006O"
						}
					],
					"InventoryType": "deviceFru"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceLocation')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 14780,
							"Rackslot": "1"
						}
					],
					"InventoryType": "deviceLocation"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceManagement')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Device": 0,
							"DnsName": "iDRAC-XXXXX",
							"EndPointAgents": [
								{
									"AgentName": "iDRAC",
									"HasCreds": 2,
									"ManagementProfileId": XXXXX,
									"ManagementURL": "https://192.168.0.1:443",
									"ProfileId": "WSMAN_OOB",
									"Status": 1000,
									"StatusDateTime": 1548142229280,
									"Version": "3.20.20.20"
								}
							],
							"InstrumentationName": "hostname.xxx.xxx.dell.com",
							"IpAddress": "100.96.45.142",
							"MacAddress": "XX:XX:XX:XX:XX:XX",
							"ManagementId": XXXXX,
							"ManagementType": {
								"Description": "Public Management Interface",
								"ManagementType": 2,
								"Name": "PUBLIC"
							}
						},
						{
							"Device": 0,
							"DnsName": "iDRAC-XXXXX",
							"EndPointAgents": [
								{
									"AgentName": "iDRAC",
									"HasCreds": 2,
									"ManagementProfileId": XXXXX,
									"ManagementURL": "unknown",
									"ProfileId": "WSMAN_OOB",
									"Status": 1000,
									"StatusDateTime": 1548142229280,
									"Version": "3.20.20.20"
								}
							],
							"InstrumentationName": "hostname.xxx.xxx.dell.com",
							"IpAddress": "[::]",
							"MacAddress": "XX:XX:XX:XX:XX:XX",
							"ManagementId": XXXXX,
							"ManagementType": {
								"Description": "Public Management Interface",
								"ManagementType": 2,
								"Name": "PUBLIC"
							}
						}
					],
					"InventoryType": "deviceManagement"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('deviceSoftware')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"DeviceDescription": "Intel(R) Ethernet 25G 2P XXV710 Mezz - 24:6E:96:9C:E6:70",
							"InstallationDate": "2001-09-03T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#701__NIC.Mezzanine.1A-1-1",
							"PciDeviceId": "158A",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"SubDeviceId": "000A",
							"SubVendorId": "8086",
							"VendorId": "8086",
							"Version": "18.5.17"
						},
						{
							"ComponentId": "25806",
							"DeviceDescription": "Diagnostics",
							"InstallationDate": "2018-10-15T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#802__Diagnostics.Embedded.1:LC.Embedded.1",
							"SoftwareType": "APAC",
							"Status": "Installed",
							"Version": "0"
						},
						{
							"ComponentId": "25227",
							"DeviceDescription": "Integrated Dell Remote Access Controller",
							"InstallationDate": "2018-07-13T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#iDRAC.Embedded.1-1#IDRACinfo",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "3.20.20.20"
						},
						{
							"ComponentId": "105688",
							"DeviceDescription": "Disk 0 on Embedded AHCI Controller 2",
							"InstallationDate": "2001-09-03T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#304_C_Disk.Direct.0-0:AHCI.Embedded.2-1",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "NB33"
						},
						{
							"ComponentId": "104684",
							"DeviceDescription": "iDRAC Service Module Installer",
							"InstallationDate": "2018-10-15T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#802__ServiceModule.Embedded.1",
							"SoftwareType": "APAC",
							"Status": "Installed",
							"Version": "0"
						},
						{
							"ComponentId": "27763",
							"DeviceDescription": "System CPLD",
							"InstallationDate": "2018-10-15T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#803__CPLD.Embedded.1",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "1.0.0"
						},
						{
							"ComponentId": "28897",
							"DeviceDescription": "Lifecycle Controller",
							"InstallationDate": "2018-07-13T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#802__USC.Embedded.1:LC.Embedded.1",
							"SoftwareType": "APAC",
							"Status": "Installed",
							"Version": "3.20.20.20"
						},
						{
							"ComponentId": "18981",
							"DeviceDescription": "OS Drivers Pack",
							"InstallationDate": "2018-10-15T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#802__DriverPack.Embedded.1:LC.Embedded.1",
							"SoftwareType": "APAC",
							"Status": "Installed",
							"Version": "0"
						},
						{
							"ComponentId": "103999",
							"DeviceDescription": "Backplane 0",
							"InstallationDate": "2018-11-29T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#314_C_RAID.Backplane.Firmware.0",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"Version": "4.27"
						},
						{
							"ComponentId": "159",
							"DeviceDescription": "BIOS",
							"InstallationDate": "2001-09-03T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#741__BIOS.Setup.1-1",
							"SoftwareType": "BIOS",
							"Status": "Installed",
							"Version": "1.0.2"
						},
						{
							"ComponentId": "25227",
							"DeviceDescription": "Integrated Dell Remote Access Controller",
							"InstallationDate": "NA",
							"InstanceId": "DCIM:PREVIOUS#iDRAC.Embedded.1-1#IDRACinfo",
							"SoftwareType": "FRMW",
							"Status": "Available",
							"Version": "3.20.21.20"
						},
						{
							"DeviceDescription": "Intel(R) Ethernet Controller XXV710 for 25GbE backplane - 24:6E:96:9C:E6:71",
							"InstallationDate": "2001-09-03T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#701__NIC.Mezzanine.1A-2-1",
							"PciDeviceId": "158A",
							"SoftwareType": "FRMW",
							"Status": "Installed",
							"SubDeviceId": "0000",
							"SubVendorId": "8086",
							"VendorId": "8086",
							"Version": "18.5.17"
						},
						{
							"ComponentId": "101734",
							"DeviceDescription": "OS Collector",
							"InstallationDate": "2018-10-15T00:00:00Z",
							"InstanceId": "DCIM:INSTALLED#802__OSCollector.Embedded.1",
							"SoftwareType": "APAC",
							"Status": "Installed",
							"Version": "0"
						}
					],
					"InventoryType": "deviceSoftware"
				},
				{
					"@odata.id": "/api/DeviceService/Devices(33333)/InventoryDetails('subsystemRollupStatus')",
					"@odata.type": "#DeviceService.InventoryDetail",
					"InventoryInfo": [
						{
							"Id": 118345,
							"Status": 1000,
							"SubsystemName": "cpuRollupStatus"
						},
						{
							"Id": 118346,
							"Status": 1000,
							"SubsystemName": "sysMemPrimaryStatus"
						},
						{
							"Id": 118347,
							"Status": 1000,
							"SubsystemName": "voltRollupStatus"
						},
						{
							"Id": 118348,
							"Status": 1000,
							"SubsystemName": "batteryRollupStatus"
						},
						{
							"Id": 118349,
							"Status": 1000,
							"SubsystemName": "licensingRollupStatus"
						},
						{
							"Id": 118350,
							"Status": 1000,
							"SubsystemName": "storageRollupStatus"
						},
						{
							"Id": 118351,
							"Status": 1000,
							"SubsystemName": "tempRollupStatus"
						},
						{
							"Id": 118352,
							"Status": 2000,
							"SubsystemName": "intrusionRollupStatus"
						}
					],
					"InventoryType": "subsystemRollupStatus"
				}
			]
		}
	}
} }


Get Inventory details of specified inventory type of specified devices

    "ansible_facts": { {
        "device_id": {
            "25010": {
                "@odata.context": "/api/$metadata#DeviceService.InventoryDetail/$entity",
                "@odata.id": "/api/DeviceService/Devices(25010)/InventoryDetails('serverDeviceCards')",
                "@odata.type": "#DeviceService.InventoryDetail",
                "InventoryInfo": [],
                "InventoryType": "serverDeviceCards"
            }
        },
        "device_service_tag": {
            "KLBR840": {
                "@odata.context": "/api/$metadata#DeviceService.InventoryDetail/$entity",
                "@odata.id": "/api/DeviceService/Devices(31474)/InventoryDetails('serverDeviceCards')",
                "@odata.type": "#DeviceService.InventoryDetail",
                "InventoryInfo": [
                    {
                        "DatabusWidth": "8x or x8",
                        "Description": "Ethernet 25G 2P XXV710 Mezz",
                        "Id": 153179,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Other",
                        "SlotNumber": "NIC.Mezzanine.1A-1-1",
                        "SlotType": "PCI Express Gen 3 x16"
                    },
                    {
                        "DatabusWidth": "8x or x8",
                        "Description": "Ethernet Controller XXV710 for 25GbE backplane",
                        "Id": 153180,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Other",
                        "SlotNumber": "NIC.Mezzanine.1A-2-1",
                        "SlotType": "PCI Express Gen 3 x16"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg SMBus",
                        "Id": 153181,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "SMBus.Embedded.3-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg SATA Controller [AHCI mode]",
                        "Id": 153182,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "AHCI.Embedded.2-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg PCI Express Root Port #5",
                        "Id": 153183,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "P2PBridge.Embedded.2-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg LPC Controller",
                        "Id": 153184,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "ISABridge.Embedded.1-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Integrated Matrox G200eW3 Graphics Controller",
                        "Id": 153185,
                        "Manufacturer": "Matrox Electronics Systems Ltd.",
                        "SlotLength": "Unknown",
                        "SlotNumber": "Video.Embedded.1-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Sky Lake-E DMI3 Registers",
                        "Id": 153186,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "HostBridge.Embedded.1-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg SSATA Controller [AHCI mode]",
                        "Id": 153187,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "AHCI.Embedded.1-1",
                        "SlotType": "Unknown"
                    },
                    {
                        "DatabusWidth": "Unknown",
                        "Description": "Lewisburg PCI Express Root Port #1",
                        "Id": 153188,
                        "Manufacturer": "Intel Corporation",
                        "SlotLength": "Unknown",
                        "SlotNumber": "P2PBridge.Embedded.1-1",
                        "SlotType": "Unknown"
                    }
                ],
                "InventoryType": "serverDeviceCards"
            }
        }
    } }



Get Health status of specified devices:
    "ansible_facts": { {
        "device_service_tag": {
            "KLBR840": {
                "@odata.context": "/api/$metadata#Collection(DeviceService.SubSystemHealthFaultModel)",
                "@odata.count": 7,
                "value": [
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "SEL/Misc"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Voltage"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Current"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Processor"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Memory"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Temperature"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "RollupStatus": "1000",
                        "SubSystem": "Battery"
                    }
                ]
            },
            "ST0004B": {
                "@odata.context": "/api/$metadata#Collection(DeviceService.SubSystemHealthFaultModel)",
                "@odata.count": 8,
                "value": [
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "MM"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "System.Modular.3"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "IOM.Slot.A1"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "Miscellaneous"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "Temperature"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "Battery"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultSummaryList": [
                            {
                                "Count": "0",
                                "Severity": "1000"
                            }
                        ],
                        "RollupStatus": "1000",
                        "SubSystem": "Fan"
                    },
                    {
                        "@odata.type": "#DeviceService.SubSystemHealthFaultModel",
                        "FaultList": [
                            {
                                "Fqdd": "System.Chassis.1#ChassisPower.1#PSCalcRedPolicy",
                                "InstanceId": "Fault#02200003#1",
                                "Message": "Power supply redundancy is lost.",
                                "MessageId": "RDU0012",
                                "RecommendedAction": "Check the event log for power supply failures. Review system configuration and power consumption.",
                                "Severity": "4000",
                                "SubSystem": "PowerSupply",
                                "TimeStamp": "2018-11-27T08:32:56+00:00"
                            }
                        ],
                        "FaultSummaryList": [
                            {
                                "Count": "1",
                                "Severity": "4000"
                            }
                        ],
                        "RollupStatus": "4000",
                        "SubSystem": "PowerSupply"
                    }
                ]
            }
        }
    } }