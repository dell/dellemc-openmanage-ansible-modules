import sys
import json
import ast

video_api_output = sys.argv[1]
NA = "Not Available"


def map_video_data(video):
    video_info = video.get("Oem", {}).get("Dell", {}).get("DellVideo", {})

    return {
        "Description": video_info.get("Description", NA),
        "DeviceDescription": video_info.get("DeviceDescription", NA),
        "FQDD": video_info.get("FQDD", NA),
        "Key": video_info.get("Key", NA),
        "Manufacturer": video_info.get("Manufacturer", NA),
    }


video_data = ast.literal_eval(video_api_output)
video_data = json.loads(video_data)

output = [map_video_data(video) for video in video_data.get("Members", [])]

print(json.dumps(output, ensure_ascii=False))
