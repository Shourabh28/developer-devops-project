#
def test_new_message_with_fixture(new_message):
    """
    GIVEN a Message storing model
    WHEN a new Message is generated
    THEN check the account_id, message_id, sender_number, and receiver_number fields are defined correctly
    """
    assert new_message.account_id == '0000'
    assert new_message.message_id == '1111'
    assert new_message.sender_number == '111111'
    assert new_message.receiver_number == '222222'
