# idrac_gather_facts

Role to gather facts from iDRAC

## Requirements
------------

### Development
Requirements to develop and contribute to the role.
```
python
ansible
molecule
docker
```
### Production
Requirements to use the role.
```
python
ansible
```
### Ansible collections
Collections required to use the role.
```
dellemc.openmanage
ansible.utils
```

## Role Variables
<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Required</th>
    <th>Default Value</th>
    <th>Choices</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>hostname</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC IP Address</td>
  </tr>
  <tr>
    <td>username</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC username</td>
  </tr>
  <tr>
    <td>password</td>
    <td>true</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- iDRAC user password.</td>
  </tr>
  <tr>
    <td>https_port</td>
    <td>false</td>
    <td>443</td>
    <td></td>
    <td>int</td>
    <td>- iDRAC port.</td>
  </tr>
  <tr>
    <td>validate_certs</td>
    <td>false</td>
    <td>true</td>
    <td></td>
    <td>bool</td>
    <td>- If C(False), the SSL certificates will not be validated.<br>- Configure C(False) only on personally controlled sites where self-signed certificates are used.<br>- Prior to collection version 5.0.0, I(validate_certs) is C(False) by default.</td>
  </tr>
  <tr>
    <td>ca_path</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>path</td>
    <td>- The Privacy Enhanced Mail (PEM) file that contains a CA certificate to be used for the validation.</td>
  </tr>
  <tr>
    <td>https_timeout</td>
    <td>false</td>
    <td>30</td>
    <td></td>
    <td>int</td>
    <td>- The socket level timeout in seconds.</td>
  </tr>
  <tr>
    <td>computer_system_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Computer system id.</td>
  </tr>
  <tr>
    <td>manager_id</td>
    <td>false</td>
    <td></td>
    <td></td>
    <td>str</td>
    <td>- Manager/BMC id.</td>
  </tr>
  <tr>
    <td>target</td>
    <td>false</td>
    <td>- System <br></td>
    <td>- System <br> - BIOS <br> - Controller <br> - CPU <br> - Enclosure <br> - EnclosureEMM <br> - Fan <br>
        - Firmware <br> - HostNIC <br> - License <br> - Memory <br> - NIC <br> - PCIeSSDBackPlane <br>
        - PowerSupply <br> - PresenceAndStatusSensor <br> - Sensors_Battery <br> - Sensors_Intrusion <br>
        - Sensors_Voltage <br> - VirtualDisk <br> - PCIeDevice <br> - PhysicalDisk <br> - SystemMetrics<br> - SecureBoot</td>
    <td>list</td>
    <td>Target component for which information needs to be gathered.
    <ul>
        <li>C(BIOS) lists the BIOS information.</li>
        <li>C(Chassis) lists the chassis.</li>
        <li>C(Controller) lists the available controllers for iDRAC.</li>
        <li>C(CPU) lists the system processors.</li>
        <li>C(Enclosure) lists the enclosures.</li> 
        <li>C(EnclosureEMM) lists the enclosure management module specific data.</li>
        <li>C(Fan) lists the fans.</li>
        <li>C(Firmware) lists the firmware inventories.</li>
        <li>C(HostNIC) lists the host NIC.</li>
        <li>C(IDRAC) lists the attributes for iDRAC.</li> 
        <li>C(License) lists the license information.</li>
        <li>C(Manager) lists the manager resources.</li>
        <li>C(Memory) lists the memory device specific data.</li>
        <li>C(NetworkAdapter) lists the network adapters.</li>
        <li>C(NetworkPort) lists the network ports.</li>
        <li>C(NetworkDeviceFunction) lists the network device functions.</li>
        <li>C(NIC) lists NIC device specific data.</li>
        <li>C(PCIeSSDBackPlane) lists PCIeSSD back plane specific data.</li>
        <li>C(PowerSupply) lists data specific to the Power Supply devices in the managed system.</li>
        <li>C(PresenceAndStatusSensor) lists the presence and status sensor specific data.</li>
        <li>C(PCIeDevice) lists the PCIeDevices.</li>
        <li>C(PhysicalDisk) lists the physical disks.</li>
        <li>C(Sensors_Battery) lists the sensors battery information.</li>
        <li>C(Sensors_Intrusion) lists the sensors intrusion information.</li>
        <li>C(Sensors_Voltage) lists the sensors voltage information.</li>
        <li>C(System) lists the ComputerSystem resources for iDRAC.</li>
        <li>C(SystemMetrics) lists the system metrics.</li>
        <li>C(ThermalSubSystem) lists the thermal sub system.</li>
        <li>C(VirtualDisk) lists the virtual disks.</li>
        <li>C(VirtualMedia) lists the virtual media.</li>
        <li>C(SecureBoot) lists the secure boot specific data.</li>
    </ul>
    </td>
  </tr>
</tbody>
</table>

## Fact variables

<table>
<thead>
  <tr>
    <th>Name</th>
    <th>Sample</th>
    <th>Description</th>
  </tr>
</thead>
  <tbody>
    <tr>
    <td>system</td>
    <td>{"BIOSReleaseDate": "03/22/2022", "BaseBoardChassisSlot": "1", "BatteryRollupStatus": "OK", "BladeGeometry": "SingleWidth,FullHeight", "CMCIP": "1.2.3.4", "CPURollupStatus": "Unknown", "ChassisModel": "", "ChassisName": "", "ChassisServiceTag": "SVCTAG1", "ChassisSystemHeightUnit": 7, "CurrentRollupStatus": "OK", "EstimatedExhaustTemperatureCelsius": 255, "EstimatedSystemAirflowCFM": 255, "ExpressServiceCode": "SERVICECODE1", "FanRollupStatus": null, "IDSDMRollupStatus": null, "Id": "System.Embedded.1", "IntrusionRollupStatus": null, "IsOEMBranded": "False", "LastSystemInventoryTime": "2019-08-09T13:23:32+00:00", "LastUpdateTime": "2022-06-10T20:19:30+00:00", "LicensingRollupStatus": "OK", "ManagedSystemSize": "7 U", "MaxCPUSockets": 2, "MaxDIMMSlots": 24, "MaxPCIeSlots": 3, "MemoryOperationMode": "OptimizerMode", "Name": "DellSystem", "NodeID": "SVCTAG2", "PSRollupStatus": null, "PlatformGUID": "325a364f-c0b6-4b80-3010-00484c4c4544", "PopulatedDIMMSlots": 2, "PopulatedPCIeSlots": 3, "PowerCapEnabledState": "Disabled", "SDCardRollupStatus": "OK", "SELRollupStatus": "OK", "ServerAllocationWatts": 18, "ServerOS.1.HostName": "MINWINPC", "ServerOS.1.OEMOSVersion": "", "ServerOS.1.OSName": "", "ServerOS.1.OSVersion": "", "ServerOS.1.ProductKey": "", "ServerOS.1.ServerPoweredOnTime": 0, "StorageRollupStatus": "OK", "SysMemErrorMethodology": "Multi-bitECC", "SysMemFailOverState": "NotInUse", "SysMemLocation": "SystemBoardOrMotherboard", "SysMemPrimaryStatus": "OK", "SystemGeneration": "14G Modular", "SystemID": 1893, "SystemRevision": "I", "TempRollupStatus": "OK", "TempStatisticsRollupStatus": "OK", "UUID": "4c4c4544-0048-3010-804b-b6c04f365a32", "VoltRollupStatus": "OK", "smbiosGUID": "44454c4c-4800-1030-804b-12345678abcd"}</td>
    <td>Response facts details for system and operating system.</td>
    </tr>
    <tr>
    <td>bios</td>
    <td>{"@Redfish.Settings": {"SupportedApplyTimes": ["OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}, "Attributes": {"AcPwrRcvry": "Last", "AdddcSetting": "Disabled", "AesNi": "Enabled", "AssetTag": "", "AuthorizeDeviceFirmware": "Disabled", "AvxIccpPregrant": "IccpHeavy128", "BootMode": "Bios", "BootSeqRetry": "Enabled", "CECriticalSEL": "Disabled", "ConTermType": "Vt100Vt220", "ControlledTurbo": "Disabled", "ControlledTurboMinusBin": 0, "CorrEccSmi": "Enabled", "CpuInterconnectBusLinkPower": "Enabled", "CpuInterconnectBusSpeed": "MaxDataRate", "CurrentEmbVideoState": "Enabled", "DcuIpPrefetcher": "Enabled", "DcuStreamerPrefetcher": "Enabled", "DeadLineLlcAlloc": "Enabled", "DellWyseP25BIOSAccess": "Enabled", "DirectoryAtoS": "Disabled", "DramRefreshDelay": "Performance", "DynamicCoreAllocation": "Disabled", "EmbSata": "AhciMode", "EmbVideo": "Enabled", "EnergyPerformanceBias": "BalancedPerformance", "ErrPrompt": "Enabled", "ExtSerialConnector": "Serial1", "FailSafeBaud": "115200", "ForceInt10": "Disabled", "GenericUsbBoot": "Disabled", "HddFailover": "Disabled", "HddPlaceholder": "Disabled", "InBandManageabilityInterface": "Enabled", "IntelTxt": "Off", "InternalUsb": "On", "IoatEngine": "Disabled", "LlcPrefetch": "Disabled", "MemFrequency": "MaxPerf", "MemOpMode": "OptimizerMode", "MemPatrolScrub": "Standard", "MemRefreshRate": "1x", "MemTest": "Disabled", "MemoryMappedIOH": "56TB", "MmioAbove4Gb": "Enabled", "MonitorMwait": "Enabled", "NativeTrfcTiming": "Enabled", "NodeInterleave": "Disabled", "NumLock": "On", "NvmeMode": "NonRaid", "OneTimeBootMode": "Disabled", "OneTimeBootSeqDev": "Floppy.iDRACVirtual.1-1", "OneTimeHddSeqDev": "", "OppSrefEn": "Disabled", "OsWatchdogTimer": "Disabled", "PCIRootDeviceUnhide": "Disabled", "PPROnUCE": "Enabled", "PasswordStatus": "Unlocked", "PcieAspmL1": "Enabled", "PowerCycleRequest": "None", "Proc1Brand": "Intel(R) Xeon(R) Bronze 3204 CPU @ 1.90GHz", "Proc1Id": "6-55-7", "Proc1L2Cache": "6x1 MB", "Proc1L3Cache": "8448 KB", "Proc1MaxMemoryCapacity": "1 TB", "Proc1Microcode": "0x5003302", "Proc1NumCores": 6, "Proc2Brand": "Intel(R) Xeon(R) Bronze 3204 CPU @ 1.90GHz", "Proc2Id": "6-55-7", "Proc2L2Cache": "6x1 MB", "Proc2L3Cache": "8448 KB", "Proc2MaxMemoryCapacity": "1 TB", "Proc2Microcode": "0x5003302", "Proc2NumCores": 6, "ProcAdjCacheLine": "Enabled", "ProcBusSpeed": "9.60 GT/s", "ProcC1E": "Enabled", "ProcCStates": "Enabled", "ProcConfigTdp": "Nominal", "ProcCoreSpeed": "1.90 GHz", "ProcCores": "All", "ProcHwPrefetcher": "Enabled", "ProcPwrPerf": "SysDbpm", "ProcVirtualization": "Enabled", "ProcX2Apic": "Enabled", "PwrButton": "Enabled", "RedirAfterBoot": "Enabled", "RedundantOsBoot": "Disabled", "RedundantOsLocation": "None", "RedundantOsState": "Visible", "SHA256SetupPassword": "", "SHA256SetupPasswordSalt": "", "SHA256SystemPassword": "", "SHA256SystemPasswordSalt": "", "SataPortA": "Auto", "SataPortACapacity": "N/A", "SataPortADriveType": "Unknown Device", "SataPortAModel": "Unknown", "SataPortB": "Auto", "SataPortBCapacity": "N/A", "SataPortBDriveType": "Unknown Device", "SataPortBModel": "Unknown", "SataPortC": "Auto", "SataPortCCapacity": "N/A", "SataPortCDriveType": "Unknown Device", "SataPortCModel": "Unknown", "SataPortD": "Auto", "SataPortDCapacity": "N/A", "SataPortDDriveType": "Unknown Device", "SataPortDModel": "Unknown", "SataPortE": "Auto", "SataPortECapacity": "N/A", "SataPortEDriveType": "Unknown Device", "SataPortEModel": "Unknown", "SataPortF": "Auto", "SataPortFCapacity": "N/A", "SataPortFDriveType": "Unknown Device", "SataPortFModel": "Unknown", "SecureBoot": "Disabled", "SecureBootMode": "DeployedMode", "SecureBootPolicy": "Standard", "SecurityFreezeLock": "Enabled", "SerialComm": "Off", "SerialPortAddress": "Com1", "SetBootOrderDis": "", "SetBootOrderEn": "Floppy.iDRACVirtual.1-1,Optical.iDRACVirtual.1-1", "SetBootOrderFqdd1": "", "SetBootOrderFqdd10": "", "SetBootOrderFqdd11": "", "SetBootOrderFqdd12": "", "SetBootOrderFqdd13": "", "SetBootOrderFqdd14": "", "SetBootOrderFqdd15": "", "SetBootOrderFqdd16": "", "SetBootOrderFqdd2": "", "SetBootOrderFqdd3": "", "SetBootOrderFqdd4": "", "SetBootOrderFqdd5": "", "SetBootOrderFqdd6": "", "SetBootOrderFqdd7": "", "SetBootOrderFqdd8": "", "SetBootOrderFqdd9": "", "SetLegacyHddOrderFqdd1": "", "SetLegacyHddOrderFqdd10": "", "SetLegacyHddOrderFqdd11": "", "SetLegacyHddOrderFqdd12": "", "SetLegacyHddOrderFqdd13": "", "SetLegacyHddOrderFqdd14": "", "SetLegacyHddOrderFqdd15": "", "SetLegacyHddOrderFqdd16": "", "SetLegacyHddOrderFqdd2": "", "SetLegacyHddOrderFqdd3": "", "SetLegacyHddOrderFqdd4": "", "SetLegacyHddOrderFqdd5": "", "SetLegacyHddOrderFqdd6": "", "SetLegacyHddOrderFqdd7": "", "SetLegacyHddOrderFqdd8": "", "SetLegacyHddOrderFqdd9": "", "SetupPassword": null, "Slot1": "Enabled", "Slot2": "Enabled", "Slot3": "Enabled", "SnoopHldOff": "Roll2KCycles", "SriovGlobalEnable": "Disabled", "SubNumaCluster": "Disabled", "SysMemSize": "32 GB", "SysMemSpeed": "2133 Mhz", "SysMemType": "ECC DDR4", "SysMemVolt": "1.20 V", "SysMfrContactInfo": "www.dell.com", "SysPassword": null, "SysProfile": "PerfPerWattOptimizedDapc", "SystemBiosVersion": "2.14.2", "SystemCpldVersion": "1.0.4", "SystemManufacturer": "Dell Inc.", "SystemMeVersion": "4.1.4.700", "SystemModelName": "PowerEdge MX740c", "SystemServiceTag": "SVCTAG3", "TpmCommand": "None", "TpmFirmware": "TpmFirmware", "TpmInfo": "Type: 1.2-NTC", "TpmPpiBypassClear": "Disabled", "TpmPpiBypassProvision": "Disabled", "TpmSecurity": "Off", "TpmStatus": "Unknown", "UefiComplianceVersion": "2.7", "UefiVariableAccess": "Standard", "UncoreFrequency": "DynamicUFS", "UpiPrefetch": "Enabled", "UsbManagedPort": "On", "UsbPorts": "AllOn", "VideoMem": "16 MB", "WorkloadProfile": "NotAvailable", "WriteCache": "Disabled", "WriteDataCrc": "Disabled"}}</td>
    <td>Response facts details for bios.</td>
    </tr>
    <tr>
    <td>controller</td>
    <td>[{
                "@Redfish.Settings": {
                    "SettingsObject": {},
                    "SupportedApplyTimes": [
                        "Immediate",
                        "OnReset",
                        "AtMaintenanceWindowStart",
                        "InMaintenanceWindowOnReset"
                    ]
                },
                "Assembly": {},
                "CacheSummary": {
                    "TotalCacheSizeMiB": 0
                },
                "ControllerRates": {
                    "ConsistencyCheckRatePercent": null,
                    "RebuildRatePercent": null
                },
                "Description": "Integrated AHCI controller 1",
                "FirmwareVersion": "2.6.13.3025",
                "Id": "AHCI.Integrated.1-1",
                "Identifiers": [
                    {
                        "DurableName": null,
                        "DurableNameFormat": null
                    }
                ],
                "Links": {
                    "PCIeFunctions": []
                },
                "Manufacturer": "DELL",
                "Model": "BOSS-S1",
                "Name": "BOSS-S1",
                "Oem": {
                    "Dell": {
                        "DellStorageController": {
                            "AlarmState": "AlarmNotSupported",
                            "AutoConfigBehavior": "NotApplicable",
                            "BackgroundInitializationRatePercent": null,
                            "BatteryLearnMode": null,
                            "BootVirtualDiskFQDD": null,
                            "CacheSizeInMB": 0,
                            "CachecadeCapability": "NotSupported",
                            "CheckConsistencyMode": null,
                            "ConnectorCount": 0,
                            "ControllerBootMode": null,
                            "ControllerFirmwareVersion": "2.6.13.3025",
                            "ControllerMode": null,
                            "CopybackMode": null,
                            "CurrentControllerMode": "NotSupported",
                            "Device": "0",
                            "DeviceCardDataBusWidth": "4x or x4",
                            "DeviceCardSlotLength": "Other",
                            "DeviceCardSlotType": "M.2 Socket 3 (Mechanical Key M)",
                            "DriverVersion": null,
                            "EncryptionCapability": "None",
                            "EncryptionMode": "None",
                            "EnhancedAutoImportForeignConfigurationMode": null,
                            "KeyID": null,
                            "LastSystemInventoryTime": "2023-12-31T12:25:07+00:00",
                            "LastUpdateTime": "2023-12-31T18:50:12+00:00",
                            "LoadBalanceMode": null,
                            "MaxAvailablePCILinkSpeed": null,
                            "MaxDrivesInSpanCount": 2,
                            "MaxPossiblePCILinkSpeed": null,
                            "MaxSpansInVolumeCount": 1,
                            "MaxSupportedVolumesCount": 1,
                            "PCISlot": null,
                            "PatrolReadIterationsCount": 0,
                            "PatrolReadMode": null,
                            "PatrolReadRatePercent": null,
                            "PatrolReadState": "Unknown",
                            "PatrolReadUnconfiguredAreaMode": null,
                            "PersistentHotspare": "NotApplicable",
                            "RAIDMode": "None",
                            "RealtimeCapability": "Incapable",
                            "ReconstructRatePercent": null,
                            "RollupStatus": "OK",
                            "SASAddress": "0",
                            "SecurityStatus": "EncryptionNotCapable",
                            "SharedSlotAssignmentAllowed": "NotApplicable",
                            "SlicedVDCapability": "NotSupported",
                            "SpindownIdleTimeSeconds": 0,
                            "SupportControllerBootMode": "NotSupported",
                            "SupportEnhancedAutoForeignImport": "NotSupported",
                            "SupportRAID10UnevenSpans": "NotSupported",
                            "SupportedInitializationTypes": [
                                "Fast"
                            ],
                            "SupportsLKMtoSEKMTransition": "No",
                            "T10PICapability": "NotSupported"
                        }
                    }
                },
                "SpeedGbps": 6.0,
                "Status": {
                    "Health": "OK",
                    "HealthRollup": "OK",
                    "State": "Enabled"
                },
                "SupportedControllerProtocols": [
                    "PCIe"
                ],
                "SupportedDeviceProtocols": [
                    "SATA"
                ],
                "SupportedRAIDTypes": [
                    "RAID1"
                ]
            }
        ]</td>
    <td>Response facts details for controller.</td>
    </tr>
    <tr>
    <td>cpu</td>
    <td>[{"Description": "Represents the properties of a Processor attached to this System", "Id": "CPU.Socket.1", "InstructionSet": "x86-64", "Manufacturer": "Intel", "MaxSpeedMHz": 4000, "Model": "Intel(R) Xeon(R) Bronze 3204 CPU @ 1.90GHz", "Name": "CPU 1", "Oem": {"Dell": {"DellAccelerators": null, "DellProcessor": {"CPUFamily": "Intel(R)Xeon(TM)", "CPUStatus": "CPUEnabled", "Cache1Associativity": "8-WaySet-Associative", "Cache1ErrorMethodology": "Parity", "Cache1InstalledSizeKB": 384, "Cache1Level": "L1", "Cache1Location": "Internal", "Cache1PrimaryStatus": "OK", "Cache1SRAMType": "Unknown", "Cache1SizeKB": 384, "Cache1Type": "Unified", "Cache1WritePolicy": "WriteBack", "Cache2Associativity": "16-WaySet-Associative", "Cache2ErrorMethodology": "Single-bitECC", "Cache2InstalledSizeKB": 6144, "Cache2Level": "L2", "Cache2Location": "Internal", "Cache2PrimaryStatus": "OK", "Cache2SRAMType": "Unknown", "Cache2SizeKB": 6144, "Cache2Type": "Unified", "Cache2WritePolicy": "WriteBack", "Cache3Associativity": "FullyAssociative", "Cache3ErrorMethodology": "Single-bitECC", "Cache3InstalledSizeKB": 8448, "Cache3Level": "L3", "Cache3Location": "Internal", "Cache3PrimaryStatus": "OK", "Cache3SRAMType": "Unknown", "Cache3SizeKB": 8448, "Cache3Type": "Unified", "Cache3WritePolicy": "WriteBack", "CurrentClockSpeedMhz": 1900, "ExternalBusClockSpeedMhz": 9600, "HyperThreadingCapable": "No", "HyperThreadingEnabled": "No", "Id": "CPU.Socket.1", "LastSystemInventoryTime": "2019-08-09T13:23:32+00:00", "LastUpdateTime": "2021-09-14T20:31:00+00:00", "Name": "DellProcessor", "TurboModeCapable": "No", "TurboModeEnabled": "No", "VirtualizationTechnologyCapable": "Yes", "VirtualizationTechnologyEnabled": "Yes", "Volts": "1.8"}, "PowerMetrics": null, "ThermalMetrics": null}}, "OperatingSpeedMHz": 1900, "ProcessorArchitecture": "x86", "ProcessorId": {"EffectiveFamily": "6", "EffectiveModel": "85", "IdentificationRegisters": "0x00050657", "MicrocodeInfo": "0x5003302", "Step": "7", "VendorId": "GenuineIntel"}, "ProcessorType": "CPU", "Socket": "CPU.Socket.1", "Status": {"Health": null, "State": "UnavailableOffline"}, "TotalCores": 6, "TotalEnabledCores": 6, "TotalThreads": 6, "TurboState": "Disabled", "Version": "Model 85 Stepping 7"}]</td>
    <td>Response facts details for cpu.</td>
    </tr>
    <tr>
    <td>enclosure</td>
    <td>[{"AssetName": null, "Connector": 0, "Id": "Enclosure.Internal.0-0:RAID.Mezzanine.1C-1", "LastSystemInventoryTime": "2019-08-09T13:23:32+00:00", "LastUpdateTime": "2022-09-23T23:44:26+00:00", "Name": "DellEnclosure", "ServiceTag": null, "SlotCount": 6, "TempProbeCount": 0, "Version": "4.35", "WiredOrder": 0}]</td>
    <td>Response facts details for enclosure.</td>
    </tr>
    <tr>
    <td>enclosure_emm</td>
    <td>[{"DeviceDescription": "EMM.Slot.0:Enclosure.Modular.4:NonRAID.Mezzanine.1C-1", "FQDD": "EMM.Slot.0:Enclosure.Modular.4:NonRAID.Mezzanine.1C-1", "Id": "EMM.Slot.0:Enclosure.Modular.4:NonRAID.Mezzanine.1C-1", "InstanceID": "EMM.Slot.0:Enclosure.Modular.4:NonRAID.Mezzanine.1C-1", "Name": "DellEnclosureEMM", "PartNumber": null, "PrimaryStatus": "OK", "Revision": "2.40", "State": "Ready"}]</td>
    <td>Response facts details for enclosure_emm.</td>
    </tr>
    <tr>
    <td>fan</td>
    <td>[{"Description": "Represents fan properties of the chassis", "HotPluggable": true, "Id": "Fan.Embedded.6A", "Location": {"PartLocation": {"LocationType": "Bay", "ServiceLabel": "System Board Fan6A"}}, "Name": "Fan 6A", "PhysicalContext": "SystemBoard", "SpeedPercent": {"SpeedRPM": 11640}, "Status": {"Health": "OK", "State": "Enabled"}}]</td>
    <td>Response facts details for fan.</td>
    </tr>
    <tr>
    <td>firmware</td>
    <td>[{"Description": "Represents Firmware Inventory", "Id": "Previous-108255-22.00.6__NIC.Embedded.2-1-1", "Name": "Broadcom Gigabit Ethernet BCM5720 - AB:CD:EF:GH:IJ:02", "Oem": {"Dell": {"DellSoftwareInventory": {"BuildNumber": 0, "Classifications": ["Firmware"], "ComponentID": "108255", "ComponentType": "FRMW", "Description": "The DellSoftwareInventory resource is a representation of an available device firmware in the managed system.", "DeviceID": "165F", "ElementName": "Broadcom Gigabit Ethernet BCM5720 - AB:CD:EF:GH:IJ:02", "HashValue": "56fa85676e6d570f714fb659f202371f1c570263b680e2d40d16059acfa9e3e6", "Id": "DCIM:PREVIOUS_0x23_701__NIC.Embedded.2-1-1", "IdentityInfoType": ["OrgID:ComponentType:VendorID:DeviceID:SubVendorID:SubDeviceID"], "IdentityInfoValue": ["DCIM:firmware:14E4:165F:1028:08FF"], "InstallationDate": "NA", "IsEntity": true, "MajorVersion": 22, "MinorVersion": 0, "Name": "DellSoftwareInventory", "PLDMCapabilitiesDuringUpdate": "0x00000000", "PLDMFDPCapabilitiesDuringUpdate": "0x00000000", "RevisionNumber": 6, "RevisionString": null, "SidebandUpdateCapable": false, "Status": "AvailableForInstallation", "SubDeviceID": "08FF", "SubVendorID": "1028", "VendorID": "14E4", "impactsTPMmeasurements": true}}}, "ReleaseDate": "2022-01-07T00:00:00Z", "SoftwareId": "108255", "Status": {"Health": "OK", "State": "Enabled"}, "Updateable": true, "Version": "22.00.6"}, {"Description": "Represents Firmware Inventory", "Id": "Previous-159-1.7.5__BIOS.Setup.1-1", "Name": "BIOS", "Oem": {"Dell": {"DellSoftwareInventory": {"BuildNumber": 0, "Classifications": ["BIOS/FCode"], "ComponentID": "159", "ComponentType": "BIOS", "Description": "The DellSoftwareInventory resource is a representation of an available device firmware in the managed system.", "DeviceID": null, "ElementName": "BIOS", "HashValue": "37e196d6b1c25ffc58f1c5c5a80a748932d22ddfbf72eedda05fbe788f57d641", "Id": "DCIM:PREVIOUS_0x23_741__BIOS.Setup.1-1", "IdentityInfoType": ["OrgID:ComponentType:ComponentID"], "IdentityInfoValue": ["DCIM:BIOS:159"], "InstallationDate": "NA", "IsEntity": true, "MajorVersion": 1, "MinorVersion": 7, "Name": "DellSoftwareInventory", "PLDMCapabilitiesDuringUpdate": "0x00000000", "PLDMFDPCapabilitiesDuringUpdate": "0x00000000", "RevisionNumber": 5, "RevisionString": null, "SidebandUpdateCapable": false, "Status": "AvailableForInstallation", "SubDeviceID": null, "SubVendorID": null, "VendorID": null, "impactsTPMmeasurements": true}}}, "ReleaseDate": "2022-09-16T00:00:00Z", "SoftwareId": "159", "Status": {"Health": "OK", "State": "Enabled"}, "Updateable": true, "Version": "1.7.5"}, {"Description": "Represents Firmware Inventory", "Id": "Previous-25227-6.00.02.00__iDRAC.Embedded.1-1", "Name": "Integrated Dell Remote Access Controller", "Oem": {"Dell": {"DellSoftwareInventory": {"BuildNumber": 7, "Classifications": ["Firmware"], "ComponentID": "25227", "ComponentType": "FRMW", "Description": "The DellSoftwareInventory resource is a representation of an available device firmware in the managed system.", "DeviceID": null, "ElementName": "Integrated Dell Remote Access Controller", "HashValue": null, "Id": "DCIM:PREVIOUS_0x23_iDRAC.Embedded.1-1_0x23_IDRACinfo", "IdentityInfoType": ["OrgID:ComponentType:ComponentID"], "IdentityInfoValue": ["DCIM:firmware:25227"], "InstallationDate": "NA", "IsEntity": true, "MajorVersion": 6, "MinorVersion": 0, "Name": "DellSoftwareInventory", "PLDMCapabilitiesDuringUpdate": "0x00000000", "PLDMFDPCapabilitiesDuringUpdate": "0x00000000", "RevisionNumber": 2, "RevisionString": null, "SidebandUpdateCapable": false, "Status": "AvailableForInstallation", "SubDeviceID": null, "SubVendorID": null, "VendorID": null, "impactsTPMmeasurements": false}}}, "ReleaseDate": "2022-08-11T00:00:00Z", "SoftwareId": "25227", "Status": {"Health": "OK", "State": "Enabled"}, "Updateable": true, "Version": "6.00.02.00"}]</td>
    <td>Response facts details for firmware.</td>
    </tr>
    <tr>
    <td>hostnic</td>
    <td>[{"Description": "Management for Host Interface", "ExternallyAccessible": false, "HostInterfaceType": "NetworkHostInterface", "Id": "Host.1", "InterfaceEnabled": false, "Name": "Managed Host Interface 1"}]</td>
    <td>Response facts details for hostnic.</td>
    </tr>
    <tr>
    <td>license</td>
    <td>[{"AuthorizationScope": "Service", "Description": "iDRAC9 x5 Enterprise Evaluation License", "DownloadURI": "/redfish/v1/LicenseService/Licenses/1188PA_girish_narasimhap/DownloadURI", "EntitlementId": "1188PA_girish_narasimhap", "ExpirationDate": "2023-02-23T00:00:00-06:00", "Id": "1188PA_girish_narasimhap", "InstallDate": null, "LicenseInfoURI": "", "LicenseOrigin": "Installed", "LicenseType": "Trial", "Links": {}, "Name": "1188PA_girish_narasimhap", "Removable": true, "Status": {"Health": "Warning", "State": "Enabled"}}]</td>
    <td>Response facts details for license.</td>
    </tr>
    <tr>
    <td>nic</td>
    <td>[{"AutoNeg": true, "Description": "Embedded NIC 1 Port 1 Partition 1", "EthernetInterfaceType": "Physical", "FQDN": null, "FullDuplex": true, "HostName": null, "IPv4Addresses": [], "IPv6AddressPolicyTable": [], "IPv6Addresses": [], "IPv6DefaultGateway": null, "IPv6StaticAddresses": [], "Id": "NIC.Embedded.1-1-1", "InterfaceEnabled": true, "LinkStatus": "LinkUp", "Links": {"Chassis": {}}, "MACAddress": "AB:CD:EF:GH:IJ:02", "MTUSize": null, "MaxIPv6StaticAddresses": null, "Name": "System Ethernet Interface", "NameServers": [], "PermanentMACAddress": "AB:CD:EF:GH:IJ:02", "SpeedMbps": 1000, "Status": {"Health": "OK", "State": "Enabled"}, "UefiDevicePath": "PciRoot(0x0)/Pci(0x1C,0x5)/Pci(0x0,0x0)", "VLAN": {}}, {"AutoNeg": false, "Description": "Embedded NIC 1 Port 2 Partition 1", "EthernetInterfaceType": "Physical", "FQDN": null, "FullDuplex": false, "HostName": null, "IPv4Addresses": [], "IPv6AddressPolicyTable": [], "IPv6Addresses": [], "IPv6DefaultGateway": null, "IPv6StaticAddresses": [], "Id": "NIC.Embedded.2-1-1", "InterfaceEnabled": true, "LinkStatus": "LinkDown", "Links": {"Chassis": {}}, "MACAddress": "AB:CD:EF:GH:IJ:02", "MTUSize": null, "MaxIPv6StaticAddresses": null, "Name": "System Ethernet Interface", "NameServers": [], "PermanentMACAddress": "AB:CD:EF:GH:IJ:02", "SpeedMbps": 0, "Status": {"Health": "OK", "State": "Enabled"}, "UefiDevicePath": "PciRoot(0x0)/Pci(0x1C,0x5)/Pci(0x0,0x1)", "VLAN": {}}]</td>
    <td>Response facts details for nic.</td>
    </tr>
    <tr>
    <td>memory</td>
    <td>[{"AllowedSpeedsMHz": [3200], "Assembly": {}, "BaseModuleType": "RDIMM", "BusWidthBits": 72, "CacheSizeMiB": 0, "CapacityMiB": 8192, "DataWidthBits": 64, "Description": "DIMM A1", "DeviceLocator": "DIMM A1", "Enabled": true, "ErrorCorrection": "MultiBitECC", "FirmwareRevision": null, "Id": "DIMM.Socket.A1", "Links": {"Chassis": {}, "Oem": {"Dell": {"CPUAffinity": []}}, "Processors": []}, "LogicalSizeMiB": 0, "Manufacturer": "Hynix Semiconductor", "MaxTDPMilliWatts": [], "MemoryDeviceType": "DDR4", "MemorySubsystemControllerManufacturerID": null, "MemorySubsystemControllerProductID": null, "MemoryType": "DRAM", "Metrics": {}, "ModuleManufacturerID": "0xad80", "ModuleProductID": null, "Name": "DIMM A1", "NonVolatileSizeMiB": 0, "Oem": {"Dell": {"DellMemory": {"BankLabel": "A", "Id": "DIMM.Socket.A1", "LastSystemInventoryTime": "2023-01-31T12:00:45+00:00", "LastUpdateTime": "2021-02-11T21:30:07+00:00", "ManufactureDate": "Mon May 04 07:00:00 2020 UTC", "MemoryTechnology": "DRAM", "Model": "DDR4 DIMM", "Name": "DellMemory", "RemainingRatedWriteEndurancePercent": null, "SystemEraseCapability": "NotSupported"}}}, "OperatingMemoryModes": ["Volatile"], "OperatingSpeedMhz": 2666, "PartNumber": "PARTNUM-XN", "RankCount": 1, "SerialNumber": "SERIAL1", "Status": {"Health": "OK", "State": "Enabled"}, "VolatileSizeMiB": 8192}]</td>
    <td>Response facts details for memory.</td>
    </tr>
    <tr>
    <td>backplane</td>
    <td>[{"Description": "An instance of DellPCIeSSDBackPlane will have PCIeSSD back plane specific data.", "FirmwareVersion": "3.72", "Id": "Enclosure.Internal.0-2", "Name": "DellPCIeSSDBackPlane", "PCIExpressGeneration": "Gen 4", "SlotCount": 8, "WiredOrder": 2}]</td>
    <td>Response facts details for backplane.</td>
    </tr>
    <tr>
    <td>power_supply</td>
    <td>[{"Assembly": {}, "Description": "An instance of PowerSupply", "FirmwareVersion": "00.17.28", "HotPluggable": true, "Id": "PSU.Slot.1", "InputNominalVoltageType": "AC240V", "InputRanges": [{"CapacityWatts": 1400.0, "NominalVoltageType": "AC240V"}], "LineInputStatus": "Normal", "Manufacturer": "DELL", "Metrics": {}, "Model": "PWR SPLY,1400W,RDNT,LTON", "Name": "PS1 Status", "Oem": {"Dell": {"DellPowerSupply": {"ActiveInputVoltage": "Unknown", "IsSwitchingSupply": true, "OperationalStatus": ["OK"], "RequestedState": "NotApplicable"}, "DellPowerSupplyView": {"DetailedState": "Presence Detected", "DeviceDescription": "Power Supply 1", "LastSystemInventoryTime": "2023-01-31T12:00:45+00:00", "LastUpdateTime": "2023-03-09T15:58:41+00:00", "PMBusMonitoring": "Capable", "Range1MaxInputPowerWatts": 1568, "RedMinNumberNeeded": 1, "RedTypeOfSet": ["N+1", "Sparing"], "RedundancyStatus": "Unknown"}}}, "PartNumber": "SPARE2", "PowerCapacityWatts": 1400.0, "PowerSupplyType": "AC", "SerialNumber": "ABCD1", "SparePartNumber": "SPARE1", "Status": {"Health": "OK", "State": "Enabled"}}]</td>
    <td>Response facts details for power_supply.</td>
    </tr>
    <tr>
    <td>presence_and_status_sensor</td>
    <td>[{"CurrentState": "Present", "Description": "An instance of DellPresenceAndStatusSensor will have presence and status sensor specific data.", "DeviceID": "iDRAC.Embedded.1#VFLASHSD", "ElementName": "VFLASH SD", "Id": "iDRAC.Embedded.1_0x23_VFLASHSD", "Name": "DellPresenceAndStatusSensor", "SensorType": "Other"}]</td>
    <td>Response facts details for presence_and_status_sensor.</td>
    </tr>
    <tr>
    <td>sensor_battery</td>
    <td>{"CurrentState": "Good", "Description": "An instance of DellSensor will represent a sensor, a hardware device that is capable of measuring the characteristics of a physical property.", "ElementName": "System Board CMOS Battery", "EnabledState": "Enabled", "HealthState": "OK", "Id": "iDRAC.Embedded.1_0x23_SystemBoardCMOSBattery", "Links": {"ComputerSystem": {}}, "Name": "DellSensor", "SensorType": "Other"}</td>
    <td>Response facts details for sensor_battery.</td>
    </tr>
    <tr>
    <td>intrusion_sensor</td>
    <td>{"PhysicalSecurity": {"IntrusionSensor": "Normal"}}</td>
    <td>Response facts details for intrusion_sensor.</td>
    </tr>
    <tr>
    <td>virtual_disk</td>
    <td>[{"@Redfish.Settings": {"SettingsObject": {}, "SupportedApplyTimes": ["Immediate", "OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}, "BlockSizeBytes": 512, "CapacityBytes": 240057409536, "Description": "Disk 0 on Integrated AHCI controller 1", "DisplayName": null, "Encrypted": null, "EncryptionTypes": [], "Id": "Disk.Direct.0-0:AHCI.Integrated.1-1", "Identifiers": [], "MediaSpanCount": null, "Name": "SSD 0", "Operations": [], "OptimumIOSizeBytes": null, "RAIDType": null, "ReadCachePolicy": null, "Status": {"Health": "OK", "HealthRollup": "OK", "State": "Enabled"}, "VolumeType": "RawDevice", "WriteCachePolicy": null}, {"@Redfish.Settings": {"SettingsObject": {}, "SupportedApplyTimes": ["Immediate", "OnReset", "AtMaintenanceWindowStart", "InMaintenanceWindowOnReset"]}, "BlockSizeBytes": 512, "CapacityBytes": 240057409536, "Description": "Disk 1 on Integrated AHCI controller 1", "DisplayName": null, "Encrypted": null, "EncryptionTypes": [], "Id": "Disk.Direct.1-1:AHCI.Integrated.1-1", "Identifiers": [], "MediaSpanCount": null, "Name": "SSD 1", "Operations": [], "OptimumIOSizeBytes": null, "RAIDType": null, "ReadCachePolicy": null, "Status": {"Health": "OK", "HealthRollup": "OK", "State": "Enabled"}, "VolumeType": "RawDevice", "WriteCachePolicy": null}]</td>
    <td>Response facts details for virtual_disk.</td>
    </tr>
    <tr>
    <td>pcie_device</td>
    <td>
    {"AssetTag": null, "Description": "Integrated Matrox G200eW3 Graphics Controller", "DeviceType": "SingleFunction", "FirmwareVersion": "", "Id": "3-0", "Manufacturer": "Matrox Electronics Systems Ltd.", "Model": null, "Name": "Integrated Matrox G200eW3 Graphics Controller", "PCIeFunctions": {}, "PartNumber": null, "SKU": null, "SerialNumber": null, "Status": {"Health": "OK", "HealthRollup": "OK", "State": "Enabled"}}, {"AssetTag": null, "Description": "PERC H730P MX", "DeviceType": "SingleFunction", "FirmwareVersion": "25.5.9.0001", "Id": "59-0", "Manufacturer": "Broadcom / LSI", "Model": null, "Name": "PERC H730P MX", "PCIeFunctions": {}, "PartNumber": "PART2", "SKU": null, "SerialNumber": "SERIALN1", "Status": {"Health": "OK", "HealthRollup": "OK", "State": "Enabled"}
    }</td>
    <td>Response facts details for pcie_device.</td>
    </tr>
    <tr>
    <td>physical_disk</td>
    <td>[{"BlockSizeBytes": 512, "CapableSpeedGbs": 6, "CapacityBytes": 240057409536, "Description": "Disk 1 on Integrated AHCI controller 1", "EncryptionAbility": "None", "EncryptionStatus": "Unencrypted", "FailurePredicted": false, "HotspareType": "None", "Id": "Disk.Direct.1-1:AHCI.Integrated.1-1", "Identifiers": [{"DurableName": null, "DurableNameFormat": null}], "Identifiers@odata.count": 1, "Location": [], "LocationIndicatorActive": null, "Manufacturer": "INTEL", "MediaType": "SSD", "Model": "SSDMODEL1", "Name": "SSD 1", "NegotiatedSpeedGbs": 6, "Oem": {"Dell": {"DellPhysicalDisk": {"AvailableSparePercent": null, "Certified": "NotApplicable", "Connector": 0, "CryptographicEraseCapable": "Capable", "Description": "An instance of DellPhysicalDisk will have Physical Disk specific data.", "DeviceProtocol": null, "DeviceSidebandProtocol": null, "DriveFormFactor": "M.2", "EncryptionProtocol": "None", "ErrorDescription": null, "ErrorRecoverable": "NotApplicable", "ForeignKeyIdentifier": null, "FreeSizeInBytes": 240057409536, "Id": "Disk.Direct.1-1:AHCI.Integrated.1-1", "LastSystemInventoryTime": "2023-03-04T05:50:09+00:00", "LastUpdateTime": "2023-02-15T16:32:30+00:00", "ManufacturingDay": 0, "ManufacturingWeek": 0, "ManufacturingYear": 0, "Name": "DellPhysicalDisk", "NonRAIDDiskCachePolicy": "Unknown", "OperationName": "None", "OperationPercentCompletePercent": 0, "PCIeCapableLinkWidth": "None", "PCIeNegotiatedLinkWidth": "None", "PPID": "TW-0919J9-PIHIT-8AB-02K7-A00", "PowerStatus": "On", "PredictiveFailureState": "SmartAlertAbsent", "ProductID": null, "RAIDType": "Unknown", "RaidStatus": "NonRAID", "SASAddress": "Not Applicable", "Slot": 1, "SystemEraseCapability": "CryptographicErasePD", "T10PICapability": "NotSupported", "UsedSizeInBytes": 0, "WWN": "Not Applicable"}}}, "Operations": [], "PartNumber": "TW-0919J9-PIHIT-8AB-02K7-A00", "PhysicalLocation": {"PartLocation": {"LocationOrdinalValue": 1, "LocationType": "Slot"}}, "PredictedMediaLifeLeftPercent": 100, "Protocol": "SATA", "Revision": "N201DL43", "RotationSpeedRPM": null, "SerialNumber": "SERIAL2", "Status": {"Health": "OK", "HealthRollup": "OK", "State": "Enabled"}, "WriteCacheEnabled": false}]</td>
    <td>Response facts details for physical_disk.</td>
    </tr>
    <tr>
    <td>secure_boot</td>
    <td>{
            "Actions": {
                "#SecureBoot.ResetKeys": {
                    "ResetKeysType@Redfish.AllowableValues": [
                        "ResetAllKeysToDefault",
                        "DeleteAllKeys",
                        "DeletePK",
                        "ResetPK",
                        "ResetKEK",
                        "ResetDB",
                        "ResetDBX"
                    ],
                    "target": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/Actions/SecureBoot.ResetKeys"
                },
                "Oem": {}
            },
            "Description": "UEFI Secure Boot",
            "Id": "SecureBoot",
            "Name": "UEFI Secure Boot",
            "Oem": {
                "Dell": {
                    "Certificates": {},
                    "FirmwareImageHashes": {}
                }
            },
            "SecureBootCurrentBoot": "Disabled",
            "SecureBootDatabases": [
                {
                    "Actions": {
                        "#SecureBootDatabase.ResetKeys": {
                            "ResetKeysType@Redfish.AllowableValues": [
                                "ResetAllKeysToDefault",
                                "DeleteAllKeys"
                            ],
                            "target": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/db/Actions/SecureBootDatabase.ResetKeys"
                        }
                    },
                    "Certificates": [
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.3",
                            "Issuer": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Corporation Third Party Marketplace Root",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "SERIAL00001",
                            "Subject": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Corporation UEFI CA 2011",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "ValidNotAfter": "2026-6-27T21:32:45+00:00",
                            "ValidNotBefore": "2011-6-27T21:22:45+00:00"
                        },
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.4",
                            "Issuer": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Root Certificate Authority 2010",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "SERIAL000002",
                            "Subject": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Windows Production PCA 2011",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "ValidNotAfter": "2026-10-19T18:51:42+00:00",
                            "ValidNotBefore": "2011-10-19T18:41:42+00:00"
                        },
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.5",
                            "Issuer": {
                                "City": "Palo Alto",
                                "Country": "US",
                                "Organization": "VMware, Inc.",
                                "State": "California"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "SERIAL3",
                            "Subject": {
                                "City": "Palo Alto",
                                "Country": "US",
                                "Organization": "VMware, Inc.",
                                "State": "California"
                            },
                            "ValidNotAfter": "2019-12-31T17:16:05+00:00",
                            "ValidNotBefore": "2008-10-16T17:16:05+00:00"
                        },
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.6",
                            "Issuer": {
                                "City": "Palo Alto",
                                "CommonName": "VMware Secure Boot Signing",
                                "Country": "US",
                                "Organization": "VMware, Inc.",
                                "State": "California"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "SERIAL00005",
                            "Subject": {
                                "City": "Palo Alto",
                                "CommonName": "VMware Secure Boot Signing",
                                "Country": "US",
                                "Organization": "VMware, Inc.",
                                "State": "California"
                            },
                            "ValidNotAfter": "2037-10-19T06:47:59+00:00",
                            "ValidNotBefore": "2017-10-24T06:47:59+00:00"
                        }
                    ],
                    "DatabaseId": "db",
                    "Description": "SecureBootDatabase",
                    "Id": "db",
                    "Name": "SecureBootDatabase",
                    "Signatures": {}
                },
                {
                    "Actions": {
                        "#SecureBootDatabase.ResetKeys": {
                            "ResetKeysType@Redfish.AllowableValues": [
                                "ResetAllKeysToDefault",
                                "DeleteAllKeys"
                            ],
                            "target": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/dbx/Actions/SecureBootDatabase.ResetKeys"
                        }
                    },
                    "Certificates": [],
                    "DatabaseId": "dbx",
                    "Description": "SecureBootDatabase",
                    "Id": "dbx",
                    "Name": "SecureBootDatabase",
                    "Signatures": {}
                },
                {
                    "Actions": {
                        "#SecureBootDatabase.ResetKeys": {
                            "ResetKeysType@Redfish.AllowableValues": [
                                "ResetAllKeysToDefault",
                                "DeleteAllKeys"
                            ],
                            "target": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/KEK/Actions/SecureBootDatabase.ResetKeys"
                        }
                    },
                    "Certificates": [
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.2",
                            "Issuer": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Corporation Third Party Marketplace Root",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "SERIAL000005",
                            "Subject": {
                                "City": "Redmond",
                                "CommonName": "Microsoft Corporation KEK CA 2011",
                                "Country": "US",
                                "Organization": "Microsoft Corporation",
                                "State": "Washington"
                            },
                            "ValidNotAfter": "2022-6-24T20:51:29+00:00",
                            "ValidNotBefore": "2011-6-24T20:41:29+00:00"
                        }
                    ],
                    "DatabaseId": "KEK",
                    "Description": "SecureBootDatabase",
                    "Id": "KEK",
                    "Name": "SecureBootDatabase",
                    "Signatures": {}
                },
                {
                    "Actions": {
                        "#SecureBootDatabase.ResetKeys": {
                            "ResetKeysType@Redfish.AllowableValues": [
                                "ResetAllKeysToDefault",
                                "DeleteAllKeys"
                            ],
                            "target": "/redfish/v1/Systems/System.Embedded.1/SecureBoot/SecureBootDatabases/PK/Actions/SecureBootDatabase.ResetKeys"
                        }
                    },
                    "Certificates": [
                        {
                            "CertificateString": null,
                            "CertificateType": "PEM",
                            "CertificateUsageTypes": [
                                "BIOS"
                            ],
                            "Description": "SecureBoot Certificate",
                            "Id": "StdSecbootpolicy.1",
                            "Issuer": {
                                "City": "Round Rock",
                                "CommonName": "Dell Inc. Platform Key",
                                "Country": "US",
                                "Organization": "Dell Inc.",
                                "State": "Texas"
                            },
                            "Name": "SecureBoot Certificate",
                            "SerialNumber": "12345ABCD",
                            "Subject": {
                                "City": "Round Rock",
                                "CommonName": "Dell Inc. Platform Key",
                                "Country": "US",
                                "Organization": "Dell Inc.",
                                "State": "Texas"
                            },
                            "ValidNotAfter": "2021-2-2T17:27:36+00:00",
                            "ValidNotBefore": "2016-2-2T17:17:37+00:00"
                        }
                    ],
                    "DatabaseId": "PK",
                    "Description": "SecureBootDatabase",
                    "Id": "PK",
                    "Name": "SecureBootDatabase",
                    "Signatures": {}
                }
            ],
            "SecureBootEnable": false,
            "SecureBootMode": "DeployedMode"
        }</td>
    <td>Response facts details for Secure Boot.</td>
    </tr>
</tbody>
</table>

## Examples
-----
```
- name: iDRAC gather facts for System, BIOS, Controller, CPU, Enclosure.
  ansible.builtin.import_role:
    name: idrac_gather_facts
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target:
      - System
      - BIOS
      - Controller
      - CPU
      - Enclosure

- name: Print the System details
  ansible.builtin.debug:
    var: system

```
```
# Get specific controllers
- name: Get all controllers
  ansible.builtin.import_role:
    name: idrac_gather_facts
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target:
      - Controller

- name: Fetch BOSS controllers
  ansible.builtin.debug:
    msg: "{{ controller | selectattr('Model', 'contains', 'BOSS') | list }}"

- name: Fetch controller with specific id
  ansible.builtin.debug:
    msg: "{{ controller | selectattr('Id', 'equalto', 'AHCI.Integrated.1-1') | list }}"

```
```
- name: iDRAC gather facts for EnclosureEMM, Fan, Firmware, HostNIC, License.
  ansible.builtin.import_role:
    name: idrac_gather_facts
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target:
      - EnclosureEMM
      - Fan
      - Firmware
      - HostNIC
      - License

- name: Print the firmware details
  ansible.builtin.debug:
    var: firmware

```
```
- name: iDRAC gather facts for Memory, NIC, PCIeSSDBackPlane, PowerSupply, PresenceAndStatusSensor, SecureBoot.
  ansible.builtin.import_role:
    name: idrac_gather_facts
  vars:
    hostname: "192.1.2.1"
    username: "username"
    password: "password"
    ca_path: "/path/to/ca_cert.pem"
    target:
      - Memory
      - NIC
      - PCIeSSDBackPlane
      - PowerSupply
      - PresenceAndStatusSensor
      - SecureBoot

- name: Print the secure boot details
  ansible.builtin.debug:
    var: secure_boot
```
```
- name: iDRAC gather facts for Sensors_Battery, Sensors_Intrusion, Sensors_Voltage, VirtualDisk, PCIeDevice, PhysicalDisk, SystemMetrics using environment variables IDRAC_USERNAME and IDRAC_PASSWORD.
  ansible.builtin.import_role:
    name: idrac_gather_facts
  vars:
    hostname: "192.1.2.1"
    # IDRAC_USERNAME and IDRAC_PASSWORD set in env
    ca_path: "/path/to/ca_cert.pem"
    target:
      - Sensors_Battery
      - Sensors_Intrusion
      - Sensors_Voltage
      - VirtualDisk
      - PCIeDevice
      - PhysicalDisk
      - SystemMetrics

- name: Print the system metrics
  ansible.builtin.debug:
    var: system_metrics
```
## Author Information
------------------

Dell Technologies <br>
Felix Stephen A (felix.s@dell.com) <br>
Jagadeesh N V (jagadeesh.n.v@dell.com)
