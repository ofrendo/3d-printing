# Postprocessing script to send GCode as file to Ender 3 V3 KE
# Input: IP address

from ..Script import Script
from UM.Logger import Logger
from UM.Message import Message
import requests
from cura.CuraApplication import CuraApplication
import re

class SendToEnder3V3KE(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Send GCode to Ender 3 V3 KE",
            "key": "SendToEnder3V3KE",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "ipAddress":
                {
                    "label": "IP Address",
                    "description": "IP Address of the Ender 3 V3 KE",
                    "type": "str",
                    "default_value": "192.168.1.1"
                }
            }
        }"""

    def get_file_name_from_gcode(self, file_contents: str) -> str:
        # Search for the following in the gcode:
        # ;MESH:my-file-name.stl
        # Goal: Extract "my-file-name"
        pattern = r'(?<=MESH:)[\w\s-]+(?=\.stl)'
        file_name: str = re.search(pattern, file_contents)
        if file_name is not None:
            extracted_string = file_name.group(0)
            return extracted_string
        else:
            raise Exception("Unable to find file name in gcode file contents")

    def execute(self, data):
        Message("Starting send to Ender 3 V3 KE...").show()

        ip_address: str = self.getSettingValueByKey("ipAddress")
        file_contents: str = ""
        for layer in data:
            file_contents += layer
        try:
            file_name: str = self.get_file_name_from_gcode(file_contents) + ".gcode"
            url: str = "http://" + ip_address + "/upload/" + file_name

            Message("Uploading file to '" + url + "'...").show()
            response = requests.post(url, files=[
                ("file", (file_name, file_contents, "application/octet-stream"))
            ])
            if response.status_code == 200:
                Message("GCode successfully uploaded.").show()
            else:
                Message("There was an error uploading GCode to " + url + ", status code=" + response.status_code + ": " + str(response)).show()

        except Exception as e:
            Message("Exception caught: " + str(e)).show()

        Message("Finished script for sending to Ender 3 V3 KE.").show()
        return data
