from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.info.lifecycle_controller_status \
    import IDRACLifecycleControllerStatusInfo
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock

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
        response = {"Members": [
            {
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1"
            }]}
        lc_info._get_controller_status_baseuri_response = MagicMock(return_value=response)
        lc_info._get_manager_uri = MagicMock(return_value="/manager_uri")
        lc_info._get_manager_response = MagicMock(return_value="mangerresponse")
        lc_info._get_lc_service_uri = MagicMock(return_value="lc_status_uri")
        lc_info._get_lc_service_response = MagicMock(return_value="lc_service_response")
        lc_info._get_lc_status_check_uri = MagicMock(return_value="lc_check_uri")
        result = lc_info.get_lifecycle_controller_status_api()
        assert result == "lc_check_uri"

    def test_get_lifecycle_controller_status_api_empty_response(self, idrac_mock):
        lc_info = IDRACLifecycleControllerStatusInfo(idrac_mock)
        response = {"Members": [
            {
                "@odata.id": "/redfish/v1/Managers/iDRAC.Embedded.1"
            }]}
        lc_info._get_controller_status_baseuri_response = MagicMock(return_value=response)
        lc_info._get_manager_uri = MagicMock(return_value="")
        result = lc_info.get_lifecycle_controller_status_api()
        assert result == ""
