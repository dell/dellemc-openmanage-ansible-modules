from ansible_collections.dellemc.openmanage.plugins.module_utils.\
    idrac_utils.lifecycle_controller.lifecycle_controller_jobs \
    import IDRACLifecycleControllerJobs
from ansible_collections.dellemc.openmanage.tests.unit.plugins.module_utils.idrac_utils.test_idrac_utils import TestUtils
from unittest.mock import MagicMock
import pytest


MANAGER_URI = "/redfish/v1/Managers/iDRAC.Embedded.1"
MANAGER_RESPONSE = {
    "Members": [
        {
            "@odata.id": MANAGER_URI
        }
    ]
}


class TestIDRACLifecycleControllerJobs(TestUtils):
    def test_get_lifecycle_controller_jobs_operation_no_job_id(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = None
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_info.get_lifecycle_controller_jobs_api = MagicMock(
            return_value="/api"
        )
        job_str = "job queue"
        response = {
            "@Message.ExtendedInfo": [
                {},
                {
                    "Message": "Successfully deleted Job queue",
                    "MessageId": "12345.6789"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value.json_data = response
        result = job_info.lifecycle_controller_jobs_operation(module_mock)
        expected_response = {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": "Successfully deleted Job queue",
                    "MessageID": "6789",
                }
            },
            "Status": "Success",
            "Message": "Successfully deleted Job queue",
            "MessageID": "6789",
            "Return": "Success",
            "retval": True
        }

        assert result == (expected_response, job_str)

    def test_get_lifecycle_controller_jobs_operation_with_job_id(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = "JID_1234"
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_info.get_lifecycle_controller_jobs_api = MagicMock(
            return_value="/api"
        )
        job_str = "job"
        response = {
            "@Message.ExtendedInfo": [
                {},
                {
                    "Message": "Successfully deleted the Job",
                    "MessageId": "12345.6789"
                }
            ]
        }
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value.json_data = response
        result = job_info.lifecycle_controller_jobs_operation(module_mock)
        expected_response = {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": "Successfully deleted the Job",
                    "MessageID": "6789",
                }
            },
            "Status": "Success",
            "Message": "Successfully deleted the Job",
            "MessageID": "6789",
            "Return": "Success",
            "retval": True
        }

        assert result == (expected_response, job_str)

    def test_lifecycle_controller_jobs_operation_no_api_uri(self, idrac_mock):
        module_mock = MagicMock()
        module_mock.params.get.return_value = None

        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_info.get_lifecycle_controller_jobs_api = MagicMock(return_value=None)

        result, job_str = job_info.lifecycle_controller_jobs_operation(module_mock)

        assert result == ""
        assert job_str == "job queue"

    def test_extract_job_deletion_info_success(self, idrac_mock):
        job_deletion_response = MagicMock()
        job_deletion_response.json_data = {
            "@Message.ExtendedInfo": [
                {},
                {
                    "Message": "Job deleted successfully",
                    "MessageId": "JOB.5678"
                }
            ]
        }

        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        result = job_info.extract_job_deletion_info(job_deletion_response)

        expected_result = {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": "Job deleted successfully",
                    "MessageID": "5678"
                }
            },
            "Status": "Success",
            "Message": "Job deleted successfully",
            "MessageID": "5678",
            "Return": "Success",
            "retval": True
        }

        assert result == expected_result

    def test_extract_job_deletion_info_missing_extended_info(self, idrac_mock):
        job_deletion_response = MagicMock()
        job_deletion_response.json_data = {}

        job_info = IDRACLifecycleControllerJobs(idrac_mock)

        with pytest.raises(KeyError) as exc_info:
            job_info.extract_job_deletion_info(job_deletion_response)

        assert "@Message.ExtendedInfo" in str(exc_info.value)

    def test_extract_error_info(self, idrac_mock):
        job_deletion_response = {
            "error": {
                "@Message.ExtendedInfo": [
                    {
                        "Message": "Failed to delete the Job",
                        "MessageId": "JOB.1234"
                    }
                ]
            }
        }

        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        result = job_info.extract_error_info(job_deletion_response)

        expected_result = {
            "Data": {
                "DeleteJobQueue_OUTPUT": {
                    "Message": "Failed to delete the Job",
                    "MessageID": "1234"
                }
            },
            "Status": "Error",
            "Message": "Failed to delete the Job",
            "MessageID": "1234",
            "Return": "Error",
            "retval": True
        }

        assert result == expected_result

    def test_extract_error_info_missing_extended_info(self, idrac_mock):
        job_deletion_response = {
            "error": {}
        }

        job_info = IDRACLifecycleControllerJobs(idrac_mock)

        with pytest.raises(KeyError) as exc_info:
            job_info.extract_error_info(job_deletion_response)

        assert "@Message.ExtendedInfo" in str(exc_info.value)

    def test_get_lifecycle_controller_status_api(self, idrac_mock):
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_info._get_controller_jobs_baseuri_response = MagicMock(return_value=MANAGER_RESPONSE)
        job_info._get_manager_uri = MagicMock(return_value="/manager_uri")
        job_info._get_manager_response = MagicMock(return_value="mangerresponse")
        job_info._get_job_service_uri = MagicMock(return_value="job_status_uri")
        job_info._get_job_service_response = MagicMock(return_value="job_service_response")
        job_info._get_delete_job_queue_uri = MagicMock(return_value="job_check_uri")
        result = job_info.get_lifecycle_controller_jobs_api()
        assert result == "job_check_uri"

    def test_get_lifecycle_controller_status_api_empty_response(self, idrac_mock):
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_info._get_controller_jobs_baseuri_response = MagicMock(return_value=MANAGER_RESPONSE)
        job_info._get_manager_uri = MagicMock(return_value="")
        result = job_info.get_lifecycle_controller_jobs_api()
        assert result == ""

    def test_get_controller_jobs_baseuri_response(self, idrac_mock):
        response = "api"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        result = job_info._get_controller_jobs_baseuri_response()
        assert result == response

    def test_get_manager_response(self, idrac_mock):
        response = "manager_response"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        result = job_info._get_manager_response("manager_api")
        assert result == response

    def test_get_lc_service_response(self, idrac_mock):
        response = "lc_service_response"
        idrac_mock.invoke_request.return_value.status_code = 200
        idrac_mock.invoke_request.return_value = response
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        result = job_info._get_job_service_response("lc_service_api")
        assert result == response

    def test_get_manager_uri(self, idrac_mock):
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        response_obj = MagicMock()
        response_obj.json_data = MANAGER_RESPONSE
        result = job_info._get_manager_uri(response_obj)
        assert result == MANAGER_URI

    def test_get_job_service_uri(self, idrac_mock):
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        job_api = "job_api"
        response = {
            "Links": {
                "Oem": {
                    "Dell": {
                        "DellJobService": {
                            "@odata.id": job_api
                        }
                    }
                }
            }
        }
        response_obj = MagicMock()
        response_obj.json_data = response
        result = job_info._get_job_service_uri(response_obj)
        assert result == job_api

    def test_get_delete_job_queue_uri(self, idrac_mock):
        job_info = IDRACLifecycleControllerJobs(idrac_mock)
        target_api = "target_api"
        response = {
            "Actions":
            {
                "#DellJobService.DeleteJobQueue": {
                    "target": target_api
                }
            }
        }
        response_obj = MagicMock()
        response_obj.json_data = response
        result = job_info._get_delete_job_queue_uri(response_obj)
        assert result == target_api
