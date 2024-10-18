# -*- coding: utf-8 -*-

# Dell OpenManage Ansible Modules
# Version 9.8.0
# Copyright (C) 2024 Dell Inc. or its subsidiaries. All Rights Reserved.

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


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

XML_EXT = ".xml"
GZ_EXT = ".gz"
XML_GZ_EXT = ".xml.gz"
HTTP_PATH = "http"
HTTPS_PATH = "https://"
PROFILE_URI = "/RepositoryProfiles"
TEST_CONNECTION_URI = "/RepositoryProfiles/TestConnection"


class OMEVVFirmwareProfile:
    def __init__(self, omevv):
        self.omevv = omevv

    def get_create_payload_details(self, name, catalog_path, description, protocol_type, share_username, share_password, share_domain):
        payload = {}
        payload["profileName"] = name
        payload["protocolType"] = protocol_type
        payload["sharePath"] = catalog_path
        if description is None:
            payload["description"] = ""
        else:
            payload["description"] = description
        payload["profileType"] = "Firmware"
        payload["shareCredential"] = {
            "username": share_username,
            "password": share_password,
            "domain": share_domain
        }
        return payload

    def get_modify_payload_details(self, name, catalog_path, description, share_username, share_password, share_domain):
        payload = {}
        payload["profileName"] = name
        payload["sharePath"] = catalog_path
        if description is None:
            payload["description"] = ""
        else:
            payload["description"] = description
        payload["profileType"] = "Firmware"
        payload["shareCredential"] = {
            "username": share_username,
            "password": share_password,
            "domain": share_domain
        }
        return payload

    def form_conn_payload(self, protocol_type, catalog_path, share_username, share_password, share_domain):
        payload = {}
        payload["protocolType"] = protocol_type
        payload["catalogPath"] = catalog_path
        payload["shareCredential"] = {
            "username": share_username if share_username is not None else "",
            "password": share_password if share_password is not None else "",
            "domain": share_domain if share_domain is not None else ""
        }
        payload["checkCertificate"] = False
        return payload

    def search_profile_name(self, data, profile_name):
        """
        Searches for a profile with the given name in the provided data.

        Args:
            data (list): A list of dictionaries representing profiles.
            profile_name (str): The name of the profile to search for.

        Returns:
            dict: The dictionary representing the profile if found, or an empty dictionary if not found.
        """
        for d in data:
            if d.get('profileName') == profile_name:
                return d
        return {}

    def validate_catalog_path(self, protocol_type, catalog_path):
        """
        Validates the catalog path based on the protocol type.

        Args:
            protocol_type (str): The type of protocol used for the catalog path.
            catalog_path (str): The path to the catalog.

        Raises:
            SystemExit: If the catalog path is invalid.

        Returns:
            None
        """
        protocol_mapping = {
            'CIFS': (lambda path: path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)),
            'NFS': (lambda path: path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)),
            'HTTP': (lambda path: path.startswith(HTTP_PATH) and (path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT))),
            "HTTPS": (lambda path: path.startswith(HTTPS_PATH) and (path.endswith(XML_EXT) or path.endswith(GZ_EXT) or path.endswith(XML_GZ_EXT)))
        }
        validator = protocol_mapping.get(protocol_type)
        if validator is None:
            self.module.exit_json(msg="Invalid catalog_path", failed=True)
        if not validator(catalog_path):
            self.module.exit_json(msg="Invalid catalog_path", failed=True)

    def test_connection(self, protocol_type, catalog_path, share_username, share_password, share_domain):
        """
        Tests the connection to the vCenter server.

        """
        payload = self.form_conn_payload(
            protocol_type, catalog_path, share_username, share_password, share_domain)
        resp = self.omevv.invoke_request("POST", TEST_CONNECTION_URI, payload)
        return resp

    def get_firmware_repository_profile(self):
        """
        Retrieves all firmware repository profile Information.

        """
        resp = self.omevv.invoke_request("GET", PROFILE_URI)
        return resp

    def get_firmware_repository_profile_by_id(self, profile_id):
        """
        Retrieves all firmware repository profile Information.

        """
        resp = self.omevv.invoke_request(
            "GET", PROFILE_URI + "/" + str(profile_id))
        return resp

    def create_firmware_repository_profile(self, name, catalog_path,
                                           description, protocol_type,
                                           share_username, share_password,
                                           share_domain):
        err_msg = None
        if name is None:
            err_msg = ""

        payload = self.get_create_payload_details(name, catalog_path,
                                                  description, protocol_type,
                                                  share_username, share_password,
                                                  share_domain)
        resp = self.omevv.invoke_request("POST", PROFILE_URI, payload)
        return resp, err_msg

    def modify_firmware_repository_profile(self, profile_id, name, catalog_path,
                                           description,
                                           share_username, share_password,
                                           share_domain):
        """
        Modifies a firmware repository profile.

        """
        err_msg = None
        if name is None:
            err_msg = ""
        payload = self.get_modify_payload_details(name, catalog_path,
                                                  description,
                                                  share_username, share_password,
                                                  share_domain)
        resp = self.omevv.invoke_request(
            "PUT", PROFILE_URI + "/" + str(profile_id), payload)
        return resp, err_msg

    def delete_firmware_repository_profile(self, profile_id):
        """
        Deletes a firmware repository profile.

        """
        resp = self.omevv.invoke_request(
            "DELETE", PROFILE_URI + "/" + str(profile_id))
        return resp
