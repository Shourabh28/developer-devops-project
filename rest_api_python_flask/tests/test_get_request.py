#
def test_get_api_endpoint_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/all' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/all')
    json_response = response.get_json()
    assert response.status_code == 200

def test_get_account_id_api_endpoint_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/get/messages/<account_id>' page is requested (GET)
    THEN check that the response is valid
    """
    account_id = "2022"
    response = test_client.get('/get/messages/{account_id}')
    json_response = response.get_json()
    assert response.status_code == 200
    #assert set(msg["account_id"] for msg in json_response) == account_id

def test_get_search_api_endpoint_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/get/messages/<account_id>' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/get/messages/<account_id>')
    json_response = response.get_json()
    assert response.status_code == 200