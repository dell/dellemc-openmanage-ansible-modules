import sys
import json

controller_sensor_api_output = sys.argv[1]
NA = "Not Available"


def controller_sensor_mapped_data(resp):
    output = {
        "FQDD": resp.get("@odata.id", "").rstrip("/").rsplit("/", 1)[-1],
        "Key": resp.get("@odata.id", "").rstrip("/").rsplit("/", 1)[-1]
    }
    return output


def get_controller_sensor_info(api_output):
    output = []
    controller_sensor_output = json.loads(api_output)
    for member in controller_sensor_output.get("Members", []):
        output.append(controller_sensor_mapped_data(member))
    return output


if __name__ == "__main__":
    result = get_controller_sensor_info(controller_sensor_api_output)
    print(json.dumps(result, indent=2))
