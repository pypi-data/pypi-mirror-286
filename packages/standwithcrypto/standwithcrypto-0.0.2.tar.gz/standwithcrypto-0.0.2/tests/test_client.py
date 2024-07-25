import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import standwithcrypto

client = standwithcrypto.Client()

def test_get_all_people():
    all_people = client.get_all_people()

    assert all_people is not None
    assert isinstance(all_people, dict)
    assert all_people['people']

def test_get_all_people_with_id():
    all_people = client.get_all_people(id='e6d24531-809a-4e68-894b-f0dadb7e03a9')

    assert all_people is not None
    assert isinstance(all_people, dict)
    assert all_people['people']

    with pytest.raises(ValueError):
        client.get_all_people(id=123)

