from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.info.lifecycle_controller_status \
    import IDRACLifecycleControllerStatusInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock


MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
MANAGER_RESPONSE = {
    "Members": [
        {
            "@odata.id": MANAGER_URI
        }
    ]
}


class TestIDRACLifecycleControllerStatusInfo(TestUtils):
    def test_get_lifecycle_controller_info(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        lc_info.get_lifecycle_controller_status_api = MagicMock(
            return_value="/api"
        )
        state = "Ready"
        response = {
            "LCStatus": "Ready"
        }
        idrac_mock.invoke_request.return_value.json_data = response
        result = lc_info.get_lifecycle_controller_status_info()
        assert result == state

    def test_get_lifecycle_controller_info_empty(self, idrac_mock):
        response = {}
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        lc_info.get_lifecycle_controller_status_api = MagicMock(
            return_value="/api"
        )
        idrac_mock.invoke_request.return_value.status_code = 400
        idrac_mock.invoke_request.return_value.json_data = response
        result = lc_info.get_lifecycle_controller_status_info()
        assert result == ""

    def test_get_lifecycle_controller_status_api(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        lc_info._get_controller_status_baseuri_response = MagicMock(return_value=MANAGER_RESPONSE)
        lc_info._get_manager_uri = MagicMock(return_value="/manager_uri")
        lc_info._get_manager_response = MagicMock(return_value="mangerresponse")
        lc_info._get_lc_service_uri = MagicMock(return_value="lc_status_uri")
        lc_info._get_lc_service_response = MagicMock(return_value="lc_service_response")
        lc_info._get_lc_status_check_uri = MagicMock(return_value="lc_check_uri")
        result = lc_info.get_lifecycle_controller_status_api()
        assert result == "lc_check_uri"

    def test_get_lifecycle_controller_status_api_empty_response(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        lc_info._get_controller_status_baseuri_response = MagicMock(return_value=MANAGER_RESPONSE)
        lc_info._get_manager_uri = MagicMock(return_value="")
        result = lc_info.get_lifecycle_controller_status_api()
        assert result == ""

    def test_get_controller_status_baseuri_response(self, idrac_mock):
        response = "api"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        result = lc_info._get_controller_status_baseuri_response()
        assert result == response

    def test_get_manager_response(self, idrac_mock):
        response = "manager_response"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        result = lc_info._get_manager_response("manager_api")
        assert result == response

    def test_get_lc_service_response(self, idrac_mock):
        response = "lc_service_response"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        result = lc_info._get_lc_service_response("lc_service_api")
        assert result == response

    def test_get_manager_uri(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        response_obj = MagicMock()
        response_obj.json_data = MANAGER_RESPONSE
        result = lc_info._get_manager_uri(response_obj)
        assert result == MANAGER_URI

    def test_get_lc_service_uri(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        lc_api = "lc_api"
        response = {
            "Links": {
                "Oem": {
                    "Dell": {
                        "DellLCService": {
                            "@odata.id": lc_api
                        }
                    }
                }
            }
        }
        response_obj = MagicMock()
        response_obj.json_data = response
        result = lc_info._get_lc_service_uri(response_obj)
        assert result == lc_api

    def test_get_lc_status_check_uri(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        target_api = "target_api"
        response = {
            "Actions":
            {
                "#DellLCService.GetRemoteServicesAPIStatus": {
                    "target": target_api
                }
            }
        }
        response_obj = MagicMock()
        response_obj.json_data = response
        result = lc_info._get_lc_status_check_uri(response_obj)
        assert result == target_api
