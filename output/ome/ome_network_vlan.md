Create a VLAN:
{
    "changed": true,
    "msg": "Successfully created the VLAN.",
    "vlan_status": {
        "CreatedBy": "admin",
        "CreationTime": null,
        "Description": null,
        "Id": 1234,
        "InternalRefNWUUId": "6d6effcc-eca4-44bd-be07-1234ab5cd67e",
        "Name": "vlan1",
        "Type": 1,
        "UpdatedBy": null,
        "UpdatedTime": "2020-01-01 07:18:45.641",
        "VlanMaximum": 40,
        "VlanMinimum": 35
    }

Modify a VLAN:
    {
    "changed": true,
    "msg": "Successfully updated the VLAN.",
    "vlan_status": {
        "Id": 1234,
        "Name": "vlan1",
        "Description": "VLAN description",
        "VlanMaximum": 130,
        "VlanMinimum": 140,
        "Type": 1,
        "CreatedBy": "admin",
        "CreationTime": "2020-01-01 05:54:36.113",
        "UpdatedBy": null,
        "UpdatedTime": "2020-01-01 05:54:36.113",
        "InternalRefNWUUId": "6d6effcc-eca4-44bd-be07-1234ab5cd67e"
    }
	
Delete a VLAN:
{
    "changed": true,
    "msg": "Successfully deleted the VLAN."
}