import sys
import json

controller_sensor_api_output = sys.argv[1]
NA = "Not Available"


def get_controller_data(resp):
    output = {
        "FQDD": resp.get("@odata.id", "").rstrip("/").rsplit("/", 1)[-1],
        "Key": resp.get("@odata.id", "").rstrip("/").rsplit("/", 1)[-1]
    }
    return output


output = []
controller_sensor_output = json.loads(controller_sensor_api_output)
for each_member in controller_sensor_output.get("Members", []):
    output.append(get_controller_data(each_member))
print(output)
