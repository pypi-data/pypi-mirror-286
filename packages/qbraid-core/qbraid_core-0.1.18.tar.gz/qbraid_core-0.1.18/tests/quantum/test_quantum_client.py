# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for QuantumClient.

"""
from unittest.mock import Mock, patch

import pytest

from qbraid_core.exceptions import RequestsApiError
from qbraid_core.services.quantum import QuantumClient, QuantumServiceRequestError


@pytest.fixture
def mock_session():
    """Fixture to provide a mock session object."""
    return Mock()


@pytest.fixture
def quantum_client(mock_session):
    """Fixture to provide a QuantumClient instance with a mocked session."""
    with patch("qbraid_core.QbraidClient.session", new=mock_session):
        client = QuantumClient()
        client.session = mock_session
        yield client


def test_update_device_success(quantum_client, mock_session):
    """Test successful update of a quantum device."""
    mock_response = Mock()
    mock_response.json.return_value = {"status": "success"}
    mock_session.put.return_value = mock_response

    data = {"device_id": "123", "status": "active"}
    response = quantum_client.update_device(data)

    assert response == {"status": "success"}
    mock_session.put.assert_called_once_with("/quantum-devices", json=data)


def test_update_device_failure(quantum_client, mock_session):
    """Test failed update of a quantum device."""
    mock_session.put.side_effect = RequestsApiError("Error")

    data = {"device_id": "123", "status": "inactive"}

    with pytest.raises(QuantumServiceRequestError):
        quantum_client.update_device(data)


def test_search_devices_success(quantum_client, mock_session):
    """Test successful search of quantum devices."""
    mock_response = Mock()
    mock_response.json.return_value = [{"device_id": "123"}]
    mock_session.get.return_value = mock_response

    query = {"type": "Simulator"}
    response = quantum_client.search_devices(query)

    assert response == [{"device_id": "123"}]
    mock_session.get.assert_called_once_with("/quantum-devices", params=query)


def test_search_jobs_success(quantum_client, mock_session):
    """Test successful search of quantum jobs."""
    mock_response = Mock()
    mock_response.json.return_value = {"jobsArray": [{"job_id": "abc"}]}
    mock_session.get.return_value = mock_response

    query = {"user": "test_user"}
    response = quantum_client.search_jobs(query)

    assert response == [{"job_id": "abc"}]
    mock_session.get.assert_called_once_with("/quantum-jobs", params=query)


def test_create_job_success(quantum_client, mock_session):
    """Test successful creation of a quantum job."""
    mock_response = Mock()
    mock_response.json.return_value = {"job_id": "abc"}
    mock_session.post.return_value = mock_response

    data = {"bitcode": b"sample_bitcode"}
    response = quantum_client.create_job(data)

    assert response == {"job_id": "abc"}
    assert data["bitcode"] == "c2FtcGxlX2JpdGNvZGU="  # base64 encoded value
    mock_session.post.assert_called_once_with("/quantum-jobs", json=data)


def test_estimate_cost_success(quantum_client, mock_session):
    """Test successful calculation of the cost of running a quantum job."""
    mock_response = Mock()
    mock_response.json.return_value = {"estimatedCredits": 10.0}
    mock_session.get.return_value = mock_response

    device_id = "device123"
    shots = 1000
    estimated_minutes = 30.0

    response = quantum_client.estimate_cost(device_id, shots, estimated_minutes)

    assert response["estimatedCredits"] == 10.0
    mock_session.get.assert_called_once_with(
        "/quantum-jobs/cost-estimate",
        params={"qbraidDeviceId": device_id, "shots": shots, "minutes": estimated_minutes},
    )


def test_estimate_cost_failure(quantum_client, mock_session):
    """Test failed calculation of the cost of running a quantum job."""
    mock_session.get.side_effect = RequestsApiError("Error")

    device_id = "device123"
    shots = 1000
    estimated_minutes = 30.0

    with pytest.raises(QuantumServiceRequestError):
        quantum_client.estimate_cost(device_id, shots, estimated_minutes)


def test_estimate_cost_value_error(quantum_client):
    """Test ValueError when invalid arguments are provided to estimate_cost."""
    with pytest.raises(ValueError):
        quantum_client.estimate_cost("device123", None, None)
