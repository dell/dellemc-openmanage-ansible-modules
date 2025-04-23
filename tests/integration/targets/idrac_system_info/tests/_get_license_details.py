import sys
import json

get_license_details = sys.argv[1]
NA = "Not Available"


def get_license_info_api(license_details):
    license_output = []
    members = json.loads(license_details).get("Members")
    for each in members:
        output = {
            "InstanceID": each.get("Id", NA),
            "Key": each.get("Id", NA),
            "LicenseType": each.get("LicenseType", NA),
            "LicenseSoldDate": each.get("LicenseSoldDate", NA),
            "LicenseDescription": each.get("LicenseDescription", [NA])[0],
            "LicenseInstallDate": each.get("LicenseInstallDate", NA),
        }
        if each.get("LicensePrimaryStatus") == "OK":
            output["PrimaryStatus"] = "Healthy"
        else:
            output["PrimaryStatus"] = each.get("LicensePrimaryStatus", NA)
        license_output.append(output)
    return license_output


print(get_license_info_api(get_license_details))
