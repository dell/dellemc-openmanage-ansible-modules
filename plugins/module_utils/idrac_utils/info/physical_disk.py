# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.12.0
# Copyright (C) 2025 Dell Inc. or its subsidiaries. All Rights Reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.

#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

GET_IDRAC_STORAGE_DETAILS_URI_10 = "/redfish/v1/Systems/System.Embedded.1/Storage"
NA = "Not Available"


class IDRACPhysicalDiskInfo(object):
    def __init__(self, idrac):
        self.idrac = idrac

    def physical_disk_mapped_data(self, disk):
        physical_disk_data = disk.get("Oem", {}).get("Dell", {}).get("DellPhysicalDisk", {})
        output = {
            "BlockSize": str(disk.get("BlockSizeBytes", NA)),
            "BusProtocol": NA,
            "DeviceDescription": str(disk.get("Description", NA)),
            "DriveFormFactor": str(physical_disk_data.get("DriveFormFactor", NA)),
            "FQDD": str(disk.get("Id", NA)),
            "FreeSize": str(physical_disk_data.get("FreeSizeInBytes", NA)),
            "HotSpareStatus": NA,
            "Key": str(disk.get("Id", NA)),
            "Manufacturer": str(disk.get("Manufacturer", NA)),
            "ManufacturingDay": str(physical_disk_data.get("ManufacturingDay", NA)),
            "ManufacturingWeek": str(physical_disk_data.get("ManufacturingWeek", NA)),
            "ManufacturingYear": str(physical_disk_data.get("ManufacturingYear", NA)),
            "MaxCapableSpeed": str(disk.get("CapableSpeedGbs", NA)) + " Gbps",
            "MediaType": str(disk.get("MediaType", NA)),
            "Model": str(disk.get("Model", NA)),
            "PPID": str(physical_disk_data.get("PPID", NA)),
            "PredictiveFailureState": str(physical_disk_data.get("PredictiveFailureState", NA)),
            "PrimaryStatus": NA,
            "RAIDNegotiatedSpeed": str(disk.get("RotationSpeedRPM", NA)),
            "RaidStatus": str(physical_disk_data.get("RaidStatus", NA)),
            "RemainingRatedWriteEndurance": NA,
            "Revision": str(disk.get("Revision", NA)),
            "SASAddress": str(physical_disk_data.get("SASAddress", NA)),
            "SecurityState": NA,
            "SerialNumber": str(disk.get("SerialNumber", NA)),
            "Size": NA,
            "Slot": str(physical_disk_data.get("Slot", NA)),
            "SupportedEncryptionTypes": NA,
            "T10PICapability": str(physical_disk_data.get("T10PICapability", NA)),
            "UsedSize": str(physical_disk_data.get("UsedSizeInBytes", NA)),
        }
        return output

    def get_physical_disk_info(self):
        output = []
        # Get storage collection
        response = self.idrac.invoke_request(method='GET', uri=GET_IDRAC_STORAGE_DETAILS_URI_10)
        members = response.json_data.get("Members", [])

        for member in members:
            storage_uri = member.get("@odata.id")
            if not storage_uri:
                continue

            # Get storage entity details (RAID controller)
            storage_resp = self.idrac.invoke_request(method='GET', uri=storage_uri)
            if storage_resp.status_code != 200:
                continue

            drives = storage_resp.json_data.get("Drives", [])
            for drive in drives:
                drive_uri = drive.get("@odata.id")
                if not drive_uri:
                    continue

                drive_resp = self.idrac.invoke_request(method='GET', uri=drive_uri)
                if drive_resp.status_code == 200:
                    output.append(self.physical_disk_mapped_data(drive_resp.json_data))

        return output
