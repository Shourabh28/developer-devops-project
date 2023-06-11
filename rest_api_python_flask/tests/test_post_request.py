#
def test_post_api_endpoint_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/create' page is posted to (POST)
    THEN check that a '200' status code is returned.
    """
    response = test_client.post('/create', json={
        "account_id": "0000",
        "message_id": "1111",
        "sender_number": "111111",
        "receiver_number": "222222" 
    })
    json_response = response.get_json()
    assert json_response == {'message': 'message saved'}
    assert response.status_code == 201